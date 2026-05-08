# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先在 `tests/openharness_cases/test_cli_workflows.py` 增加默认模式配置、单次覆盖、非法配置和设置命令不执行 update 的失败测试。
  - 增加 `tests/openharness_cases/test_entrypoint.py` 帮助页断言。
  - 实现后运行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`。
  - 运行 `uv run pytest tests/openharness_cases/test_entrypoint.py -q`。
  - 最后运行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q` 和 `uv run openharness check-tasks`。
- Fallback Path:
  - 如果完整相关测试被环境阻塞，至少必须保留 update targeted 测试证据；如果配置读写路径、模式优先级或非法配置失败路径没有证据，不能宣称完成。
- Planned Evidence:
  - red run 证明新增测试在实现前失败。
  - green run 证明配置读写、默认选择、单次覆盖和帮助页通过。
  - `openharness verify update-default-mode` 生成最终 JSON artifact。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/commands.py`：增加 update 配置路径解析、配置读写、模式解析和非法配置处理。
- `openharness_cli/cli.py`：增加 `--mode` 与 `--set-default-mode` 参数和帮助文案。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖默认模式配置行为和失败路径。
- `tests/openharness_cases/test_entrypoint.py`：覆盖帮助页可发现性。
- `INSTALL.codex.md`：说明如何设置默认更新模式。
- `docs/archived/task-packages/update-default-mode/*`：记录本轮需求、设计、验证和证据。

## Interfaces
用户接口：

- `openharness update --set-default-mode pull`
- `openharness update --set-default-mode force-sync`
- `openharness update --mode pull`
- `openharness update --mode force-sync`
- `openharness update --force-sync`

环境接口：

- `OPENHARNESS_CONFIG_PATH`：测试和特殊环境可用它覆盖配置文件路径。
- 默认配置路径：`${XDG_CONFIG_HOME}/openharness/config.yaml` 或 `~/.config/openharness/config.yaml`。

配置契约：

```yaml
update:
  default_mode: force-sync
```

可观测性入口：

- 测试读取配置文件内容确认保存行为。
- monkeypatch `_run_command` 记录命令序列确认模式解析结果。
- stdout 输出保存路径和模式，非法配置输出错误。

## Module Internals
- parser 层通过 `choices=("pull", "force-sync")` 限制命令行合法值。
- commands 层提供小型 helper：
  - `_openharness_config_path()` 解析配置路径。
  - `_load_openharness_config()` 读取 YAML，空文件按空配置处理。
  - `_save_openharness_config()` 创建父目录并写回 YAML。
  - `_resolve_update_mode(args)` 按优先级返回模式或错误。
- `cmd_update` 先处理 `--set-default-mode`，再解析本次运行模式，最后复用现有普通/强制同步命令编排。

## Data Semantics
`update.default_mode` 语义：

- 缺失：等价于 `pull`。
- `pull`：无参数 update 执行普通 `git pull`。
- `force-sync`：无参数 update 执行 `git fetch --prune` 和 `git reset --hard '@{u}'` 后再升级工具。
- 其他值：配置无效，命令返回 1，不执行任何外部更新命令。

优先级语义：

1. `--force-sync` 固定为 `force-sync`。
2. `--mode <mode>` 固定为该次运行模式。
3. `update.default_mode`。
4. 内建默认 `pull`。

## Stage Gates
- 测试策略已明确：配置行为先写失败测试。
- 实现落点已明确：parser、commands、测试和安装文档。
- 接口精度已明确：两个合法模式、一个设置参数、一个单次模式参数和一个配置路径环境变量。
- 错误处理已明确：非法配置失败且无副作用。
- 预期证据已明确：pytest、check-tasks 和 final verify artifact。

## Decision Closure
- 接受：使用 `pull` 作为普通模式名称，因为它对应现有 `git pull` 行为，短且明确。
- 接受：保留 `--force-sync` 作为快捷方式，同时新增更通用的 `--mode force-sync`。
- 接受：使用 `OPENHARNESS_CONFIG_PATH` 做测试隔离，而不是 monkeypatch `Path.home()`。
- 拒绝：非法配置静默回退到 `pull`，因为这会隐藏用户配置错误。

## Error Handling
- 配置文件 YAML 解析失败时，打印错误并返回 1，不执行 update。
- `update.default_mode` 不是 `pull` 或 `force-sync` 时，打印错误并返回 1，不执行 update。
- `--set-default-mode` 写入失败时让异常暴露为命令失败；测试不覆盖权限错误。
- 静默出错风险：配置路径写错导致测试或用户读取了另一个文件；因此输出保存路径，测试使用 `OPENHARNESS_CONFIG_PATH` 固定路径。

## Migration Notes
- 未配置用户不需要迁移，行为保持普通 update。
- 已使用 `--force-sync` 的用户可以选择保存默认模式，也可以继续使用单次参数。
- 回滚时删除配置 helper 和新增参数即可；默认 `git pull` 路径应保持可用。

## Recommended Diagrams
不需要新增图示。模式优先级是线性覆盖关系，测试断言比图示更直接。

## Detailed Reflection
反思结论：

- 这轮最容易出错的不是命令序列，而是默认模式优先级；测试必须覆盖保存默认值与单次覆盖同时存在的情况。
- 配置读写不应扩展成全局系统；本轮只建立局部 helper，避免提前承诺更大的配置 API。
- 强制同步仍然有破坏性，帮助文案和安装说明必须继续强调默认设置只影响 OpenHarness source clone。
