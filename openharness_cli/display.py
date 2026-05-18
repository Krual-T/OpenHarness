from __future__ import annotations

from typing import TYPE_CHECKING

from .harness_context import harness, HarnessContext
from .models import parse_status

if TYPE_CHECKING:
    from .models import TaskPackage


def describe_stage(package: TaskPackage) -> dict[str, str]:
    wf = package.workflow
    status = package.info.status
    next_s = wf.next_status(status)
    return {
        "current_stage": package.current_status,
        "current_stage_description": wf.descriptions.get(status, "Unknown workflow stage."),
        "next_stage": next_s.value if next_s else "",
        "next_step": wf.next_steps.get(status, "No next step available."),
    }


@harness
def output_state_hook(ctx: HarnessContext, state: str) -> None:
    status = parse_status(state)
    if status is None:
        return
    relative = status.hook
    if not relative:
        return
    skill_path = ctx.repo_root / relative
    if not skill_path.exists():
        print(f"[hook] skill file not found: {relative}", flush=True)
        return
    print(f"--- BEGIN: {relative} ---", flush=True)
    print(skill_path.read_text(encoding="utf-8"), flush=True)
    print(f"--- END: {relative} ---", flush=True)
