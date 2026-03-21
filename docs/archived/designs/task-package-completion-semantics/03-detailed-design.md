# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - Run `uv run python skills/using-openharness/scripts/openharness.py check-designs` after protocol docs, templates, and compatibility package wording are updated.
  - Run `uv run pytest` after CLI text, aliases, and repository tests are updated.
- Fallback Path:
  - If full historical wording cleanup cannot land safely in one round, update active protocol surfaces first and mark remaining archived-package cleanup explicitly in evidence.
- Planned Evidence:
  - `05-verification.md` should record design validation and repository test results after the terminology and status-semantics rollout.
  - `06-evidence.md` should record which historical packages were explicitly marked as legacy archive semantics and which follow-ups remain.

Move to `in_progress` only when detailed design is concrete enough to execute.

## Files Added Or Changed
- Update `AGENTS.md` so the repository map names the end-to-end unit as `task package` and makes archive meaning explicit.
- Update `skills/using-openharness/SKILL.md` and relevant child skills so workflow wording consistently says `task package`.
- Update `skills/using-openharness/references/manifest.yaml` comments and discovery wording where human-facing labels still imply `design package`.
- Update `skills/using-openharness/references/templates/*` so new packages teach `task package` semantics and point design-complete-but-not-implemented work to `detailed_ready`.
- Update `skills/using-openharness/scripts/openharness.py`:
  - keep compatibility behavior for existing paths and data model
  - change user-facing output and help text to `task package`
  - add `check-tasks` and `new-task` aliases alongside legacy `check-designs` and `new-design`
- Update `skills/using-openharness/tests/test_openharness.py` so tests assert the new task-package vocabulary and alias behavior.
- Update `docs/designs/harness-completion-roadmap/*` so `OH-004` no longer teaches that archived design baselines are completed streams in the end-to-end sense.
- Update the most misleading historical package docs, especially `docs/archived/designs/python-verification-maturity/*`, so they are explicitly marked as legacy archive semantics rather than current protocol truth.

## Interfaces
- `task package terminology`
  - User-facing docs, templates, and CLI help text should say `task package`.
  - Compatibility path names and low-level internal identifiers may remain `design`-prefixed where changing them adds churn without changing meaning.
- `status semantics`
  - `detailed_ready` means design is complete enough to execute, but implementation is not yet complete.
  - `in_progress` means implementation work is actively underway.
  - `verifying` means implementation is complete enough to gather fresh evidence.
  - `archived` means the task package is done, evidenced, and no longer active.
- `historical migration`
  - Older archived packages written under the old semantics must be marked so they are not misread as current protocol examples of full completion.

## Error Handling
- If a wording update would make historical evidence inaccurate, prefer adding an explicit legacy note over silently rewriting history.
- If a CLI rename would break existing workflows, keep the old command name as an alias instead of removing it immediately.
- If any package still needs future implementation work, it must not be presented in active protocol docs as a completed archived stream under the new semantics.

## Migration Notes
- This round is a protocol migration, not a path migration.
- The repository may continue to store task packages under `docs/designs/` until a later dedicated path-migration round proves worthwhile.
- `OH-007` is the main regression case that should be used to validate whether the new wording prevents false archive interpretation.

## Detailed Reflection
- I challenged the testing strategy first. The highest risk is not parser breakage; it is leaving the old semantic contradiction intact in docs while only renaming labels.
- I challenged whether all archived packages needed full rewriting. They do not; targeted legacy markers are enough where the old semantics would otherwise mislead future handoffs.
- I checked whether the CLI needed a hard rename. It does not; aliases are enough to move the protocol forward without needless breakage.
- I checked whether `detailed_ready` was concrete enough to serve as the pre-implementation resting point. It is, and using it avoids inventing another state.
- No bounded subagent discussion was used because the main design question is repository-local protocol alignment, not a contested external dependency.
