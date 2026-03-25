# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - 补充一次并行 `new-task --auto-id` 场景验证，确认新建 package 的 `task_id` 唯一且结果可通过 `check-tasks`
- Executed Path:
  - 先执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py -k "duplicate_task_id or duplicate_allocated_id"`，验证新回归测试先红后绿后的最终通过结果。
  - 再执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py`，确认 task package core 测试全量通过。
  - 最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 active / archived task package 协议仍然干净。
- Path Notes:
  - 本轮自动化验证重点是防止重复编号被静默落盘，因此用稳定的重复编号模拟来覆盖旧竞争窗口，而不是依赖脆弱的时序赛跑。
  - 当前尚未补真实多进程并行场景测试；这被记录为已接受的残余风险，但不阻塞本轮归档，因为核心根因已有自动化回归保护，且全仓库 `check-tasks` 通过。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 聚焦测试能覆盖旧竞争窗口，并在修复后稳定通过。
- `check-tasks` 不再能观察到由并发 `--auto-id` 创建出的重复 `task_id`。
- CLI 兼容路径保持稳定，显式 `task_id` 用法不回归。

## Traceability
- `01-requirements.md` 里的核心目标是“并发下唯一编号且无静默坏状态”。
- `02-overview-design.md` 把根因收敛为“分配编号与创建 package 不在同一临界区”，并明确推荐仓库级锁方案。
- `03-detailed-design.md` 把实现落点、测试策略和失败路径写成可执行计划。
- `test_create_task_package_rejects_duplicate_task_id` 覆盖显式 `task_id` 冲突不再静默落盘。
- `test_cmd_new_task_auto_id_rejects_duplicate_allocated_id` 覆盖 `--auto-id` 拿到重复编号时命令应直接失败。
- 全量 `test_task_package_core.py` 与 `check-tasks` 证明改动没有破坏仓库现有 task package 主路径。

## Risk Acceptance
- 当前接受的风险一：锁实现基于 `fcntl.flock`，适合当前 Linux 文件系统环境；如果未来需要在不支持该语义的平台上运行，还需要补平台兼容策略。
- 当前接受的风险二：本轮没有增加真实多进程并行场景测试，而是用稳定的重复编号模拟保护根因；若后续继续扩展 `new-task` 并发行为，可以再补一条端到端并发验证用例。

## Latest Result
- 当前状态：通过。`test_task_package_core.py` 20 项全部通过，`check-tasks` 通过，回归测试覆盖了旧竞争窗口的核心坏状态。
- Latest Artifact:
  - 无单独 artifact 文件；本轮以测试命令输出和归档后的 task package 文档作为主要证据。
