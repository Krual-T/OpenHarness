# Installing OpenHarness for Codex

Enable OpenHarness skills in Codex via native skill discovery.

This installation has two parts:

- install the OpenHarness skills so Codex can discover them
- install the global `openharness` CLI so you can run `openharness <cmd>` directly

The CLI installation does not require any changes to the target project's `pyproject.toml`.

Before executing any installation commands, prompt the user to specify the target directory for the OpenHarness skill symlink. (Note: This applies only to the symlink directory; the cloned project is stored by default in `~/.agents/skill-hub`.)

## Prerequisites

- Git
- `uv`

## Installation

1. **Ask for the target directory first.**

   Confirm a single `<target dir>` with the user before making filesystem changes.

   Example result layout:

   - OpenHarness clone: `~/.agents/skill-hub/openharness`
   - Skill link: `<target dir>/.agents/skills/openharness`

2. **Clone the OpenHarness repository into the local skill hub:**
   ```bash
   git clone https://github.com/Krual-T/OpenHarness.git ~/.agents/skill-hub/openharness
   ```

3. **Install the global `openharness` command:**
   ```bash
   uv tool install --editable ~/.agents/skill-hub/openharness
   ```

   After this, the following commands should work:
   ```bash
   openharness bootstrap
   openharness check-tasks
   ```

4. **Create the skills symlink inside the chosen target directory:**
   ```bash
   mkdir -p <target dir>/.agents/skills
   ln -s ~/.agents/skill-hub/openharness/skills <target dir>/.agents/skills/openharness
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "<target dir>\\.agents\\skills"
   cmd /c mklink /J "<target dir>\\.agents\\skills\\openharness" "~\\.agents\\skill-hub\\openharness\\skills"
   ```

5. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la <target dir>/.agents/skills/openharness
```

You should see a symlink (or junction on Windows) pointing to your OpenHarness skills directory.

Then verify the global CLI from the target project's root directory:

```bash
openharness bootstrap
```

If the command is not found, rerun:

```bash
uv tool install --editable ~/.agents/skill-hub/openharness
```

## Updating

```bash
openharness update
```

This command updates the OpenHarness clone and then refreshes the installed CLI tool.
Skills still update through the symlink because the source clone is the same repository.

## Existing Installations

If you already installed the OpenHarness skill symlink before the global CLI existed, this existing installation only needs one extra command:

```bash
uv tool install --editable ~/.agents/skill-hub/openharness
```

After that, you can use:

```bash
openharness bootstrap
openharness check-tasks
openharness update
openharness verify <task-name-or-id>
```

All active workflow docs use `openharness <cmd>` as the only documented entrypoint.
If you are not currently in the target project's root directory, pass `--repo <project-root>` explicitly.

## Uninstalling

```bash
rm <target dir>/.agents/skills/openharness
```

Remove the global CLI if needed:

```bash
uv tool uninstall openharness
```

Optionally delete the clone: `rm -rf ~/.agents/skill-hub/openharness`.

## Attribution

OpenHarness reuses and adapts source material from [`obra/superpowers`](https://github.com/obra/superpowers). If you redistribute substantial portions of this repository, keep the upstream copyright and license notice intact.
