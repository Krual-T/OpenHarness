# OH-040 Pluggable Runtime Validation Workflows

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务包的意图是探索 OpenHarness 如何支持可插拔的 runtime 级验证路径。
- runtime 验证天然依赖具体项目的入口、外部系统、凭证、观测面和通过标准，因此 OpenHarness 需要一种方式让项目专属验证工作流被发现、配置、执行和报告。
- `lark-cli` 只作为第一个参考样例，用来验证这套机制是否能承接真实项目中的外部系统交互验证。

## Current Status
- Status: `verifying`
- 当前已实现 RWP 最小协议表面：`openharness rwp list/show/run`、`.harness/rwp/workflows/` 发现、`.env` 加载、`openharness.rwp.get_logger()` runtime API，以及 RWP 相关 skill/guidance 文档迁移。最终验证 artifact 已写入 `04-verification.md` 与 `05-evidence.md`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
