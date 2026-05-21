
from .common import (
    Path,
    ALL_DESIGN_FILES,
    REPO_ROOT,
    TaskPackageDocument,
    json,
    pytest,
    setup_harness,
    validate_task_package,
    discover_task_packages,
)
import importlib
import subprocess
from typer.testing import CliRunner
from openharness_cli.cli import app

runner = CliRunner()


def test_bootstrap_reports_yaml_quote_hint_for_invalid_status_yaml(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "bad-yaml").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "bad-yaml"
    for doc in ALL_DESIGN_FILES:
        if doc != TaskPackageDocument.TASK_INFO:
            doc.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-998\n"
        "title: Bad YAML\n"
        "status: proposed\n"
        "summary: `overview-design.md` guidance: fix quoting\n"
        "owner: codex\n"
        "created_at: 2026-03-30\n"
        "updated_at: 2026-03-30\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list", "--json"])
    assert result.exit_code == 1
    assert "wrap the whole sentence in double quotes" in result.stdout
    assert 'summary: "`overview-design.md` guidance: fix quoting"' in result.stdout


def test_bootstrap_reports_stage_guidance_in_text_output(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-960\n"
        "title: Visible Stage\n"
        "status: overview_designing\n"
        "summary: stage guidance\n"
        "owner: codex\n"
        "created_at: 2026-03-24\n"
        "updated_at: 2026-03-24\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list"])
    assert result.exit_code == 0
    assert "Harness manifest:" not in result.stdout
    assert "Task package root:" not in result.stdout
    assert "current stage:" in result.stdout
    assert "next stage:" in result.stdout
    assert "next step:" in result.stdout
    assert "`overview_designing`" in result.stdout


def test_task_package_view_injects_current_stage_skill(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    state_root = repo_root / "skills" / "using-openharness" / "states" / "exploring-solution-space"
    state_root.mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (state_root / "instructions.md").write_text("# Overview Stage\n\nUse overview guidance.\n", encoding="utf-8")
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-964\n"
        "title: Visible Stage View\n"
        "status: overview_designing\n"
        "summary: stage view\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "view", "visible-stage"])

    assert result.exit_code == 0
    assert "Task: OH-964 Visible Stage View" in result.stdout
    assert "Status: `overview_designing`" in result.stdout
    assert "--- BEGIN: skills/using-openharness/states/exploring-solution-space/instructions.md ---" in result.stdout
    assert "# Overview Stage" in result.stdout


def test_transition_verified_reports_auto_archive(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "ready-to-archive").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "ready-to-archive"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text(
        "# 证据\n\n## 验证结果\npassed\n",
        encoding="utf-8",
    )
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-966\n"
        "title: Ready To Archive\n"
        "status: verifying\n"
        "summary: auto archive message\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "entrypoints:\n"
        "  - docs/task-packages/ready-to-archive/requirements.md\n"
        "verification:\n"
        "  verify_by: qualitative\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "ready-to-archive", "verified"],
    )

    assert result.exit_code == 0
    assert "Archived task package: OH-966" in result.stdout
    assert "already in `verifying`" not in result.stdout
    assert not root.exists()
    archived_info = repo_root / "docs" / "archived" / "task-packages" / "ready-to-archive" / "task-info.yaml"
    assert archived_info.exists()
    archived_text = archived_info.read_text(encoding="utf-8")
    assert "docs/archived/task-packages/ready-to-archive/requirements.md" in archived_text
    assert "README.md" not in archived_text


def test_transition_verified_keeps_source_status_when_archive_target_exists(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "archive-conflict").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archive-conflict").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "archive-conflict"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text(
        "# 证据\n\n## 验证结果\npassed\n",
        encoding="utf-8",
    )
    info_path = TaskPackageDocument.TASK_INFO.path_from(root)
    info_path.write_text(
        "id: OH-967\n"
        "title: Archive Conflict\n"
        "status: verifying\n"
        "summary: archive conflict\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "verification:\n"
        "  verify_by: qualitative\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "archive-conflict", "verified"],
    )

    assert result.exit_code == 1
    assert "archive target already exists" in result.stdout
    assert root.exists()
    assert "status: verifying" in info_path.read_text(encoding="utf-8")


def test_update_uses_installed_openharness_source_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    source_root = tmp_path / "openharness-source"
    source_root.mkdir()
    update_module = importlib.import_module("openharness_cli.commands.update")
    calls: list[tuple[tuple[str, ...], Path | None]] = []

    def fake_run(command_parts, cwd=None):
        calls.append((tuple(command_parts), Path(cwd) if cwd is not None else None))
        return subprocess.CompletedProcess(command_parts, 0)

    monkeypatch.setattr(update_module.subprocess, "run", fake_run)
    monkeypatch.setattr(update_module, "_source_root_from_installed_metadata", lambda: source_root)

    result = runner.invoke(app, ["--repo", str(project_root), "update"])

    assert result.exit_code == 0
    assert calls == [
        (("git", "pull"), source_root),
        (("uv", "tool", "upgrade", "--reinstall", "openharness"), source_root),
    ]
    assert f"Updated OpenHarness from {source_root}" in result.stdout


def test_openharness_source_root_falls_back_to_module_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    update_module = importlib.import_module("openharness_cli.commands.update")
    monkeypatch.setattr(update_module, "_source_root_from_installed_metadata", lambda: None)

    assert update_module._openharness_source_root() == REPO_ROOT


def test_init_parser_accepts_repo_argument() -> None:
    result = runner.invoke(app, ["--repo", "/tmp/example-repo", "init"])
    assert result.exit_code == 0


def test_init_creates_harness_gitignore_that_ignores_everything(
    tmp_path: Path, capsys
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    result = runner.invoke(app, ["--repo", str(repo_root), "init"])
    captured = capsys.readouterr()
    assert result.exit_code == 0
    assert (repo_root / ".harness" / ".gitignore").read_text(encoding="utf-8") == "*\n"
    assert "OpenHarness initialized" in result.stdout


def test_validate_design_package_rejects_overview_designed_without_reflection(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "overview-no-reflection").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "overview-no-reflection"
    TaskPackageDocument.REQUIREMENTS.path_from(root).write_text(
        "# 需求\n\n"
        "## 目标\nA\n\n"
        "## 问题陈述\nB\n\n"
        "## 必须交付的结果\n1. C\n\n"
        "## 非目标\n- D\n\n"
        "## 约束\n- E\n",
        encoding="utf-8",
    )
    TaskPackageDocument.OVERVIEW_DESIGN.path_from(root).write_text(
        "# 总体设计\n\n"
        "## 系统边界\nA\n\n"
        "## 推荐结构\nB\n\n"
        "## 关键流程\nC\n\n"
        "## 取舍\nD\n",
        encoding="utf-8",
    )
    TaskPackageDocument.DETAILED_DESIGN.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.VERIFICATION_DESIGN.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-904\n"
        "title: Overview No Reflection\n"
        "status: overview_designed\n"
        "summary: overview missing reflection\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert any("overview_designed requires non-placeholder content" in error for error in errors)
    assert any("## 总体设计反思" in error for error in errors)
