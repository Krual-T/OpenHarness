# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先新增或调整测试，覆盖正式包入口、旧脚本兼容入口以及安装文档中的关键命令说明。
- 再实现正式包目录、`pyproject.toml` 脚本入口和兼容层改造。
- 最后执行 `uv run pytest ...` 与 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Fallback Path:
- 如果 `uv tool install` 的真实安装验证在当前环境不适合直接执行，则至少通过自动化测试验证 `project.scripts`、入口模块和文档说明一致；若连打包配置都无法被测试覆盖，则不能宣称完成。
- Planned Evidence:
- 新增或更新的测试用例。
- `pyproject.toml` 中的 CLI 脚本配置。
- 更新后的安装文档，包含新装与已安装用户说明。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `pyproject.toml`：增加构建与命令入口配置。
- `openharness_cli/` 或等价正式包目录：承载可安装 CLI 实现。
- `skills/using-openharness/scripts/openharness.py`：保留兼容入口并转向正式包。
- `skills/using-openharness/tests/...`：补充入口与文档测试。
- `INSTALL.codex.md`：补齐安装和迁移说明。

## Interfaces
稳定接口：

- 命令行接口 `openharness <subcommand> [options]`
- 兼容脚本接口 `uv run python skills/using-openharness/scripts/openharness.py <subcommand>`

内部接口：

- `openharness_cli.main:main` 作为 console script 入口。
- 旧脚本继续重导出 parser、commands 和公共符号，保持测试与外部导入兼容。

## Stage Gates
- 必须先有失败测试，证明当前仓库尚未提供全局命令入口的打包配置或文档保障。
- 详细设计需要明确迁移顺序：先加正式包和打包配置，再保留脚本兼容层，最后更新文档。
- 预期证据包括测试通过记录、任务协议检查通过记录、安装文档中的迁移说明。

## Decision Closure
- 接受：使用 `uv tool install --editable <repo>` 作为推荐安装路径，因为它符合现有 `uv` 工作流且不要求用户改目标项目配置。
- 拒绝：本轮不做 alias 方案作为主方案，因为其稳定性与可文档化程度不足。
- 延期：是否额外提供单文件发行物留到未来需要跨环境分发时再评估。

## Error Handling
- 如果用户未安装 `openharness` 命令，技能文档和安装文档应提示执行 `uv tool install --editable <repo>`。
- 如果用户仅安装了技能软链接，没有安装工具命令，旧脚本路径仍然可以作为回退入口。
- 测试应确保文档不会错误声称“安装技能后自动获得命令”。

## Migration Notes
- 新用户：按更新后的 `INSTALL.codex.md` 完成仓库克隆、工具安装、技能软链接、重启 Codex。
- 已安装用户：在现有克隆仓库上额外执行一次 `uv tool install --editable ~/.agents/skill-hub/openharness`，必要时执行 `uv tool upgrade openharness` 或重新安装以刷新命令环境。
- 回滚时可以卸载全局工具命令，同时保留技能软链接与旧脚本调用。

## Detailed Reflection
反思结论：

- 测试重点不该放在真实 shell PATH 行为，而应放在仓库可打包性、入口可导入性和文档不误导用户。
- 兼容层必须尽量薄，否则未来会出现“双份 CLI 实现”漂移。
- 将正式包放在仓库顶层比继续埋在 `skills/.../scripts` 更适合工具安装，也更符合 console script 约定。
