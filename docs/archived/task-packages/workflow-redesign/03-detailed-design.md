# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if legacy wording in compatibility skills causes failures, update the affected docs and rerun the standard repository validation commands
- Planned Evidence:
  - manifest and template updates that remove `04-implementation-plan.md`
  - workflow docs and skills aligned to the new exploration-centric flow
  - passing repository validation after archival

## Files Added Or Changed
- Update manifest, templates, README, AGENTS, and current package docs to remove `04-implementation-plan.md` from the fixed required protocol.
- Add a new core skill `skills/exploring-solution-space/SKILL.md`.
- Update `skills/using-openharness/SKILL.md` and `skills/using-openharness/references/skill-hub.md` to route through exploration and runtime verification.
- Update `skills/brainstorming/SKILL.md` so `01` is the primary output and the next step is exploration, not plan-writing.
- Update tests to assert the new required file set and workflow wording.

## Interfaces
- `manifest.yaml.required_design_files` must no longer include `04-implementation-plan.md`.
- New templates must scaffold packages without `04`.
- `brainstorming` writes or stabilizes `01-requirements.md`.
- `exploring-solution-space` writes gathered evidence into `02` and informs `03`.
- `03-detailed-design.md` must cover:
  - test design first
  - implementation landing points
  - runtime verification approach
  - suggested implementation order

## Error Handling
- Existing packages that still contain `04-implementation-plan.md` may keep the file temporarily, but validation must not require it.
- Tests should validate the new minimum protocol while still tolerating extra legacy files in already-created packages.

## Migration Notes
- Existing active packages in this repo should stop listing `04` in their README and status entrypoints for new work.
- `writing-plans` may remain in the repo for now, but it is no longer a required part of the fixed workflow.

## Detailed Reflection
- I checked whether workflow redesign should include execution-skill removal in the same round. It should not; clarifying the fixed protocol was enough for the first restructuring wave.
- I checked whether runtime verification planning needed its own separate package first. It did not; the redesign only needed to reserve the right slot for it in the fixed workflow.
