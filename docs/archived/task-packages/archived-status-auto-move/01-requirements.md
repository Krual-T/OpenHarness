# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
当 active task package 的 `STATUS.yaml` 已经声明 `status: archived` 时，OpenHarness 自动把它移动到 archived 根目录，并保持包内路径引用一致。

单一成功指标：`uv run openharness check-tasks` 面对 active 根目录里的 `status: archived` 包时，不再报位置错误，而是自动移动并通过协议校验。

## Problem Statement
目标用户是维护 OpenHarness task package 的人和 agent。核心场景是任务收尾时已经把 `STATUS.yaml` 写成 `archived`，但目录仍留在 `docs/task-packages/<task>/`。当前 CLI 会把这种状态识别为非法位置并报错，导致“状态已经归档”和“目录尚未归档”之间出现人为同步负担。

现在要做，是因为归档语义已经明确为“包不再 active”，而目录位置是这个语义的一部分；如果状态能表达归档，CLI 应该能把位置规范化，而不是只把这个矛盾留给维护者手动修。

## Required Outcomes
1. `discover_task_packages` 或等价 CLI 读取路径能自动处理 active 根目录中的 `status: archived` 包。
   - Acceptance criteria: 测试能构造 active 根目录里的 archived 包，执行 `cmd_check_tasks` 后 active 路径消失、archived 路径存在，且返回码为 0。
2. 自动移动沿用现有归档拷贝/路径重写逻辑。
   - Acceptance criteria: 包内 `docs/task-packages/<task>/...` 引用会改成 `docs/archived/task-packages/<task>/...`。
3. 现有显式 `transition <task> archived` 路径继续可用。
   - Acceptance criteria: 既有归档 transition 测试仍通过。

## Non-Goals
- 不把 `verify` 改成验证通过后自动归档；验证仍只负责产出 artifact 和回写 `verification.last_run_*`。
- 不放宽 `transition <task> archived` 的 passed artifact / fingerprint 前置条件。
- Counterexample: 一个处于 `verifying` 且验证刚通过的包，看起来“快要归档”，但本轮不会让它因为 `verify` 成功而自动移动。

## Constraints
- 不能破坏现有 archived 包必须位于 `docs/archived/task-packages` 的校验语义。
- 自动移动必须是事务式或复用已有事务式归档实现，避免失败时同时丢失 active 和 archived 两份。
- 成本上限是一轮小型 CLI 行为变更：优先新增测试和复用现有 helper，不重做生命周期状态机。
