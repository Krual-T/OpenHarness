# Installing OpenHarness for Codex

Enable OpenHarness skills in Codex via native skill discovery.

Before executing any installation commands, prompt the user to specify the target directory for the OpenHarness skill symlink. (Note: This applies only to the symlink directory; the cloned project is stored by default in `~/.agents/skill-hub`.)

## Prerequisites

- Git

## Installation

1. **Ask for the target directory first.**

   Confirm a single `<target dir>` with the user before making filesystem changes.

   Example result layout:

   - OpenHarness clone: `~/.agents/skill-hub/openharness`
   - Skill link: `<target dir>/.agents/skills/openharness`

2. **Clone the OpenHarness repository into the chosen target directory:**
   ```bash
   git clone https://github.com/Krual-T/OpenHarness.git ~/.agents/skill-hub/openharness
   ```

3. **Create the skills symlink inside the chosen target directory:**
   ```bash
   mkdir -p <target dir>/.agents/skills
   ln -s ~/.agents/skill-hub/openharness/skills <target dir>/.agents/skills/openharness
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "<target dir>\\.agents\\skills"
   cmd /c mklink /J "<target dir>\\.agents\\skills\\openharness" "~\\.agents\\skill-hub\\openharness\\skills"
   ```

4. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la <target dir>/.agents/skills/openharness
```

You should see a symlink (or junction on Windows) pointing to your OpenHarness skills directory.

## Updating

```bash
cd .agents/skill-hub/openharness && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm <target dir>/.agents/skills/openharness
```

Optionally delete the clone: `rm -rf ~/.agents/skill-hub/openharness`.

## Attribution

OpenHarness reuses and adapts source material from [`obra/superpowers`](https://github.com/obra/superpowers). If you redistribute substantial portions of this repository, keep the upstream copyright and license notice intact.
