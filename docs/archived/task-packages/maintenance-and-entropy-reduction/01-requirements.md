# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 OpenHarness 的维护与熵减工作从 `OH-004` 父级路线图中拆成一个可执行的 focused package，让后续代理能用固定入口审计仓库漂移、选择第一波修复项，并把结果稳定写回仓库事实源。

## Problem Statement
`OH-004` 现在只剩一个活跃流: `maintenance and entropy reduction`。如果继续把这一流留在父级路线图中，后续维护工作仍然会出现三个问题：

- 仓库已经出现真实的熵增信号，但没有一个 focused package 负责把它们收敛成固定流程。当前 `uv run python skills/project-memory/scripts/check_stale.py` 与 `uv run python skills/project-memory/scripts/audit_memory.py` 已经报告多个 stale memory object 和缺失 `owner` 的元数据。
- `openharness.py check-tasks` 能校验 task package 结构与状态语义，但仓库没有定义“多久做一次维护审计、发现问题后写回哪里、何时需要再拆子包”。
- skill hub、README、per-skill 文本已经部分靠测试约束，但仍缺少一个统一维护视角，把 task package、`.project-memory/` 与 skill surface 放到同一条审计链路里。

如果这条流不单独产品化，后续清理很容易再次退化成聊天记忆、临时修补或一次性扫尾。

## Required Outcomes
1. 把 `maintenance and entropy reduction` 从 `OH-004` 拆成独立 focused package，并明确它与 `OH-004`、`OH-008`、`OH-009`、`OH-012`、`OH-015` 的依赖关系。
2. 定义维护工作的三个直接表面：task package 健康度、`.project-memory/` 新鲜度与元数据质量、live skill surface 的文本与测试漂移。
3. 定义维护轮次的触发条件、执行顺序、证据写回位置，以及何时应在 `OH-017` 内修复、何时再拆新的子 package。
4. 给出首个实施波次的推荐范围，使下一轮可以直接进入 `in_progress`，而不是重新讨论维护流到底先修什么。
5. 回写 `OH-004`，使父级路线图明确记录维护流已经由 `OH-017` 接管。

## Non-Goals
- 本轮不直接实现一个全新的 `maintenance` CLI 子命令。
- 本轮不重开运行时能力、状态语义或 taxonomy 基线设计；这些内容应复用已归档 package。
- 本轮不尝试一次性清理所有 archived package 或所有历史 memory object。

## Constraints
- 维护流必须优先复用现有能力：`openharness.py check-tasks`、`openharness.py bootstrap`、`project-memory` 脚本与现有 `pytest` 文本测试，而不是另造一套并行流程。
- 维护结果必须写回 task package 文档、必要的 `.project-memory/` YAML、以及相关 skill/docs/tests；不能只留在聊天记录里。
- `OH-017` 应保持 focused package 边界，不把新的协议扩展或大规模产品设计再次塞回维护流里。
- task package 正文继续遵守中文优先、英文结构与键名不变的仓库协议。
