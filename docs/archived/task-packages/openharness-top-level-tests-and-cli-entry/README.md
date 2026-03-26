# OH-031 Move OpenHarness Tests To Top Level And Remove Script Compatibility Entry

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮任务把 OpenHarness 仓库自测从 `skills/using-openharness/tests/` 迁到项目顶层 `tests/`，同时移除 `skills/using-openharness/scripts/openharness.py` 这一层历史兼容入口，收敛成以 `openharness_cli` 和 `openharness` 控制台命令为正式入口；旧路径的历史证据通过 `docs/archived/legacy/` 快照保留，不逐个改旧任务包。

## Current Status
- 当前处于实现准备阶段。目标是完成测试迁移、删除兼容脚本、修正导入与文档，再以新的顶层测试路径完成验证。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
