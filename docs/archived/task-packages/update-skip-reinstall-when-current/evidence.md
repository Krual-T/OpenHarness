# 证据

## 变更文件

- `openharness_cli/commands/update.py`：新增 `git rev-parse HEAD` 读取；强制同步前后比较 HEAD；无变化时跳过 reinstall 并提示已经是最新代码。
- `openharness_cli/main.py`：兜底入口同步新增 HEAD 比较和跳过 reinstall 行为。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖默认更新无变化跳过 reinstall、有变化执行 reinstall、同步重试路径仍正常、`dev-source` 仍 reinstall。
- `tests/openharness_cases/test_entrypoint.py`：覆盖 fallback 无变化跳过 reinstall、有变化执行 reinstall、失败路径仍不 reinstall。
- `pyproject.toml`、`uv.lock`：版本号提升到 `3.0.1`。

## 测试结果

### RED

命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -k "update or parser_help" -v
```

结果：

```text
8 failed, 6 passed, 14 deselected
```

失败点符合预期：代码尚未读取 `git rev-parse HEAD`，仍在强制同步后直接 reinstall。

### 相关测试

命令：

```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py -v
```

结果：

```text
28 passed
```

### 全量测试

命令：

```bash
uv run pytest tests/ -v
```

结果：

```text
73 passed
```

## 验收标准覆盖

| 验收标准 | 覆盖测试 | 结果 |
| --- | --- | --- |
| 强制同步前后读取 `git rev-parse HEAD` | `test_update_uses_installed_openharness_source_root`、`test_update_reinstalls_after_force_sync_changes_head` | 通过 |
| `HEAD` 未变化时跳过 reinstall 并提示已经是最新代码 | `test_update_uses_installed_openharness_source_root`、`test_fallback_update_skips_reinstall_when_head_unchanged` | 通过 |
| `HEAD` 变化时继续 reinstall | `test_update_reinstalls_after_force_sync_changes_head`、`test_fallback_update_reinstalls_when_head_changes` | 通过 |
| 同步失败时仍重试并阻断 reinstall | `test_update_stops_after_three_default_sync_failures`、`test_fallback_update_retries_default_force_sync_and_stops_before_upgrade` | 通过 |
| `dev-source` 仍总是 reinstall | `test_update_dev_source_skips_git_sync`、`test_update_reinstalls_existing_tool_source`、`test_fallback_update_dev_source_skips_git_sync` | 通过 |

## 残余风险

- 未用真实 Git 远端执行端到端更新。接受理由：本轮明确不在当前项目目录运行真实 `openharness update`，调用序列和输出由单元测试覆盖。
- 如果源码 commit 没变但本机工具安装损坏，默认 update 会跳过 reinstall。接受理由：这是“源码没变不 reinstall”的目标行为；主动修复安装可使用 `openharness update --mode dev-source`。

## 后续事项

无。

## 验证结果

通过。
