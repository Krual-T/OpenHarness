# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k "new_task or legacy_positional or task_package_commands_use_current_handlers_only"`
  - `uv run pytest skills/using-openharness/tests/test_openharness.py`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Fallback Path:
  - 如果聚焦测试覆盖不足，则直接以完整 `test_openharness.py` 结果为准。
  - 如果完整 pytest 通过但 `check-tasks` 失败，仍不能宣称完成。
- Planned Evidence:
  - parser 只剩一个位置参数 `task_name`。
  - 旧位置参数形式在测试中触发 `SystemExit`。
  - `cmd_new_task` 测试不再传入 `legacy_task_id`、`legacy_title`。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/scripts/openharness_cli/cli.py`
  - 删除旧位置参数定义。
- `skills/using-openharness/scripts/openharness_cli/commands.py`
  - 删除旧兼容字段读取逻辑。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 把旧调用改成 flag 形式，并新增旧位置参数失败断言。
- `skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
  - 删掉旧字段构造，补一条缺少 `--task-id/--auto-id` 的失败路径测试。
- `docs/archived/task-packages/remove-legacy-new-task-args/*`
  - 记录本轮协议修复。

## Interfaces
稳定接口是 `new-task` CLI：

- 位置参数：仅 `task_name`
- 可选 flag：`--task-id`、`--title`、`--auto-id`、`--owner`、`--summary`、`--status`、`--repo`

不再存在的接口：
- `legacy_task_id`
- `legacy_title`

## Stage Gates
进入实现前必须已经明确：

1. 正向成功调用样例要改成 flag 形式。
2. 反向失败调用样例要覆盖旧位置参数。
3. handler 不再依赖旧字段存在。

## Decision Closure
接受：
- 在 parser 层硬删除旧位置参数。
- 让错误旧调用直接失败。

拒绝：
- 保留兼容但只打印提醒。
- 在 handler 层静默猜测第二、第三个位置参数的语义。

延期：
- 若未来需要显式迁移提示，可单独讨论更友好的错误文案，但不影响先删除兼容。

## Error Handling
关键失败路径：

1. 用户不给 `--task-id` 且不传 `--auto-id`。
   - 继续返回当前明确错误。
2. 用户继续使用旧位置参数。
   - argparse 直接报错，不进入 handler。

这样可以避免“命令成功但语义错位”这种更隐蔽的错误。

## Migration Notes
迁移顺序：

1. 先改测试。
2. 再改 parser 和 handler。
3. 最后跑完整验证并归档任务包。

回滚时如果真的要恢复兼容，也应配套明确 warning 和过期计划，而不是恢复当前这种无提示双轨模式。

## Detailed Reflection
反思结论：

1. 这类 CLI 兼容问题更适合用 parser 测试锁住，而不是只测业务结果。
2. 接口收紧后，仓库脚本更难被“看似自然、实则过时”的调用方式误用。
