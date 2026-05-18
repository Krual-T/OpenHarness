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
修复 `openharness task-package transition <task> verified` 在自动归档成功后打印错误信息的问题。

单一成功指标：当 `verified` gate 自动推进到 `archived` 并移动任务包后，CLI 输出 `Archived task package: ...`，不再输出 `already in <旧状态>`。

## Problem Statement
当前 `execute_transition()` 在归档成功时返回 `(None, [])`。命令层只在用户显式输入 `archived` 时把这个返回值解释为归档成功；如果用户输入的是 `verified`，但 `verified` gate 自动推进到 `archived`，命令层会把同一个返回值误判为无更新，并打印 `already in <旧状态>`。

目标用户是执行 OpenHarness 任务包流转的 agent 和维护者。核心场景是验证完成后运行 `openharness task-package transition <task> verified`。错误输出会让使用者以为归档没有发生，虽然实际目录已经移动。

## Required Outcomes
1. CLI 能识别“自动归档成功”这个结果。
   - acceptance criteria：`transition <task> verified` 自动归档后输出 `Archived task package`，且任务包移动到 archived root。
2. 直接归档路径不退化。
   - acceptance criteria：`transition <task> archived` 仍输出 `Archived task package`。
3. 真正 no-op 的场景仍能保留已有输出语义。
   - acceptance criteria：目标状态等于当前状态时仍可输出 already in。

## Non-Goals
- 不重做整个 transition 状态机。
- 不改变 gate 规则、归档目录结构或验证门禁。
- 不调整 `verified` 自动归档这一产品语义。counterexample：把 `verified` 改成可停留状态，不属于本轮。

## Constraints
- 保持现有 CLI 文案风格，优先最小改动。
- 测试使用现有 Typer CLI runner，不引入新依赖。
- Python 命令使用 `uv run ...`。
