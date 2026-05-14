# Session Routing

本文件负责 using-openharness 的会话入口逻辑：判断是否需要任务上下文、处理 bootstrap 结果、创建新任务包。

## 判断是否需要任务上下文

收到用户请求后，先读 `AGENTS.md` 了解仓库地图、`uv run` 约定和提交要求，然后判断：

**需要任务上下文**：用户请求涉及代码修改、设计决策、bug 修复、新增功能
**不需要任务上下文**：纯问答、解释代码、讨论方案（未到执行阶段）

不需要时直接回应用户；需要时，从项目根目录运行 `openharness bootstrap`。

## Bootstrap 结果处理

运行 `openharness bootstrap` 后，根据输出分三种情况：

### 有匹配的活跃任务包

读取 `STATUS.yaml` → 确认 `task_type` → 按 state-routing-table.md 推进。

如何判断"匹配"：bootstrap 列出的活跃任务包中，`title` 和 `summary` 与用户请求相关。不确定时列出候选包让用户确认。

### 有活跃任务包但不匹配用户请求

这是新任务。运行：

```
openharness new-task <name> --auto-id
```

创建后包状态为 `proposing`，调用 `brainstorming` 写 `01-requirements.md`，然后按状态路由表推进。

### 无活跃任务包

这也是新任务。同样运行 `openharness new-task <name> --auto-id`，然后同上流程。

## 新建任务包

```bash
openharness new-task <name> --auto-id
```

`<name>` 建议使用简短的英文 slug，如 `fix-auth-timeout`、`add-export-csv`。

创建后：
1. 包状态为 `proposing`
2. 调用 `brainstorming` 收敛需求
3. 第一次写入 `01-requirements.md` 时即使用模板文件（`templates/01-requirements.md`）
4. 需求收敛后提议 task_type，等用户确认后写入 `STATUS.yaml`
