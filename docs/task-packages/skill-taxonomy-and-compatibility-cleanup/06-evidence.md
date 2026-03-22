# Evidence

## Residual Risks
- The repository may contain edge-case skills whose wording still sits between optional and compatibility helper semantics.
- Imported generic skills may need a lighter-touch explanation rule than repository-owned skills.
- `writing-plans` still survives as a narrower compatibility helper, so future taxonomy work may still choose to retire it or tighten its remaining scope further.

## Manual Steps
- None yet.

## Files
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/README.md`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/STATUS.yaml`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/01-requirements.md`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/02-overview-design.md`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/03-detailed-design.md`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/05-verification.md`
- `docs/task-packages/skill-taxonomy-and-compatibility-cleanup/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/README.md`
- `docs/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/task-packages/harness-completion-roadmap/03-detailed-design.md`
- `docs/task-packages/harness-completion-roadmap/05-verification.md`
- `docs/task-packages/harness-completion-roadmap/06-evidence.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`
- removed `skills/executing-plans/SKILL.md`
- removed `skills/writing-skills/**`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task skill-taxonomy-and-compatibility-cleanup OH-008 "Skill Taxonomy And Compatibility Cleanup" --owner codex --summary "Clarify core protocol skills, optional helpers, compatibility shims, and imported generic skills so the skill hub and per-skill docs stop drifting."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`
- `rmdir skills/executing-plans`
- `rmdir skills/writing-skills/examples`
- `rmdir skills/writing-skills`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'retired_skills_are_not_shipped_live or key_repo_skills_are_vendored_locally or optional_execution_skills_are_not_described_as_core_protocol or skill_hub_declares_no_parallel_entry_skill or openharness_skill_is_repo_entry_skill'`
- `git stash push --keep-index -u -m codex-temp-verify-008-commit`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Follow-ups
- Decide later whether `writing-plans` should remain as a narrower compatibility helper or also be retired.
- Start the maintenance package only after this taxonomy is stable enough to reuse.
