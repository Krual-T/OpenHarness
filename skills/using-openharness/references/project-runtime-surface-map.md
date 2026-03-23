# Project Runtime Surface Map

OpenHarness expects repositories that need runtime-aware verification to keep a discoverable project runtime surface map.

This map is the project-facing inventory that turns the shared runtime capability contract into concrete repository guidance.

## Minimum Contents

Each runtime surface entry should declare at least:

- runtime surface
- purpose
- prerequisites
- driver method
- observation points
- success criteria
- failure evidence
- helper skill or bootstrap package
- writeback expectations

The writeback expectations should point back into the normal task-package flow:

- `03-detailed-design.md`
  - record whether runtime verification is required
  - record the chosen surface, prerequisites, driver method, and expected observations
- `05-verification.md`
  - record the executed runtime path and the evidence that was actually gathered
- `06-evidence.md`
  - record artifact paths, commands, helper references, residual risks, and follow-up actions

## Recommended Shape

The map can live anywhere stable and versioned, as long as `AGENTS.md`, `using-openharness`, or a repository onboarding document points to it.

A simple table is usually enough:

| Surface | Purpose | Prerequisites | Driver | Evidence | Helper Or Bootstrap |
| --- | --- | --- | --- | --- | --- |
| API | Validate service behavior through HTTP or RPC flows | Local env, seed data, auth fixture | project API command or script | responses, traces, logs | linked helper skill or bootstrap package |

## Helper Boundary Rules

- One helper should cover one dominant runtime surface.
- One helper should keep one dominant driver method.
- One helper should keep one dominant evidence shape.
- Split a helper when unrelated surfaces would force different prerequisites, commands, or observations into one body.
- Do not advertise a helper as reusable until it can name its prerequisites, observations, and failure evidence clearly.

## Bootstrap Path

1. Decide whether the active task actually needs runtime-aware evidence.
2. Inspect the project runtime surface map.
3. If a matching surface entry exists and the linked helper contract fits the task, reuse the linked helper.
4. If the surface is mapped but there is no reusable helper yet, add one narrow helper and link it from the map.
5. If the repository cannot explain the surface, prerequisites, driver method, or evidence flow clearly, open a bootstrap package first.
6. Record the chosen path back into the active task package before claiming runtime verification coverage.

Use `references/adding-project-runtime-helper.md` when step 4 or step 5 applies.

## Adoption Notes

- The map is an inventory, not a dumping ground for every runtime troubleshooting step.
- The entry skill stays `using-openharness`; helper skills remain optional project-level extensions.
- If one surface needs several unrelated evidence loops, split that surface into multiple clearer entries instead of hiding variety in one helper.
