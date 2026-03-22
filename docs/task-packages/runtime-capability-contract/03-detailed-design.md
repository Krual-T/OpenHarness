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
- Add `OH-013` package documents for the runtime capability contract.
- Update `OH-004` so the roadmap reflects this new follow-up stream.
- In a later implementation wave, likely update:
  - `skills/using-openharness/SKILL.md`
  - `skills/using-openharness/references/skill-hub.md`
  - task-package templates or reference docs that describe runtime writeback requirements
  - possibly `.project-memory/` conventions if runtime capability knowledge becomes reusable project memory

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
- This package should remain design-only until a focused implementation task updates live OpenHarness docs and skill routing.
- The package is upstream of project-level runtime-surface mapping work because repositories need the core declaration contract before they can attach multiple helper skills coherently.

## Detailed Reflection
- I challenged whether the contract needed a machine-readable schema immediately. It does not yet; the first useful step is stable design wording and routing rules.
- I checked whether runtime capability mapping should live entirely in `OH-014`. It should not, because `OH-014` is about project onboarding structure, while this package defines the reusable OpenHarness-side protocol that all projects should consume.
- I checked whether the protocol was still too abstract. The added declaration fields and routing choices make it concrete enough for a later implementation wave.
