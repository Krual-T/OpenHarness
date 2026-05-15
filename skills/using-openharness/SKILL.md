---
name: using-openharness
description: 当会话开始时使用——建立仓库工作流技能的使用方式，在任何回应之前读取
---

# using-openharness

唯一仓库入口。读完本文件必须知道：当前在哪个状态、该调哪个 skill、完成条件是什么、失败时回退到哪。

## 入口流程

1. 先读 `AGENTS.md`，了解仓库地图、`uv run` 约定、提交要求。
2. 判断是否需要任务上下文——详见 [session-routing.md](references/session-routing.md)。
3. 需要时运行 `openharness bootstrap`，按结果分三种情况处理。
4. 确认任务分类（task_type）——详见 [task-classification.md](references/task-classification.md)。
5. 按状态路由表调用对应 skill——详见 [state-routing-table.md](references/state-routing-table.md)。

## 新建任务包

```
openharness new-task <name> --auto-id
```

创建后状态为 `proposing`，调用 `brainstorming` 写 `01-requirements.md`。

## 状态路由

所有状态→skill→写作指南→退出条件的映射见 [state-routing-table.md](references/state-routing-table.md)。

## 回退

任何状态可回退：`openharness transition <task> <目标状态>`。常见场景和回退目标见路由表。

## CLI 与约束

速查命令和关键约束见 [cli-reference.md](references/cli-reference.md)。
