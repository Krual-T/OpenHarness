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
让 live 示例文档和 CLI 回归测试跟当前 OpenHarness 协议一致。单一成功指标：相关测试命令通过，且 live 示例不再指导用户使用已废弃的状态文件或命令。

## Problem Statement
当前 `AGENTS.example.md` 仍保留旧协议引用，例如 `STATUS.yaml`、`openharness bootstrap`、`manifest.yaml` 和 `systematic-debugging`。这个文件是新仓库可复制的 live 示例，漂移会把错误协议传播到新项目。

同时，`task-package view` 已成为入口 skill 推荐的当前任务进入方式，gate 失败不落盘也是状态可靠性的关键行为，但两者缺少聚焦回归测试。

## Required Outcomes
1. `AGENTS.example.md` 使用当前协议词汇和命令。
   - acceptance criteria: 文件中不再出现 `STATUS.yaml`、`openharness bootstrap`、`manifest.yaml`、`systematic-debugging`。
   - acceptance criteria: 文件中指向 `task-info.yaml`、`openharness task-package list`、`openharness task-package view <task>` 和当前任务包文件结构。
2. `task-package view` 有 CLI 回归测试。
   - acceptance criteria: 测试构造一个活跃任务包，执行 `openharness task-package view <task>` 后能看到任务摘要和注入的状态 skill 内容。
3. gate 失败不落盘有回归测试。
   - acceptance criteria: 从 `proposing` transition 到 `requirements_designed` 且缺少 `collaboration.task_type` / `verification.verify_by` 时命令失败，并保持 `task-info.yaml.status == proposing`。

## Non-Goals
- 不调整 archived 历史任务包中的旧协议引用。
- 不重新设计 verifying/implementing 的 evidence 语义。
- 不改 `AGENTS.md` 仓库级约定。
- counterexample: 如果发现其他 skill 文案还有可优化处，但不影响本轮三个交付项，应单独开后续任务包。

## Constraints
- 仓库 Python 命令使用 `uv run ...`。
- 只修改用户要求范围内的 live 示例和测试，保持实现代码最小化。
- 测试应使用现有 `CliRunner`、临时仓库和 task package helpers，不引入新依赖。
- cost cap: 单个聚焦提交完成。
