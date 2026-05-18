# 证据

## 验证结果
结论：通过。

verifying 阶段已按 `verification-design.md` 重新执行全部必需命令，新增回归测试、CLI workflow 测试和全量测试均通过。

## 文件
- `openharness_cli/commands/update.py` — `update` 优先使用安装元数据里的 OpenHarness source root；没有安装元数据时回退到模块所在仓库根。
- `tests/openharness_cases/test_cli_workflows.py` — 新增 `test_update_uses_installed_openharness_source_root` 和 `test_openharness_source_root_falls_back_to_module_repo`，拦截 subprocess 调用并断言 cwd。
- `docs/archived/task-packages/update-repo-root-bug/*` — 归档需求、验证策略和实现证据。

## 测试结果
- RED：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update_uses_harness_context_repo_root`
  - 首次测试写法问题：monkeypatch dotted path 被 `openharness_cli.commands.update` 导出函数遮蔽，测试未能正确 patch 模块。
  - 修正测试后看到目标失败：`git pull` 的 cwd 是 `/home/Shaokun.Tang/Projects/openharness/openharness_cli`，不是 `--repo` 指定目录。
- 纠正：用户指出 `HarnessConfig.repo_root` 表示当前被 harness 管理的项目，不是 OpenHarness 安装来源。重新排查 `INSTALL.codex.md`、历史 task package 和全局安装的 `direct_url.json` 后，确认 `update` 应更新 OpenHarness source clone，而不是业务项目。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k 'update_uses_installed_openharness_source_root or openharness_source_root_falls_back_to_module_repo'`
  - verifying 最终结果：退出码 `0`，`2 passed, 10 deselected`。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py`
  - verifying 最终结果：退出码 `0`，`12 passed`。
- `uv run pytest`
  - verifying 最终结果：退出码 `0`，`56 passed, 1 skipped`。

## 验收标准覆盖
| 验收标准 | 证据 | 结果 |
|----------|------|------|
| `update` 使用 OpenHarness 安装来源 source root | `openharness_cli/commands/update.py` | 通过 |
| `git pull` 和 `uv tool upgrade --reinstall openharness` 的 cwd 来自 OpenHarness source root | `test_update_uses_installed_openharness_source_root` | 通过 |
| 本地源码运行可回退到模块所在仓库根 | `test_openharness_source_root_falls_back_to_module_repo` | 通过 |
| 不执行真实 `git` 或 `uv` | 测试 monkeypatch `subprocess.run` | 通过 |

## 残余风险
- 测试没有执行真实 `git pull` 或 `uv tool upgrade --reinstall openharness`。接受理由：这两个命令有网络和安装副作用，本轮只修复 cwd 选择，mock 测试已覆盖该行为。
- 当前 shell 中的全局 `openharness` 仍可能是修复前版本，直到重新安装工具。接受理由：源码和测试已修复，安装刷新是部署动作；全局安装元数据已确认记录了 `file:///home/Shaokun.Tang/.agents/skill-hub/openharness`。

## 后续事项
修复提交后，执行 `uv tool upgrade --reinstall openharness` 刷新全局命令。
