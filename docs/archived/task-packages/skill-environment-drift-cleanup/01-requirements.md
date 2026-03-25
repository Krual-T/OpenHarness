# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 skills 中明显偏离当前仓库环境的指令收敛到可执行、可理解、与本仓库协议一致的状态，减少后续执行时临场改写和误判成本。

## Problem Statement
当前部分 skills 仍然引用旧环境或外部仓库里的约定，例如 `CLAUDE.md`、`TodoWrite`、`Task(...)`、固定 reviewer subagent type，以及与本仓库 `uv` 约定不一致的 Python 工作流命令。这些内容未必会立刻触发测试失败，但会持续降低 skill 的可信度，也会让执行者在真正使用时被迫临时绕开或重解释规则。

这类漂移问题一旦扩散，skills 就会逐步从“可执行的仓库协议”退化成“只能参考的长文档”，影响后续 skill routing、任务包写回和验证路径的一致性。

## Target User And Scenario
- 目标用户是进入 `openharness` 仓库执行任务的协作者，包括主智能体和后续维护这些 skill 的人。
- 核心场景是协作者按照 skill 指令执行任务时，不需要再自己识别“这是不是旧仓库残留”或“这条命令在当前环境到底能不能跑”。

## Success Metric
- 在本轮完成后，受影响 skill 的正文与示例中不再包含会直接误导当前仓库执行的旧入口名、不可用工具名或与 `uv run` 约定冲突的默认工作流。

## Required Outcomes
1. 梳理所有受影响的 skill 文件，列出每一处环境漂移或能力假设不匹配的问题。
2. 将这些问题按类型分类，例如旧入口约定、工具能力假设、命令约定冲突、外部仓库残留措辞。
3. 为每一类问题给出明确处理规则，决定是删除、替换为当前约定，还是降级为非强制示例。
4. 完成修改后，skills 中不应再出现会直接误导当前仓库执行的旧环境依赖。

## Acceptance Criteria
1. `using-git-worktrees` 不再引用 `CLAUDE.md`、`pip install`、`poetry install` 这类与当前仓库默认协议不匹配的入口或安装流程。
2. `subagent-driven-development`、`dispatching-parallel-agents` 等文档中不再出现 `TodoWrite`、`Task(...)`、固定 reviewer subagent type 等当前环境不可用或不成立的能力假设。
3. 如果某条能力只是通用背景说明而不是本仓库强约束，文档会明确降级为“可选做法”或直接移除，不再写成必须动作。
4. 至少通过一次 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认任务包协议仍然有效。

## Non-Goals
- 不在这项任务里重做整个 skill 架构分层。
- 不顺带改写所有措辞风格或压缩所有长文档。
- 不把设计协议、阶段制度和 skill 拆分策略一并处理，那属于独立任务。

## Constraints
- 必须以 `AGENTS.md` 和 `using-openharness` 为当前仓库事实来源，不再延续外部仓库约定。
- task package 文档正文保持中文，章节标题、状态值、路径和 YAML 键名保持英文。
- 本轮以 skill 文档与相关引用资料为主要修改对象，不应借机扩大到无关代码重构。
- 反例：如果只是把旧术语换个说法，但仍然保留不可用工具或错误执行路径，这不算完成。

## Effort Boundary
- 本轮只处理仓库内已有 skill 文档、必要的引用模板和与之直接相关的任务包文档。
- 不新增新的运行时 helper、外部脚本或额外校验器；防回归约束以现有 harness 校验和文档边界收敛为主。

## Counterexample
- 如果文档只是把 `TodoWrite` 改成“记录任务清单”，但仍要求执行者依赖不存在的自动任务面板，这仍然属于环境漂移，没有达到完成标准。
