# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - validate the new package with `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest` to confirm the repository still passes after adding `OH-016`
- Fallback Path:
  - if unrelated tests fail, keep the package at design status and record the blocker rather than claiming workflow productization
- Planned Evidence:
  - design documents that define helper-addition decision rules
  - repository surfaces that later implementation must update
  - verification output showing the package is structurally valid

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- Add `docs/task-packages/adding-project-runtime-helper/*`.
- Update `docs/task-packages/harness-completion-roadmap/README.md` so the roadmap shows this new follow-up package.
- In a later implementation wave, likely update:
  - `skills/using-openharness/SKILL.md`
  - `skills/using-openharness/references/skill-hub.md`
  - a runtime surface map template or example artifact
  - helper-skill examples or scaffolding guidance
  - possibly `.project-memory/` if helper-creation heuristics become reusable project memory

## Interfaces
- Decision interface:
  - existing helper match
  - mapped surface with missing helper
  - missing or underspecified surface that requires bootstrap
- Helper boundary interface:
  - one dominant runtime surface
  - one dominant driver style
  - one evidence shape
  - explicit writeback contract
- Repository update interface:
  - runtime surface map entry
  - helper skill path
  - task-package writeback targets
  - skill-hub or adoption-doc references where applicable

## Error Handling
- If a repository tries to create a new helper without a clear runtime surface map entry, stop and bootstrap that surface first.
- If a proposed helper spans unrelated surfaces such as API plus browser plus worker, split it before treating it as reusable.
- If a proposed helper cannot state prerequisites, observations, and evidence clearly, keep it as task-local exploration instead of promoting it to a reusable helper.
- If an existing helper already covers the same surface and evidence shape, reuse or refine it instead of creating a near-duplicate.

## Migration Notes
- This package should stay design-only until a later task productizes the helper-creation workflow in live docs, examples, and possibly scaffolding support.
- Conceptually it sits downstream of `OH-013` and `OH-014`, because helper creation should consume the runtime capability contract and the runtime surface map instead of inventing new local rules.
- The likely next implementation wave should package together route updates, helper-adoption guidance, and at least one example surface artifact so the workflow is discoverable in practice.

## Detailed Reflection
- I challenged whether the package needed a machine-readable helper schema now. It does not yet; the first useful step is to define the decision rules and repository update points clearly.
- I checked whether this package duplicated `OH-013` or `OH-014`. It does not. Those packages define the contract and repository model; this package defines the focused operational path for adding one helper within that model.
- I checked whether the helper boundary rules were still too vague. Requiring one dominant surface, one dominant driver style, and one evidence shape makes the intended narrowness concrete enough for later implementation.
