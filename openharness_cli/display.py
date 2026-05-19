
from pathlib import Path

from .harness_context import harness, HarnessContext
from .models import parse_status, TaskPackage


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
    pkg_root = Path(__file__).resolve().parents[1]
    candidates = [
        ctx.repo_root / relative,
        pkg_root / relative,
        ctx.repo_root / ".claude" / "skills" / relative,
        ctx.repo_root / ".codex" / "skills" / relative,
        ctx.repo_root / ".codex" / "skills" / "openharness" / relative,
        ctx.repo_root / ".agents" / "skills" / relative,
        ctx.repo_root / ".agents" / "skills" / "openharness" / relative,
    ]
    skill_path = next((c for c in candidates if c.exists()), None)
    if skill_path is None:
        print(f"[hook] skill file not found: {relative}", flush=True)
        return
    print(f"--- BEGIN: {relative} ---", flush=True)
    print(skill_path.read_text(encoding="utf-8"), flush=True)
    print(f"--- END: {relative} ---", flush=True)
