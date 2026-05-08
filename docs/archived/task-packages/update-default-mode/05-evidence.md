# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 没有真实运行 `openharness update` 的外部命令，避免修改当前 OpenHarness 工作树；测试覆盖的是模式解析、配置读写和命令编排。
- 配置写入权限错误没有单独测试；这类错误会作为命令异常暴露，后续如果需要更友好的错误信息应单独处理。

## Manual Steps
- 无。

## Files
- `openharness_cli/cli.py`：新增 `--mode` 与 `--set-default-mode` 参数。
- `openharness_cli/commands.py`：新增用户配置路径、默认模式读写、模式优先级和非法配置处理。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖默认模式配置、单次覆盖和非法配置。
- `tests/openharness_cases/test_entrypoint.py`：覆盖帮助页可发现性。
- `INSTALL.codex.md`：记录默认模式设置和单次覆盖用法。
- `docs/archived/task-packages/update-default-mode/*`：记录本轮需求、设计、验证和证据。

## Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，red run: 3 failed, 7 passed, 21 deselected。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，green run: 10 passed, 21 deselected。
- `uv run pytest tests/openharness_cases/test_entrypoint.py -q`，3 passed。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`，86 passed。
- `final verification command`: `uv run openharness check-tasks`，passed, validated 48 task package(s)。
- 归档前还需执行 `uv run openharness verify update-default-mode`，由 CLI 生成最终 JSON artifact。

## Artifact Paths
- `.harness/artifacts/OH-046/verification-runs/latest.json`

## Follow-ups
- 如果未来出现多个用户级配置项，再考虑新增独立 `openharness config` 命令和配置查看能力。
