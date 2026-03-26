# OH-026 Remove legacy new-task positional compatibility

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务包聚焦移除 `openharness.py new-task` 对旧位置参数形式的兼容，避免继续把 `task_name task_id title` 这种过时调用默默当成合法输入。
- 本轮结论是收紧 CLI：`new-task` 只接受 `task_name` 作为位置参数，`task_id` 与 `title` 必须通过 `--task-id`、`--title` 显式传入，并用测试固定这一边界。

## Current Status
- 当前已完成实现与验证，本任务包将在本轮归档。
- 当前状态应与 `STATUS.yaml` 一致，为 `archived`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
