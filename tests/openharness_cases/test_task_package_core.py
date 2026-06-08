
import pytest
from typer.testing import CliRunner

from .common import (
    ACTIVE_STATUSES,
    Path,
    REPO_ROOT,
    ALL_DESIGN_FILES,
    TaskPackageDocument,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    setup_harness,
    slugify_task_name,
    summarize_task_package,
    validate_task_package,
)
from openharness_cli.cli import app
from openharness_cli.core.yaml import load_yaml

runner = CliRunner()
REMOVED_TASK_INFO_KEYS = ("done" + "_criteria", "depends" + "_on", "scope")
TASK_TYPE_PLACEHOLDER = "<mechanical|standard|structural|>"
DESIGN_REVIEW_MODE_PLACEHOLDER = "<stepwise|auto|>"
VERIFICATION_METHOD_PLACEHOLDER = "<unit_test|qualitative|>"
RWP_ENABLED_PLACEHOLDER = "<true|false|>"
RWP_REASON_PLACEHOLDER = "<rwp reason>"


def _write_minimal_openharness_repo(repo_root: Path) -> None:
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    for name, contents in {
        "task-package.task-info.yaml": (
            "id: <TASK_ID>\n"
            "title: <TITLE>\n"
            "status: <STATUS>\n"
            "summary: <SUMMARY>\n"
            "owner: <GIT OWNER>\n"
            "created_at: <DATE>\n"
            "updated_at: <DATE>\n"
            "collaboration:\n"
            f"  task_type: {TASK_TYPE_PLACEHOLDER}\n"
            f"  design_review_mode: {DESIGN_REVIEW_MODE_PLACEHOLDER}\n"
            "verification:\n"
            f"  method: {VERIFICATION_METHOD_PLACEHOLDER}\n"
            "  rwp:\n"
            f"    enabled: {RWP_ENABLED_PLACEHOLDER}\n"
            f"    reason: {RWP_REASON_PLACEHOLDER}\n"
        ),
        "task-package.requirements.md": "req\n",
        "task-package.overview-design.md": "overview\n",
        "task-package.detailed-design.md": "detailed\n",
        "task-package.verification-design.md": "verify\n",
        "task-package.evidence.md": "evidence\n",
    }.items():
        (repo_root / "skills" / "using-openharness" / "references" / "templates" / name).write_text(
            contents,
            encoding="utf-8",
        )


def test_harness_config_default_task_package_paths() -> None:
    hx = setup_harness(REPO_ROOT)
    assert hx.config.task_packages_root == REPO_ROOT / "docs" / "task-packages"
    assert hx.config.archived_task_packages_root == REPO_ROOT / "docs" / "archived" / "task-packages"


def test_self_hosting_design_package_is_discoverable() -> None:
    setup_harness(REPO_ROOT)
    packages = discover_task_packages()
    package = next(package for package in packages if package.name == "self-hosting-bootstrap")
    assert package.task_id == "OH-001"
    assert package.current_status == "archived"
    assert "Self-Hosting Bootstrap" in summarize_task_package(package)


def test_workflow_redesign_package_is_discoverable() -> None:
    setup_harness(REPO_ROOT)
    packages = discover_task_packages()
    package = next(package for package in packages if package.name == "workflow-redesign")
    assert package.task_id == "OH-002"
    assert package.current_status == "archived"
    assert "Workflow Redesign" in summarize_task_package(package)


def test_reflective_design_review_package_is_discoverable() -> None:
    setup_harness(REPO_ROOT)
    packages = discover_task_packages()
    package = next(package for package in packages if package.name == "reflective-design-review")
    assert package.task_id == "OH-003"
    assert package.current_status == "archived"
    assert "Reflective Design Review" in summarize_task_package(package)


def test_active_statuses_do_not_include_archived() -> None:
    assert "implementing" in ACTIVE_STATUSES
    assert "archived" not in ACTIVE_STATUSES


