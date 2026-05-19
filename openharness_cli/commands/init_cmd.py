import json
import platform
import tomllib
from pathlib import Path

import tomli_w
import typer

from ..models.agent_type import AgentType

OH_CLONE = Path.home() / ".agents" / "skill-hub" / "openharness"

if platform.system() == "Windows":
    _SKILL_CAT_CMD = "Get-Content $env:USERPROFILE/.agents/skill-hub/openharness/skills/using-openharness/SKILL.md"
else:
    _SKILL_CAT_CMD = "cat $HOME/.agents/skill-hub/openharness/skills/using-openharness/SKILL.md"


def _prompt_overwrite(path: Path) -> bool:
    try:
        answer = input(f"{path} already exists with different hook config. Overwrite? [y/N]: ")
        return answer.strip().lower() in ("y", "yes")
    except (EOFError, OSError):
        print(f"Skipping {path} (non-interactive mode)")
        return False


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

    hook_entry = {
        "matcher": "startup|resume",
        "hooks": [
            {
                "type": "command",
                "command": _SKILL_CAT_CMD,
            }
        ],
    }

    settings: dict = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"ERROR: {settings_path} is not valid JSON, fix it manually before retrying")
            raise typer.Exit(code=1)

    hooks: list = settings.setdefault("hooks", {}).setdefault("SessionStart", [])

    for existing in hooks:
        if existing == hook_entry:
            return

    if hooks:
        if not _prompt_overwrite(settings_path):
            return

    hooks.append(hook_entry)
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _setup_claude(repo_root: Path) -> None:
    skills_dir = repo_root / ".claude" / "skills"
    link = skills_dir / "using-openharness"
    target = OH_CLONE / "skills" / "using-openharness"
    _create_symlink(link, target)
    _write_session_start_hook(repo_root)


def _setup_codex_hook(repo_root: Path) -> None:
    codex_dir = repo_root / ".codex"
    hooks_path = codex_dir / "hooks.json"

    hooks_config = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _SKILL_CAT_CMD,
                        }
                    ],
                }
            ]
        }
    }

    codex_dir.mkdir(parents=True, exist_ok=True)

    if hooks_path.exists():
        try:
            existing = json.loads(hooks_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            if _prompt_overwrite(hooks_path):
                hooks_path.write_text(json.dumps(hooks_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            if existing == hooks_config:
                pass
            elif _prompt_overwrite(hooks_path):
                hooks_path.write_text(json.dumps(hooks_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        hooks_path.write_text(json.dumps(hooks_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Ensure hooks is enabled in config.toml
    config_path = codex_dir / "config.toml"
    if config_path.exists():
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        features = config.setdefault("features", {})
        if "hooks" not in features:
            print(f"WARNING: {config_path} exists but 'hooks' is not enabled")
            if _prompt_overwrite(config_path):
                features["hooks"] = True
                config_path.write_text(tomli_w.dumps(config), encoding="utf-8")
    else:
        config = {"features": {"hooks": True}}
        config_path.write_text(tomli_w.dumps(config), encoding="utf-8")


def _setup_codex(repo_root: Path) -> None:
    agents_dir = repo_root / ".agents" / "skills"
    link = agents_dir / "openharness"
    target = OH_CLONE / "skills"
    _create_symlink(link, target)
    _setup_codex_hook(repo_root)


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
