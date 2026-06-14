
import pytest

from pathlib import Path
import tomllib

from .common import openharness


def test_entrypoint_re_exports_package_main_and_parser() -> None:
    package_root = Path(__file__).resolve().parents[2] / "openharness_cli"
    assert package_root.is_dir()
    assert hasattr(openharness, "main")
    assert hasattr(openharness, "app")


def test_pyproject_exposes_openharness_console_script() -> None:
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("openharness") == "openharness_cli.main:main"


def test_parser_help_includes_top_level_description() -> None:
    from typer.testing import CliRunner
    from openharness_cli.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert "Openharness repository workflow CLI." in result.stdout
    assert "update" in result.stdout
    assert "Update" in result.stdout

    result = runner.invoke(app, ["update", "--help"])
    assert "Update the OpenHarness clone and refresh the installed CLI tool." in result.stdout
    assert "--force-sync" in result.stdout
    assert "Discard local changes" in result.stdout
    assert "dev-source" in result.stdout


def test_update_reinstalls_existing_tool_source(monkeypatch) -> None:
    from typer.testing import CliRunner
    import subprocess
    from openharness_cli.cli import app

    calls: list[tuple[list[str], str]] = []

    def fake_run(command, cwd=None, capture_output=False, text=False):
        calls.append((list(command), str(cwd)))
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    runner = CliRunner()
    result = runner.invoke(app, ["update", "--mode", "dev-source"])

    assert result.exit_code == 0
    assert [command for command, _ in calls] == [
        ["uv", "tool", "upgrade", "--reinstall", "openharness"],
    ]


def test_fallback_update_retries_default_force_sync_and_stops_before_upgrade(monkeypatch, capsys, tmp_path: Path) -> None:
    import subprocess
    import pytest
    from openharness_cli import main as entrypoint

    calls: list[list[str]] = []

    def fake_run(command, cwd=None, capture_output=False, text=False):
        calls.append(list(command))
        return subprocess.CompletedProcess(
            args=command,
            returncode=1,
            stdout="fallback stdout",
            stderr="fallback stderr",
        )

    monkeypatch.setattr(entrypoint, "_find_source_root", lambda: tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        entrypoint._run_update()

    output = capsys.readouterr().out
    assert exc_info.value.code == 1
    assert calls == [
        ["git", "fetch", "--prune"],
        ["git", "fetch", "--prune"],
        ["git", "fetch", "--prune"],
    ]
    assert "Attempt 3/3 failed for `git fetch --prune`" in output
    assert "stdout: fallback stdout" in output
    assert "stderr: fallback stderr" in output
    assert "refusing to continue with tool upgrade" in output


def test_fallback_update_dev_source_skips_git_sync(monkeypatch, tmp_path: Path) -> None:
    import subprocess
    from openharness_cli import main as entrypoint

    calls: list[list[str]] = []

    def fake_run(command, cwd=None, capture_output=False, text=False):
        calls.append(list(command))
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(entrypoint, "_find_source_root", lambda: tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run)

    entrypoint._run_update(["--dev-source"])

    assert calls == [["uv", "tool", "upgrade", "--reinstall", "openharness"]]
