# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run targeted repository tests for the new hub model and README baseline wording
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run full `uv run pytest`
- Fallback Path:
  - if targeted taxonomy tests fail for wording drift outside the intended files, update the affected live docs first and rerun targeted tests
  - if `check-tasks` fails on package semantics, fix the task docs before claiming implementation is ready
  - if the full suite fails, fix the regression and rerun the full verification path
- Planned Evidence:
  - updated `OH-011` package docs
  - updated `OH-004` roadmap references
  - updated live `README.md`
  - updated live `skill-hub.md`
  - updated affected `skills/*/SKILL.md` files
  - repository tests that pin the new model

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/*`
- `docs/archived/task-packages/harness-completion-roadmap/*`
- `README.md`
- `skills/using-openharness/references/skill-hub.md`
- affected `skills/*/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`

## Interfaces
The live repository should expose the model through three interfaces:

1. `README.md`
   - describes the product goal and Python-first verification baseline
2. `skills/using-openharness/references/skill-hub.md`
   - declares protocol status and workflow stages in one stable place
3. affected `SKILL.md` files
   - briefly state each skill's protocol role and primary stage or trigger

The task-package protocol continues to own project-specific runtime verification detail. The hub and README should not pretend to know the runtime evidence needed for every downstream repository.

## Error Handling
- If a skill appears to span multiple stages, keep one primary stage and mention the trigger nuance briefly instead of inventing a new taxonomy branch.
- If a skill is repository-owned but not part of the mandatory path, classify it as an optional helper even if it is very important in some repos.
- If a wording change would over-promise runtime verification, prefer explicit weaker wording that points back to task-package verification fields.

## Migration Notes
- `OH-008` remains the archived baseline that retired the old plan-oriented surface.
- `OH-011` is the follow-up that makes the live repository describe skills according to actual usage and routing.
- `OH-007` remains the archived baseline for Python verification maturity; this package only productizes its minimum live wording, not the whole historical design.
- After implementation and verification, `OH-011` should be archived and referenced from `OH-004` so the roadmap stays accurate.

## Detailed Reflection
- I challenged the testing strategy first. The important behavior here is wording-driven routing, so repository text tests are appropriate and should fail on drift.
- I checked whether the implementation should stop at `skill-hub.md`. It should not; the README and affected skill docs must align or the repository will still tell mixed stories.
- I checked whether the Python verification wording was concrete enough. It is concrete enough for live docs because it only commits to the Python floor and explicitly leaves stronger runtime verification to task packages.
- No bounded subagent discussion was used in this round because the implementation path is direct once the two-layer model is accepted.
