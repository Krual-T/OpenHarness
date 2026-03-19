# Installing OpenHarness for Codex

Enable OpenHarness skills in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the OpenHarness repository:**
   ```bash
   git clone https://github.com/Krual-T/OpenHarness.git ~/.codex/openharness
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.codex/skills
   ln -s ~/.codex/openharness/.codex/skills ~/.codex/skills/openharness
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills"
   cmd /c mklink /J "$env:USERPROFILE\.codex\skills\openharness" "$env:USERPROFILE\.codex\openharness\.codex\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la ~/.codex/skills/openharness
```

You should see a symlink (or junction on Windows) pointing to your OpenHarness skills directory.

## Updating

```bash
cd ~/.codex/openharness && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.codex/skills/openharness
```

Optionally delete the clone: `rm -rf ~/.codex/openharness`.

## Attribution

OpenHarness reuses and adapts source material from [`obra/superpowers`](https://github.com/obra/superpowers). If you redistribute substantial portions of this repository, keep the upstream copyright and license notice intact.
