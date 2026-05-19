
import importlib
import subprocess

from .common import Path, pytest
from typer.testing import CliRunner
from openharness_cli.cli import app

runner = CliRunner()


def _write_workflow(repo_root: Path, slug: str, *, name: str, description: str) -> Path:
    workflow_root = repo_root / ".harness" / "rwp" / "workflows" / slug
    workflow_root.mkdir(parents=True)
    (workflow_root / "workflow.md").write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        "# Workflow\n\n"
        "## Purpose\n"
        "Exercise runtime behavior.\n",
        encoding="utf-8",
    )
    (workflow_root / "scripts").mkdir()
    return workflow_root


def test_rwp_list_reports_workflow_summaries(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    _write_workflow(
        repo_root,
        "lark-message-runtime-validation",
        name="lark-message-runtime-validation",
        description="Validate real Lark message runtime behavior.",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "rwp", "list"])
    assert result.exit_code == 0
    assert "lark-message-runtime-validation" in result.stdout
    assert "Validate real Lark message runtime behavior." in result.stdout
    assert ".harness/rwp/workflows/lark-message-runtime-validation" in result.stdout


def test_rwp_view_prints_full_workflow_document(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    _write_workflow(
        repo_root,
        "runtime-smoke",
        name="custom-runtime-smoke",
        description="Validate runtime smoke behavior.",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "rwp", "view", "custom-runtime-smoke"])
    assert result.exit_code == 0
    assert "# Workflow" in result.stdout
    assert "Exercise runtime behavior." in result.stdout


def test_rwp_run_forwards_extra_args_to_script(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    workflow_root = _write_workflow(
        repo_root,
        "runtime-smoke",
        name="runtime-smoke",
        description="Validate runtime smoke behavior.",
    )
    script_path = workflow_root / "scripts" / "smoke.py"
    script_path.write_text("print('smoke')\n", encoding="utf-8")

    calls: list[str] = []

    def fake_run(cmd_parts, **kwargs):
        calls.append(" ".join(cmd_parts))
        return subprocess.CompletedProcess(args=cmd_parts, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = runner.invoke(app, [
        "--repo", str(repo_root), "rwp", "run", "runtime-smoke", "smoke.py",
        "--target", "sandbox",
    ])

    assert result.exit_code == 0
    assert calls == [
        f"uv run python {script_path} --target sandbox",
    ]


def test_rwp_run_exposes_openharness_runtime_api_to_project_python(
    tmp_path: Path
) -> None:
    repo_root = tmp_path / "repo"
    workflow_root = _write_workflow(
        repo_root,
        "runtime-api",
        name="runtime-api",
        description="Validate OpenHarness runtime API import.",
    )
    script_path = workflow_root / "scripts" / "runtime_api.py"
    script_path.write_text(
        "from pathlib import Path\n"
        "from openharness.rwp import get_logger\n"
        "Path('runtime-api-result.txt').write_text(get_logger().name, encoding='utf-8')\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, [
        "--repo", str(repo_root), "rwp", "run", "runtime-api", "runtime_api.py",
    ])

    assert result.exit_code == 0
    assert (repo_root / "runtime-api-result.txt").read_text(encoding="utf-8") == "openharness.rwp"


def test_rwp_run_rejects_missing_script_name(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    _write_workflow(
        repo_root,
        "runtime-smoke",
        name="runtime-smoke",
        description="Validate runtime smoke behavior.",
    )

    result = runner.invoke(app, [
        "--repo", str(repo_root), "rwp", "run", "runtime-smoke", "",
    ])

    assert result.exit_code == 1
    assert "explicit script name" in result.stdout


def test_openharness_rwp_get_logger_returns_standard_logger() -> None:
    rwp = importlib.import_module("openharness.rwp")

    logger = rwp.get_logger()

    assert logger.name == "openharness.rwp"
    assert hasattr(logger, "info")
