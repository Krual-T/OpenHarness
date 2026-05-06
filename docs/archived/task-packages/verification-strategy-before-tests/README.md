# OH-043 Verification Strategy Before Tests

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
本任务解决 OH-042 推进过程中暴露出来的验证策略问题：OpenHarness 不应把“先写 pytest”机械套到所有任务上，而应先在 detailed design 中明确验证对象和证据路径，再决定是否需要自动测试、协议审查、子智能体 dry run、runtime workflow 或人工场景验证。

## Current Status
当前仅完成需求上下文记录，尚未进入 overview / detailed design，也尚未实现。

建议新会话先确认任务分类。推荐分类是 `protocol/architecture`，因为它会影响 OpenHarness 的 skill 行为、验证路径和 agent 工作流；确认后再写入 `STATUS.yaml.collaboration.task_type`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
