# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
去掉 `new-task` 的旧位置参数兼容，让错误调用在 parser 层直接失败，避免再次误生成诸如 `docs/task-packages/name` 这类错误目录。

## Problem Statement
当前 `new-task` 同时接受：

- 新形式：`new-task <task_name> --task-id <id> --title <title>`
- 旧兼容形式：`new-task <task_name> <legacy_task_id> <legacy_title>`

这会带来两个问题：

1. CLI 表面允许两套心智模型并存，容易让协作者误用。
2. 一旦误把旧形式当成当前规范，CLI 会静默成功，生成错误任务包目录，而不是在入口处立即报错。

这次就出现了实际误用，因此需要把兼容层彻底删除，而不是继续容忍。

## Required Outcomes
1. `new-task` parser 不再接受 `legacy_task_id`、`legacy_title` 这两个位置参数。
2. `cmd_new_task` 不再读取旧兼容字段。
3. 自动化测试覆盖新形式成功、旧形式失败这两条路径。
4. 本轮验证命令通过，并把证据写回任务包。

单一成功指标是：`parser.parse_args(["new-task", "name", "OH-999", "Title"])` 会失败，而 `["new-task", "name", "--task-id", "OH-999", "--title", "Title"]` 会成功。

Acceptance Criteria:
1. CLI `new-task --help` 不再展示 `legacy_task_id` 与 `legacy_title`。
2. 仓库测试不再构造旧兼容字段。
3. 旧位置参数形式会在测试中触发失败，而不是进入 handler。

## Non-Goals
- 不改 task package 的整体协议。
- 不顺手调整 `transition`、`verify` 等其他子命令参数风格。
- 不兼容更多过渡别名或自动修正错误输入。

## Constraints
- `new-task` 的主路径必须更明确，而不是更“聪明”。
- 变更后测试和脚本调用都必须使用 flag 形式传递 `task_id` 与 `title`。
- 完成前至少运行 metadata/CLI 相关测试、完整 harness 测试和 `check-tasks`。
