# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先补一个聚焦测试，稳定模拟两个并发 `--auto-id` 创建请求在读取相同最大编号后竞争落盘的场景；该测试在修复前应失败，修复后应通过。
  - 再运行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py`，确认自动编号、重复编号与并发安全相关行为一起通过。
  - 最后运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认仓库 task package 协议仍然干净。
  - 若实现阶段需要更贴近真实 CLI，可再补一次从子进程并行调用 `new-task --auto-id` 的场景测试或手工验证，作为补充证据而不是唯一证据。
- Fallback Path:
  - 如果稳定的真实并发子进程测试过于脆弱，就退回到可控的测试钩子或 monkeypatch，同样要求能稳定构造旧实现的竞争窗口。
  - 如果完整测试被无关历史问题阻塞，至少保留聚焦测试与 `check-tasks` 的结果，并在 `05-verification.md` 明确记录阻塞原因；在这种情况下不能宣称本包已验证完成。
  - 如果锁实现引入平台差异，优先缩小实现到当前仓库稳定支持的平台表面，并把未覆盖平台写成残余风险，而不是假装跨平台已经完成验证。
- Planned Evidence:
  - 一个能证明旧缺陷存在的失败测试模型，以及修复后的通过结果。
  - `test_task_package_core.py` 通过结果。
  - `check-tasks` 通过结果。
  - `06-evidence.md` 中记录新增 helper、测试点和并行场景观察结论。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/scripts/openharness_cli/commands.py`
  - 调整 `cmd_new_task()`，把 `--auto-id` 路径改为调用新的并发安全 scaffold helper，而不是先算编号再单独创建。
- `skills/using-openharness/scripts/openharness_cli/repository.py`
  - 新增仓库级锁 helper。
  - 新增或重组自动编号创建 helper，把“分配编号 + 创建 package”并入同一临界区。
  - 在 `create_task_package()` 或其上层入口补显式 `task_id` 重复检测，避免目录不同但编号重复。
- `skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
  - 先写失败测试，再覆盖并发安全主路径、显式重复编号保护和锁释放行为。
- `docs/archived/task-packages/new-task-auto-id-concurrency-fix/*`
  - 记录这轮需求、设计、验证与实现证据。

## Interfaces
命令接口：

- `new-task`
  - 参数协议不变。
  - `--auto-id` 仍由用户显式开启。
  - 成功输出继续包含 `Task id: <id>`，但该 `id` 现在来自锁内创建结果，而不是锁外预分配。

repository 接口：

- 保留 `allocate_next_task_id()` 作为纯计算 helper，供测试或非并发场景复用。
- 新增一个专门的“并发安全自动建包” helper，职责是：
  - 获取并释放仓库锁；
  - 在锁内分配 `task_id`；
  - 调用 package 创建；
  - 返回实际创建结果。
- `create_task_package()` 继续负责模板落盘，但在入口前后都不能再允许重复 `task_id` 被静默写入。

锁接口：

- 锁只在仓库内部使用，不暴露给 CLI 用户。
- 锁文件或锁目录应落在仓库可忽略的位置，例如 `.harness` 下的专用锁路径，避免污染 task package 根目录。
- 锁需要用 `try/finally` 保证正常失败时释放。

## Stage Gates
- 必须有先失败后通过的测试策略，证明修复的是根因而不是偶然时序。
- 必须明确锁持有范围只覆盖最小必要临界区，避免把无关文档写入也串进锁里。
- 必须明确显式 `task_id` 冲突如何报错，以及对应测试覆盖。
- 必须明确证据类型：聚焦测试、协议校验、并行场景观察。
- 必须保留实现后可回滚的边界，避免把锁逻辑散落到多个模块后难以撤回。

## Decision Closure
- 接受：用仓库级本地锁串行化 `--auto-id` 临界区，因为这是唯一能直接消除重复编号根因的轻量方案。
- 接受：把临界区 helper 放在 `repository.py`，因为它比 `commands.py` 更接近真实数据边界，也更容易被测试。
- 接受：显式 `task_id` 路径同步补重复编号检测，因为否则仓库仍允许写入语义冲突的 package。
- 拒绝：只增加命令层重试逻辑。理由是不同目录名下的重复 `task_id` 可能已经落盘，重试无法消除已产生的坏状态。
- 拒绝：引入新的第三方锁依赖。理由是当前仓库规模不需要，为一个很窄的临界区扩大依赖面不划算。
- 延期：是否把锁能力抽象成通用仓库事务框架。触发条件是未来还有第二个以上命令需要同类文件系统级互斥。

## Error Handling
如果锁获取失败或超时，命令要显式返回错误并说明当前仓库存在并发创建占用，不能静默降级回旧逻辑。

如果在锁内计算出 `task_id` 后创建失败，要把这次失败视为整个 `new-task` 失败；不能输出一个看似已经分配成功的编号。

如果显式 `task_id` 已存在于现有 active 或 archived package，应该立即报错，避免继续制造需要人工清理的重复状态。

如果锁实现使用文件系统路径，需要考虑异常退出后的清理策略；实现时要优先选择“进程退出可自动释放”或“可检测并安全清理”的方案，并把无法完全消除的尾部风险写进验证和证据页。

## Migration Notes
实施顺序：

1. 先补聚焦测试，稳定复现旧竞争窗口。
2. 在 repository 层实现锁与并发安全 helper。
3. 调整 `cmd_new_task()` 走新 helper。
4. 补显式 `task_id` 冲突保护与相关测试。
5. 跑测试与 `check-tasks`，回写 `05-verification.md` 和 `06-evidence.md`。

兼容策略：

- 保留旧命令参数形态，不要求历史 evidence 回写。
- 不迁移现有 task package 结构，也不改动现有归档路径。

回滚注意事项：

- 如果锁逻辑带来问题，可只回退 helper 与命令接入层；现有 task package 模板和状态协议不受影响。

## Detailed Reflection
我先反思测试策略：真正难点不是“函数返回了什么”，而是“两个调用共享同一个仓库视图时是否还能保持唯一编号”。因此后续测试不能只测单线程编号递增，必须至少有一个可稳定构造竞争窗口的模型。

我也反思了接口边界：如果把锁散落在 `cmd_new_task()` 里，后续任何新入口只要直接调用 repository helper，就可能重新绕过保护。把临界区定义在 repository 层，能让仓库操作边界更一致。

最后我挑战了迁移假设：这轮修复应该保持小而硬，只解决编号分配与创建的并发一致性，不借机扩展成新的 task id 策略工程；否则设计会在确认前继续膨胀。
