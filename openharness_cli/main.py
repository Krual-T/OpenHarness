import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


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


def _run_update() -> None:
    source = _find_source_root()
    print(f"OpenHarness source: {source}", flush=True)
    result = subprocess.run(["git", "pull"], cwd=source)
    if result.returncode != 0:
        print("WARNING: git pull failed, continuing with tool upgrade anyway", flush=True)
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
