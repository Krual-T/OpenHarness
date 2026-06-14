import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


SYNC_RETRY_ATTEMPTS = 3
OUTPUT_SNIPPET_LIMIT = 2000


def _find_source_root() -> Path:
    """Locate the OpenHarness source clone without importing the package."""
    # 1) Try installed metadata (uv tool install from local path)
    try:
        from importlib.metadata import distribution
        dist = distribution("openharness")
        direct_url_text = dist.read_text("direct_url.json")
        if direct_url_text:
            direct_url = json.loads(direct_url_text)
            url = direct_url.get("url")
            if isinstance(url, str):
                parsed = urlparse(url)
                if parsed.scheme == "file":
                    return Path(unquote(parsed.path)).resolve()
    except Exception:
        pass

    # 2) Walk up from this file looking for .git + pyproject.toml
    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        if (parent / ".git").exists() and (parent / "pyproject.toml").exists():
            return parent

    # 3) Fallback: parents[2] from openharness_cli/main.py
    return module_path.parents[2]


def _snippet(value: str | None) -> str:
    if not value:
        return "(empty)"
    stripped = value.strip()
    if len(stripped) <= OUTPUT_SNIPPET_LIMIT:
        return stripped
    return f"{stripped[:OUTPUT_SNIPPET_LIMIT]}... [truncated]"


def _run_sync_command(command_parts: list[str], source: Path) -> bool:
    command_display = " ".join(command_parts)
    for attempt in range(1, SYNC_RETRY_ATTEMPTS + 1):
        result = subprocess.run(
            command_parts,
            cwd=source,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True

        print(
            f"Attempt {attempt}/{SYNC_RETRY_ATTEMPTS} failed for `{command_display}` "
            f"in {source} (exit {result.returncode}).",
            flush=True,
        )
        print(f"stdout: {_snippet(result.stdout)}", flush=True)
        print(f"stderr: {_snippet(result.stderr)}", flush=True)
    return False


def _run_update() -> None:
    source = _find_source_root()
    print(f"OpenHarness source: {source}", flush=True)
    if not _run_sync_command(["git", "pull"], source):
        print(
            f"ERROR: git pull failed after {SYNC_RETRY_ATTEMPTS} attempts; "
            "refusing to continue with tool upgrade.",
            flush=True,
        )
        sys.exit(1)
    subprocess.run(["uv", "tool", "upgrade", "--reinstall", "openharness"], cwd=source)


try:
    from .cli import app
except ModuleNotFoundError:
    app = None  # type: ignore[assignment]


def main() -> None:
    if app is None:
        if len(sys.argv) >= 2 and sys.argv[1] == "update":
            _run_update()
            return
        print(
            "ERROR: missing dependencies. Run `openharness update` to reinstall.",
            flush=True,
        )
        sys.exit(1)
    app()
