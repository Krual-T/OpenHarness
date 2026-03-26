# Evidence

## Residual Risks
- Some downstream repositories may still need clearer examples showing when `pytest` is only the minimum floor and when project-specific runtime verification is required immediately.
- A later maintenance package may still want to audit whether every future skill added to the repository keeps the same protocol-status and stage wording.

## Manual Steps
- None.

## Files
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/README.md`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/STATUS.yaml`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/01-requirements.md`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/02-overview-design.md`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/03-detailed-design.md`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/04-verification.md`
- `docs/archived/task-packages/skill-taxonomy-and-stage-model/05-evidence.md`
- `README.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/test-driven-development/SKILL.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/dispatching-parallel-agents/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task skill-taxonomy-and-stage-model OH-011 "Skill Taxonomy And Stage Model" --owner codex --summary "Reshape OpenHarness skill classification around protocol status plus workflow stage, and define pytest as the Python baseline verification floor in live docs."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'skill_hub_uses_protocol_status_plus_stage_model or readme_describes_plug_and_play_harness_and_python_pytest_floor'`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model requirements_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model overview_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model detailed_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model verifying`
- `uv run python skills/using-openharness/scripts/openharness.py verify skill-taxonomy-and-stage-model`
- `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model archived`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Artifact Paths
- `.harness/artifacts/OH-012/verification-runs/20260322T164921906572Z.json`

## Follow-ups
- Reuse this package as the live baseline if later maintenance work adds automated audits for skill taxonomy drift.
- Reuse archived `OH-007 Python Verification Maturity` when a later package needs stronger examples or template support around the pytest-floor versus runtime-verification distinction.
