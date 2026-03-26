# OH-027 为 OpenHarness 提供全局命令入口

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务为 OpenHarness 增加可安装的全局命令 `openharness`，让智能体和维护者不再依赖冗长的 `uv run python .../openharness.py <cmd>` 路径调用。
- 本轮范围包括 CLI 打包入口、现有脚本兼容层、安装文档与已安装用户的迁移说明，不包括原生二进制发布。

## Current Status
- 当前实现、文档和验证都已完成，正在整理证据并准备归档。
- 本轮已经验证全局 `openharness` 命令可安装可执行，旧脚本入口保持兼容。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
