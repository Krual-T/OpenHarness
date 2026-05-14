---
name: using-openharness
description: 在任何对话开始时使用——建立如何发现和使用仓库工作流技能，在做出任何回应之前
---

<SUBAGENT-STOP>
如果你作为子代理被调度执行特定任务，跳过本技能，除非任务明确涉及仓库 harness 协议。
</SUBAGENT-STOP>

# using-openharness

唯一仓库入口。读完本文件必须知道：当前在哪个状态、该调哪个 skill、该读哪份写作指南、完成条件是什么、失败时回退到哪、下一步 `openharness transition` 到哪。

## 入口

1. 先读 `AGENTS.md`，了解仓库地图、`uv run` 约定、提交要求
2. 判断是否需要任务上下文：
   - **需要**：用户请求涉及代码修改、设计决策、bug 修复、新增功能
   - **不需要**：纯问答、解释代码、讨论方案（未到执行阶段）
3. 不需要时直接回应用户；需要时，从项目根目录运行 `openharness bootstrap`

**bootstrap 结果处理**：

- **有匹配的活跃任务包**：读取 `STATUS.yaml` → 确认 `task_type` → 按状态路由表推进
- **有活跃任务包但不匹配用户请求**：这是新任务，先建包再推进
- **无活跃任务包**：这是新任务，先建包再推进

**新建任务包**：

```
openharness new-task <name> --auto-id
```

创建后包状态为 `proposing`，调用 `brainstorming` 写 `01-requirements.md`，然后按状态路由表推进。

## 任务分类

读取 `STATUS.yaml` 后，首先确认 `collaboration.task_type` 是否已填写。

### task_type

| 值 | 含义 | 适用场景 |
|----|------|---------|
| `mechanical` | 机械任务 | 改动范围明确、无架构决策、不需要设计文档，直接改代码+验证 |
| `standard development` | 标准开发 | 需要完整的需求→设计→实现→验证流程 |
| `protocol/architecture` | 协议/架构 | 涉及跨模块契约、状态模型、迁移策略，需要更审慎的逐项设计确认 |

**如何确认**：
- 如果 `STATUS.yaml` 中 `task_type` 已存在，直接使用
- 如果缺失，根据任务性质提议一个分类，说明理由，等用户确认后再写入。不要自行决定
- 写入路径：`STATUS.yaml.collaboration.task_type`

### design_review_mode

仅在非 `mechanical` 任务时适用：

| 值 | 行为 |
|----|------|
| `stepwise` | 每个设计决策点向用户确认后才继续。`protocol/architecture` 默认此项 |
| `auto` | 记录决策点但不逐项打断用户。用户明确授权后才使用 |

**如何确认**：
- `mechanical` 任务不需要此字段
- `protocol/architecture` 默认 `stepwise`，除非用户说"不用逐项确认"
- `standard development` 主动提议 `stepwise`，但用户可以选 `auto`
- 写入路径：`STATUS.yaml.collaboration.design_review_mode`

## 状态路由表

### 标准流程

`standard development` 和 `protocol/architecture` 走此流程：

```
proposing → requirements_designed → overview_designing → overview_designed → detailed_designing
                                                                                      │
                                                                                      ▼
                                archived ← verifying ← implemented ← detailed_designed
```

| 当前状态 | 含义 | 调用 skill | 读写作指南 | 产出 | 退出条件 | 推进命令 |
|---------|------|-----------|-----------|------|---------|---------|
| `proposing` | 收敛需求 | `brainstorming` | `requirements-writing-guidance.md` | `01-requirements.md` | 指南 6 项退出检查通过，task_type 已确认 | `openharness transition <task> requirements_designed` |
| `requirements_designed` | 需求就绪 | — | — | — | — | `openharness transition <task> overview_designing` |
| `overview_designing` | 探索方案 | `exploring-solution-space` | `overview-design-writing-guidance.md` | `02-overview-design.md` | 指南 5 项退出检查通过 | `openharness transition <task> overview_designed` |
| `overview_designed` | 总设就绪 | — | — | — | — | `openharness transition <task> detailed_designing` |
| `detailed_designing` | 详细设计 | `exploring-solution-space` | `detailed-design-writing-guidance.md` | `03-detailed-design.md` | 指南 7 项退出检查通过 | `openharness transition <task> detailed_designed` |
| `detailed_designed` | 详设就绪 | — | — | — | — | `openharness transition <task> implementing` |
| `implementing` | 执行实现 | 见下方"实现阶段 skill 选择" | — | 代码、测试 | 实现完成、测试通过 | `openharness transition <task> implemented` |
| `implemented` | 实现完成 | — | — | — | — | `openharness transition <task> verifying` |
| `verifying` | 验证记录 | `verification-before-completion` | `verification-writing-guidance.md`、`evidence-writing-guidance.md` | `04-verification.md`、`05-evidence.md` | `openharness check-tasks` 通过，`openharness verify <task>` 通过 | `openharness transition <task> archived` |
| `archived` | 终态 | `finishing-a-development-branch` | — | — | 分支合并/PR/保留 | 归档到 `docs/archived/task-packages/` |

