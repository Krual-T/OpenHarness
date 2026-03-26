# Evidence

## Residual Risks
- 当前虽然已把协议落到 live skills，但尚未验证这些角色注入规则在真实复杂任务中的交互成本。
- 尚未把角色挑战问题清单提炼成可复用模板或提示词。
- 当前阶段门禁与收敛优先级仍是文档定义，尚未在真实任务中证明它们足以压制流程膨胀。

## Manual Steps
- 无。

## Files
- `docs/archived/task-packages/gstack-methodology/README.md`
- `docs/archived/task-packages/gstack-methodology/STATUS.yaml`
- `docs/archived/task-packages/gstack-methodology/01-requirements.md`
- `docs/archived/task-packages/gstack-methodology/02-overview-design.md`
- `docs/archived/task-packages/gstack-methodology/03-detailed-design.md`
- `docs/archived/task-packages/gstack-methodology/04-verification.md`
- `docs/archived/task-packages/gstack-methodology/05-evidence.md`
- `skills/using-openharness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.04-verification.md`
- `skills/using-openharness/tests/test_openharness.py`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py new-task gstack-methodology 001 "Absorb Gstack Methodology And Multi-Agent Perspectives"`
- `uv run python skills/using-openharness/scripts/openharness.py transition gstack-methodology in_progress`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -q`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Artifact Paths
- `docs/archived/task-packages/gstack-methodology/04-verification.md`
- `docs/archived/task-packages/gstack-methodology/05-evidence.md`

## Follow-ups
- 为每个角色整理一份问题清单和“可否决条件”模板，避免角色定义停留在抽象层。
- 在真实任务包里验证这套协议是否会引入过重的讨论成本。
- 若进入实现轮次，应把“挑战处置状态”设计为显式文档槽位，而不是散落在聊天记录里。
