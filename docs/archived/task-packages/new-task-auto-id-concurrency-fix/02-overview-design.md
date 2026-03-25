# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮只覆盖 `using-openharness` CLI 里与新建 task package 直接相关的仓库表面：

- `skills/using-openharness/scripts/openharness_cli/commands.py`
  - `cmd_new_task()` 的入口编排。
- `skills/using-openharness/scripts/openharness_cli/repository.py`
  - `allocate_next_task_id()`、`create_task_package()` 及新增的并发安全 helper。
- `skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
  - 自动编号与并发安全相关的聚焦测试。

不纳入范围的部分：

- 任务模板内容本身。
- `bootstrap`、`transition`、`verify` 等其他子命令行为。
- 仓库级 task id 前缀策略与多前缀治理。

## Proposed Structure
推荐把 `--auto-id` 的关键路径从命令层下沉到 repository helper，形成一个显式的“带仓库锁的 scaffold”主路径：

1. `cmd_new_task()` 只负责解析参数和决定走显式 `task_id` 还是自动编号。
2. 当走 `--auto-id` 时，改为调用一个新的 repository helper，由它：
   - 获取仓库级互斥锁；
   - 在锁内重新扫描现有 package 并分配下一个 `task_id`；
   - 立刻创建 task package；
   - 释放锁并返回最终 `task_root` 与 `task_id`。
3. 显式 `task_id` 仍复用现有 `create_task_package()`，但会补上更明确的重复编号防护，避免出现“目录不同但编号已冲突”的静默坏状态。

锁实现优先选择标准库即可完成、无需额外依赖的仓库本地文件系统方案。锁的存在只服务于 `new-task --auto-id` 的临界区，不暴露为新的用户配置项。

## Key Flows
主路径：

1. 用户调用 `uv run python skills/using-openharness/scripts/openharness.py new-task some-task --title "Some Task" --auto-id ...`
2. `cmd_new_task()` 识别为自动编号路径。
3. repository helper 进入仓库级锁。
4. 在锁内重新读取 task package 集合，计算最新可用 `task_id`。
5. 立即执行 package 创建；若创建失败，则把失败作为整次创建失败返回。
6. 创建成功后释放锁，CLI 输出实际分配的 `task_id`。

失败路径：

1. 若锁获取失败或锁内创建失败，命令直接返回错误，不产生“编号已经分配但 package 未知是否可用”的假象。
2. 若发现显式 `task_id` 已经被占用，立即报错，不允许继续写出新的重复编号 package。

状态流：

- 当前 task package 先从 `proposed` 前进到 `detailed_ready`，作为设计就绪的停点。
- 等待确认后再进入实现、验证与归档。

## Stage Gates
- 需要明确主临界区放在哪一层，避免命令层与 repository 层职责继续混杂。
- 需要明确锁保护的最小范围，以及失败时如何清理。
- 需要明确显式 `task_id` 与自动编号两条路径的重复编号边界。
- 需要给出至少一种可稳定复现旧竞争条件的测试方案，不能只写“理论上可能并发”。
- 需要保留回滚方向：如果新 helper 引入问题，应能仅回退并发保护改动，而不牵动任务模板和其他命令。

## Trade-offs
推荐方案是“仓库级锁 + 锁内编号分配 + 锁内创建”。

收益：

- 直接消除当前根因，而不是依赖重试碰运气。
- 逻辑集中在 repository helper，命令层继续保持薄。
- 不需要引入三方锁库，也不需要修改现有 task id 协议。

代价：

- 需要新增少量锁管理代码和对应测试夹具。
- 并发创建会被串行化，但这是可接受的，因为新建 task package 的临界区很短。

不选的方向：

- 只在创建失败后重试分配编号：无法阻止两个不同目录成功落盘同一 `task_id`，根因仍在。
- 只在 `check-tasks` 里发现重复再让用户清理：这是事后发现，不满足 intake 主路径的稳定性要求。
- 引入第三方锁库：对当前仓库过重，而且会扩大依赖面。

## Overview Reflection
我先挑战了“是否只需要失败重试”。结论是否定的，因为当前冲突不是目录名冲突，而是 `task_id` 语义冲突；只要两个任务名不同，两个目录都可能成功创建，事后重试已经来不及。

我也比较了“在命令层加锁”与“在 repository helper 加锁”。最终接受后者，因为并发安全的真实边界是“分配编号并立刻创建 package”这一段仓库操作，而不是命令解析本身。把临界区放在 helper 层，后续即使还有别的入口复用这段能力，也不会绕过保护。

最后我确认了验证影响：仅有文档设计还不够，后续实现必须补一个可重复的并发测试模型，否则这轮修复很容易退化成只在单线程下看起来成立。
