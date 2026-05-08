# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先新增一个失败测试：构造 active 根目录下 `status: archived` 的 task package，执行 `cmd_check_tasks`，期望自动移动到 archived 根目录、路径引用被重写且返回 0。
  - 然后实现最小代码使该测试通过。
  - 最后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py` 和 `uv run openharness check-tasks`。
- Fallback Path:
  - 如果目标测试无法稳定表达行为，退回到更低层的 repository/lifecycle 单元测试；如果现有 task package 校验失败，不能宣称完成，需先修复协议文档或状态。
- Planned Evidence:
  - 测试 red/green 结果、最终 pytest 输出、`openharness check-tasks` 输出，以及本包 `04-verification.md` / `05-evidence.md` 的执行记录。

## Files Added Or Changed
- `tests/openharness_cases/test_cli_workflows.py`：新增 CLI 行为测试，锁定 active archived 包会自动移动。
- `openharness_cli/repository.py`：在发现 task packages 时触发 active archived 包规范化。
- `openharness_cli/lifecycle.py`：如有必要调整 helper 可见性或错误消息，但优先复用现有 `_archive_task_package`。
- `docs/archived/task-packages/archived-status-auto-move/*`：记录需求、设计、验证和证据。

## Interfaces
稳定契约是 `discover_task_packages(repo_root, manifest)` 返回的 package 列表应满足状态与目录位置的一致性。边界条件是：只有位于 active 根目录、且 `STATUS.yaml.status == archived` 的包会被自动移动；位于 archived 根目录但状态不是 archived 的包仍由 validation 报错。

可观测入口是 CLI 返回码、stdout/stderr 错误文本、active/archived 目录是否存在、包内路径是否重写，以及 `check-tasks` 是否通过。

## Module Internals
`repository.py` 负责扫描目录、读取 `STATUS.yaml`、识别需要规范化的包，并把副作用交给 lifecycle helper。`lifecycle.py` 负责实际目录移动、临时目录、backup、路径重写和移动后的校验。`validation.py` 不承担修复动作，只继续声明最终不变量。

## Data Semantics
`STATUS.yaml.status` 的 `archived` 值是归档意图的权威信号。active 根目录中的 archived 包是可自动修复的不一致中间态；archived 根目录中的非 archived 包仍是错误，因为它没有表达归档意图。

## Stage Gates
- 测试先失败，失败原因是 active archived 包尚未自动移动。
- 实现落点限定在 repository/lifecycle 发现与移动边界。
- 自动移动后的包必须继续通过 validation。
- 最终验证必须覆盖新增 CLI 测试、相关 task package core 测试和当前仓库 task package 校验。

## Decision Closure
接受 discovery 带副作用，但只在 `status: archived` 已明确表达归档意图时触发。拒绝把 `verify` 成功作为自动归档触发点，因为它会扩大行为范围并改变完成闭环语义。

## Error Handling
主要失败路径包括 archived 目标目录已存在、移动事务失败、移动后包仍不满足 validation。静默出错风险是 helper 返回失败但 discovery 继续返回不一致包；实现必须把失败转成明确异常，让 CLI 返回错误。

## Migration Notes
实施顺序是先加测试，再改 discovery，最后跑相关测试和 `check-tasks`。兼容策略是保留 `transition <task> archived` 的现有行为；如果自动移动引发不可接受副作用，回滚点是移除 discovery 中的规范化调用，保留显式 transition 路径。

## Recommended Diagrams
不新增图。测试夹具会更直接展示状态、路径和预期结果。

## Detailed Reflection
测试策略要避免只测试 helper，因为用户可见行为发生在 CLI 命令入口。接口边界要避免让 validation 同时负责修复和校验，所以修复放在 discovery，validation 继续保持最终不变量。迁移假设是 active archived 状态代表明确归档意图；如果未来发现有人临时写 archived 但不想移动，需要新增显式禁用开关，而不是削弱默认一致性。
