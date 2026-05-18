# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Result
- verify_by：`unit_test`
- result：passed

## Test Results
| Command | Exit Code | Result |
|---------|-----------|--------|
| `uv run pytest tests/openharness_cases/test_entrypoint.py -q` | 0 | `4 passed in 0.15s` |
| `uv run pytest tests/openharness_cases -q` | 0 | `54 passed, 1 skipped in 0.80s` |

## Files
- `openharness_cli/commands/update.py`：工具刷新命令改为 `uv tool upgrade --reinstall openharness`。
- `tests/openharness_cases/test_entrypoint.py`：增加 update subprocess 参数测试。
- `docs/task-packages/update-reinstall-tool/`：记录本轮需求、验证设计和证据。

## Residual Risks
- 不真实执行 update；通过 monkeypatch 检查命令参数。
