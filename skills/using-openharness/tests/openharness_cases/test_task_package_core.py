from __future__ import annotations

from .common import (
    ACTIVE_STATUSES,
    Path,
    REPO_ROOT,
    REQUIRED_TASK_PACKAGE_FILES,
    TaskScaffoldRequest,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    load_manifest,
    openharness,
    slugify_task_name,
    summarize_task_package,
    validate_task_package,
)


def test_manifest_points_to_task_package_roots() -> None:
    manifest = load_manifest(REPO_ROOT)
    assert manifest.task_packages_root == REPO_ROOT / "docs" / "task-packages"
    assert manifest.archived_task_packages_root == REPO_ROOT / "docs" / "archived" / "task-packages"


def test_self_hosting_design_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "self-hosting-bootstrap")
    assert package.task_id == "OH-001"
    assert package.status_name == "archived"
    assert "Self-Hosting Bootstrap" in summarize_task_package(package)


def test_workflow_redesign_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "workflow-redesign")
    assert package.task_id == "OH-002"
    assert package.status_name == "archived"
    assert "Workflow Redesign" in summarize_task_package(package)


def test_reflective_design_review_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "reflective-design-review")
    assert package.task_id == "OH-003"
    assert package.status_name == "archived"
    assert "Reflective Design Review" in summarize_task_package(package)


def test_active_statuses_do_not_include_archived() -> None:
    assert "in_progress" in ACTIVE_STATUSES
    assert "archived" not in ACTIVE_STATUSES


def test_allocate_next_task_id_uses_existing_prefix_and_width(tmp_path: Path) -> None:
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    for root_name, task_id, status in (
        ("one", "OH-018", "proposed"),
        ("two", "OH-099", "archived"),
    ):
        root = repo_root / "docs" / ("task-packages" if status == "proposed" else "archived/task-packages") / root_name
        root.mkdir(parents=True)
        for name in REQUIRED_TASK_PACKAGE_FILES:
            (root / name).write_text("# x\n", encoding="utf-8")
        (root / "STATUS.yaml").write_text(
            f"id: {task_id}\n"
            "title: Example\n"
            f"status: {status}\n"
            "summary: example\n"
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

    assert allocate_next_task_id(repo_root) == "OH-100"


def test_cmd_new_task_supports_auto_id(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    for name, contents in {
        "task-package.README.md": "# <DESIGN_ID> <TITLE>\n",
        "task-package.STATUS.yaml": (
            "id: <DESIGN_ID>\n"
            "title: <TITLE>\n"
            "status: <STATUS>\n"
            "summary: <SUMMARY>\n"
            "owner: <OWNER>\n"
            "created_at: <DATE>\n"
            "updated_at: <DATE>\n"
            "done_criteria:\n"
            "  - x\n"
            "verification:\n"
            "  required_commands: []\n"
            "  required_scenarios: []\n"
        ),
        "task-package.01-requirements.md": "req\n",
        "task-package.02-overview-design.md": "overview\n",
        "task-package.03-detailed-design.md": "detailed\n",
        "task-package.05-verification.md": "verify\n",
        "task-package.06-evidence.md": "evidence\n",
    }.items():
        (repo_root / "skills" / "using-openharness" / "references" / "templates" / name).write_text(
            contents,
            encoding="utf-8",
        )

    existing = repo_root / "docs" / "task-packages" / "existing"
    existing.mkdir(parents=True)
    for file_name in REQUIRED_TASK_PACKAGE_FILES:
        (existing / file_name).write_text("# x\n", encoding="utf-8")
    (existing / "STATUS.yaml").write_text(
        "id: OH-009\n"
        "title: Existing\n"
        "status: proposed\n"
        "summary: existing\n"
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

    result = openharness.cmd_new_task(
        __import__("argparse").Namespace(
            repo=str(repo_root),
            task_name="next-task",
            legacy_task_id="",
            legacy_title="",
            task_id="",
            title="Next Task",
            auto_id=True,
            owner="codex",
            summary="auto id",
            status="proposed",
        )
    )

    captured = capsys.readouterr()
    created = repo_root / "docs" / "task-packages" / "next-task" / "STATUS.yaml"
    assert result == 0
    assert "Task id: OH-010" in captured.out
    assert "id: OH-010" in created.read_text(encoding="utf-8")


def test_design_packages_validate_cleanly() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    assert find_duplicate_task_ids(packages) == {}
    errors = [error for package in packages for error in validate_task_package(package)]
    assert errors == []


def test_find_duplicate_task_ids_reports_conflicts(tmp_path: Path) -> None:
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )

    first = repo_root / "docs" / "task-packages" / "one"
    second = repo_root / "docs" / "archived" / "task-packages" / "two"
    for root, status in ((first, "proposed"), (second, "archived")):
        root.mkdir(parents=True)
        for name in REQUIRED_TASK_PACKAGE_FILES:
            (root / name).write_text("# x\n", encoding="utf-8")
        (root / "STATUS.yaml").write_text(
            "id: OH-999\n"
            "title: Duplicate\n"
            f"status: {status}\n"
            "summary: dup\n"
            "owner: codex\n"
            "created_at: 2026-03-23\n"
            "updated_at: 2026-03-23\n"
            "done_criteria:\n"
            "  - x\n"
            "verification:\n"
            "  required_commands:\n"
            "    - uv run pytest\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    manifest = load_manifest(repo_root)
    packages = discover_task_packages(repo_root, manifest)
    duplicates = find_duplicate_task_ids(packages)

    assert set(duplicates) == {"OH-999"}
    assert {package.name for package in duplicates["OH-999"]} == {"one", "two"}


def test_load_manifest_prefers_repo_local_skills_layout(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    assert manifest.path == (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml")


def test_validate_task_package_rejects_unknown_status_and_missing_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "broken").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "broken"
    for name in (
        "README.md",
        "01-requirements.md",
        "02-overview-design.md",
        "03-detailed-design.md",
        "05-verification.md",
        "06-evidence.md",
    ):
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Broken Package\n"
        "status: invalid_status\n"
        "summary: bad\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "entrypoints:\n"
        "  - docs/task-packages/broken/README.md\n"
        "  - docs/task-packages/broken/missing.md\n"
        "verification:\n"
        "  required_commands: []\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/task-packages/broken/06-evidence.md\n"
        "    - docs/task-packages/broken/nope.md\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("unknown status" in error for error in errors)
    assert any("missing referenced path" in error for error in errors)


def test_validate_task_package_rejects_archived_status_in_active_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "wrong-place").mkdir(parents=True)
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "wrong-place"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Wrong Place\n"
        "status: archived\n"
        "summary: bad\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n",
        encoding="utf-8",
    )
    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)
    assert any("archived package must live under" in error for error in errors)


def test_validate_task_package_rejects_verifying_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "verifying-empty").mkdir(parents=True)
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
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
    root = repo_root / "docs" / "task-packages" / "verifying-empty"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-901\n"
        "title: Verifying Empty\n"
        "status: verifying\n"
        "summary: missing verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
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

    assert any("verifying status requires at least one verification path" in error for error in errors)


