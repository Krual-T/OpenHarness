# State Routing Table

本文件负责 OpenHarness 的状态路由：标准/机械流程的完整路由表、implementing 阶段技能选择决策树、回退与异常处理。

## 标准流程

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

## 机械流程

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

## 实现阶段 skill 选择

`implementing` 状态使用以下决策树选择技能：

```
任务是否以调试失败/修复 bug 为中心？
  ├── YES → systematic-debugging
  └── NO  → 用户是否明确要求子代理或并行调度？
               ├── YES → subagent-driven-development
               └── NO  → 任务是否有明确行为契约且适合自动化测试？
                           ├── YES → test-driven-development
                           └── NO  → 直接手动实现（无特定 skill）
```

多个 skill 可组合使用。例如：`subagent-driven-development` 分发任务，子 agent 内部用 `test-driven-development` 实现，遇到失败用 `systematic-debugging` 排查。

| 场景 | 调用 |
|------|------|
| 有明确行为契约、可写自动化测试 | `test-driven-development` |
| 工作可拆分为独立子任务、需要并行或隔离执行 | `subagent-driven-development` |
| 遇到 bug、测试失败、意外行为 | `systematic-debugging` |

## 路由表说明

- `_designed` / `implemented` 是 gate 状态：前一阶段已完成，等待推进。不需调用 skill，只执行 `transition`
- `_designing` / `implementing` / `verifying` / `proposing` 是活跃状态：调用对应 skill 执行工作
- 每个活跃状态的退出条件在对应写作指南的 Exit Check 中定义
- `verifying` 阶段：`verification-before-completion` skill 负责写文档和人工审查，`openharness verify <task>` 负责运行 `STATUS.yaml` 中声明的验证命令并记录产物。两者互补，不是替代
- 验证失败时，应调用 `systematic-debugging` 排查根因，而非直接回退到 `implementing`

## 门禁规则

所有 `_designed` / `implemented` gate 状态在 `transition` 推进前，代理**必须**完成对应写作指南的全部 Exit Check。

**硬性阻塞规则**：
- 任何一条 Exit Check 问题答不上来 → **阻塞**，不得 `transition`
- 写作指南的 Anti-Rationalization 表中的任何借口出现 → **阻塞**，回到活跃状态重新工作
- 如果对完成度有疑问 → 宁可回退到活跃状态重新工作，也不要带着未解决的歧义推进

**不要过度阻塞**：
- 如果一个阶段已明显完成（所有 Exit Check 问题都能明确回答），不要在 gate 状态反复犹豫——直接 `transition` 推进
- Gate 状态的目的是确保质量，不是制造停滞

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

## 相关文档

- `session-routing.md`：会话入口和 bootstrap 处理
- `task-classification.md`：任务分类和审查模式
- `cli-reference.md`：CLI 速查和关键约束
