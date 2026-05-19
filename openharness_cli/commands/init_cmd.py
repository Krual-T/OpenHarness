import json
from pathlib import Path

import typer

from ..models.agent_type import AgentType

OH_CLONE = Path.home() / ".agents" / "skill-hub" / "openharness"


def _ensure_clone_exists() -> None:
    if not OH_CLONE.exists():
        print(f"ERROR: OpenHarness clone not found at {OH_CLONE}")
        print("Run install.sh first, or clone manually:")
        print(f"  git clone https://github.com/Krual-T/OpenHarness.git {OH_CLONE}")
        raise typer.Exit(code=1)
    if not (OH_CLONE / ".git").exists():
        print(f"ERROR: {OH_CLONE} exists but is not a git repository")
        print("Remove it and run install.sh again.")
        raise typer.Exit(code=1)


def _create_symlink(link_path: Path, target: Path) -> None:
    if link_path.exists() or link_path.is_symlink():
        if link_path.is_symlink() and link_path.resolve() == target.resolve():
            return
        print(f"WARNING: {link_path} exists, replacing with symlink")
        link_path.unlink()
    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target)


def _write_session_start_hook(repo_root: Path) -> None:
    claude_dir = repo_root / ".claude"
    settings_path = claude_dir / "settings.json"

    settings: dict = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"ERROR: {settings_path} is not valid JSON, fix it manually before retrying")
            raise typer.Exit(code=1)

    hooks: dict = settings.setdefault("hooks", {})
    existing = hooks.get("SessionStart")
    if existing and existing != "using-openharness":
        print(f"WARNING: SessionStart hook already set to '{existing}', not overwriting")
        return
    if existing == "using-openharness":
        return

    hooks["SessionStart"] = "using-openharness"
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _setup_claude(repo_root: Path) -> None:
    skills_dir = repo_root / ".claude" / "skills"
    link = skills_dir / "using-openharness"
    target = OH_CLONE / "skills" / "using-openharness"
    _create_symlink(link, target)
    _write_session_start_hook(repo_root)


def _setup_codex(repo_root: Path) -> None:
    agents_dir = repo_root / ".agents" / "skills"
    link = agents_dir / "openharness"
    target = OH_CLONE / "skills"
    _create_symlink(link, target)


def _bridge_agent_files(repo_root: Path, agent_type: AgentType) -> None:
    agents_md = repo_root / "AGENTS.md"
    claude_md = repo_root / "CLAUDE.md"

    if agents_md.exists() and not claude_md.exists():
        if agent_type in (AgentType.CLAUDE, AgentType.ALL):
            claude_md.symlink_to("AGENTS.md")
    elif claude_md.exists() and not agents_md.exists():
        if agent_type in (AgentType.CODEX, AgentType.ALL):
            agents_md.symlink_to("CLAUDE.md")
    elif agents_md.exists() and claude_md.exists():
        if not agents_md.is_symlink() and not claude_md.is_symlink():
            print("INFO: AGENTS.md and CLAUDE.md both exist, skipping bridge")


def init(
    ctx: typer.Context,
    agent: str = typer.Option("all", "--agent", help="Target agent platform: claude, codex, or all"),
) -> None:
    """Initialize OpenHarness in the current project."""
    hx = ctx.obj
    repo_root = hx.repo_root

    try:
        agent_type = AgentType(agent)
    except ValueError:
        valid = ", ".join(sorted(a.value for a in AgentType))
        print(f"ERROR: unknown agent type '{agent}', expected one of: {valid}")
        raise typer.Exit(code=1)

    # Common: create .harness/ directory
    harness_root = repo_root / ".harness"
    harness_root.mkdir(parents=True, exist_ok=True)
    (harness_root / ".gitignore").write_text("*\n", encoding="utf-8")

    # Verify clone exists
    _ensure_clone_exists()

    # Platform-specific setup
    if agent_type in (AgentType.CLAUDE, AgentType.ALL):
        _setup_claude(repo_root)

    if agent_type in (AgentType.CODEX, AgentType.ALL):
        _setup_codex(repo_root)

    # Bridge AGENTS.md ↔ CLAUDE.md
    _bridge_agent_files(repo_root, agent_type)

    print(f"OpenHarness initialized for agent: {agent_type.value}")
