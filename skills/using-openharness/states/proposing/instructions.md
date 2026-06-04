# 需求分析

## 入口分流

在开始工作前，先判断当前处于哪种场景：

| 场景 | 行为 |
|------|------|
| 任务包在非 proposing 状态 | 按 CLI hook 输出直接跳到当前状态对应指令 |
| 任务包在 proposing，`requirements.md` 已有内容 | 读取现有 requirements.md，增量收敛——续写，不是重写 |
| 任务包在 proposing，`requirements.md` 为空 | 需求编写流程（下方） |

增量收敛模式：读取现有 `requirements.md` → 检查是否有新的歧义或缺失 → 仅补充/修改变化部分 → 阶段结束检查 仍须全部通过。

## 步骤

### 1. 回述理解

从对话历史中提取已确认的结论，用 3-5 行向用户回述：

- 要解决什么问题
- 目标用户是谁
- 核心场景是什么
- 边界（做什么、不做什么）

获得用户确认后，进入需求编写。

### 2. 写入 `requirements.md`

将已确认的理解写入 `requirements.md`，包含模板要求的所有章节。

**核心要求：这份文档是需求阶段的唯一交付物，必须做到自包含 handoff。** 任何一个不了解本轮对话的人（或 AI）拿到这份文档，不翻聊天记录、不追问，就应该能理解：

- 当前矛盾是什么、为什么现在做（背景 + 问题陈述）
- 做完以后什么事实成立（目标 + 成功指标）
- 怎样判断做完还是没做完（验收标准）
- 边界在哪（非目标 + 约束）

不能依赖"读者看过聊天记录"来补全信息。如果写完发现还需要口头解释别人才能懂，说明文档没写完。

写完后告知用户文件路径，让用户直接在 IDE 中审阅。**不得将全文贴到聊天里。**

### 3. 需求文档确认停点

用户审阅 `requirements.md` 完毕并确认后，才继续。用户要求修改则回到步骤 2 调整。

### 4. 确认工作流分叉字段

向下方"工作流分叉字段"章节的三条字段逐一解释含义、给出建议值及理由，**三条字段一并陈述，一次性获得用户确认**后写入 `task-info.yaml`。

### 5. 自检阶段结束检查

逐项确认下方"阶段结束检查"章节的 9 个问题都能明确回答。

## 工作流分叉字段

阶段结束检查 第 7-9 项依赖以下三条字段，**必须在自检阶段结束检查前确认完毕**。三条字段向用户一并解释含义、给出建议值及理由，一次性获得用户确认后写入 `task-info.yaml`。

| 字段 | 可选值 | 说明 |
|------|-------|------|
| `collaboration.task_type` | `mechanical` / `standard development` / `protocol/architecture` | `mechanical` — 格式、命名、路径等低判断成本改动，跳过 overview/detailed；`standard development` — 常规功能、修复，需要设计但非架构级；`protocol/architecture` — 影响长期协议、skill 行为、公共接口，需逐项设计确认 |
| `collaboration.design_review_mode` | `stepwise` / `auto` | `stepwise` — 每个设计点逐个确认；`auto` — agent 自主推进但记录关键决策。`mechanical` 不需要此字段 |
| `verification.verify_by` | `unit_test` / `qualitative` / `rwp` | `unit_test` — pytest 验证可明确断言的逻辑；`qualitative` — 人工/子 agent 审核文档、协议、skill 行为；`rwp` — 真实世界场景手动验证 |

- `protocol/architecture` 默认建议 `stepwise`；`standard development` 默认建议 `stepwise`，用户可选 `auto`
- 混合任务可设主 `verify_by`，其余在 `verification-design.md` 补充
- 后续阶段只消费这三项字段；如果后续发现分类错误，应回退需求阶段修正

## 阶段结束检查

