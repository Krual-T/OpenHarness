---
name: brainstorming
description: 当任务状态是 proposing（需求未收敛、范围未明确）时使用
---

# 需求分析

## 何时使用

任务需求不明确、范围未收敛、需要先写清楚需求再动手时。本 skill 由 CLI 在 transition 到 `proposing` 或 `task-package new` 时自动注入。

## 入口分流

在开始工作前，先判断当前处于哪种场景：

| 场景 | 行为 |
|------|------|
| 任务包在非 proposing 状态 | 按 CLI hook 输出直接跳到当前状态对应指令 |
| 任务包在 proposing，`01-requirements.md` 已有内容 | 读取现有 01，增量收敛——续写，不是重写 |
| 任务包在 proposing，`01-requirements.md` 为空 | 完整 brainstorming 流程（下方） |

增量收敛模式：读取现有 `01-requirements.md` → 检查是否有新的歧义或缺失 → 仅补充/修改变化部分 → Exit Check 仍须全部通过。

## 步骤

### 0. 判断任务清晰度

先判断当前任务属于哪种情况：

- **清晰任务**：改动范围明确、无架构决策、用户的指令可以直接转化为验收标准 → 跳至**快通道**
- **模糊任务**：问题开放、目标未明确、涉及取舍判断或跨模块影响 → 继续**完整流程**

### 完整流程

1. **阅读上下文**：当前任务包、相关文件、文档和最近提交，了解项目现状
2. **挑战前提**：在提出任何方案之前，先挑战问题本身
   - 为什么现在做这件事，而不是以后？
   - 不做会怎样？这真的是问题，还是问题的症状？
   - 当前矛盾具体是什么？（不能只写"体验不好"）
3. **收集关键信息**：仅在仍有关键歧义时向用户提问。一次一个问题还是批量取决于歧义数量——不要在已经清楚的事情上反复确认
4. **提出方案**：方案数量取决于不确定性
   - 不确定性低 → 一个推荐方案 + 至少一个被拒绝的方案及其理由
   - 不确定性高 → 2-3 个方案，含取舍分析和明确推荐
   - 不要因为某个方案看起来明显就跳过替代方案
5. **写入 `01-requirements.md`**：目标用户、核心场景、成功指标、边界、约束、验收标准、至少一个反例
6. **自检 Exit Check**：逐项确认下面 7 个问题都能明确回答

### 快通道

清晰任务跳过完整流程的步骤 2-4，直接：

- 用产品视角快速确认：用户是谁、为什么现在做（3-5 行即可）
- 写入 `01-requirements.md`
- 自检 Exit Check

## Exit Check

离开需求阶段前，**必须**能明确回答下面 7 个问题（任何一条答不上来 → 阻塞，使用 `openharness task-package transition <task> requirements_designed` 前必须全部通过）：

1. 目标用户是谁？
2. 核心场景是什么？
3. 单一成功指标是什么？
4. 哪些 acceptance criteria 会决定本轮是否算完成？
5. 哪个 counterexample 必须被排除？
6. 哪个限制一旦被突破，这就不再是同一个 task package？
7. task_type（`mechanical` / `standard development` / `protocol/architecture`）是否已确认并写入 `STATUS.yaml`？
8. verify_by（`unit_test` / `qualitative` / `rwp`）是否已确定并写入 `STATUS.yaml.verification.verify_by`？

如果这些问题还答不上来，**阻塞**。不要进入 `02-overview-design.md`。

## 要点

- 模板文件位于 `skills/using-openharness/references/templates/task-package.01-requirements.md`
- 需求阶段的结束标志是 `01-requirements.md` 足够坚实（Exit Check 全部能回答），不是文字变得更长
- 在任务包里记录讨论结论，不要只留在聊天里
- 需求收敛后，提议一种任务分类（`mechanical` / `standard development` / `protocol/architecture`），等用户确认后写入 `STATUS.yaml.collaboration.task_type`
- Goal 不要写成抽象价值词；应该能回答"做完以后什么事实会成立"
- Problem Statement 至少要写出一个已经存在的矛盾，而不是只写未来愿景
- Required Outcomes 的每一项，后续都应该能在 `verification_design.md` 里找到对应验证
- Non-Goals 至少写一个 counterexample
- Constraints 写协议边界、兼容性条件、依赖限制和 cost cap；如果某个限制被突破就会变成另一个 task package，也写在这里

## 与相邻文档的边界

- 这里写"要解决什么问题"，不写"具体怎么设计"
- 可以写约束，但不要在这里展开模块边界、文件改动和迁移顺序
- 如果一段内容已经在比较方案优劣、定义系统边界或安排实现步骤，它更应该去 `02-overview-design.md` 或 `03-detailed-design.md`

## 常见失败模式

- 把 Goal 写成空泛口号，例如"提升质量""优化体验"
- 只列功能愿望，不说明当前问题
- Non-Goals 缺失，导致范围自然膨胀
- Required Outcomes 不可验证，只剩主观表述
- 把设计方案提前写进需求，导致后续没有真正的探索空间

## 反合理化

| 借口 | 为什么不成立 |
|------|-------------|
| "需求已经很清楚了，直接开始设计吧" | 清楚到能写下来 ≠ 实际上写下来了。没写进 `01-requirements.md` 的需求，在实现阶段会被遗忘或曲解。 |
| "用户只问了一个小功能" | 小功能也可能有隐式假设。不写下目标用户、场景和 counterexample，范围就会在实现时自然膨胀。 |
| "用户说了要什么，不需要再分析" | 用户说的 ≠ 需求。需求需要转化为可验证的验收标准，否则验证阶段无法判断完成。 |
| "先写代码，需求后面补" | 后面不会补的。需求文档不是负担——它是你和未来维护者之间的契约。 |
| "这次改动很小，不需要完整需求分析" | 如果确实属于清晰任务，走快通道即可。但"改动小"不是跳过需求文档的理由——边界模糊的小改动最容易在实现时引发争议。 |
