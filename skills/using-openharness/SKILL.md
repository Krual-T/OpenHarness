---
name: using-openharness
description: OpenHarness 仓库入口——会话开始时加载。定义任务包协议、状态流转、受保护文件和输出约定。
---

# using-openharness

OpenHarness 是任务包驱动的协作协议。所有代码修改、设计决策、bug 修复必须通过任务包追踪，不允许绕过。

## 入口判断

收到用户请求后，先读 `AGENTS.md` 了解仓库地图和约定，然后判断：

**需要任务包**：代码修改、设计决策、bug 修复、新增功能
**不需要任务包**：纯问答、解释代码、讨论方案（未到执行）

不需要时直接回应用户。需要时：

```
openharness task-package list
```

按输出：
- **有匹配活跃包** → 读取 STATUS.yaml，按 CLI 输出的状态指令推进
- **无匹配或空** → 新建任务包

## 核心命令

| 场景 | 命令 |
|------|------|
| 列出活跃任务包 | `openharness task-package list` |
| 新建任务包 | `openharness task-package new <name> --auto-id` |
| 推进状态 | `openharness transition <task> <目标状态>` |
| 协议验证 | `openharness check-tasks` |

`<name>` 用简短英文 slug，如 `fix-auth-timeout`、`add-export-csv`。

其他命令见 [references/cli-reference.md](references/cli-reference.md)。

## 状态流转

每次 `openharness transition` 成功后，CLI 自动输出新状态的指令内容（hook 模式）。Agent 直接执行即可，不需要主动查状态路由表。

中间 gate 状态（`requirements_designed`、`overview_designed`、`detailed_designed`、`verification_designed`、`implemented`、`verified`）CLI 自动检查前置条件并推进。

回退：`openharness transition <task> <目标状态>`。

## 受保护文件

以下文件/目录不在任务包追踪内，不允许随意修改：

- `AGENTS.md` — 仓库级约定，修改需明确用户同意
- `skills/using-openharness/` — harness 协议定义，修改需通过任务包
- `openharness_cli/` — CLI 源码，修改需通过任务包
- `.harness/` — harness 运行时状态，不可手动修改

## 输出约定

- 向用户展示信息使用通俗易懂的中文，不写中英穿插的口号式短句
- 文档正文用中文；节标题、命令、状态值、YAML 键、文件名、路径保持英文
- 设计决策写入任务包文档，不留在聊天里
