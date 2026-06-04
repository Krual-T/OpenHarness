---
name: using-openharness
description: OpenHarness SDD 任务包协作协议——代码修改、设计决策、bug 修复、新增功能时使用此流程。
---

# using-openharness

OpenHarness 是 SDD 驱动的任务包协作协议。具体阶段指令由 CLI 输出的阶段 instructions 接管。

## 任务包边界

需要任务包：

- 代码修改
- 设计决策
- bug 修复
- 新增功能
- 会改变仓库事实源的文档更新

不需要任务包：

- 纯问答
- 解释现有代码
- 未进入执行的方案讨论

不需要任务包时直接回应用户。已经进入任务包的设计讨论，确认后的设计决策仍应写回任务包文档。

## 先理解，再建包

需要任务包时，**不要直接建包**。先完成理解：

1. **搜集上下文**：根据用户问题对项目或网络进行探索，搜集理解用户意图所需的相关上下文
2. **确认问题**：向用户确认你对问题/目标的理解是否正确——不管 AI 自认为多清楚，必须获得用户确认
3. **明确边界**：搞清楚这次要做什么、不做什么

只有在理解清楚、用户也确认之后，才执行：

```
openharness task-package list
```

按输出：

- 有匹配活跃包：`openharness task-package view <task-name>|<task-id>`
- 无匹配或空：`openharness task-package new <name>`

随后执行 CLI 输出的当前阶段 instructions。进入 proposing 后，理解工作已在上游完成，不要再从头问"这个任务清晰还是模糊"——直接从需求编写开始。

## 阶段完成

每个活跃阶段完成后，用 `transition` 推进到对应完成态：

```
openharness task-package transition <task-name>|<task-id> <完成态>
```

| 当前阶段 | 完成态 |
|----------|--------|
| `proposing` | `requirements_designed` |
| `overview_designing` | `overview_designed` |
| `detailed_designing` | `detailed_designed` |
| `verification_designing` | `verification_designed` |
| `implementing` | `implemented` |
| `verifying` | `verified` |

Agent 只负责把当前阶段 transition 到对应完成态；后续推进由 CLI 处理。
