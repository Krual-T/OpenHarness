# 需求

## 背景

OpenHarness 刚把旧 `verification-designing` 阶段重构为 `planning` 阶段，并引入 `plan.md` 作为实现计划与验证设计的承载文档。当前 `planning/instructions.md` 虽然已经使用 `plan.md`，但方法论仍不够准确：它在计划阶段再次校验任务类型，并把 `standard`、`structural` 的前置文档读取规则硬编码在同一段里。

计划阶段已经是 workflow 分流后的结果。能进入 `planning`，说明需求阶段已经确定了任务类型；本阶段应该专注于把需求和可能存在的设计文档转成可执行计划，而不是重新判断任务是否该进入计划。

## 问题陈述

使用 OpenHarness skill 的开发者和智能体在进入 `planning` 阶段时，需要一份清楚的写作指令，知道应读取哪些输入、计划允许写到什么深度、如何把工作拆成可执行步骤。

当前 `planning/instructions.md` 的问题是：

1. 它在计划阶段展示“校验任务类型”，容易让智能体把阶段职责倒退到需求分流。
2. 它没有利用已有 Jinja 上下文按 `task_type` 渲染前置文档说明，导致 `standard` 和 `structural` 看到同一套不够精确的说明。
3. 它没有充分吸收主流 plan mode 的共性结构，例如目标与上下文、输入文档、文件修改计划、进度记录、决策发现和完成判定。

## 目标

完成后，`planning/instructions.md` 应当表达以下事实：

1. `plan.md` 是一份实现计划，不是新的任务类型判断阶段。
2. `standard` 的 `plan.md` 可以承担轻量实现设计：从需求推出必要的文件落点、执行步骤和验证设计，但不展开成架构设计。
3. `structural` 的 `plan.md` 只消费 `overview-design.md` 和 `detailed-design.md` 的设计结论，把它们转成执行步骤和验证设计；如果设计不成立，应回退设计阶段。
4. 指令使用 Jinja 按 `task_type` 渲染前置读取内容和计划深度说明。
5. 计划写作方法吸收 Codex、Claude、Cursor、OpenSpec、Superpowers 等 plan 模式的共性：可审阅、可恢复、可执行、可验证。

## 交付物

1. 更新 `skills/using-openharness/states/planning/instructions.md`，移除计划阶段的任务类型校验，改为按 `task_type` 渲染输入文档与计划深度。
2. 调整计划阶段的写作结构，覆盖目标与上下文、输入文档、实施步骤、文件修改计划、验证设计、进度记录、决策与发现、风险接受和完成判定。
3. 更新或新增测试，防止 planning 指令重新出现“校验任务类型”这类阶段边界错误，并确认核心章节存在。

## 非目标

本轮不改 workflow 状态机、不改 `plan.md` 文件名、不新增第二套 plan 模板。比如，为 `standard` 和 `structural` 分别创建两份模板，不属于本任务。

本轮也不重新设计 `overview-design.md` 或 `detailed-design.md` 的内容，只修正 planning 阶段如何消费这些文档。

## 约束

1. 只能修正 planning 阶段的方法论和必要测试，不扩大到新一轮工作流重构。
2. `plan.md` 模板保持一套；差异通过 Jinja 渲染的阶段指令表达。
3. `mechanical` 不进入 planning，因此 planning 指令不需要为 mechanical 写执行路径。
4. 修改后文字要直接指导执行计划写作，避免把 plan 写成新的形式主义文档。

## 自检

- [x] 不了解本轮对话的人，读完「背景」和「问题陈述」，能知道当前需要修正 planning 指令。
- [x] 「目标」和「交付物」能判断做完还是没做完。
- [x] 「非目标」排除了 workflow 重构和双模板方案。
- [x] 「约束」写清了 Jinja 渲染、一套模板和阶段边界。
