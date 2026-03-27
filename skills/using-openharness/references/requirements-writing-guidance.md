# Requirements Writing Guidance

本说明只负责 `01-requirements.md`。

它不负责告诉你当前该不该进入需求阶段，也不负责替代需求收敛本身；这些事情由 `brainstorming` 负责。

## Purpose

定义这轮任务为什么存在、要解决什么问题、成功到底意味着什么。

## Questions This Document Must Answer

- 为什么现在要做这件事，而不是以后再做？
- 当前痛点、缺口、冲突或风险具体是什么？
- 本轮必须交付哪些结果？
- 这些结果的 `acceptance criteria` 是什么？
- 本轮明确不做什么？
- 有哪些不能违反的约束？
- 目标用户是谁？核心场景是什么？
- 单一成功指标是什么？
- 本轮允许付出的 `cost cap` 是什么？
- 哪个 `counterexample` 看起来相似，但仍然不属于这个任务包？

## Section Mapping

- `Goal`
  - 写目标结果和单一成功指标。
  - 不要写成抽象价值词；应该能回答“做完以后什么事实会成立”。
- `Problem Statement`
  - 写目标用户、核心场景、当前痛点、为什么现在要做。
  - 至少要写出一个已经存在的矛盾，而不是只写未来愿景。
- `Required Outcomes`
  - 写本轮必须交付的结果，以及每项结果最小的 `acceptance criteria`。
  - 这里的每一项，后续都应该能在 `04-verification.md` 里找到对应验证。
- `Non-Goals`
  - 写明确排除项。
  - 至少写一个 `counterexample`，说明“看起来相关但不属于本轮”的情况。
- `Constraints`
  - 写协议边界、兼容性条件、依赖限制和 `cost cap`。
  - 如果某个限制被突破就会变成另一个 task package，也写在这里。

## Boundary With Adjacent Documents

- 这里写“要解决什么问题”，不写“具体怎么设计”。
- 可以写约束，但不要在这里展开模块边界、文件改动和迁移顺序。
- 如果一段内容已经在比较方案优劣、定义系统边界或安排实现步骤，它更应该去 `02-overview-design.md` 或 `03-detailed-design.md`。

## Common Failure Modes

- 把 Goal 写成空泛口号，例如“提升质量”“优化体验”。
- 只列功能愿望，不说明当前问题。
- Non-Goals 缺失，导致范围自然膨胀。
- Required Outcomes 不可验证，只剩主观表述。
- 把设计方案提前写进需求，导致后续没有真正的探索空间。

## Minimum Acceptable Shape

- `Goal` 至少写清希望达成的真实结果，并且这个结果不能只包含“提升”“优化”“增强”这类抽象词。
- `Problem Statement` 至少写清当前矛盾、目标用户、核心场景和为什么现在要做。
- `Required Outcomes` 至少按可检查粒度列出必须交付物，并为核心结果写出最小 `acceptance criteria`。
- `Non-Goals` 至少写出明确排除项，并包含一个 `counterexample`。
- `Constraints` 至少写清当前不能突破的协议或兼容性边界，以及本轮 `cost cap`。

## Exit Check

离开需求阶段前，至少能明确回答下面 6 个问题：

- 目标用户是谁？
- 核心场景是什么？
- 单一成功指标是什么？
- 哪些 `acceptance criteria` 会决定本轮是否算完成？
- 哪个 `counterexample` 必须被排除？
- 哪个限制一旦被突破，这就不再是同一个 task package？

如果这 6 个问题还答不上来，就不要进入 `02-overview-design.md`。

## How To Use The Template

- 模板里的每个标题都应被视为必答题，而不是可选灵感。
- 先把 Problem Statement 写扎实，再列 Outcomes；不要倒过来。
- 先写“当前到底哪里痛”，再写“准备交付什么”；不要反过来从愿望倒推问题。
- 如果你写完后仍然无法解释“为什么不是另一个问题包”，说明需求还没收敛。
