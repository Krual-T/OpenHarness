---
name: using-openharness
description: 仅在每个会话开始时使用。
---

# using-openharness

OpenHarness 是 SDD 驱动的任务包协作协议。这个入口 skill 只在每个会话开始时建立任务包协作规则；具体阶段动作由 CLI 输出的阶段 skill 接管。

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

## 进入任务包

需要任务包时：

```
openharness task-package list
```

按输出：

- 有匹配活跃包：`openharness task-package view <task>`
- 无匹配或空：`openharness task-package new <name>`

随后执行 CLI 输出的当前阶段 skill。

## 阶段完成

每个活跃阶段完成后，用 `transition` 推进到对应完成态：

```
openharness task-package transition <task> <完成态>
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
