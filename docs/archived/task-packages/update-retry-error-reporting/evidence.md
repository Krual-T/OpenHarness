# 证据

## 落地内容

- `openharness_cli/commands/update.py`：`pull` 和 `force-sync` 的源码同步命令改为最多尝试 3 次；每次失败输出命令、尝试次数、退出码、stdout 摘要和 stderr 摘要；全部失败后阻断工具升级。
- `openharness_cli/main.py`：依赖缺失时的 `openharness update` 兜底入口同步采用同样的重试和报错方式；全部失败后退出，不继续执行 `uv tool upgrade --reinstall openharness`。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖 `pull` 前两次失败第三次成功、三次失败后退出、`force-sync` 同步命令重试。
- `tests/openharness_cases/test_entrypoint.py`：覆盖兜底入口同步失败三次后停止升级。
- `pyproject.toml`：版本号从 `2.0.1` 提升到 `2.0.2`。

## 验证结果

### 聚焦测试

命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py -v
```

结果：

```text
16 passed
```

提交前版本变更后的相关测试复跑：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -v
```

结果：

```text
21 passed
```

### 全量测试

命令：

```bash
uv run pytest tests/ -v
```

结果：

```text
66 passed
```

## 验收标准覆盖

| 验收标准 | 覆盖测试 | 结果 |
| --- | --- | --- |
| 同步源码失败时最多尝试 3 次 | `test_update_retries_pull_and_reports_failures`、`test_update_stops_after_three_pull_failures`、`test_update_retries_force_sync_commands`、`test_fallback_update_retries_pull_and_stops_before_upgrade` | 通过 |
| 每次失败显示命令、尝试次数、退出码、stdout 和 stderr 摘要 | `test_update_retries_pull_and_reports_failures`、`test_update_stops_after_three_pull_failures`、`test_fallback_update_retries_pull_and_stops_before_upgrade` | 通过 |
| 三次失败后不继续执行工具升级 | `test_update_stops_after_three_pull_failures`、`test_fallback_update_retries_pull_and_stops_before_upgrade` | 通过 |
| `pull` 和 `force-sync` 两种同步模式都使用重试机制 | `test_update_retries_pull_and_reports_failures`、`test_update_retries_force_sync_commands` | 通过 |

## 剩余工作

无。

## 残余风险

- 未覆盖真实 GitHub 网络抖动，只用 subprocess 模拟不同退出码和输出。接受理由：本轮改动的核心是 CLI 命令编排、报错展示和阻断升级，单元测试可以稳定覆盖。
- `uv tool upgrade --reinstall openharness` 仍不自动重试。接受理由：需求明确只处理源码同步失败；工具升级失败通常需要单独诊断。

## 最终验证结论

通过。