def test_allocate_next_task_id_uses_existing_prefix_and_width(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    for root_name, task_id, status in (
        ("one", "TASK-018", "proposing"),
        ("two", "TASK-099", "archived"),
    ):
        root = repo_root / "docs" / ("task-packages" if status == "proposing" else "archived/task-packages") / root_name
        root.mkdir(parents=True)
        for doc in ALL_DESIGN_FILES:
            doc.path_from(root).write_text("# x\n", encoding="utf-8")
        TaskPackageDocument.TASK_INFO.path_from(root).write_text(
            f"id: {task_id}\n"
            "title: Example\n"
            f"status: {status}\n"
            "summary: example\n"
            "owner: codex\n"
            "created_at: 2026-03-24\n"
            "updated_at: 2026-03-24\n"
            "verification:\n"
            "  required_commands: []\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    setup_harness(repo_root)
    assert allocate_next_task_id() == "TASK-100"


def test_new_package_creates_with_auto_id(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    _write_minimal_openharness_repo(repo_root)

    existing = repo_root / "docs" / "task-packages" / "existing"
    existing.mkdir(parents=True)
    for doc in ALL_DESIGN_FILES:
        doc.path_from(existing).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(existing).write_text(
        "id: TASK-009\n"
        "title: Existing\n"
        "status: proposed\n"
        "summary: existing\n"
        "owner: codex\n"
        "created_at: 2026-03-24\n"
        "updated_at: 2026-03-24\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    from openharness_cli.commands.task_package import new_package
    new_package(
        task_name="next-task",
        title="Next Task",
        summary="auto id",
        status="proposing",
    )

    captured = capsys.readouterr()
    created = repo_root / "docs" / "task-packages" / "next-task" / "task-info.yaml"
    status = load_yaml(created)
    assert "Task id: TASK-010" in captured.out
    assert status["id"] == "TASK-010"
    assert all(key not in status for key in REMOVED_TASK_INFO_KEYS)


def test_new_package_injects_git_owner_from_effective_git_config(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    _write_minimal_openharness_repo(repo_root)
    repo_root.mkdir(exist_ok=True)
    import subprocess

    subprocess.run(["git", "init", "-q"], cwd=repo_root, check=True)
    subprocess.run(["git", "config", "user.name", "Temp Owner"], cwd=repo_root, check=True)

    result = runner.invoke(
        app,
        [
            "--repo",
            str(repo_root),
            "task-package",
            "new",
            "git-owner-smoke",
            "--title",
            "Git Owner Smoke",
        ],
    )

    assert result.exit_code == 0
    info_path = repo_root / "docs" / "task-packages" / "git-owner-smoke" / "task-info.yaml"
    info_text = info_path.read_text(encoding="utf-8")
    status = load_yaml(info_path)
    assert status["owner"] == "Temp Owner"
    assert "<GIT OWNER>" not in info_text


def test_new_package_rejects_owner_option(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    _write_minimal_openharness_repo(repo_root)

    result = runner.invoke(
        app,
        [
            "--repo",
            str(repo_root),
            "task-package",
            "new",
            "manual-owner",
            "--owner",
            "codex",
        ],
    )

    assert result.exit_code != 0
    assert not (repo_root / "docs" / "task-packages" / "manual-owner").exists()


def test_find_duplicate_task_ids_reports_conflicts(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)

    first = repo_root / "docs" / "task-packages" / "one"
    second = repo_root / "docs" / "archived" / "task-packages" / "two"
    for root, status in ((first, "proposing"), (second, "archived")):
        root.mkdir(parents=True)
        for doc in ALL_DESIGN_FILES:
            doc.path_from(root).write_text("# x\n", encoding="utf-8")
        TaskPackageDocument.TASK_INFO.path_from(root).write_text(
            "id: OH-999\n"
            "title: Duplicate\n"
            f"status: {status}\n"
            "summary: dup\n"
            "owner: codex\n"
            "created_at: 2026-03-23\n"
            "updated_at: 2026-03-23\n"
            "verification:\n"
            "  required_commands:\n"
            "    - uv run pytest\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    setup_harness(repo_root)
    packages = discover_task_packages()
    duplicates = find_duplicate_task_ids(packages)

    assert set(duplicates) == {"OH-999"}
    assert {package.name for package in duplicates["OH-999"]} == {"one", "two"}


def test_validate_task_package_rejects_unknown_status_but_allows_stale_entrypoints(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "task-packages" / "broken").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "broken"
    for doc in (
        TaskPackageDocument.REQUIREMENTS,
        TaskPackageDocument.OVERVIEW_DESIGN,
        TaskPackageDocument.DETAILED_DESIGN,
        TaskPackageDocument.VERIFICATION_DESIGN,
        TaskPackageDocument.EVIDENCE,
    ):
        doc.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-999\n"
        "title: Broken Package\n"
        "status: invalid_status\n"
        "summary: bad\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "entrypoints:\n"
        "  - docs/task-packages/broken/README.md\n"
        "  - docs/task-packages/broken/missing.md\n"
        "verification:\n"
        "  required_commands: []\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/task-packages/broken/evidence.md\n"
        "    - docs/task-packages/broken/nope.md\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert any("unknown status" in error for error in errors)
    removed_done_key = REMOVED_TASK_INFO_KEYS[0]
    assert all(f"missing required key `{removed_done_key}`" not in error for error in errors)
    assert all("missing referenced path" not in error for error in errors)


def test_validate_task_package_ignores_archived_legacy_references(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-legacy").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "legacy" / "skills" / "using-openharness" / "scripts").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "legacy" / "skills" / "using-openharness" / "scripts" / "openharness.py").write_text(
        "legacy snapshot\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "archived" / "task-packages" / "archived-legacy"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-903\n"
        "title: Archived Legacy\n"
        "status: archived\n"
        "summary: archived with legacy file reference\n"
        "owner: codex\n"
        "created_at: 2026-03-27\n"
        "updated_at: 2026-03-27\n"
        "verification:\n"
        "  required_commands:\n"
        "    - uv run pytest\n"
        "  required_scenarios: []\n"
        "evidence:\n"
        "  code:\n"
        "    - skills/using-openharness/scripts/openharness.py\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert all("missing referenced path" not in error for error in errors)


def test_gate_precondition_failure_does_not_persist_intermediate_status(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "missing-gate-fields").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "missing-gate-fields"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    info_path = TaskPackageDocument.TASK_INFO.path_from(root)
    info_path.write_text(
        "id: OH-965\n"
        "title: Missing Gate Fields\n"
        "status: proposing\n"
        "summary: gate precondition\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "missing-gate-fields", "requirements_designed"],
    )

    assert result.exit_code == 1
    assert "task_type is not confirmed" in result.stdout
    assert "verification method is not determined" in result.stdout
    assert "RWP setting is not confirmed" in result.stdout
    assert load_yaml(info_path)["status"] == "proposing"


def test_gate_precondition_requires_rwp_reason_after_rwp_setting_is_confirmed(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "missing-rwp-reason").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "missing-rwp-reason"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    info_path = TaskPackageDocument.TASK_INFO.path_from(root)
    info_path.write_text(
        "id: OH-969\n"
        "title: Missing RWP Reason\n"
        "status: proposing\n"
        "summary: gate precondition\n"
        "owner: codex\n"
        "created_at: 2026-06-09\n"
        "updated_at: 2026-06-09\n"
        "collaboration:\n"
        "  task_type: standard\n"
        "  design_review_mode: stepwise\n"
        "verification:\n"
        "  method: unit_test\n"
        "  rwp:\n"
        "    enabled: false\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "missing-rwp-reason", "requirements_designed"],
    )

    assert result.exit_code == 1
    assert "RWP reason is not documented" in result.stdout
    assert load_yaml(info_path)["status"] == "proposing"


def test_validate_task_package_reports_unknown_verification_method(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "task-packages" / "bad-method").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "bad-method"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-970\n"
        "title: Bad Method\n"
        "status: proposing\n"
        "summary: invalid method\n"
        "owner: codex\n"
        "created_at: 2026-06-09\n"
        "updated_at: 2026-06-09\n"
        "collaboration:\n"
        "  task_type: standard\n"
        "  design_review_mode: stepwise\n"
        "verification:\n"
        "  method: rwp\n"
        "  rwp:\n"
        "    enabled: false\n"
        "    reason: no runtime evidence\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert any("unknown verification.method `rwp`" in error for error in errors)
    assert package.raw_verification_method == "rwp"
    assert package.verification_method == ""


def test_validate_task_package_rejects_string_rwp_enabled(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "task-packages" / "bad-rwp-enabled").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "bad-rwp-enabled"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-971\n"
        "title: Bad RWP Enabled\n"
        "status: proposing\n"
        "summary: invalid rwp enabled\n"
        "owner: codex\n"
        "created_at: 2026-06-09\n"
        "updated_at: 2026-06-09\n"
        "verification:\n"
        "  method: unit_test\n"
        "  rwp:\n"
        "    enabled: \"false\"\n"
        "    reason: no runtime evidence\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert any("`verification.rwp.enabled` must be a boolean" in error for error in errors)


def test_slugify_task_name_normalizes_human_text() -> None:
    assert slugify_task_name("Harness Replay Flow") == "harness-replay-flow"


def test_create_task_package_from_templates(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    for file_name, content in {
        "task-package.task-info.yaml": (
            "id: <TASK_ID>\n"
            "title: <TITLE>\n"
            "status: <STATUS>\n"
            "summary: <SUMMARY>\n"
            "owner: <GIT OWNER>\n"
            "created_at: <DATE>\n"
            "updated_at: <DATE>\n"
            "collaboration:\n"
            f"  task_type: {TASK_TYPE_PLACEHOLDER}\n"
            f"  design_review_mode: {DESIGN_REVIEW_MODE_PLACEHOLDER}\n"
            "verification:\n"
            f"  method: {VERIFICATION_METHOD_PLACEHOLDER}\n"
            "  rwp:\n"
            f"    enabled: {RWP_ENABLED_PLACEHOLDER}\n"
            f"    reason: {RWP_REASON_PLACEHOLDER}\n"
        ),
        "task-package.requirements.md": "req\n",
        "task-package.overview-design.md": "overview\n",
        "task-package.detailed-design.md": "detail\n",
        "task-package.verification-design.md": "verify\n",
        "task-package.evidence.md": "evidence\n",
    }.items():
        (template_root / file_name).write_text(content, encoding="utf-8")

    setup_harness(repo_root)
    task_root, task_id = create_task_package(
        task_name="Harness Replay",
        title="Harness Replay",
        summary="Replay scenarios.",
    )

    assert task_root == repo_root / "docs" / "task-packages" / "harness-replay"
    assert task_id.startswith("TASK-")
    assert not (task_root / "README.md").exists()
    assert TaskPackageDocument.REQUIREMENTS.path_from(task_root).exists()
    assert not TaskPackageDocument.OVERVIEW_DESIGN.path_from(task_root).exists()
    assert not TaskPackageDocument.DETAILED_DESIGN.path_from(task_root).exists()
    assert not TaskPackageDocument.VERIFICATION_DESIGN.path_from(task_root).exists()
    assert not TaskPackageDocument.EVIDENCE.path_from(task_root).exists()
    status = load_yaml(TaskPackageDocument.TASK_INFO.path_from(task_root))
    assert status["id"] == task_id
    assert status["summary"] == "Replay scenarios."
    assert status["owner"] != "<GIT OWNER>"
    assert all(key not in status for key in REMOVED_TASK_INFO_KEYS)
    assert status["collaboration"]["task_type"] == TASK_TYPE_PLACEHOLDER
    assert status["collaboration"]["design_review_mode"] == DESIGN_REVIEW_MODE_PLACEHOLDER
    assert status["verification"]["method"] == VERIFICATION_METHOD_PLACEHOLDER
    assert status["verification"]["rwp"]["enabled"] == RWP_ENABLED_PLACEHOLDER
    assert status["verification"]["rwp"]["reason"] == RWP_REASON_PLACEHOLDER


def test_key_repo_skills_are_vendored_locally() -> None:
    # Entry skill
    assert (REPO_ROOT / "skills" / "using-openharness").is_dir()
    assert (REPO_ROOT / "skills" / "using-openharness" / "SKILL.md").exists()
    # Hook-injected state skills
    states_base = REPO_ROOT / "skills" / "using-openharness" / "states"
    for name in [
        "proposing",
        "exploring-solution-space",
        "detailed-design",
        "verification-designing",
        "implementing",
        "verifying",
    ]:
        assert (states_base / name).is_dir(), f"state skill {name} missing"
        assert (states_base / name / "instructions.md").exists(), f"state skill {name}/instructions.md missing"
    assert not (states_base / "finishing-a-development-branch").exists()


def test_retired_skills_are_not_shipped_live() -> None:
    for name in ["executing-plans", "writing-plans", "writing-skills"]:
        assert not (REPO_ROOT / "skills" / name).exists()
