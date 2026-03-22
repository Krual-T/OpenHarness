# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if taxonomy wording changes only touch docs, still run both commands because tests already cover skill-hub wording
  - if broader wording changes break unrelated tests, narrow the failing scope, fix the taxonomy drift, then rerun the full suite
- Planned Evidence:
  - updated task-package docs
  - updated skill hub and affected `SKILL.md` files
  - tests that pin the intended category wording and boundary rules
  - removal of `skills/writing-plans/`, `skills/writing-skills/`, and `skills/executing-plans/`

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/*`
- `docs/task-packages/harness-completion-roadmap/*`
- `skills/using-openharness/references/skill-hub.md`
- affected `skills/*/SKILL.md` files whose category wording does not match the taxonomy
- `skills/using-openharness/tests/test_openharness.py`
- `skills/writing-plans/**`
- `skills/writing-skills/**`
- `skills/executing-plans/**`

## Interfaces
- The hub remains the repository-wide index of skill categories.
- Each affected skill doc needs a short, explicit self-description that matches one taxonomy category.
- Tests should assert boundary rules that matter to routing, such as `openharness` remaining the only repository entry skill and retired plan-oriented skills not existing in the live repository.
- If a skill is retired, no live skill should still advertise it as an execution option or required dependency.

## Error Handling
- If repository exploration finds a skill that does not fit any current category, prefer refining the taxonomy in this package before editing the skill ad hoc.
- If one skill intentionally spans two concepts, document the primary category first and explain the secondary nuance briefly instead of inventing a new category for one edge case.
- If the taxonomy requires a broader cleanup than fits in one implementation round, keep this package focused on the highest-confusion skills first and record the remainder in evidence.

## Migration Notes
- `OH-004` is the parent roadmap; this package should absorb the implementation-ready taxonomy detail so the roadmap can stay broad.
- `OH-006` already tightened status semantics, so this package does not need to redefine readiness states.
- The later maintenance package should reuse the final taxonomy from this package when deciding what counts as stale, misleading, or optional.
- `writing-plans` is retired in this round rather than preserved as a compatibility stub.

## Detailed Reflection
- I challenged whether this package needed code changes or only doc edits. It does need tests, because the problem is taxonomy drift and drift must be caught automatically.
- I challenged whether the skill hub alone was enough. It is not, because per-skill wording can still imply the wrong protocol strength unless those docs are aligned too.
- I checked whether runtime verification is concrete enough. It is, because the repository already has tests that inspect skill wording directly, so `check-tasks` plus `pytest` is the right baseline for this package.
- I checked whether deleting `writing-plans` is safe. It is safe because the live repository protocol no longer depends on plan files, and the user explicitly requested full retirement rather than compatibility preservation.
