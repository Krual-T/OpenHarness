# Evidence

## Residual Risks
- The repository may contain edge-case skills whose wording still sits between optional-helper and imported-generic semantics.
- Imported generic skills may need a lighter-touch explanation rule than repository-owned skills.
- Archived packages may still carry indirect wording from the retired plan-oriented surface after the first cleanup pass.

## Manual Steps
- None.

## Files
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/README.md`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/STATUS.yaml`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/01-requirements.md`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/02-overview-design.md`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/03-detailed-design.md`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/05-verification.md`
- `docs/archived/task-packages/skill-taxonomy-and-compatibility-cleanup/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/README.md`
- `docs/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/task-packages/harness-completion-roadmap/03-detailed-design.md`
- `docs/task-packages/harness-completion-roadmap/05-verification.md`
- `docs/task-packages/harness-completion-roadmap/06-evidence.md`
- `README.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`
- `docs/archived/task-packages/reflective-design-review/06-evidence.md`
- `docs/archived/task-packages/workflow-redesign/02-overview-design.md`
- `docs/archived/task-packages/workflow-redesign/03-detailed-design.md`
- `docs/archived/task-packages/workflow-redesign/06-evidence.md`
- removed `skills/writing-plans/**`
- removed `skills/executing-plans/SKILL.md`
- removed `skills/writing-skills/**`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task skill-taxonomy-and-compatibility-cleanup OH-008 "Skill Taxonomy And Compatibility Cleanup" --owner codex --summary "Clarify core protocol skills, optional helpers, compatibility shims, and imported generic skills so the skill hub and per-skill docs stop drifting."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'retired_skills_are_not_shipped_live or key_repo_skills_are_vendored_locally or optional_execution_skills_are_not_described_as_core_protocol or skill_hub_declares_no_parallel_entry_skill or openharness_skill_is_repo_entry_skill'`
- `git stash push --keep-index -u -m codex-temp-verify-008-commit`
- `rmdir skills/writing-plans/references`
- `rmdir skills/writing-plans`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Follow-ups
- Start the maintenance package only after this taxonomy is stable enough to reuse.
