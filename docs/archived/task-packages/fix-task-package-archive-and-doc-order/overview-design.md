# Overview Design

## System Boundary

本轮覆盖 `openharness_cli` 的任务包归档、任务包创建、状态推进时的阶段文档创建，以及对应模板、状态 skill 文案和测试。历史已归档任务包不做文件名迁移。

## Proposed Structure

推荐结构是保留现有 workflow 模型，但把“完成某 gate 后必需的文件”和“当前活跃阶段需要预创建的工作文件”分开：

- `TaskPackageDocument` 定义无前缀语义文件名。
- `Workflow.required_files()` 继续表达验证门禁所需文件。
- `Workflow.scaffold_files()` 用 `working_files` 在进入活跃阶段时预创建当前阶段要写的文件。
- `create_task_package()` 只创建 `proposing` 阶段需要的文件。
- `execute_transition()` 在成功进入新活跃阶段后补齐该阶段文件；`verified` gate 直接尝试归档，失败时不持久化中间状态。

## Key Flows

新建任务包时，CLI 根据默认 workflow 为 `proposing` 创建 `README.md`、`task-info.yaml`、`requirements.md`。推进到后续活跃阶段时，CLI 先校验 gate，再写状态并补齐当前阶段文件。推进到 `verified` 时，CLI 检查证据后直接执行归档；如果目标已存在，源任务包保持原状态。

## Stage Gates

进入详细设计前必须确认：

- 文件名不表达阶段序号；`Workflow.working_files` 表达当前活跃阶段应创建哪份文档。
- 新建包不提前创建 overview、detailed、verification、evidence。
- 归档失败不应留下已改状态但未移动的任务包。
- 不在 skill 中硬编码阶段序号。

## Trade-offs

采用无前缀语义文件名，而不是固定全局编号。代价是单纯按文件名排序无法表达完整 workflow 顺序；好处是 skill 不需要硬编码 `04-verification-design.md` 这类顺序细节，顺序统一由 workflow 状态决定。

拒绝的方案：保留带数字前缀的文件名。这个方案会把顺序写死进 skill 和模板，不符合“根据 workflow 动态生成顺序”的目标。

## Recommended Diagrams

不需要额外 PlantUML。状态流已经在 `task-info.yaml` 模板中表达，本轮变化集中在文件创建时机和归档原子性。

## Overview Reflection

挑战：是否应通过文件名前缀表达顺序。结论是拒绝。用户明确指出 skill 中硬编码 `04-verification-design.md` 不合理，因此新 CLI、模板和测试都使用无前缀语义文件名；顺序由 workflow 决定。
