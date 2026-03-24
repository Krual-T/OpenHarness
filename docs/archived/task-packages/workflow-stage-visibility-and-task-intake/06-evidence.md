# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- skill 文案现在明确了“阶段播报”和“脑暴结束再建包”，但真实运行时若上层代理系统绕过这些 skills，仍可能退回到旧行为。
- 自动编号没有仓库级固定前缀配置，当前策略依赖已有 task id 分布；对 OpenHarness 够用，但对未来更复杂的仓库可能还要补配置位。

## Manual Steps
- 无。

## Files
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/README.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/01-requirements.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/02-overview-design.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/03-detailed-design.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/05-verification.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/06-evidence.md`
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/STATUS.yaml`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `README.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task workflow-stage-visibility-and-task-intake OH-018 "Workflow Stage Visibility And Task Intake" --owner codex --summary "Improve OpenHarness so humans and agents can see the current workflow stage clearly, and automatically scaffold a task package when brainstorming finishes and the agent is about to enter the next stage."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "allocate_next_task_id or scaffolds_task_package_before_exploration_when_missing or requires_explicit_stage_checkpoints or bootstrap_reports_stage_guidance_in_text_output or bootstrap_json_includes_stage_guidance"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-stage-visibility-and-task-intake requirements_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-stage-visibility-and-task-intake overview_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-stage-visibility-and-task-intake detailed_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-stage-visibility-and-task-intake in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py verify workflow-stage-visibility-and-task-intake`

## Artifact Paths
- `.harness/artifacts/OH-018/verification-runs/20260324T160213488137Z.json`
- `.harness/artifacts/OH-018/verification-runs/latest.json`
- `.harness/artifacts/OH-018/verification-runs/`

## Follow-ups
- 如果后续仍然频繁出现“设计未审核即开始实现”的体验问题，应单独开包讨论是否要在 `detailed_ready -> in_progress` 之间引入更明确的人类确认闸门。
- 如果将来 OpenHarness 被用于混合多个 task id 前缀的仓库，可以再开包为 `new-task` 增加可配置前缀策略。
