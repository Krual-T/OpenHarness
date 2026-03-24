# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 OpenHarness 的任务入口从“仓库里有状态机但人感知不到”收敛成“阶段清楚、下一步清楚、该建 task package 的时机也清楚”的使用体验。

单一成功指标：当 agent 或人运行入口流程时，能够在一次输出里明确看到当前 stage、下一 stage 与建议下一步；当当前工作尚无 package 且 brainstorming 已经结束时，agent 会先自动创建 package 再进入下一阶段。

## Problem Statement
当前流程的主要摩擦有三点：

- 阶段信息主要埋在 `STATUS.yaml.status` 和技能文字里，人需要自己推断“现在做到哪里了、下一步是什么”。
- 入口 CLI 只有列包和列状态，没有把阶段含义、下一合法阶段和建议动作直接输出出来，因此 agent 即使运行了 `bootstrap`，也很容易只把它当作包列表。
- 新任务虽然有 `new-task`，但自动化创建的最佳时机没有被写清楚，而且创建时需要显式提供 `task_id`，不利于在 brainstorming 结束后顺滑进入下一阶段。

如果这些问题不收敛，OpenHarness 会继续表现为“协议比体验更清楚”，人类协作者仍然要靠聊天记忆而不是仓库输出来判断流程状态。

## Required Outcomes
1. `openharness.py bootstrap` 的文本输出和 JSON 输出都要显式给出当前 stage、下一 stage 和建议下一步，而不是只列状态名。
2. `openharness.py new-task` 要支持在不手工指定 `task_id` 的情况下自动分配下一个稳定编号，便于 agent 在 brainstorming 结束后直接落包。
3. `using-openharness` 与 `brainstorming` 要把阶段播报与建包时机写成清晰规则：没有 package 时，不在最初模糊讨论时建包，而是在 brainstorming 结束、准备进入 exploration 前自动建包。
4. 现有老命令用法要继续可用，不能为了新入口把现有脚本调用全部打断。
5. 仓库测试要覆盖新的 CLI 行为和技能文案约束。

## Non-Goals
- 本轮不重做整个状态机，也不引入新的 workflow status。
- 本轮不把“进入实现前必须人工批准”设成新的强制协议，这属于单独的审核闸门议题。
- 本轮不把 task package 的所有创建参数都变成交互式提问式 CLI。
- 本轮不重构 archive、verification artifact 或 runtime capability 流程。

## Constraints
- 必须保持 `docs/task-packages/<task>/` 与 `docs/archived/task-packages/<task>/` 的协议不变。
- 必须保留现有 `new-task task_name task_id title` 这种可脚本化用法，新增能力只能向后兼容扩展。
- 需要同步更新 task package、协议说明与测试，避免“代码变了但 skill 还教旧流程”。
- 文档正文继续以中文为主，章节标题、状态值、YAML 键名、命令与路径保持英文。
- 由于 OpenHarness 被当作仓库入口协议使用，本轮改动必须优先提升可见性和可预期性，而不是增加新的隐式判断。
