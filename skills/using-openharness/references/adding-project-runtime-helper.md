# Adding Project Runtime Helper

Use this guide when a repository already follows the OpenHarness runtime capability model and now needs one more reusable helper for a specific runtime surface.

This workflow sits downstream of `runtime-capability-contract.md` and `project-runtime-surface-map.md`. It does not create a second repository entry skill.

## Decision Rule

Choose exactly one path:

1. `reuse existing helper`
   - The runtime surface is already mapped.
   - A linked helper already matches the task's prerequisites, driving method, and evidence shape.
2. `add new helper`
   - The runtime surface is already mapped clearly enough to act on.
   - No existing helper fits the task's dominant validation loop.
   - Add one new narrow helper and link it from the runtime surface map.
3. `bootstrap first`
   - The repository still cannot state the runtime surface, prerequisites, driving method, or evidence flow clearly enough.
   - Open or refine a focused bootstrap package before advertising reusable helper support.

Do not treat `no matching helper yet` as the same problem as `missing runtime surface definition`.

## Minimum Helper Contract

Do not treat a helper as reusable until it can declare at least:

- owning runtime surface
- purpose and dominant validation loop
- prerequisites
- driver commands or scripts
- observation points and evidence sources
- success criteria
- failure evidence expectations
- writeback expectations for `03-detailed-design.md`, `05-verification.md`, and `06-evidence.md`

Keep each helper narrow:

- one dominant runtime surface
- one dominant driver style
- one dominant evidence shape

If a proposed helper spans unrelated surfaces or evidence loops, split it before linking it from the runtime surface map.

## Repository Surfaces To Update

When you add new helper coverage, update the repository surfaces that advertise or depend on it:

- the runtime surface map entry for that surface
- the helper skill path and its contract text
- repository onboarding references such as `skill-hub` or equivalent adoption docs
- task-package writeback targets that will record planned and executed runtime verification
- `.project-memory/` when the helper-addition rule becomes a reusable project fact

These repository updates should keep the runtime story discoverable without creating a parallel workflow root.

## Task-Package Writeback

- `03-detailed-design.md`
  - record whether the task will reuse an existing helper, add new helper coverage, or bootstrap first
  - record the chosen runtime surface, prerequisites, driving method, expected observations, and the helper path when one exists
- `05-verification.md`
  - record the executed runtime path, the evidence actually gathered, and whether the helper behaved as expected
- `06-evidence.md`
  - record artifact paths, commands, helper references, residual risks, and follow-up cleanup such as missing helper refinements

## Boundary Notes

- Keep `using-openharness` as the only entry skill.
- Do not promote task-local debugging notes into a reusable helper until the minimum helper contract is explicit.
- Do not leave helper knowledge only in chat, shell history, or one package's ad hoc notes.
