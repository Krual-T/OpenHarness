#!/usr/bin/env python3
"""Shared helpers for the repo-local project memory skill."""

from __future__ import annotations

import difflib
import re
import sqlite3
import subprocess
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import yaml

MEMORY_DIRNAME = ".project-memory"
ALIASES_FILENAME = "aliases.yaml"
INDEX_FILENAME = "index.sqlite"
MEMORY_KIND_DIRS = {
    "workflow": "workflows",
    "fact": "facts",
    "decision": "decisions",
}
COMMON_LIST_FIELDS = ("intent_aliases", "tags", "notes")
COMMON_OPTIONAL_TEXT_FIELDS = (
    "review_after",
    "valid_until",
    "superseded_by",
    "archive_reason",
    "deprecation_reason",
    "archived_at",
    "archived_by",
)
METADATA_TEXT_FIELDS = ("health_status", "health_checked_at")
METADATA_LIST_FIELDS = ("stale_reasons", "archived_aliases")
KIND_LIST_FIELDS = {
    "workflow": ("steps", "entrypoints"),
    "fact": ("applies_to",),
    "decision": ("alternatives", "consequences", "revisit_when"),
}
KIND_TEXT_FIELDS = {
    "workflow": (),
    "fact": ("statement", "details"),
    "decision": ("question", "decision", "rationale"),
}
ALLOWED_BASE_STATUSES = {"draft", "reviewed", "verified", "deprecated", "archived", "invalid"}
REUSABLE_BASE_STATUSES = {"reviewed", "verified"}
INACTIVE_BASE_STATUSES = {"deprecated", "archived", "invalid"}
DEFAULT_BASE_STATUS = "reviewed"
DEFAULT_MIN_SCORE = 18.0
DEFAULT_MIN_CONFIDENCE = 0.7
DEFAULT_SCORE_RATIO = 0.25
SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}


class ProjectMemoryError(RuntimeError):
    """Raised when project memory operations cannot proceed."""


@dataclass(slots=True)
class MemoryPaths:
    repo_root: Path
    memory_root: Path
    workflows_dir: Path
    facts_dir: Path
    decisions_dir: Path
    aliases_file: Path
    index_db: Path

    def dir_for_kind(self, kind: str) -> Path:
        normalized_kind = normalize_memory_kind(kind)
        if normalized_kind == "workflow":
            return self.workflows_dir
        if normalized_kind == "fact":
            return self.facts_dir
        if normalized_kind == "decision":
            return self.decisions_dir
        raise ProjectMemoryError(f"Unsupported memory kind: {kind}")


def utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def utc_today() -> date:
    return datetime.utcnow().date()


def parse_dateish(value: str) -> date | None:
    text = normalize_string(value)
    if not text:
        return None
    for candidate in (text, text.replace("Z", "+00:00")):
        try:
            return datetime.fromisoformat(candidate).date()
        except ValueError:
            pass
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def supported_memory_kinds() -> tuple[str, ...]:
    return tuple(MEMORY_KIND_DIRS.keys())


def normalize_memory_kind(kind: str) -> str:
    normalized = str(kind or "").strip().lower()
    if normalized not in MEMORY_KIND_DIRS:
        raise ProjectMemoryError(
            f"Unsupported memory kind: {kind}. Expected one of: {', '.join(supported_memory_kinds())}"
        )
    return normalized


def parse_memory_kinds(kinds: Iterable[str] | None) -> tuple[str, ...]:
    if not kinds:
        return supported_memory_kinds()
    normalized = tuple(dict.fromkeys(normalize_memory_kind(kind) for kind in kinds))
    return normalized or supported_memory_kinds()


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise ProjectMemoryError("Could not locate repo root from the current working directory")


def get_memory_paths(repo_root: Path | None = None) -> MemoryPaths:
    resolved_root = (repo_root or find_repo_root()).resolve()
    memory_root = resolved_root / MEMORY_DIRNAME
    return MemoryPaths(
        repo_root=resolved_root,
        memory_root=memory_root,
        workflows_dir=memory_root / "workflows",
        facts_dir=memory_root / "facts",
        decisions_dir=memory_root / "decisions",
        aliases_file=memory_root / ALIASES_FILENAME,
        index_db=memory_root / INDEX_FILENAME,
    )


def ensure_memory_layout(repo_root: Path | None = None) -> MemoryPaths:
    paths = get_memory_paths(repo_root)
    paths.workflows_dir.mkdir(parents=True, exist_ok=True)
    paths.facts_dir.mkdir(parents=True, exist_ok=True)
    paths.decisions_dir.mkdir(parents=True, exist_ok=True)
    if not paths.aliases_file.exists():
        dump_yaml(paths.aliases_file, {"aliases": {}})
    return paths


def load_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return default
    payload = yaml.safe_load(text)
    return default if payload is None else payload


def dump_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def git_stdout(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ProjectMemoryError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def current_branch(repo_root: Path) -> str:
    return git_stdout(repo_root, "rev-parse", "--abbrev-ref", "HEAD")


def current_commit(repo_root: Path) -> str:
    return git_stdout(repo_root, "rev-parse", "HEAD")


def make_relative_path(path_text: str | Path, repo_root: Path) -> str:
    path = Path(path_text)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()
    return path.as_posix()


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "").lower().strip()
    chars: list[str] = []
    for char in normalized:
        if char.isalnum() or "\u4e00" <= char <= "\u9fff":
            chars.append(char)
        else:
            chars.append(" ")
    return " ".join("".join(chars).split())


