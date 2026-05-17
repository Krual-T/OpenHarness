# CLI Reference

本文件提供 OpenHarness CLI 的速查参考和关键约束。

## CLI 速查

| 场景 | 命令 |
|------|------|
| 列出活跃任务包 | `openharness task-package list` |
| 创建任务包 | `openharness task-package new <name> --auto-id` |
| 推进状态 | `openharness transition <task> <target>` |
| 结构验证 | `openharness check-tasks` |
| 查看写作指南 | `openharness writing-guide list` / `read <name>` |
| 自更新 | `openharness update` |
| 运行时工作流 | `openharness rwp list` / `show` / `run` |

## 关键约束

- `STATUS.yaml` 是唯一状态源；`README.md` 的 Current Status 必须与其一致
- 文档正文中文；节标题、命令、状态值、YAML 键、文件名、路径保持英文
- 设计决策写入 task-package 文档，不留在聊天里
- 不要绕过 using-openharness 自创平行工作流
- 验证由 Agent 在 `verifying` 阶段直接执行命令，证据写入 `evidence.md`
- 向用户展示信息时使用通俗易懂的中文，不写中英穿插的口号式短句
