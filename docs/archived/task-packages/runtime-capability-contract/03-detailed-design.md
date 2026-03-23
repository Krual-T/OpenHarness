# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - validate the new packages with `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest` to ensure the repository still passes after adding runtime-capability design packages
- Fallback Path:
  - if repository tests fail for unrelated reasons, keep the package at design status and record the blocker rather than claiming protocol completion
- Planned Evidence:
  - design documents that define the capability declaration shape
  - routing rules that distinguish capability reuse from capability bootstrap
  - a concrete list of repository surfaces that later implementation must touch

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Testing-First Design
This is a design package. Its immediate tests are repository-legibility tests:

- the package must satisfy `check-tasks`
- the package must make the runtime capability protocol concrete enough that a later implementation wave can update skills, templates, and examples without rediscovering the design
- the package must define routing semantics clearly enough to separate runtime capability bootstrap from runtime capability usage

## Files Added Or Changed
- Keep `OH-013` package documents aligned with the implementation wave and later archive them as the completed baseline.
- Update `skills/using-openharness/SKILL.md` so the entry skill routes runtime-aware work through a runtime capability contract instead of ad hoc debugging language.
- Update `skills/using-openharness/references/skill-hub.md` so the live skill hub advertises the contract and keeps project helpers optional.
- Add `skills/using-openharness/references/runtime-capability-contract.md` as the shared reference that defines declaration shape, routing choices, and task-package writeback expectations.
- Update `README.md` so the public repository surface explains the runtime capability contract and the bootstrap-task path.
- Extend `skills/using-openharness/tests/test_openharness.py` so the live docs and reference contract are locked by repository tests.

## Interfaces
- Runtime capability declaration interface:
  - surface name
  - prerequisites
  - driving method
  - observation points
  - success criteria
  - failure evidence
  - task-package writeback targets
- Routing interface:
  - `using-openharness` decides among code-only execution, runtime-helper reuse, or runtime-capability bootstrap
- Verification interface:
  - this contract composes with the existing runtime-verification ladder rather than replacing it

## Error Handling
- If a repository tries to encode every runtime concern into one helper skill, this contract should redirect it toward multiple narrow capability helpers.
- If a repository has runtime needs but no stable capability map yet, the agent should open a bootstrap package before improvising runtime verification.
- If a helper skill cannot declare its prerequisites, observations, and evidence clearly, it is not ready to be treated as a reusable runtime capability.

## Migration Notes
- This implementation wave productizes the contract in live docs and test coverage without introducing a machine-readable schema yet.
- The package remains upstream of project-level runtime-surface mapping work because repositories still need `OH-014` to describe repository-specific runtime surface maps and helper examples.

## Detailed Reflection
- I challenged whether the contract needed a machine-readable schema immediately. It still does not; the docs-first contract is now concrete enough to route work and constrain downstream packages.
- I checked whether runtime capability mapping should live entirely in `OH-014`. It should not, because `OH-014` is about project onboarding structure, while this package defines the reusable OpenHarness-side protocol that all projects should consume.
- I checked whether the implementation wave should update templates now. I rejected that for this round because `OH-014` owns repository-facing surface-map structure, while `OH-013` only needs to productize the shared contract and routing rules first.
