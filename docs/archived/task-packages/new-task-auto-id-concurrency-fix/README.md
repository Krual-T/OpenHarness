# OH-024 New Task Auto ID Concurrency Fix

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 修复 `openharness.py new-task --auto-id` 在并行执行时可能生成重复 `task_id` 的竞争条件，把“分配编号”和“创建 task package”收敛到同一个仓库级临界区内，并补齐回归测试与验证路径。

## Current Status
- 当前已完成实现与验证，`new-task --auto-id` 的编号分配和 package 创建已经被收敛到同一个仓库级临界区。
- 本包将归档为 `archived`，不再属于 active work。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
