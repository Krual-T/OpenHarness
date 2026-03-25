# Installing OpenHarness for Codex

Enable OpenHarness skills in Codex via native skill discovery.

Before running any install command, ask the user which target directory should hold the OpenHarness clone and skill link. Do not default to `~` or any home-directory path unless the user explicitly chooses it.

## Prerequisites

- Git

## Installation

1. **Ask for the target directory first.**

   Confirm a single `<target dir>` with the user before making filesystem changes.

   Example result layout:

   - OpenHarness clone: `<target dir>/openharness`
   - Skill link: `<target dir>/.agents/skills/openharness`

2. **Clone the OpenHarness repository into the chosen target directory:**
   ```bash
   git clone https://github.com/Krual-T/OpenHarness.git <target dir>/openharness
   ```

3. **Create the skills symlink inside the chosen target directory:**
   ```bash
   mkdir -p <target dir>/.agents/skills
   ln -s <target dir>/openharness/skills <target dir>/.agents/skills/openharness
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "<target dir>\\.agents\\skills"
   cmd /c mklink /J "<target dir>\\.agents\\skills\\openharness" "<target dir>\\openharness\\skills"
   ```

4. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la <target dir>/.agents/skills/openharness
```

You should see a symlink (or junction on Windows) pointing to your OpenHarness skills directory.

## Updating

```bash
cd <target dir>/openharness && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm <target dir>/.agents/skills/openharness
```

Optionally delete the clone: `rm -rf <target dir>/openharness`.

## Attribution

OpenHarness reuses and adapts source material from [`obra/superpowers`](https://github.com/obra/superpowers). If you redistribute substantial portions of this repository, keep the upstream copyright and license notice intact.
