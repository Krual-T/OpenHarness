# Runtime Capability Contract

OpenHarness treats project-specific runtime support as a repository protocol, not as one universal runtime-debug skill.

This contract now routes through Runtime Workflow Package (RWP) records. The detailed project-facing shape lives in `runtime-workflow-packages.md`.

## Capability Layers

OpenHarness separates runtime support into three layers:

1. `core protocol`
   - `using-openharness` decides whether a task is code-only or runtime-aware.
   - The core protocol keeps routing, evidence expectations, and writeback rules stable across repositories.
2. `Runtime Workflow Package`
   - A project may declare runtime workflows under `.harness/rwp/workflows/<workflow-name>/workflow.md`.
   - Each package describes prerequisites, scripts/, runtime observation, success criteria, failure evidence, and task-package writeback.
3. `runtime execution`
   - `openharness rwp list` exposes only workflow summaries.
   - `openharness rwp view <workflow>` exposes one workflow detail document.
   - `openharness rwp run <workflow> <script.py> [args...]` runs an explicit Python script from that workflow.

## Declaration Shape

Each Runtime Workflow Package should declare at least:

- `name` and `description` in the `workflow.md` metadata header
- prerequisites
- scripts/
- runtime observation
- success criteria
- failure evidence
- limitations
- writeback expectations

The writeback expectations must stay inside the normal task-package flow:

- `overview-design.md`
  - record whether RWP selection was considered and which package was selected, rejected, or deferred
- `detailed-design.md`
  - record the chosen RWP, prerequisites, scripts to run, expected observations, and fallback path
- `verification-design.md`
  - record the executed `openharness rwp run ...` command, stdout/stderr summary, runtime observations, deviations, blockers, and blind spots
- `evidence.md`
  - record artifact paths, log paths, external evidence, commands, residual risks, and follow-up actions

## Routing Contract

When a task needs runtime-aware evidence, `using-openharness` should choose exactly one of these paths:

1. `code-only execution`
   - the task does not require runtime-aware evidence beyond the existing package verification plan
2. `select an existing RWP`
   - assign a subagent to inspect `openharness rwp list`
   - inspect details with `openharness rwp view <workflow>` only for strong candidates
   - write the selected RWP into the task package before claiming runtime coverage
3. `missing RWP gap`
   - no declared package fits the task
   - write the gap and fallback verification path into the task package
4. `bootstrap a new RWP`
   - the project repeatedly needs the same runtime validation loop
   - add a focused Runtime Workflow Package under `.harness/rwp/workflows/`

Do not claim supported runtime verification before either selecting a matching RWP or recording the missing-RWP gap.

## Boundary Rules

- Do not create a second repository entry skill for runtime work.
- Do not use `SKILL.md` for RWP records; OpenHarness CLI controls progressive disclosure.
- Do not keep runtime evidence only in chat or shell history; write it back into the task package.
- Do not treat a script directory as a full RWP unless `workflow.md` states prerequisites, observations, success criteria, failure evidence, and writeback expectations.

## Relationship To Other OpenHarness Work

- This contract is the OpenHarness-side protocol layer.
- The project-facing Runtime Workflow Package guidance lives in `runtime-workflow-packages.md`.
- Repository-specific RWP examples belong under downstream `.harness/rwp/workflows/` directories.
