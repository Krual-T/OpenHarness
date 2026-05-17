from __future__ import annotations

from pathlib import Path

from .domain import TaskStatus


def describe_stage(package) -> dict[str, str]:
    wf = package.workflow
    status = package.info.status
    next_s = wf.next_status(status)
    return {
        "current_stage": package.current_status,
        "current_stage_description": wf.descriptions.get(status, "Unknown workflow stage."),
        "next_stage": next_s.value if next_s else "",
        "next_step": wf.next_steps.get(status, "No next step available."),
    }


def output_state_hook(repo_root: Path, state: str) -> None:
    try:
        status = TaskStatus(state)
    except ValueError:
        return
    relative = status.hook
    if not relative:
        return
    skill_path = repo_root / relative
    if not skill_path.exists():
        print(f"[hook] skill file not found: {relative}", flush=True)
        return
    print(f"--- BEGIN: {relative} ---", flush=True)
    print(skill_path.read_text(encoding="utf-8"), flush=True)
    print(f"--- END: {relative} ---", flush=True)
