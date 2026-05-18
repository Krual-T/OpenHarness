
import re
import subprocess
from datetime import datetime, timezone

from ..harness_context import harness, HarnessContext


@harness
def get_git_author(ctx: HarnessContext) -> str:
    try:
        result = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True,
            cwd=ctx.repo_root, timeout=5,
        )
        name = result.stdout.strip()
        if name:
            return name
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return "unassigned"


def current_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def slugify_task_name(raw_name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", raw_name.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("task name must contain at least one ASCII letter or number")
    return cleaned


def humanize_task_name(task_name: str) -> str:
    slug = slugify_task_name(task_name)
    return " ".join(part.capitalize() for part in slug.split("-"))
