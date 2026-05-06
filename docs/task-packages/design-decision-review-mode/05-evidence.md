# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 本轮未新增 pytest 文档字符串测试；残余风险是协议行为仍依赖 agent 正确读取 skill 文档。
- 子智能体复审已覆盖主要行为链路，但不能穷尽所有未来任务类型和措辞变体。

## Manual Steps
- 子智能体协议审查已执行两轮：
  - 第一轮结论为不通过，指出分类缺失前置确认、粗粒度确认语义和 overview `auto` 写回要求的缺口。
  - 修正后第二轮结论为通过，确认当前规则足够让新会话 agent 稳定执行逐项设计确认。

## Files
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
  - 新增可选 `collaboration` 字段示例。
- `skills/using-openharness/SKILL.md`
  - 新增任务分类与设计确认模式的入口解释、触发规则和缺失 `task_type` 的前置确认要求。
- `skills/brainstorming/SKILL.md`
  - 新增 requirements 收敛后的任务分类建议、人类确认和 `collaboration.task_type` 写入规则。
- `skills/exploring-solution-space/SKILL.md`
  - 新增逐项设计确认执行规则、`N/M` 进度、`stepwise` / `auto` 写入和用户响应语义。
- `skills/using-openharness/references/overview-design-writing-guidance.md`
  - 新增 overview 级 confirmed design points 写回要求，并说明 `auto` 也要记录关键 decision points。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
  - 新增 detailed 级 confirmed design points 写回要求。
- `docs/task-packages/design-decision-review-mode/STATUS.yaml`
  - 记录本任务的 `collaboration.task_type: protocol/architecture` 和 `collaboration.design_review_mode: stepwise`，并声明验证命令和协议审查场景。
- `docs/task-packages/design-decision-review-mode/04-verification.md`
  - 记录验证路径、执行结果、子智能体审查结果和残余风险。
- `docs/task-packages/design-decision-review-mode/05-evidence.md`
  - 记录本轮证据索引。

## Commands
- `uv run openharness transition design-decision-review-mode in_progress`
- `uv run openharness check-tasks`
- `uv run openharness transition design-decision-review-mode verifying`
- final verification command: `uv run openharness verify design-decision-review-mode`

## Artifact Paths
- `.harness/artifacts/OH-042/verification-runs/20260506T103938431619Z.json`
- 验证结论记录在 `docs/task-packages/design-decision-review-mode/04-verification.md`。
- 证据索引记录在 `docs/task-packages/design-decision-review-mode/05-evidence.md`。

## Follow-ups
- 暂无单独后续任务。
- 如果未来发现 agent 仍跳过分类确认、误解 `auto` 或不写回 confirmed decision points，应开启新的协议修正 task package。
