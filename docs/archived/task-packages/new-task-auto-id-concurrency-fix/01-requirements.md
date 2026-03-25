# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 `openharness.py new-task --auto-id` 变成可并发使用的仓库入口能力。多个 agent 或终端同时创建 task package 时，系统仍然要稳定地产生唯一编号，并且保证最终落盘结果不出现重复 `task_id` 或半成功半失败却未被显式暴露的状态。

本轮单一成功指标是：在同一仓库里并行发起多次 `new-task --auto-id`，新创建的 package 最终都拥有唯一 `task_id`，而且随后的 `check-tasks` 不会报重复编号。

## Problem Statement
当前实现把 `--auto-id` 路径拆成了两个无保护步骤：

1. `cmd_new_task()` 先调用 `allocate_next_task_id()` 扫描现有 package，推导下一个编号。
2. 然后再调用 `create_task_package()` 按该编号写入新目录和模板文件。

这是一种典型的先检查再执行（time-of-check / time-of-use）竞争窗口。两个并发进程都可能在创建前看见相同的最大编号，于是分别拿到同一个新 `task_id`。由于 task package 目录名来自 `task_name` 而不是 `task_id`，只要任务名不同，两个进程都能各自建目录成功，重复编号直到后续 `check-tasks` 才会被动发现。

这会直接破坏仓库对 task package 的唯一标识假设，也会让自动 intake 流程在高并发场景下产生脏状态。

## Required Outcomes
1. `new-task --auto-id` 必须把“读取当前编号状态”“选择下一个编号”“创建 task package”收敛为同一段仓库级原子流程，避免并行请求拿到相同编号。
2. 修复后的主路径必须把编号冲突当成创建失败的一部分显式处理，不能继续依赖后置的 `check-tasks` 兜底。
3. 显式 `task_id` 路径继续兼容现有命令行接口，包括旧的 `new-task task_name task_id title` 用法；本轮不改变它的参数协议。
4. 必须新增自动化测试，能够稳定覆盖旧缺陷模型与修复后的行为，避免只凭人工时序碰运气。
5. 任务完成时要有清晰验证路径，至少包含聚焦测试、仓库协议校验，以及一次并行创建场景的证据记录。
6. 设计与实现都应尽量局限在 `using-openharness` CLI 内部，不把并发控制扩散成新的仓库级配置面。

## Non-Goals
- 不在本轮引入新的 task id 前缀配置机制，也不改变 `allocate_next_task_id()` 当前“按已有前缀分布选择主前缀”的策略。
- 不借机重写整个 `new-task` 流程，也不调整 task package 模板内容。
- 不把任意显式 `task_id` 并发写冲突都提升为跨仓库事务系统；本轮优先修复 `--auto-id` 的仓库内竞争条件。
- 不新增外部三方依赖，只为锁或并发辅助能力去扩展 `pyproject.toml`。

## Constraints
- 必须继续使用仓库现有 Python / `uv run` 工作流，不引入一次性手工依赖。
- 改动应保持 `commands.py` 对外行为稳定，避免破坏现有脚本和历史 evidence 中的命令形态。
- 解决方案需要在仓库本地文件系统上工作，不能依赖额外服务、守护进程或数据库。
- 需要把根因修复放在仓库 helper / repository 层，而不是仅在命令层加文案提示或重试几次碰运气。
- 详细设计完成后先停在 `detailed_ready`，等待确认后再进入实现。
