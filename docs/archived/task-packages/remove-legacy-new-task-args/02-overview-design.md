# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖三类表面：

1. `skills/using-openharness/scripts/openharness_cli/cli.py` 的 `new-task` 参数定义。
2. `skills/using-openharness/scripts/openharness_cli/commands.py` 的 `cmd_new_task` 入参处理。
3. `skills/using-openharness/tests/` 中与 `new-task` 参数边界相关的测试。

不纳入范围：
- 任务包模板本身；
- 其他 CLI 子命令；
- 任何向后兼容迁移提示机制。

## Proposed Structure
推荐方案很直接：

1. parser 层删除旧位置参数 `legacy_task_id`、`legacy_title`。
2. handler 层只读取 `task_id`、`title` 这两个显式 flag。
3. 测试层把旧位置参数从正向用例改成失败用例。

主路径应只有一条：

- `new-task <task_name> [--task-id <id> | --auto-id] [--title <title>]`

这比保留双轨兼容更清晰，也更符合仓库当前文档方向。

## Key Flows
行为流如下：

1. 用户输入 `new-task`。
2. parser 只接受 `task_name` 这个位置参数。
3. 如果需要显式 id，必须走 `--task-id`；如果要自动分配，必须走 `--auto-id`。
4. 如果还传入额外的旧位置参数，argparse 直接报错并退出。
5. handler 仅处理已经规范化的参数，不再做旧字段兜底。

## Stage Gates
进入 detailed 前需要明确：

1. 旧兼容要删除到 parser 层，而不是仅在 handler 层忽略。
2. 哪些测试仍然写着旧字段，需要一起收敛。
3. 错误调用的期望行为是“报错退出”，不是“猜测修正”。

## Trade-offs
收益：
- CLI 心智模型更单一。
- 错误输入更早暴露。
- 避免再次产生误导性 task package 目录。

代价：
- 任何仍在使用旧位置参数的调用都会立即失效。

不选的方向：
- 继续兼容旧参数，但给 warning。问题是 warning 仍然允许错误路径成功执行，不能真正防止误生成目录。
- 只在 handler 层删逻辑，不改 parser。问题是 parser 仍会把旧位置参数视为合法接口。

## Overview Reflection
反思后确认：

1. 这不是需要保留的“平滑兼容”，因为旧形式已经造成实际误用。
2. 最合适的切断点是 parser，而不是更后面的命令逻辑。
3. 测试必须从“旧形式还能工作”切换为“旧形式必须失败”，否则回归保护不完整。
