# OH-035 Intake Routing And First Reply Naturalness

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本轮任务聚焦于修正 OpenHarness 在“刚收到用户请求时”过于协议化、过于像执行日志的入口体验。
- 重点不是否定 `using-openharness`、阶段播报或 `bootstrap`，而是重新划清它们的适用边界：什么情况下应作为前台入口动作，什么情况下只应作为后台上下文。
- 计划覆盖 intake routing、首轮用户可见回复、`bootstrap` 的使用时机，以及技能协议与实际对话体验之间的衔接方式。

## Current Status
- 当前处于 `archived`：协议约束、测试和任务文档已经同步完成，本轮不再属于 active work。
- 本轮已经把入口主轴判断、`bootstrap` 的前台/后台边界，以及首轮回复避免执行日志回放的约束写进正式 skill 协议，并通过验证。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