离开需求阶段前，agent 必须逐条自检下面 9 个问题。**自检通过后，将 9 条结论向用户逐条陈述，获得用户确认后才可执行 transition。** 用户否定任一条 → 回到对应步骤修正，重新过阶段结束检查。

任何一条 agent 自己答不上来 → **阻塞**，不得进入 `overview-design.md`。

1. 目标用户是谁？
2. 核心场景是什么？
3. 单一成功指标是什么？
4. 哪些验收标准会决定本轮是否算完成？
5. 哪些反例必须被排除？
6. 哪些限制一旦被突破，这就不再是同一个 task package？
7. task_type（`mechanical` / `standard development` / `protocol/architecture`）是否已确认并写入 `task-info.yaml`？
8. design_review_mode（`stepwise` / `auto`）是否已确认并写入 `task-info.yaml.collaboration.design_review_mode`？
9. verify_by（`unit_test` / `qualitative` / `rwp`）是否已确定并写入 `task-info.yaml.verification.verify_by`？
10. **Handoff 自检**：把这份 `requirements.md` 交给一个不了解本轮对话的人，他能否仅凭文档就理解当前矛盾、目标、边界和验收标准？

如果这些问题还答不上来，**阻塞**。不要进入 `overview-design.md`。

## 要点

- 模板文件位于 `skills/using-openharness/references/templates/task-package.requirements.md`
- 需求阶段的结束标志是 `requirements.md` 足够坚实（阶段结束检查 全部能回答），不是文字变得更长
- **`requirements.md` 是需求阶段的唯一交付物，必须自包含**：零上下文读者能仅凭文档理解问题、目标、边界和验收标准，不需要翻聊天记录
- 在任务包里记录讨论结论，不要只留在聊天里
- 需求收敛后，必须确认并写入 `task-info.yaml` 的三项工作流分叉字段：`collaboration.task_type`、`collaboration.design_review_mode`、`verification.verify_by`
- 后续阶段只消费这三项字段；如果后续发现分类错误，应回退需求阶段修正
- 目标不要写成抽象价值词；应该能回答"做完以后什么事实会成立"
- 问题陈述至少要写出一个已经存在的矛盾，而不是只写未来愿景
- 必须交付的结果中每一项，后续都应该能在 `verification-design.md` 里找到对应验证
- 非目标至少写一个反例
- 约束写协议边界、兼容性条件、依赖限制和 cost cap；如果某个限制被突破就会变成另一个 task package，也写在这里

## 与相邻文档的边界

- 这里写"要解决什么问题"，不写"具体怎么设计"
- 可以写约束，但不要在这里展开模块边界、文件改动和迁移顺序
- 如果一段内容已经在比较方案优劣、定义系统边界或安排实现步骤，它更应该去 `overview-design.md` 或 `detailed-design.md`

## 常见失败模式

- 把 Goal 写成空泛口号，例如"提升质量""优化体验"
- 只列功能愿望，不说明当前问题
- Non-Goals 缺失，导致范围自然膨胀
- 必须交付的结果不可验证，只剩主观表述
- 把设计方案提前写进需求，导致后续没有真正的探索空间

## 反合理化

| 借口 | 为什么不成立 |
|------|-------------|
| "需求已经很清楚了，直接开始设计吧" | 清楚到能写下来 ≠ 实际上写下来了。没写进 `requirements.md` 的需求，在实现阶段会被遗忘或曲解。 |
| "用户只问了一个小功能" | 小功能也可能有隐式假设。不写下目标用户、场景和反例，范围就会在实现时自然膨胀。 |
| "用户说了要什么，不需要再分析" | 用户说的 ≠ 需求。需求需要转化为可验证的验收标准，否则验证阶段无法判断完成。 |
| "先写代码，需求后面补" | 后面不会补的。需求文档不是负担——它是你和未来维护者之间的契约。 |
| "这次改动很小，不需要完整需求分析" | 改动小 ≠ 边界清晰。边界模糊的小改动最容易在实现时引发争议。 |
