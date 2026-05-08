# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先在 `tests/openharness_cases/test_cli_workflows.py` 增加 `--force-sync` 行为测试，观察新增测试在实现前失败。
  - 再实现 parser 参数和 handler 分支，使测试通过。
  - 运行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q` 验证 update 行为。
  - 运行 `uv run pytest tests/openharness_cases/test_entrypoint.py -q` 验证帮助文案。
  - 最后运行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q` 覆盖相关 CLI 与文档协议面。
- Fallback Path:
  - 如果完整相关测试被环境问题阻塞，至少必须保留针对 `update` 的红绿测试结果，并在 `04-verification.md` 写明未覆盖的范围；没有命令顺序和失败中断证据时不能宣称完成。
- Planned Evidence:
  - 新增失败测试的 red 输出。
  - 实现后的 targeted update 测试输出。
  - 帮助页测试输出和相关协议测试输出。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/cli.py`：为 `update` parser 增加 `--force-sync` 参数和风险说明。
- `openharness_cli/commands.py`：在 `cmd_update` 中根据 `args.force_sync` 选择普通同步或强制同步命令序列。
- `tests/openharness_cases/test_cli_workflows.py`：增加 `--force-sync` 命令顺序和失败中断测试，保留默认路径兼容性断言。
- `tests/openharness_cases/test_entrypoint.py`：增加帮助文案对 `--force-sync` 的断言。
- `INSTALL.codex.md`：补充安装后强制同步更新的用户入口说明。
- `docs/archived/task-packages/update-force-sync/*`：记录需求、设计、验证和证据。

## Interfaces
用户接口：

- `openharness update`
- `openharness update --force-sync`

接口契约：

- 不传 `--force-sync` 时，命令序列保持 `git pull`、`uv tool upgrade openharness`。
- 传 `--force-sync` 时，命令序列为强制同步步骤、`uv tool upgrade openharness`。
- 任一同步步骤返回非 0 时，handler 返回 1，并不执行后续工具升级。

可观测性入口：

- pytest 通过 monkeypatch `_run_command` 记录 `(repo_root, command)` 序列。
- 用户通过 stdout 中的错误消息识别失败发生在同步阶段还是工具升级阶段。

## Module Internals
- `cli.py` 只新增参数声明，不执行任何副作用。
- `commands.py` 负责编排命令序列和失败中断；它不直接调用 subprocess。
- `lifecycle._run_command` 继续负责实际副作用执行，本轮不改变其签名。
- `main.py` 的 monkeypatch 桥接保持原状，确保测试替身仍能控制 update 的外部命令执行。

## Data Semantics
关键数据是 `args.force_sync`：

- `False`：默认安全同步，使用普通 `git pull`。
- `True`：用户显式授权强制同步，允许将 OpenHarness 源码 clone 对齐到上游跟踪分支。

该布尔值只在本次进程内存在，不写入 task package、不写入配置文件，也不改变后续 update 的默认值。

## Stage Gates
- 测试策略已经明确：先写 `--force-sync` 的失败测试，再实现。
- 实现落点已经明确：parser、handler、测试和安装文案。
- 接口精度已经明确：新增单个布尔参数，默认值为 `False`。
- 失败传播已经明确：同步阶段失败阻止工具升级。
- 预期证据类型已经明确：pytest 输出和任务包验证记录。

## Decision Closure
- 接受：使用 `--force-sync` 而不是更短的 `--force`，因为它更具体，能减少与 `uv tool install --force` 或其他强制语义混淆。
- 接受：强制同步通过 git 命令序列表达，并继续走 `_run_command`，保持测试可替换。
- 拒绝：在 handler 内解析当前分支并拼接 `origin/<branch>`；使用上游跟踪引用能避免错误猜测远端。
- 延期：对没有上游跟踪分支的 clone 提供更友好的修复建议，本轮只保证失败中断和错误可见。

## Error Handling
- `git fetch` 或强制重置失败时，打印强制同步失败消息并返回 1，不继续执行 `uv tool upgrade openharness`。
- `uv tool upgrade openharness` 失败时，保持现有失败消息并返回 1。
- 静默出错风险：如果测试只断言返回值，不断言命令序列，可能误把普通 `git pull` 当成强制同步；因此测试必须记录完整命令顺序。
- 误用风险：用户可能不理解强制同步会覆盖本地 clone 偏移；帮助文案必须直说该参数会 discard local changes in the OpenHarness source clone。

## Migration Notes
- 先提交测试和实现，再更新安装文案和任务包验证证据。
- 兼容策略是默认命令完全保持原行为，只有新参数触发新路径。
- 回滚触发点是 update 相关测试或帮助页测试失败；回滚时只需移除新参数分支，默认路径不应受影响。

## Recommended Diagrams
不需要新增图示。线性命令序列由详细设计和测试断言表达即可。

## Detailed Reflection
反思结论：

- 测试必须先失败，才能证明新增断言确实覆盖了还不存在的 `--force-sync`。
- 接口边界应保持小：一个布尔参数足够表达用户意图，不需要新增配置或交互确认。
- 验证不能真实执行强制同步，否则会破坏当前开发工作树；命令替身是本轮更合适的证据。
