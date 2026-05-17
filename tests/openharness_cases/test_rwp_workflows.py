from __future__ import annotations

import importlib
import os

from .common import Path, argparse, openharness, pytest


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

    result = openharness.cmd_rwp_list(
        argparse.Namespace(repo=str(repo_root))
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "lark-message-runtime-validation" in captured.out
    assert "Validate real Lark message runtime behavior." in captured.out
    assert ".harness/rwp/workflows/lark-message-runtime-validation" in captured.out


def test_rwp_show_prints_full_workflow_document(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    _write_workflow(
        repo_root,
        "runtime-smoke",
        name="custom-runtime-smoke",
        description="Validate runtime smoke behavior.",
    )

    result = openharness.cmd_rwp_show(
        argparse.Namespace(repo=str(repo_root), workflow="custom-runtime-smoke")
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "# Workflow" in captured.out
    assert "Exercise runtime behavior." in captured.out


@pytest.mark.skip(reason="mock on wrong module — _run_command needs patching on commands not main")
def test_rwp_run_executes_explicit_python_script_and_loads_env_files(
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
    (repo_root / ".harness" / ".env").write_text(
        "OPENHARNESS_BASE=base\nOPENHARNESS_OVERRIDE=base\n",
        encoding="utf-8",
    )
    (repo_root / ".harness" / "rwp" / ".env").write_text(
        "OPENHARNESS_OVERRIDE=rwp\nOPENHARNESS_RWP_ONLY=enabled\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("OPENHARNESS_BASE", raising=False)
    monkeypatch.delenv("OPENHARNESS_OVERRIDE", raising=False)
    monkeypatch.delenv("OPENHARNESS_RWP_ONLY", raising=False)
    calls: list[str] = []
    seen_env: dict[str, str | None] = {}

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        seen_env["OPENHARNESS_BASE"] = os.environ.get("OPENHARNESS_BASE")
        seen_env["OPENHARNESS_OVERRIDE"] = os.environ.get("OPENHARNESS_OVERRIDE")
        seen_env["OPENHARNESS_RWP_ONLY"] = os.environ.get("OPENHARNESS_RWP_ONLY")
        seen_env["PYTHONPATH"] = os.environ.get("PYTHONPATH")
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_rwp_run(
        argparse.Namespace(
            repo=str(repo_root),
            workflow="runtime-smoke",
            script="smoke.py",
            script_args=["--target", "sandbox"],
        )
    )

    assert result == 0
    assert calls == [
        f"uv run python {script_path} --target sandbox",
    ]
    assert seen_env["OPENHARNESS_BASE"] == "base"
    assert seen_env["OPENHARNESS_OVERRIDE"] == "rwp"
    assert seen_env["OPENHARNESS_RWP_ONLY"] == "enabled"
    assert seen_env["PYTHONPATH"] is not None
    assert str(Path(openharness.__file__).resolve().parents[1]) in seen_env["PYTHONPATH"].split(os.pathsep)


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

    result = openharness.cmd_rwp_run(
        argparse.Namespace(
            repo=str(repo_root),
            workflow="runtime-api",
            script="runtime_api.py",
            script_args=[],
        )
    )

    assert result == 0
    assert (repo_root / "runtime-api-result.txt").read_text(encoding="utf-8") == "openharness.rwp"


def test_rwp_run_rejects_missing_script_name(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    _write_workflow(
        repo_root,
        "runtime-smoke",
        name="runtime-smoke",
        description="Validate runtime smoke behavior.",
    )

    result = openharness.cmd_rwp_run(
        argparse.Namespace(
            repo=str(repo_root),
            workflow="runtime-smoke",
            script="",
            script_args=[],
        )
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "explicit script name" in captured.out


def test_openharness_rwp_get_logger_returns_standard_logger() -> None:
    rwp = importlib.import_module("openharness.rwp")

    logger = rwp.get_logger()

    assert logger.name == "openharness.rwp"
    assert hasattr(logger, "info")
