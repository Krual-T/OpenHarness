# Runtime Workflow Packages

Runtime Workflow Packages (RWP) are project-level runtime validation records discovered by OpenHarness CLI.

They are not Codex skills and must not use `SKILL.md`. OpenHarness exposes them gradually so agents can avoid loading every runtime workflow into the main context.

## Package Shape

An RWP lives under:

```text
.harness/rwp/
  workflows/
    <workflow-name>/
      workflow.md
      scripts/
        <script.py>
  libs/
  logs/
```

The discoverable workflow root is `.harness/rwp/workflows`.

`workflow.md` starts with a metadata header:

```markdown
---
name: <RWP_NAME>
description: <DESCRIPTION>
---
```

The body should explain:

- purpose
- when to use the workflow
- prerequisites
- scripts/
- runtime observation
- success criteria
- failure evidence
- limitations
- writeback guidance

## Selection Flow

When runtime verification may apply, the main agent should assign a subagent to select candidate RWPs:

1. Run `openharness rwp list`.
2. Use each `description` to identify strong candidates.
3. Run `openharness rwp show <workflow>` only for strong candidates.
4. Report selected RWPs, rejected near matches, and writeback points.
5. The main agent records the final selection in the task package.

OpenHarness CLI does not select workflows automatically.

## Execution Flow

Run a workflow script with:

```bash
openharness rwp run <workflow> <script.py> [args...]
```

Rules:

- the script name must be explicit
- only `.py` files under the workflow `scripts/` directory are runnable
- OpenHarness does not define workflow-specific script names
- script arguments are passed through without interpretation
- project-specific shared code belongs in `libs/`
- runtime logs and observation artifacts belong in `logs/`

## Environment And Logger

`openharness rwp run` automatically attempts to load:

- `.harness/.env`
- `.harness/rwp/.env`

Values from `.harness/rwp/.env` override values from `.harness/.env`.

OpenHarness provides this runtime API:

```python
from openharness.rwp import get_logger

logger = get_logger()
```

`get_logger()` returns a standard Python logger. OpenHarness does not force a logging layout; each workflow decides how to attach handlers and which logs or artifacts to write.

## Writeback

RWP usage must enter the normal task-package loop:

- `02-overview-design.md`
  - record the selected, rejected, or deferred workflow at overview level
- `03-detailed-design.md`
  - record prerequisites, script names, expected runtime observation, success criteria, failure evidence, and fallback path
- `04-verification.md`
  - record executed `openharness rwp run ...` commands, exit codes, stdout/stderr summaries, runtime observations, deviations, and blockers
- `05-evidence.md`
  - record artifact paths, log paths, external records, manual steps, residual risks, and follow-ups

If no RWP fits the task, record the missing-RWP gap rather than claiming runtime verification coverage.
