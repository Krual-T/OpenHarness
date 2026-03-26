# OH-028 为 OpenHarness 增加 update 子命令

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务为 OpenHarness 增加 `openharness update` 子命令，把原本需要手工执行的仓库更新与工具刷新收敛成一个稳定入口。
- 本轮范围包括 CLI 子命令、失败处理、安装文档和相关测试，不扩展为通用包管理器。

## Current Status
- 当前处于设计与测试准备阶段，目标已经明确，下一步是先写失败测试再接入 CLI。
- 当前实现、文档与验证都已完成，正在补齐证据并准备归档。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
