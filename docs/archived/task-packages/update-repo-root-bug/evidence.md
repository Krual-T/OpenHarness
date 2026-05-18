# 证据

## 验证结果
结论：通过。

verifying 阶段已按 `verification-design.md` 重新执行全部必需命令，新增回归测试、CLI workflow 测试和全量测试均通过。

## 文件
- `openharness_cli/commands/update.py` — `update` 使用 `HarnessContext.current().config.repo_root` 作为 repo root。
- `tests/openharness_cases/test_cli_workflows.py` — 新增 `test_update_uses_harness_context_repo_root`，拦截 subprocess 调用并断言 cwd。
- `docs/archived/task-packages/update-repo-root-bug/*` — 归档需求、验证策略和实现证据。

## 测试结果
- RED：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update_uses_harness_context_repo_root`
  - 首次测试写法问题：monkeypatch dotted path 被 `openharness_cli.commands.update` 导出函数遮蔽，测试未能正确 patch 模块。
  - 修正测试后看到目标失败：`git pull` 的 cwd 是 `/home/Shaokun.Tang/Projects/openharness/openharness_cli`，不是 `--repo` 指定目录。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update_uses_harness_context_repo_root`
  - verifying 最终结果：退出码 `0`，`1 passed, 10 deselected`。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py`
  - verifying 最终结果：退出码 `0`，`11 passed`。
- `uv run pytest`
  - verifying 最终结果：退出码 `0`，`55 passed, 1 skipped`。

## 验收标准覆盖
| 验收标准 | 证据 | 结果 |
|----------|------|------|
| `update` 使用 `HarnessContext.current().config.repo_root` | `openharness_cli/commands/update.py` | 通过 |
| `git pull` 和 `uv tool upgrade --reinstall openharness` 的 cwd 来自 repo root | `test_update_uses_harness_context_repo_root` | 通过 |
| 不执行真实 `git` 或 `uv` | 测试 monkeypatch `subprocess.run` | 通过 |

## 残余风险
- 测试没有执行真实 `git pull` 或 `uv tool upgrade --reinstall openharness`。接受理由：这两个命令有网络和安装副作用，本轮只修复 cwd 选择，mock 测试已覆盖该行为。
- 当前 shell 中的全局 `openharness` 仍可能是修复前版本，直到重新安装工具。接受理由：源码和测试已修复，安装刷新是部署动作。

## 后续事项
修复提交后，执行 `uv tool upgrade --reinstall openharness` 刷新全局命令。
