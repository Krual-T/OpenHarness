---
name: brainstorming
description: 在开始任何创造性工作之前使用——创建功能、构建组件、添加功能或修改行为。探索用户意图、需求和设计。
triggers_on: [proposing]
requires: [using-openharness]
next_skills: [exploring-solution-space]
---

# 需求分析

## 何时使用

任务需求不明确、范围未收敛、需要先写清楚设计再动手时。

## 步骤

1. 阅读当前任务包、相关文件、文档和最近提交，了解项目上下文
2. 仅在需求仍有关键歧义时向用户提问，一次只问一个问题
3. 提出 2-3 个可行方案，包含取舍和明确推荐
4. 收集并写入 `01-requirements.md`：目标用户、核心场景、成功指标、边界、约束、验收标准、至少一个反例
5. 用产品视角挑战需求：用户是谁、场景是什么、为什么现在做、不做会怎样
6. 自检：`01-requirements.md` 能否回答 `references/requirements-writing-guidance.md` 中定义的问题
7. 需求足够具体后，交给 `exploring-solution-space` 继续

## 要点

- 一次一个问题，不要连珠炮式提问
- 需求要可执行，不要装饰性描述
- 不要因为某个方案看起来明显就跳过替代方案
- 在任务包里记录讨论结论，不要只留在聊天里
- 需求阶段的结束标志是 `01-requirements.md` 足够坚实，不是文字变得更长
- 模板文件位于 `using-openharness/references/templates/01-requirements.md`
- 参考 `references/requirements-writing-guidance.md`
- 需求收敛后，提议一种任务分类（`mechanical` / `standard development` / `protocol/architecture`），等用户确认后写入 `STATUS.yaml.collaboration.task_type`

## 反合理化

| 借口 | 为什么不成立 |
|------|-------------|
| "需求已经很清楚了，直接开始设计吧" | 清楚到能写下来 ≠ 实际上写下来了。没写进 `01-requirements.md` 的需求，在实现阶段会被遗忘或曲解。 |
| "用户只问了一个小功能" | 小功能也可能有隐式假设。不写下目标用户、场景和 counterexample，范围就会在实现时自然膨胀。 |
| "先写代码，需求后面补" | 后面不会补的。需求文档不是负担——它是你和未来维护者之间的契约。 |
