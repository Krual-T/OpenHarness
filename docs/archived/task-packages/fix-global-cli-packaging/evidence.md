# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Result
- verify_by：`unit_test`
- result：passed
- summary：全局 `openharness` 已从当前仓库重新安装，安装态包能导入 CLI 子包，transition 不再尝试补建 README。

## Test Results
| Command | Exit Code | Result |
|---------|-----------|--------|
| `uv tool install --force .` | 0 | 全局工具从 `file:///home/Shaokun.Tang/Projects/openharness` 安装成功 |
| `/home/Shaokun.Tang/.local/share/uv/tools/openharness/bin/python3 - <<'PY' ...` | 0 | `TaskPackageDocument` 为 `task-info.yaml`、`requirements.md`、`overview-design.md`、`detailed-design.md`、`verification-design.md`、`evidence.md`；`scaffold_files(proposing)` 为 `task-info.yaml`、`requirements.md` |
| `tmpdir=$(mktemp -d); cd "$tmpdir" && openharness --repo /home/Shaokun.Tang/Projects/openharness task-package transition TASK-004 overview_designing` | 0 | transition 成功，无 `task-package.README.md` 缺失 |
| `uv run pytest tests/openharness_cases -q` | 0 | `53 passed, 1 skipped in 0.72s` |

## Files
- `pyproject.toml`：改用 setuptools package discovery，包含 `openharness_cli.*` 子包。
- `docs/task-packages/fix-global-cli-packaging/`：记录本轮需求、验证设计和证据。

## Residual Risks
- `openharness update` 仍可能从配置的源克隆执行同步策略；本轮未改 update 行为。
- 验证过程中临时 transition 了 `TASK-004`，已将其 `status` 恢复为 `requirements_designed`。

## Follow-ups
- 可另开任务评估 `openharness update` 是否应更明确提示安装源路径。
