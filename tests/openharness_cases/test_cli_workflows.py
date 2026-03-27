from __future__ import annotations

from .common import (
    Path,
    REQUIRED_TASK_PACKAGE_FILES,
    REPO_ROOT,
    argparse,
    json,
    load_manifest,
    openharness,
    pytest,
    validate_task_package,
    discover_task_packages,
)


def test_verify_reports_declared_manual_scenarios_without_claiming_execution(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "manual-only").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "manual-only"
    (root / "README.md").write_text("# Manual Only\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "04-verification.md").write_text("x\n", encoding="utf-8")
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Manual Only\n"
        "status: requirements_ready\n"
        "summary: manual verification only\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios:\n"
        "    - Open the app and confirm the banner text changes.\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="manual-only", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    assert result == 0
    assert calls == []
    assert "Declared manual scenarios" in captured.out
    assert "not executed automatically" in captured.out


def test_transition_rejects_skipped_forward_moves(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "skip-me").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "skip-me"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-950\n"
        "title: Skip Me\n"
        "status: proposed\n"
        "summary: transition skip coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_transition(
        argparse.Namespace(repo=str(repo_root), task="skip-me", target_status="overview_ready")
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "next legal forward status is `requirements_ready`" in captured.out
    assert "status: proposed" in (root / "STATUS.yaml").read_text(encoding="utf-8")


def test_bootstrap_reports_stage_guidance_in_text_output(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-960\n"
        "title: Visible Stage\n"
        "status: requirements_ready\n"
        "summary: stage guidance\n"
        "owner: codex\n"
        "created_at: 2026-03-24\n"
        "updated_at: 2026-03-24\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_bootstrap(argparse.Namespace(repo=str(repo_root), json=False, all=False))

    captured = capsys.readouterr()
    assert result == 0
    assert "Harness manifest:" not in captured.out
    assert "Task package root:" not in captured.out
    assert "current stage:" in captured.out
    assert "next stage:" in captured.out
    assert "next step:" in captured.out
    assert "`overview_ready`" in captured.out


def test_bootstrap_reports_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-962\n"
        "title: Visible Stage Author Entry\n"
        "status: requirements_ready\n"
        "summary: author entry surface\n"
        "owner: codex\n"
        "created_at: 2026-03-27\n"
        "updated_at: 2026-03-27\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_bootstrap(argparse.Namespace(repo=str(repo_root), json=False, all=False))

    captured = capsys.readouterr()
    assert result == 0
    assert "author entry:" in captured.out
    assert "author-entry.md" in captured.out


def test_update_runs_git_pull_then_uv_tool_upgrade_in_repo_root(
    capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[Path, str]] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append((repo, command))
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_update(argparse.Namespace())

    captured = capsys.readouterr()
    assert result == 0
    assert calls == [
        (REPO_ROOT, "git pull"),
        (REPO_ROOT, "uv tool upgrade openharness"),
    ]
    assert "Updated OpenHarness" in captured.out


def test_update_stops_when_git_pull_fails(capsys, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[Path, str]] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append((repo, command))
        if command == "git pull":
            return 1
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_update(argparse.Namespace())

    captured = capsys.readouterr()
    assert result == 1
    assert calls == [(REPO_ROOT, "git pull")]
    assert "git pull failed" in captured.out


def test_bootstrap_json_includes_stage_guidance(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-961\n"
        "title: Visible Stage Json\n"
        "status: detailed_ready\n"
        "summary: stage guidance json\n"
        "owner: codex\n"
        "created_at: 2026-03-24\n"
        "updated_at: 2026-03-24\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo ok\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_bootstrap(argparse.Namespace(repo=str(repo_root), json=True, all=False))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    task = payload["task_packages"][0]
    assert result == 0
    assert task["current_stage"] == "detailed_ready"
    assert task["next_stage"] == "in_progress"
    assert "implementation" in task["next_step"]


def test_bootstrap_json_includes_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-963\n"
        "title: Visible Stage Json Author Entry\n"
        "status: detailed_ready\n"
        "summary: author entry json\n"
        "owner: codex\n"
        "created_at: 2026-03-27\n"
        "updated_at: 2026-03-27\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_bootstrap(argparse.Namespace(repo=str(repo_root), json=True, all=False))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["author_entry"]["path"].endswith("author-entry.md")


def test_verify_records_artifact_and_status_metadata(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "artifact-run").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "artifact-run"
    (root / "README.md").write_text("# Artifact Run\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "04-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: x\n"
        "- Executed Path: y\n"
        "- Path Notes: z\n\n"
        "## Required Commands\n- echo ok\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "05-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- none\n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- a\n\n"
        "## Commands\n- echo ok\n\n"
        "## Follow-ups\n- none\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-951\n"
        "title: Artifact Run\n"
        "status: in_progress\n"
        "summary: verify artifact coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo ok\n"
        "  required_scenarios: []\n"
        "  last_run_at: \"\"\n"
        "  last_run_result: \"\"\n"
        "  last_run_artifact: \"\"\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="artifact-run", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    status = openharness._load_yaml(root / "STATUS.yaml")
    artifact_rel = status["verification"]["last_run_artifact"]
    artifact_path = repo_root / artifact_rel
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

    assert result == 0
    assert calls == ["echo ok"]
    assert "Recorded verification artifact" in captured.out
    assert artifact_path.exists()
    assert (artifact_path.parent / "latest.json").exists()
    assert status["verification"]["last_run_result"] == "passed"
    assert status["verification"]["last_run_at"]
    assert artifact["task_id"] == "OH-951"
    assert artifact["overall_result"] == "passed"
    assert artifact["package_fingerprint"]
    assert artifact["required_commands_snapshot"] == ["echo ok"]
    assert artifact["command_results"][0]["command"] == "echo ok"
    assert artifact["command_results"][0]["exit_code"] == 0


def test_transition_to_archived_moves_package_and_rewrites_paths(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "archive-me").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "archive-me"
    (root / "README.md").write_text("# Archive Me\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "04-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: docs/task-packages/archive-me/03-detailed-design.md\n"
        "- Executed Path: docs/task-packages/archive-me/04-verification.md\n"
        "- Path Notes: ok\n\n"
        "## Required Commands\n- echo ok\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "05-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- none\n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- docs/task-packages/archive-me/README.md\n\n"
        "## Commands\n- echo ok\n\n"
        "## Follow-ups\n- none\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-952\n"
        "title: Archive Me\n"
        "status: verifying\n"
        "summary: archive transition coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "entrypoints:\n"
        "  - docs/task-packages/archive-me/README.md\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo ok\n"
        "  required_scenarios: []\n"
        "  last_run_at: \"\"\n"
        "  last_run_result: \"\"\n"
        "  last_run_artifact: \"\"\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/task-packages/archive-me/04-verification.md\n"
        "    - docs/task-packages/archive-me/05-evidence.md\n"
        "  code: []\n"
        "  tests: []\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(openharness, "_run_command", lambda repo, command: 0)

    verify_result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="archive-me", check_tasks_only=False)
    )
    assert verify_result == 0

    result = openharness.cmd_transition(
        argparse.Namespace(repo=str(repo_root), task="archive-me", target_status="archived")
    )

    captured = capsys.readouterr()
    archived_root = repo_root / "docs" / "archived" / "task-packages" / "archive-me"

    assert result == 0
    assert "Archived task package" in captured.out
    assert not root.exists()
    assert archived_root.exists()
    archived_status = (archived_root / "STATUS.yaml").read_text(encoding="utf-8")
    archived_verification = (archived_root / "04-verification.md").read_text(encoding="utf-8")
    archived_evidence = (archived_root / "05-evidence.md").read_text(encoding="utf-8")
    assert "status: archived" in archived_status
    assert "docs/archived/task-packages/archive-me/README.md" in archived_status
    assert "docs/archived/task-packages/archive-me/04-verification.md" in archived_status
    assert "docs/archived/task-packages/archive-me/03-detailed-design.md" in archived_verification
    assert "docs/archived/task-packages/archive-me/README.md" in archived_evidence


def test_verify_rejects_packages_with_no_declared_verification_path(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "no-verification").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "no-verification"
    (root / "README.md").write_text("# No Verification\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "04-verification.md").write_text("x\n", encoding="utf-8")
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-998\n"
        "title: No Verification\n"
        "status: requirements_ready\n"
        "summary: missing verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="no-verification", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "insufficient verification" in captured.out
    assert "No command-backed verification or manual scenarios declared" in captured.out


def test_verify_defaults_to_later_stage_statuses_only(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )

    def write_package(name: str, status: str, command: str) -> None:
        root = repo_root / "docs" / "task-packages" / name
        root.mkdir(parents=True)
        (root / "README.md").write_text(f"# {name}\n", encoding="utf-8")
        (root / "01-requirements.md").write_text(
            "# Requirements\n\n"
            "## Goal\nA\n\n"
            "## Problem Statement\nB\n\n"
            "## Required Outcomes\n1. C\n\n"
            "## Non-Goals\n- D\n\n"
            "## Constraints\n- E\n",
            encoding="utf-8",
        )
        if status in {"overview_ready", "detailed_ready", "in_progress", "verifying", "archived"}:
            (root / "02-overview-design.md").write_text(
                "# Overview Design\n\n"
                "## System Boundary\nA\n\n"
                "## Proposed Structure\nB\n\n"
                "## Key Flows\nC\n\n"
                "## Trade-offs\nD\n\n"
                "## Overview Reflection\nE\n",
                encoding="utf-8",
            )
        else:
            (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
        if status in {"detailed_ready", "in_progress", "verifying", "archived"}:
            (root / "03-detailed-design.md").write_text(
                "# Detailed Design\n\n"
                "## Runtime Verification Plan\n"
                "- Verification Path:\n  - x\n"
                "- Fallback Path:\n  - y\n"
                "- Planned Evidence:\n  - z\n\n"
                "## Files Added Or Changed\n- a\n\n"
                "## Interfaces\nb\n\n"
                "## Error Handling\nc\n\n"
                "## Migration Notes\nd\n\n"
                "## Detailed Reflection\ne\n",
                encoding="utf-8",
            )
        else:
            (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
        if status in {"verifying", "archived"}:
            (root / "04-verification.md").write_text(
                "# Verification\n\n"
                "## Verification Path\n"
                "- Planned Path: x\n"
                "- Executed Path: y\n"
                "- Path Notes: z\n\n"
                "## Required Commands\n- cmd\n\n"
                "## Expected Outcomes\n- ok\n\n"
                "## Latest Result\n- pass\n",
                encoding="utf-8",
            )
        else:
            (root / "04-verification.md").write_text("x\n", encoding="utf-8")
        (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
        (root / "STATUS.yaml").write_text(
            f"id: {name.upper()}\n"
            f"title: {name}\n"
            f"status: {status}\n"
            "summary: status coverage\n"
            "owner: codex\n"
            "created_at: 2026-03-21\n"
            "updated_at: 2026-03-21\n"
            "done_criteria:\n"
            "  - x\n"
            "verification:\n"
            "  required_commands:\n"
            f"    - {command}\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    write_package("requirements", "requirements_ready", "echo requirements")
    write_package("detailed", "detailed_ready", "echo detailed")
    write_package("progress", "in_progress", "echo progress")
    write_package("verifying", "verifying", "echo verifying")

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="", check_tasks_only=False)
    )

    capsys.readouterr()
    assert result == 0
    assert calls == ["echo progress", "echo verifying"]


def test_verify_allows_explicit_package_target_before_in_progress(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "early-target"
    root.mkdir(parents=True)
    (root / "README.md").write_text("# Early Target\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "04-verification.md").write_text("x\n", encoding="utf-8")
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-777\n"
        "title: Early Target\n"
        "status: detailed_ready\n"
        "summary: explicit verify target\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo targeted\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="early-target", check_tasks_only=False)
    )

    capsys.readouterr()
    assert result == 0
    assert calls == ["echo targeted"]


def test_validate_design_package_rejects_requirements_ready_with_placeholder_requirements(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "placeholder-reqs").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "placeholder-reqs"
    (root / "README.md").write_text("# Placeholder Reqs\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\n\n"
        "## Problem Statement\n\n"
        "## Required Outcomes\n"
        "1. \n\n"
        "## Non-Goals\n"
        "- \n\n"
        "## Constraints\n"
        "- \n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "04-verification.md").write_text("x\n", encoding="utf-8")
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-903\n"
        "title: Placeholder Reqs\n"
        "status: requirements_ready\n"
        "summary: requirements shell only\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("requirements_ready requires non-placeholder content" in error for error in errors)


def test_validate_design_package_rejects_overview_ready_without_reflection(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "overview-no-reflection").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "overview-no-reflection"
    (root / "README.md").write_text("# Overview No Reflection\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "04-verification.md").write_text("x\n", encoding="utf-8")
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-904\n"
        "title: Overview No Reflection\n"
        "status: overview_ready\n"
        "summary: overview missing reflection\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("overview_ready requires non-placeholder content" in error for error in errors)
    assert any("## Overview Reflection" in error for error in errors)


def test_validate_design_package_rejects_archived_without_evidence_anchors(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-thin-evidence").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "archived" / "task-packages" / "archived-thin-evidence"
    (root / "README.md").write_text("# Archived Thin Evidence\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Detailed Reflection\nd\n",
        encoding="utf-8",
    )
    (root / "04-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: x\n"
        "- Executed Path: y\n"
        "- Path Notes: z\n\n"
        "## Required Commands\n- cmd\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "05-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- \n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- \n\n"
        "## Commands\n- \n\n"
        "## Follow-ups\n- later\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-905\n"
        "title: Archived Thin Evidence\n"
        "status: archived\n"
        "summary: archived without evidence anchors\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - uv run pytest\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("archived requires non-placeholder content" in error for error in errors)


def test_validate_design_package_accepts_detailed_ready_with_filled_semantic_anchors(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "detailed-solid").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 04-verification.md\n"
        "  - 05-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "detailed-solid"
    (root / "README.md").write_text("# Detailed Solid\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Stage Gates\nD0\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Stage Gates\ng\n\n"
        "## Decision Closure\nh\n\n"
        "## Error Handling\nc\n\n"
        "## Detailed Reflection\nd\n",
        encoding="utf-8",
    )
    (root / "04-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path:\n  - x\n"
        "- Executed Path:\n  - y\n"
        "- Path Notes:\n  - z\n\n"
        "## Required Commands\n- uv run pytest\n\n"
        "## Expected Outcomes\n- a\n\n"
        "## Traceability\n- b\n\n"
        "## Risk Acceptance\n- c\n\n"
        "## Latest Result\n- d\n",
        encoding="utf-8",
    )
    (root / "05-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-906\n"
        "title: Detailed Solid\n"
        "status: detailed_ready\n"
        "summary: detailed anchors filled\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]

    assert validate_task_package(package) == []