def test_validate_task_package_rejects_archived_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-empty").mkdir(parents=True)
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
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
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
    root = repo_root / "docs" / "archived" / "task-packages" / "archived-empty"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-902\n"
        "title: Archived Empty\n"
        "status: archived\n"
        "summary: archived without verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
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

    assert any("archived status requires at least one verification path" in error for error in errors)


def test_slugify_task_name_normalizes_human_text() -> None:
    assert slugify_task_name("Harness Replay Flow") == "harness-replay-flow"


def test_create_task_package_from_templates(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\ntask_packages_root: docs/task-packages\narchived_task_packages_root: docs/archived/task-packages\nrequired_design_files:\n"
        "  - README.md\n  - STATUS.yaml\n  - 01-requirements.md\n  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n  - 05-verification.md\n  - 06-evidence.md\n",
        encoding="utf-8",
    )
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    for file_name, content in {
        "task-package.README.md": "# <DESIGN_ID> <TITLE>\n",
        "task-package.STATUS.yaml": "id: <DESIGN_ID>\ntitle: <TITLE>\nstatus: <STATUS>\nsummary: <SUMMARY>\nowner: <OWNER>\ncreated_at: <DATE>\nupdated_at: <DATE>\ndone_criteria:\n  - x\nverification:\n  required_commands: []\n",
        "task-package.01-requirements.md": "req\n",
        "task-package.02-overview-design.md": "overview\n",
        "task-package.03-detailed-design.md": "detail\n",
        "task-package.05-verification.md": "verify\n",
        "task-package.06-evidence.md": "evidence\n",
    }.items():
        (template_root / file_name).write_text(content, encoding="utf-8")

    task_root = create_task_package(
        TaskScaffoldRequest(
            repo_root=repo_root,
            task_name="Harness Replay",
            task_id="OH-016",
            title="Harness Replay",
            owner="codex",
            summary="Replay scenarios.",
        )
    )

    assert task_root == repo_root / "docs" / "task-packages" / "harness-replay"
    assert (task_root / "README.md").read_text(encoding="utf-8") == "# OH-016 Harness Replay\n"
    assert not (task_root / "04-implementation-plan.md").exists()
    assert "summary: Replay scenarios." in (task_root / "STATUS.yaml").read_text(encoding="utf-8")


def test_key_repo_skills_are_vendored_locally() -> None:
    expected = [
        "using-openharness",
        "exploring-solution-space",
        "using-git-worktrees",
        "verification-before-completion",
        "systematic-debugging",
        "finishing-a-development-branch",
    ]
    for name in expected:
        path = REPO_ROOT / "skills" / name
        assert path.is_dir()
        assert (path / "SKILL.md").exists()


def test_retired_skills_are_not_shipped_live() -> None:
    for name in ["executing-plans", "writing-plans", "writing-skills"]:
        assert not (REPO_ROOT / "skills" / name).exists()