def tokenize(text: str) -> set[str]:
    normalized = normalize_text(text)
    if not normalized:
        return set()
    tokens: set[str] = set()
    for part in re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]+", normalized):
        tokens.add(part)
        if all("\u4e00" <= char <= "\u9fff" for char in part) and len(part) > 2:
            tokens.update(part[index : index + 2] for index in range(len(part) - 1))
    return tokens


def normalize_string(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        raw_items = value
    elif value in (None, ""):
        raw_items = []
    else:
        raw_items = [value]
    return dedupe_list([normalize_string(item) for item in raw_items if normalize_string(item)])


def dedupe_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        trimmed = item.strip()
        if not trimmed or trimmed in seen:
            continue
        seen.add(trimmed)
        result.append(trimmed)
    return result


def merge_string_lists(existing: Any, incoming: list[str]) -> list[str]:
    return normalize_string_list([*normalize_string_list(existing), *incoming])


def load_alias_entries(repo_root: Path | None = None) -> dict[str, dict[str, str]]:
    paths = ensure_memory_layout(repo_root)
    payload = load_yaml(paths.aliases_file, {"aliases": {}})
    aliases = payload.get("aliases") if isinstance(payload, dict) else {}
    if not isinstance(aliases, dict):
        return {}

    entries: dict[str, dict[str, str]] = {}
    for alias_text, value in aliases.items():
        alias = normalize_string(alias_text)
        if not alias:
            continue
        if isinstance(value, str):
            object_id = normalize_string(value)
            object_kind = ""
        elif isinstance(value, dict):
            object_id = normalize_string(value.get("id"))
            object_kind = normalize_string(value.get("kind")).lower()
            if object_kind and object_kind not in MEMORY_KIND_DIRS:
                object_kind = ""
        else:
            continue
        if object_id:
            entries[alias] = {"id": object_id, "kind": object_kind}
    return entries


def load_alias_map(repo_root: Path | None = None) -> dict[str, dict[str, str]]:
    raw_aliases = load_alias_entries(repo_root)
    normalized: dict[str, dict[str, str]] = {}
    for alias_text, entry in raw_aliases.items():
        alias_norm = normalize_text(alias_text)
        if alias_norm:
            normalized[alias_norm] = {"id": entry["id"], "kind": entry.get("kind", "")}
    return normalized


def save_alias_map(repo_root: Path | None, aliases: dict[str, dict[str, str]]) -> Path:
    paths = ensure_memory_layout(repo_root)
    serialized: dict[str, Any] = {}
    for alias_text, entry in sorted(aliases.items(), key=lambda item: item[0]):
        alias = normalize_string(alias_text)
        object_id = normalize_string(entry.get("id"))
        object_kind = normalize_string(entry.get("kind")).lower()
        if not alias or not object_id:
            continue
        if object_kind:
            serialized[alias] = {"id": object_id, "kind": object_kind}
        else:
            serialized[alias] = object_id
    dump_yaml(paths.aliases_file, {"aliases": serialized})
    return paths.aliases_file


def memory_file_path(repo_root: Path | None, kind: str, object_id: str) -> Path:
    paths = ensure_memory_layout(repo_root)
    return paths.dir_for_kind(kind) / f"{object_id}.yaml"


def workflow_file_path(repo_root: Path | None, workflow_id: str) -> Path:
    return memory_file_path(repo_root, "workflow", workflow_id)


def load_memory_object(repo_root: Path | None, kind: str, object_id: str) -> dict[str, Any]:
    path = memory_file_path(repo_root, kind, object_id)
    if not path.exists():
        return {}
    payload = load_yaml(path, {})
    if not isinstance(payload, dict):
        return {}
    payload.setdefault("id", object_id)
    payload["kind"] = normalize_memory_kind(kind)
    payload["_path"] = path
    return payload


def load_memory_objects(
    repo_root: Path | None = None,
    kinds: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    paths = ensure_memory_layout(repo_root)
    objects: list[dict[str, Any]] = []
    for kind in parse_memory_kinds(kinds):
        for object_path in sorted(paths.dir_for_kind(kind).glob("*.yaml")):
            payload = load_yaml(object_path, {})
            if not isinstance(payload, dict):
                continue
            payload.setdefault("id", object_path.stem)
            payload["kind"] = kind
            payload["_path"] = object_path
            objects.append(payload)
    return objects


def load_workflows(repo_root: Path | None = None) -> list[dict[str, Any]]:
    return load_memory_objects(repo_root, kinds=("workflow",))


def find_memory_object_by_id(
    repo_root: Path | None,
    object_id: str,
    kinds: Iterable[str] | None = None,
) -> dict[str, Any] | None:
    for kind in parse_memory_kinds(kinds):
        payload = load_memory_object(repo_root, kind, object_id)
        if payload:
            return payload
    return None


def find_memory_objects_by_id(
    repo_root: Path | None,
    object_id: str,
    kinds: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for kind in parse_memory_kinds(kinds):
        payload = load_memory_object(repo_root, kind, object_id)
        if payload:
            matches.append(payload)
    return matches


def normalize_scope(scope: Any) -> dict[str, str]:
    if not isinstance(scope, dict):
        return {}
    normalized: dict[str, str] = {}
    for key, value in scope.items():
        key_text = normalize_string(key)
        value_text = normalize_string(value)
        if key_text and value_text:
            normalized[key_text] = value_text
    return normalized


def normalize_base_status(status: Any) -> str:
    normalized = normalize_string(status).lower()
    return normalized or DEFAULT_BASE_STATUS


def resolve_evidence_path(repo_root: Path, evidence: dict[str, Any] | str) -> Path | None:
    if isinstance(evidence, str):
        path_text = evidence
    elif isinstance(evidence, dict):
        path_text = normalize_string(evidence.get("path"))
    else:
        return None
    if not path_text:
        return None
    evidence_path = Path(path_text)
    if evidence_path.is_absolute():
        return evidence_path
    return repo_root / evidence_path


def normalize_evidence_items(repo_root: Path, evidence_items: Any) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    if not isinstance(evidence_items, list):
        evidence_items = []
    seen_paths: set[str] = set()
    for evidence in evidence_items:
        resolved_path = resolve_evidence_path(repo_root, evidence)
        path_text = (
            make_relative_path(resolved_path, repo_root)
            if resolved_path is not None
            else normalize_string(evidence.get("path") if isinstance(evidence, dict) else evidence)
        )
        path_text = normalize_string(path_text)
        if not path_text or path_text in seen_paths:
            continue
        seen_paths.add(path_text)
        kind = "file"
        if isinstance(evidence, dict):
            kind = normalize_string(evidence.get("kind")) or "file"
        normalized.append({"path": path_text, "kind": kind})
    return normalized


def compact_memory_object(memory_object: dict[str, Any]) -> dict[str, Any]:
    compacted: dict[str, Any] = {}
    for key, value in memory_object.items():
        if key == "_path":
            continue
        if value in ("", None, [], {}):
            continue
        compacted[key] = value
    return compacted


def normalize_memory_object(repo_root: Path | None, memory_object: dict[str, Any]) -> dict[str, Any]:
    paths = ensure_memory_layout(repo_root)
    payload = dict(memory_object)
    payload.pop("_path", None)

    kind = normalize_memory_kind(payload.get("kind", "workflow"))
    object_id = normalize_string(payload.get("id"))
    title = normalize_string(payload.get("title"))
    if not object_id:
        raise ProjectMemoryError("memory object id is required")
    if not title:
        raise ProjectMemoryError("memory object title is required")

    scope = normalize_scope(payload.get("scope"))
    scope.setdefault("repo", paths.repo_root.name)

    normalized: dict[str, Any] = {
        "id": object_id,
        "kind": kind,
        "title": title,
        "summary": normalize_string(payload.get("summary")),
        "scope": scope,
        "status": normalize_base_status(payload.get("status")),
        "created_at": normalize_string(payload.get("created_at")) or utc_now_iso(),
        "updated_at": normalize_string(payload.get("updated_at")) or utc_now_iso(),
    }

    confidence = payload.get("confidence")
    if confidence not in (None, ""):
        normalized["confidence"] = float(confidence)

    owner = normalize_string(payload.get("owner"))
    if owner:
        normalized["owner"] = owner

    last_verified_commit = normalize_string(payload.get("last_verified_commit"))
    if last_verified_commit:
        normalized["last_verified_commit"] = last_verified_commit

    for field in COMMON_OPTIONAL_TEXT_FIELDS:
        value = normalize_string(payload.get(field))
        if value:
            normalized[field] = value

    for field in METADATA_TEXT_FIELDS:
        value = normalize_string(payload.get(field))
        if value:
            normalized[field] = value

    for field in COMMON_LIST_FIELDS:
        normalized[field] = normalize_string_list(payload.get(field))

    for field in METADATA_LIST_FIELDS:
        values = normalize_string_list(payload.get(field))
        if values:
            normalized[field] = values

    for field in KIND_LIST_FIELDS[kind]:
        normalized[field] = normalize_string_list(payload.get(field))

    for field in KIND_TEXT_FIELDS[kind]:
        value = normalize_string(payload.get(field))
        if value:
            normalized[field] = value

    normalized["evidence"] = normalize_evidence_items(paths.repo_root, payload.get("evidence"))
    return compact_memory_object(normalized)


def validate_memory_object(
    memory_object: dict[str, Any],
    repo_root: Path | None = None,
) -> tuple[dict[str, Any], list[str], list[str]]:
    normalized = normalize_memory_object(repo_root, memory_object)
    kind = normalized["kind"]
    errors: list[str] = []
    warnings: list[str] = []

    status = normalize_base_status(normalized.get("status"))
    if status not in ALLOWED_BASE_STATUSES:
        errors.append(
            f"invalid_status:{status}. expected one of {', '.join(sorted(ALLOWED_BASE_STATUSES))}"
        )

    confidence = normalized.get("confidence")
    if confidence is None:
        warnings.append("missing_confidence")
    else:
        try:
            confidence_value = float(confidence)
        except (TypeError, ValueError):
            errors.append("invalid_confidence")
        else:
            if not 0.0 <= confidence_value <= 1.0:
                errors.append("confidence_out_of_range")
            elif confidence_value < DEFAULT_MIN_CONFIDENCE:
                warnings.append("low_confidence")

    if not normalized.get("evidence"):
        errors.append("missing_evidence")
    if status not in INACTIVE_BASE_STATUSES and not normalize_string(normalized.get("owner")):
        warnings.append("missing_owner")
    if status not in INACTIVE_BASE_STATUSES and not normalize_string_list(normalized.get("intent_aliases")):
        warnings.append("missing_aliases")
    if status not in INACTIVE_BASE_STATUSES and not normalize_string((normalized.get("scope") or {}).get("branch")):
        warnings.append("missing_scope_branch")

    review_after = normalize_string(normalized.get("review_after"))
    if review_after and parse_dateish(review_after) is None:
        errors.append("invalid_review_after")
    valid_until = normalize_string(normalized.get("valid_until"))
    if valid_until and parse_dateish(valid_until) is None:
        errors.append("invalid_valid_until")

    if kind == "workflow":
        if not normalize_string_list(normalized.get("steps")) and not normalize_string_list(
            normalized.get("entrypoints")
        ):
            errors.append("workflow_requires_steps_or_entrypoints")
    elif kind == "fact":
        if not normalize_string(normalized.get("statement")):
            errors.append("fact_requires_statement")
        if not normalize_string_list(normalized.get("applies_to")):
            errors.append("fact_requires_applies_to")
    elif kind == "decision":
        if not normalize_string(normalized.get("question")):
            errors.append("decision_requires_question")
        if not normalize_string(normalized.get("decision")):
            errors.append("decision_requires_decision")
        if not normalize_string(normalized.get("rationale")):
            errors.append("decision_requires_rationale")
        if not normalize_string_list(normalized.get("alternatives")):
            errors.append("decision_requires_alternatives")
        if not normalize_string_list(normalized.get("consequences")):
            errors.append("decision_requires_consequences")
        if not normalize_string_list(normalized.get("revisit_when")) and not review_after:
            errors.append("decision_requires_revisit_trigger")
    if status == "deprecated":
        if not normalize_string(normalized.get("deprecation_reason")) and not normalize_string(
            normalized.get("archive_reason")
        ):
            errors.append("deprecated_requires_reason")
        if not normalize_string(normalized.get("superseded_by")):
            warnings.append("deprecated_without_superseded_by")
    if status in {"archived", "invalid"}:
        if not normalize_string(normalized.get("archive_reason")):
            errors.append(f"{status}_requires_archive_reason")
        if not normalize_string(normalized.get("archived_at")):
            errors.append(f"{status}_requires_archived_at")
        if not normalize_string(normalized.get("archived_by")):
            errors.append(f"{status}_requires_archived_by")

    return normalized, dedupe_list(errors), dedupe_list(warnings)


def alias_conflicts_for_object(
    repo_root: Path | None,
    memory_object: dict[str, Any],
) -> list[str]:
    paths = ensure_memory_layout(repo_root)
    normalized, _, _ = validate_memory_object(memory_object, paths.repo_root)
    alias_map = load_alias_map(paths.repo_root)
    conflicts: list[str] = []
    for alias_text in normalize_string_list(normalized.get("intent_aliases")):
        alias_norm = normalize_text(alias_text)
        existing = alias_map.get(alias_norm)
        if not existing:
            continue
        same_object = (
            existing.get("id") == normalized["id"]
            and (not existing.get("kind") or existing.get("kind") == normalized["kind"])
        )
        if not same_object:
            conflicts.append(
                f"alias_conflict:{alias_text}->{existing.get('kind') or 'unknown'}:{existing.get('id')}"
            )
    return dedupe_list(conflicts)


def evaluate_memory_object_status(
    memory_object: dict[str, Any],
    repo_root: Path | None = None,
) -> tuple[str, list[str]]:
    paths = ensure_memory_layout(repo_root)
    resolved_root = paths.repo_root
    hard_reasons: list[str] = []
    soft_reasons: list[str] = []
    evidence_items = memory_object.get("evidence") or []
    if not isinstance(evidence_items, list):
        evidence_items = []
    last_verified_commit = normalize_string(memory_object.get("last_verified_commit"))
    base_status = normalize_base_status(memory_object.get("status"))

    superseded_by = normalize_string(memory_object.get("superseded_by"))
    if base_status == "archived":
        reasons: list[str] = []
        archive_reason = normalize_string(memory_object.get("archive_reason"))
        archived_by = normalize_string(memory_object.get("archived_by"))
        archived_at = normalize_string(memory_object.get("archived_at"))
        if archive_reason:
            reasons.append(f"archive_reason:{archive_reason}")
        if archived_by:
            reasons.append(f"archived_by:{archived_by}")
        if archived_at:
            reasons.append(f"archived_at:{archived_at}")
        return "archived", reasons or ["archived"]
    if base_status == "invalid":
        reasons = []
        archive_reason = normalize_string(memory_object.get("archive_reason"))
        archived_by = normalize_string(memory_object.get("archived_by"))
        if archive_reason:
            reasons.append(f"archive_reason:{archive_reason}")
        if archived_by:
            reasons.append(f"archived_by:{archived_by}")
        return "invalid", reasons or ["invalid"]
    if superseded_by or base_status == "deprecated":
        reasons = []
        deprecation_reason = normalize_string(memory_object.get("deprecation_reason")) or normalize_string(
            memory_object.get("archive_reason")
        )
        if superseded_by:
            reasons.append(f"superseded_by:{superseded_by}")
        if deprecation_reason:
            reasons.append(f"deprecation_reason:{deprecation_reason}")
        return "deprecated", reasons or ["deprecated"]

    valid_until = parse_dateish(normalize_string(memory_object.get("valid_until")))
    if valid_until and utc_today() > valid_until:
        hard_reasons.append(f"valid_until_passed:{valid_until.isoformat()}")

    review_after = parse_dateish(normalize_string(memory_object.get("review_after")))
    if review_after and utc_today() > review_after:
        soft_reasons.append(f"review_after_passed:{review_after.isoformat()}")

    scope = memory_object.get("scope") or {}
    if isinstance(scope, dict):
        scope_branch = normalize_string(scope.get("branch"))
        if scope_branch:
            try:
                branch = current_branch(resolved_root)
            except ProjectMemoryError:
                branch = ""
            if branch and scope_branch != branch:
                hard_reasons.append(f"branch_mismatch:{branch}!={scope_branch}")

    for evidence in evidence_items:
        evidence_path = resolve_evidence_path(resolved_root, evidence)
        evidence_label = (
            make_relative_path(evidence_path, resolved_root)
            if evidence_path is not None
            else "<unknown>"
        )
        if evidence_path is None or not evidence_path.exists():
            hard_reasons.append(f"missing_evidence:{evidence_label}")
            continue
        if last_verified_commit:
            result = subprocess.run(
                ["git", "diff", "--name-only", last_verified_commit, "--", evidence_label],
                cwd=resolved_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                hard_reasons.append(f"invalid_commit:{last_verified_commit}")
            elif result.stdout.strip():
                hard_reasons.append(f"changed_since_verify:{evidence_label}")
        result = subprocess.run(
            ["git", "status", "--short", "--", evidence_label],
            cwd=resolved_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            hard_reasons.append(f"local_changes:{evidence_label}")

    if hard_reasons:
        return "stale", dedupe_list([*hard_reasons, *soft_reasons])
    if soft_reasons:
        return "review_due", dedupe_list(soft_reasons)
    if evidence_items and base_status in REUSABLE_BASE_STATUSES:
        return base_status, []
    return base_status, []


def evaluate_workflow_status(workflow: dict[str, Any], repo_root: Path | None = None) -> tuple[str, list[str]]:
    return evaluate_memory_object_status(workflow, repo_root)


def reuse_blockers_for_object(
    memory_object: dict[str, Any],
    score: float,
    effective_status: str,
    *,
    min_score: float,
    min_confidence: float,
) -> list[str]:
    blockers: list[str] = []
    if score < min_score:
        blockers.append(f"score_below_threshold:{score:.2f}<{min_score:.2f}")
    if effective_status not in REUSABLE_BASE_STATUSES:
        blockers.append(f"non_reusable_status:{effective_status}")
    confidence = memory_object.get("confidence")
    if confidence in (None, ""):
        blockers.append("missing_confidence")
    else:
        try:
            confidence_value = float(confidence)
        except (TypeError, ValueError):
            blockers.append("invalid_confidence")
        else:
            if confidence_value < min_confidence:
                blockers.append(
                    f"confidence_below_threshold:{confidence_value:.2f}<{min_confidence:.2f}"
                )
    return dedupe_list(blockers)


def audit_memory_objects(
    repo_root: Path | None,
    kinds: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    paths = ensure_memory_layout(repo_root)
    findings: list[dict[str, Any]] = []
    objects = load_memory_objects(paths.repo_root, kinds=parse_memory_kinds(kinds))
    title_index: dict[tuple[str, str], list[str]] = {}
    alias_index: dict[str, list[str]] = {}

    for memory_object in objects:
        normalized, errors, warnings = validate_memory_object(memory_object, paths.repo_root)
        kind = normalized["kind"]
        object_id = normalized["id"]
        title_key = (kind, normalize_text(normalized.get("title", "")))
        title_index.setdefault(title_key, []).append(object_id)
        for alias_text in normalize_string_list(normalized.get("intent_aliases")):
            alias_index.setdefault(normalize_text(alias_text), []).append(f"{kind}:{object_id}")

        status, reasons = evaluate_memory_object_status(normalized, paths.repo_root)
        if status == "stale":
            findings.append(
                {
                    "severity": "high",
                    "kind": kind,
                    "id": object_id,
                    "issue": "stale_object",
                    "details": reasons,
                }
            )
        elif status == "review_due":
            findings.append(
                {
                    "severity": "medium",
                    "kind": kind,
                    "id": object_id,
                    "issue": "review_due",
                    "details": reasons,
                }
            )

        for error in errors:
            findings.append(
                {
                    "severity": "high",
                    "kind": kind,
                    "id": object_id,
                    "issue": error,
                    "details": [],
                }
            )
        for warning in warnings:
            findings.append(
                {
                    "severity": "medium" if warning == "low_confidence" else "low",
                    "kind": kind,
                    "id": object_id,
                    "issue": warning,
                    "details": [],
                }
            )

    for alias_text, entry in load_alias_entries(paths.repo_root).items():
        alias_norm = normalize_text(alias_text)
        if not alias_norm:
            continue
        object_kind = entry.get("kind") or ""
        if not object_kind:
            resolved = find_memory_object_by_id(paths.repo_root, entry["id"])
            object_kind = normalize_string(resolved.get("kind")) if resolved else "unknown"
        alias_index.setdefault(alias_norm, []).append(f"{object_kind}:{entry['id']}")

    for (kind, _), object_ids in title_index.items():
        unique_ids = sorted(set(object_ids))
        if len(unique_ids) > 1:
            for object_id in unique_ids:
                findings.append(
                    {
                        "severity": "medium",
                        "kind": kind,
                        "id": object_id,
                        "issue": "duplicate_normalized_title",
                        "details": unique_ids,
                    }
                )

    for alias_norm, owners in alias_index.items():
        unique_owners = sorted(set(owners))
        if alias_norm and len(unique_owners) > 1:
            for owner in unique_owners:
                kind, object_id = owner.split(":", 1)
                findings.append(
                    {
                        "severity": "high",
                        "kind": kind,
                        "id": object_id,
                        "issue": "alias_collision",
                        "details": [alias_norm, *unique_owners],
                    }
                )

    findings.sort(
        key=lambda item: (
            -SEVERITY_ORDER.get(item["severity"], 0),
            item["kind"],
            item["id"],
            item["issue"],
        )
    )
    return findings


def iter_search_values(memory_object: dict[str, Any]) -> list[str]:
    kind = normalize_memory_kind(memory_object.get("kind", "workflow"))
    values: list[str] = [
        normalize_string(memory_object.get("id")),
        normalize_string(memory_object.get("title")),
        normalize_string(memory_object.get("summary")),
    ]
    for field in COMMON_LIST_FIELDS:
        values.extend(normalize_string_list(memory_object.get(field)))
    for field in KIND_LIST_FIELDS[kind]:
        values.extend(normalize_string_list(memory_object.get(field)))
    for field in KIND_TEXT_FIELDS[kind]:
        values.append(normalize_string(memory_object.get(field)))
    scope = normalize_scope(memory_object.get("scope"))
    values.extend(scope.values())
    return [value for value in values if value]


def memory_object_search_text(memory_object: dict[str, Any]) -> str:
    return "\n".join(iter_search_values(memory_object))


def rebuild_index(
    repo_root: Path | None = None,
    memory_objects: list[dict[str, Any]] | None = None,
) -> Path:
    paths = ensure_memory_layout(repo_root)
    memory_objects = memory_objects if memory_objects is not None else load_memory_objects(paths.repo_root)
    alias_map = load_alias_entries(paths.repo_root)
    conn = sqlite3.connect(paths.index_db)
    try:
        conn.execute("DROP TABLE IF EXISTS memory_objects")
        conn.execute("DROP TABLE IF EXISTS workflows")
        conn.execute("DROP TABLE IF EXISTS aliases")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_objects (
                object_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                file_path TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                status TEXT NOT NULL,
                last_verified_commit TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                search_text TEXT NOT NULL,
                PRIMARY KEY (kind, object_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS aliases (
                alias_norm TEXT NOT NULL,
                object_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                alias_text TEXT NOT NULL,
                PRIMARY KEY (alias_norm, kind, object_id)
            )
            """
        )
        conn.execute("DELETE FROM memory_objects")
        conn.execute("DELETE FROM aliases")
        for memory_object in memory_objects:
            object_id = normalize_string(memory_object.get("id"))
            if not object_id:
                continue
            kind = normalize_memory_kind(memory_object.get("kind", "workflow"))
            status, _ = evaluate_memory_object_status(memory_object, paths.repo_root)
            file_path = str(memory_object.get("_path", memory_file_path(paths.repo_root, kind, object_id)))
            conn.execute(
                """
                INSERT INTO memory_objects (
                    object_id,
                    kind,
                    file_path,
                    title,
                    summary,
                    status,
                    last_verified_commit,
                    updated_at,
                    search_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    object_id,
                    kind,
                    make_relative_path(file_path, paths.repo_root),
                    normalize_string(memory_object.get("title")),
                    normalize_string(memory_object.get("summary")),
                    status,
                    normalize_string(memory_object.get("last_verified_commit")),
                    normalize_string(memory_object.get("updated_at")),
                    memory_object_search_text(memory_object),
                ),
            )
            for alias_text in normalize_string_list(memory_object.get("intent_aliases")):
                alias_norm = normalize_text(alias_text)
                if alias_norm:
                    conn.execute(
                        "INSERT OR REPLACE INTO aliases (alias_norm, object_id, kind, alias_text) VALUES (?, ?, ?, ?)",
                        (alias_norm, object_id, kind, alias_text),
                    )
        for alias_text, entry in alias_map.items():
            alias_norm = normalize_text(alias_text)
            if not alias_norm:
                continue
            object_id = entry["id"]
            object_kind = entry.get("kind", "")
            if not object_kind:
                resolved = find_memory_object_by_id(paths.repo_root, object_id)
                object_kind = normalize_string(resolved.get("kind")) if resolved else ""
            if object_kind:
                conn.execute(
                    "INSERT OR REPLACE INTO aliases (alias_norm, object_id, kind, alias_text) VALUES (?, ?, ?, ?)",
                    (alias_norm, object_id, object_kind, alias_text),
                )
        conn.commit()
    finally:
        conn.close()
    return paths.index_db


def sync_index(repo_root: Path | None = None) -> Path:
    paths = ensure_memory_layout(repo_root)
    index_path = paths.index_db
    source_files = [paths.aliases_file]
    for kind in supported_memory_kinds():
        source_files.extend(paths.dir_for_kind(kind).glob("*.yaml"))
    source_mtime = max((path.stat().st_mtime for path in source_files if path.exists()), default=0)
    if not index_path.exists() or index_path.stat().st_mtime < source_mtime:
        rebuild_index(paths.repo_root)
    return index_path


def save_memory_object(
    repo_root: Path | None,
    memory_object: dict[str, Any],
    *,
    allow_alias_reassign: bool = False,
) -> Path:
    paths = ensure_memory_layout(repo_root)
    normalized, errors, _ = validate_memory_object(memory_object, paths.repo_root)
    if errors:
        raise ProjectMemoryError("; ".join(errors))
    conflicts = alias_conflicts_for_object(paths.repo_root, normalized)
    if conflicts and not allow_alias_reassign:
        raise ProjectMemoryError("; ".join(conflicts))
    dump_path = memory_file_path(paths.repo_root, normalized["kind"], normalized["id"])
    dump_yaml(dump_path, normalized)

    alias_map = load_alias_entries(paths.repo_root)
    alias_map = {
        alias_text: entry
        for alias_text, entry in alias_map.items()
        if not (
            entry.get("id") == normalized["id"]
            and (not entry.get("kind") or entry.get("kind") == normalized["kind"])
        )
    }
    for alias_text in normalized.get("intent_aliases", []):
        alias_map[alias_text] = {"id": normalized["id"], "kind": normalized["kind"]}
    save_alias_map(paths.repo_root, alias_map)
    rebuild_index(paths.repo_root)
    return dump_path


def save_workflow(
    repo_root: Path | None,
    workflow: dict[str, Any],
    *,
    allow_alias_reassign: bool = False,
) -> Path:
    payload = dict(workflow)
    payload["kind"] = "workflow"
    return save_memory_object(repo_root, payload, allow_alias_reassign=allow_alias_reassign)


def save_fact(
    repo_root: Path | None,
    fact: dict[str, Any],
    *,
    allow_alias_reassign: bool = False,
) -> Path:
    payload = dict(fact)
    payload["kind"] = "fact"
    return save_memory_object(repo_root, payload, allow_alias_reassign=allow_alias_reassign)


def save_decision(
    repo_root: Path | None,
    decision: dict[str, Any],
    *,
    allow_alias_reassign: bool = False,
) -> Path:
    payload = dict(decision)
    payload["kind"] = "decision"
    return save_memory_object(repo_root, payload, allow_alias_reassign=allow_alias_reassign)


def archive_memory_object(
    repo_root: Path | None,
    object_id: str,
    *,
    kind: str | None = None,
    status: str = "archived",
    reason: str,
    archived_by: str,
    superseded_by: str = "",
    note: str = "",
    move_aliases_to_superseded: bool = False,
) -> tuple[Path, Path | None]:
    paths = ensure_memory_layout(repo_root)
    archive_status = normalize_base_status(status)
    if archive_status not in INACTIVE_BASE_STATUSES:
        raise ProjectMemoryError(
            f"Unsupported archive status: {status}. Expected one of: {', '.join(sorted(INACTIVE_BASE_STATUSES))}"
        )

    target_kind = normalize_memory_kind(kind) if kind else None
    if target_kind:
        memory_object = load_memory_object(paths.repo_root, target_kind, object_id)
    else:
        matches = find_memory_objects_by_id(paths.repo_root, object_id)
        if len(matches) > 1:
            raise ProjectMemoryError(
                f"Memory object id is ambiguous across kinds: {object_id}. Pass --kind explicitly."
            )
        memory_object = matches[0] if matches else {}
    if not memory_object:
        raise ProjectMemoryError(f"Memory object not found: {object_id}")

    archived_object = dict(memory_object)
    archived_object["status"] = archive_status
    archived_object["updated_at"] = utc_now_iso()
    archived_object["archive_reason"] = reason.strip()
    if archive_status == "deprecated":
        archived_object["deprecation_reason"] = reason.strip()
    archived_object["archived_at"] = utc_now_iso()
    archived_object["archived_by"] = archived_by.strip()
    if superseded_by.strip():
        archived_object["superseded_by"] = superseded_by.strip()
    if note.strip():
        archived_object["notes"] = merge_string_lists(archived_object.get("notes"), [note.strip()])

    old_aliases = normalize_string_list(archived_object.get("intent_aliases"))
    replacement_path: Path | None = None
    if move_aliases_to_superseded:
        if not superseded_by.strip():
            raise ProjectMemoryError("--move-aliases-to-superseded requires superseded_by")
        replacement_object = find_memory_object_by_id(paths.repo_root, superseded_by.strip())
        if not replacement_object:
            raise ProjectMemoryError(f"Replacement memory object not found: {superseded_by}")
        replacement_payload = dict(replacement_object)
        replacement_payload["intent_aliases"] = merge_string_lists(
            replacement_payload.get("intent_aliases"),
            old_aliases,
        )
        replacement_payload["updated_at"] = utc_now_iso()
        archived_object["archived_aliases"] = merge_string_lists(
            archived_object.get("archived_aliases"),
            old_aliases,
        )
        archived_object["intent_aliases"] = []
        archived_path = save_memory_object(paths.repo_root, archived_object)
        replacement_path = save_memory_object(
            paths.repo_root,
            replacement_payload,
            allow_alias_reassign=True,
        )
        return archived_path, replacement_path

    archived_path = save_memory_object(paths.repo_root, archived_object)
    return archived_path, replacement_path


def query_memory_objects(
    repo_root: Path | None,
    query: str,
    limit: int = 5,
    kinds: Iterable[str] | None = None,
    *,
    include_unusable: bool = False,
    min_score: float = DEFAULT_MIN_SCORE,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
) -> list[dict[str, Any]]:
    paths = ensure_memory_layout(repo_root)
    sync_index(paths.repo_root)
    target_kinds = parse_memory_kinds(kinds)
    query_norm = normalize_text(query)
    query_tokens = tokenize(query)
    alias_map = load_alias_map(paths.repo_root)
    alias_hit = alias_map.get(query_norm)
    matches: list[dict[str, Any]] = []

    for memory_object in load_memory_objects(paths.repo_root, target_kinds):
        object_id = normalize_string(memory_object.get("id"))
        kind = normalize_memory_kind(memory_object.get("kind", "workflow"))
        score = 0.0
        reasons: list[str] = []
        title = normalize_string(memory_object.get("title"))
        summary = normalize_string(memory_object.get("summary"))
        aliases = normalize_string_list(memory_object.get("intent_aliases"))
        tags = normalize_string_list(memory_object.get("tags"))
        search_values = iter_search_values(memory_object)

        if alias_hit and alias_hit["id"] == object_id and (not alias_hit.get("kind") or alias_hit["kind"] == kind):
            score += 120
            reasons.append("alias_map_exact")

        title_norm = normalize_text(title)
        if query_norm and title_norm and query_norm == title_norm:
            score += 100
            reasons.append("title_exact")
        elif query_norm and title_norm and (query_norm in title_norm or title_norm in query_norm):
            score += 70
            reasons.append("title_overlap")

        for alias in aliases:
            alias_norm = normalize_text(alias)
            if not alias_norm:
                continue
            if query_norm == alias_norm:
                score += 100
                reasons.append(f"alias_exact:{alias}")
                continue
            if query_norm and (query_norm in alias_norm or alias_norm in query_norm):
                score += 80
                reasons.append(f"alias_overlap:{alias}")
                continue
            similarity = difflib.SequenceMatcher(None, query_norm, alias_norm).ratio()
            if similarity >= 0.72:
                score += 40 + (similarity * 20)
                reasons.append(f"alias_similar:{alias}")

        candidate_tokens = tokenize(" ".join([title, summary, *aliases, *tags, *search_values]))
        if query_tokens and candidate_tokens:
            overlap = len(query_tokens & candidate_tokens) / len(query_tokens)
            if overlap > 0:
                score += overlap * 35
                reasons.append(f"token_overlap:{overlap:.2f}")

        blob_norm = normalize_text(memory_object_search_text(memory_object))
        if query_norm and blob_norm and query_norm in blob_norm:
            score += 25
            reasons.append("memory_text_overlap")

        if query_norm:
            similarity = difflib.SequenceMatcher(None, query_norm, blob_norm).ratio()
            if similarity >= 0.62:
                score += similarity * 20
                reasons.append(f"memory_text_similarity:{similarity:.2f}")

        status, stale_reasons = evaluate_memory_object_status(memory_object, paths.repo_root)
        if status in REUSABLE_BASE_STATUSES:
            score += 2
        if status in {"stale", "review_due", "deprecated"}:
            score -= 15

        if score <= 0:
            continue

        matches.append(
            {
                "object": memory_object,
                "score": round(score, 2),
                "effective_status": status,
                "base_status": normalize_base_status(memory_object.get("status")),
                "stale_reasons": stale_reasons,
                "match_reasons": dedupe_list(reasons),
            }
        )

    matches.sort(
        key=lambda item: (
            -item["score"],
            item["object"]["kind"],
            item["object"]["id"],
        )
    )
    reusable_reference_scores = [
        match["score"]
        for match in matches
        if match["effective_status"] in REUSABLE_BASE_STATUSES
    ]
    top_score = reusable_reference_scores[0] if reusable_reference_scores else (matches[0]["score"] if matches else 0.0)
    filtered: list[dict[str, Any]] = []
    for match in matches:
        relative_floor = top_score * DEFAULT_SCORE_RATIO if top_score >= 50 else min_score
        blockers = reuse_blockers_for_object(
            match["object"],
            match["score"],
            match["effective_status"],
            min_score=max(min_score, relative_floor),
            min_confidence=min_confidence,
        )
        match["reuse_blockers"] = blockers
        match["reusable"] = not blockers
        if include_unusable or match["reusable"]:
            filtered.append(match)
    return filtered[:limit]


def query_workflows(
    repo_root: Path | None,
    query: str,
    limit: int = 5,
    *,
    include_unusable: bool = False,
    min_score: float = DEFAULT_MIN_SCORE,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
) -> list[dict[str, Any]]:
    matches = query_memory_objects(
        repo_root,
        query,
        limit=limit,
        kinds=("workflow",),
        include_unusable=include_unusable,
        min_score=min_score,
        min_confidence=min_confidence,
    )
    return [
        {
            "workflow": match["object"],
            "score": match["score"],
            "status": match["effective_status"],
            "stale_reasons": match["stale_reasons"],
            "match_reasons": match["match_reasons"],
            "reusable": match["reusable"],
            "reuse_blockers": match["reuse_blockers"],
        }
        for match in matches
    ]