### 机械流程

`mechanical` 任务走此流程，跳过所有设计阶段：

```
proposing → requirements_designed → implementing → verifying → archived
```

| 当前状态 | 含义 | 调用 skill | 读写作指南 | 产出 | 退出条件 | 推进命令 |
|---------|------|-----------|-----------|------|---------|---------|
| `proposing` | 收敛需求 | `brainstorming` | `requirements-writing-guidance.md` | `01-requirements.md` | 指南 6 项退出检查通过 | `openharness transition <task> requirements_designed` |
| `requirements_designed` | 需求就绪 | — | — | — | — | `openharness transition <task> implementing` |
| `implementing` | 执行实现 | 见下方"实现阶段 skill 选择" | — | 代码、测试 | 实现完成、测试通过 | `openharness transition <task> verifying` |
| `verifying` | 验证记录 | `verification-before-completion` | `verification-writing-guidance.md`、`evidence-writing-guidance.md` | `04-verification.md`、`05-evidence.md` | `openharness check-tasks` 通过，`openharness verify <task>` 通过 | `openharness transition <task> archived` |
| `archived` | 终态 | `finishing-a-development-branch` | — | — | 分支合并/PR/保留 | 归档到 `docs/archived/task-packages/` |

### 实现阶段 skill 选择

`implementing` 状态可调用以下 skill，按场景选择：

| 场景 | 调用 |
|------|------|
| 有明确行为契约、可写自动化测试 | `test-driven-development` |
| 工作可拆分为独立子任务、需要并行或隔离执行 | `subagent-driven-development` |
| 遇到 bug、测试失败、意外行为 | `systematic-debugging` |

多个 skill 可组合使用。例如：`subagent-driven-development` 分发任务，子 agent 内部用 `test-driven-development` 实现，遇到失败用 `systematic-debugging` 排查。

### 路由表说明

- `_designed` / `implemented` 是 gate 状态：前一阶段已完成，等待推进。不需调用 skill，只执行 `transition`
- `_designing` / `implementing` / `verifying` / `proposing` 是活跃状态：调用对应 skill 执行工作
- 每个活跃状态的退出条件在对应写作指南的 Exit Check 中定义
- `verifying` 阶段：`verification-before-completion` skill 负责写文档和人工审查，`openharness verify <task>` 负责运行 `STATUS.yaml` 中声明的验证命令并记录产物。两者互补，不是替代

## 回退与异常

任何状态都可以回退到前面的状态。需要回退时：

```
openharness transition <task> <目标状态>
```

常见回退场景：

| 异常 | 当前状态 | 回退到 |
|------|---------|--------|
| 验证失败，需要修改代码 | `verifying` | `implementing` |
| 设计卡住，方向需重新讨论 | `overview_designing` / `detailed_designing` | `proposing` |
| 详设时发现总设方向有问题 | `detailed_designing` | `overview_designing` |
| 实现时发现设计不可行 | `implementing` | `detailed_designing` |

回退后，对应文档可能需要重写。回退不是跳过——回到 `proposing` 意味着 `01-requirements.md` 的退出检查必须重新满足。

## CLI 速查

| 场景 | 命令 |
|------|------|
| 列出活跃任务包 | `openharness bootstrap` |
| 创建任务包 | `openharness new-task <name> --auto-id` |
| 推进状态 | `openharness transition <task> <target>` |
| 结构验证 | `openharness check-tasks` |
| 运行验证命令 | `openharness verify <task>` |
| 查看写作指南 | `openharness writing-guide list` / `read <name>` |
| 自更新 | `openharness update` |
| 运行时工作流 | `openharness rwp list` / `show` / `run` |

## 关键约束

- `STATUS.yaml` 是唯一状态源；`README.md` 的 Current Status 必须与其一致
- 文档正文中文；节标题、命令、状态值、YAML 键、文件名、路径保持英文
- 设计决策写入 task-package 文档，不留在聊天里
- 不要绕过本 skill 自创平行工作流
- 验证产物必须由 `openharness verify` 实际运行产生，不要推断"应该通过"
