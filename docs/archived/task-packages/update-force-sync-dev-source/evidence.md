# 证据

## 变更文件

- `openharness_cli/commands/update.py`：默认模式改为 `force-sync`；新增 `dev-source` 模式；`--set-default-mode` 支持 `dev-source`；无参数更新执行 `git fetch --prune`、`git reset --hard @{u}` 后 reinstall。
- `openharness_cli/main.py`：依赖缺失兜底入口默认执行强制同步；支持 `--dev-source` 和 `--mode dev-source` 跳过 git 同步。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖默认强制同步、重试失败输出、`dev-source` 跳过 git 同步、保存默认 `dev-source`。
- `tests/openharness_cases/test_entrypoint.py`：覆盖 help 文案、正常入口 `dev-source`、fallback 默认强制同步失败阻断、fallback `dev-source`。
- `INSTALL.md`：说明默认更新会强制同步安装源码目录，并提示开发者使用 `dev-source`。
- `README.md`：更新 CLI 摘要。
- `skills/using-openharness/references/cli-reference.md`：更新 CLI 速查和约束说明。
- `pyproject.toml`、`uv.lock`：版本号提升到 `3.0.0`。

## 测试结果

### RED

命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -k "update or parser_help" -v
```

结果：

```text
9 failed, 1 passed, 14 deselected
```

失败点符合预期：默认仍调用 `git pull`、`dev-source` 未识别、fallback 入口不接收参数。

### 相关测试

命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -v
```

结果：

```text
25 passed
```

### 全量测试

命令：

```bash
uv run pytest tests/ -v
```

结果：

```text
70 passed
```

## 验收标准覆盖

| 验收标准 | 覆盖测试 | 结果 |
| --- | --- | --- |
| 无参数 `openharness update` 默认执行 `git fetch --prune`、`git reset --hard @{u}`、reinstall | `test_update_uses_installed_openharness_source_root` | 通过 |
| 默认强制同步失败时沿用 3 次重试和 stdout/stderr 报错 | `test_update_retries_default_force_sync_and_reports_failures`、`test_update_stops_after_three_default_sync_failures` | 通过 |
| `--force-sync` 显式入口仍可用 | `test_update_retries_force_sync_commands` | 通过 |
| `--mode dev-source` 跳过 git 同步，只 reinstall | `test_update_dev_source_skips_git_sync`、`test_update_reinstalls_existing_tool_source` | 通过 |
| `--set-default-mode dev-source` 可保存 | `test_update_set_default_mode_accepts_dev_source` | 通过 |
| 旧的 `pull` 默认配置不再被接受 | `test_update_rejects_legacy_pull_default_mode` | 通过 |
| 依赖缺失兜底入口默认强制同步，失败三次后不 reinstall | `test_fallback_update_retries_default_force_sync_and_stops_before_upgrade` | 通过 |
| 依赖缺失兜底入口支持 `dev-source` | `test_fallback_update_dev_source_skips_git_sync` | 通过 |
| 文档说明默认强制同步和开发源码模式 | `test_install_doc_mentions_openharness_update`、人工 diff 检查 | 通过 |

## 残余风险

- 没有用真实 Git upstream 仓库跑端到端自更新。接受理由：本轮明确不在当前项目目录运行真实 `openharness update`，核心行为通过 subprocess 调用序列单元测试覆盖。
- `dev-source` 只支持当前已安装来源目录，不支持传入任意路径。接受理由：需求边界已明确，不在本轮引入新安装来源解析。
- 默认强制同步会丢弃安装源码目录本地改动。接受理由：这是本轮目标行为，文档和 help 文案已经提示安装源码目录应视为工具托管缓存。

## 后续事项

无。

## 验证结果

通过。
