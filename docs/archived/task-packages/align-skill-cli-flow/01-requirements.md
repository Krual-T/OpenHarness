# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 为什么现在要做这件事，而不是以后再做？
> - 当前痛点、缺口、冲突或风险具体是什么？
> - 本轮必须交付哪些结果？这些结果的 acceptance criteria 是什么？
> - 本轮明确不做什么？哪个 counterexample 看起来相似，但仍然不属于这个任务包？
> - 目标用户是谁？核心场景是什么？单一成功指标是什么？
> - 本轮允许付出的 cost cap 是什么？
> - 有哪些不能违反的约束？
>
> **写法建议**：先写 Problem Statement（当前到底哪里痛），再写 Required Outcomes（准备交付什么），不要倒过来。模板里的每个标题都是必答题。如果你写完后仍然无法解释"为什么不是另一个问题包"，说明需求还没收敛。

## Goal
让 `using-openharness` 入口、状态 skill 和任务包模板描述的流程，与当前 CLI 的 `task-package` 状态机保持一致。

单一成功指标：agent 按 skill 中的下一步命令推进任务时，不会因为跳过 gate 状态而被 CLI 拒绝，也不会把验证计划和验证证据混写。

## Problem Statement
当前仓库经历过一次流程大改，CLI 已经形成新的状态机，但部分 skill 和模板仍保留旧指令。例如验证设计阶段提示直接 transition 到 `implementing`，实现阶段提示直接 transition 到 `verifying`；真实 CLI 要求先 transition 到 `verification_designed` 或 `implemented` 这类 gate 状态，再自动推进。

目标用户是使用 OpenHarness 的 agent 和维护者。核心场景是 agent 根据 CLI 注入的 skill 指令推进任务包。如果指令和状态机不一致，agent 会执行错误命令，或者误以为应该跳过 gate。

## Required Outcomes
1. `skills/using-openharness/SKILL.md` 说明当前 hook 触发边界和 gate 推进规则，避免入口层继续暗示 agent 自行猜状态路由。
   - acceptance criteria：入口说明中能看出 `new`、`view`、`transition` 会输出当前活跃状态指令，且 agent 应按 CLI 输出执行。
2. 状态 skill 中所有完成阶段后的 transition 命令与当前 CLI gate 状态一致。
   - acceptance criteria：`verification-designing` 指向 `verification_designed`；`implementing` 指向 `implemented`；`verifying` 保持指向 `verified`。
3. 任务包模板中的状态流和验证设计写法不再与当前 harness 冲突。
   - acceptance criteria：mechanical 流程包含 `requirements_designed[G]`；`verification_design.md` 模板只写计划，不要求在设计阶段记录已执行路径。

## Non-Goals
- 不改变 CLI 状态机、状态枚举、gate 规则或 hook 实现。
- 不新增针对性测试；这次漂移是预期的大改后文档未同步问题，本轮只做对齐。
- 不重新设计 task package 工作流。counterexample：把 mechanical 流程改成完全跳过验证设计，不属于本轮。

## Constraints
- 当前 CLI 行为是事实来源，文档向代码对齐，不反向改状态机。
- 改动范围限制在 `skills/using-openharness/` 和当前任务包文档。
- 验证方式为 qualitative：审核改动后的指令是否与 `openharness_cli/workflows.py` 和 `transition_engine.py` 一致。
- cost cap：不做广泛重写，只修会误导 agent 的流程指令。
