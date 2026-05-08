# OH-044 Archived Status Auto Move

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 让 OpenHarness 在读取 task package 时自动规范化 active 根目录下的 `status: archived` 包，把它移动到 `docs/archived/task-packages/<task>/` 并重写包内路径。

## Current Status
- 设计已收敛，接下来用 TDD 修改 CLI 发现流程与测试。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
