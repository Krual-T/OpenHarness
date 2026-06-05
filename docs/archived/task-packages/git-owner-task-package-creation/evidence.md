# 证据

## 变更文件

- `openharness_cli/commands/task_package.py`：移除 `task-package new` 的 `--owner` 参数，创建时不再从 CLI 传 owner。
- `openharness_cli/core/task_packages.py`：创建流程始终从 Git author 解析 owner，并替换模板中的 `<GIT OWNER>`。
- `tests/openharness_cases/test_task_package_core.py`：覆盖 `<GIT OWNER>` 注入、占位符不残留、`--owner` 被拒绝。
- `tests/openharness_cases/test_protocol_docs.py`：覆盖 `task-package new --help` 不展示 `--owner`。
- `tests/openharness_cases/test_yaml_quoting.py`：同步测试模板占位符和创建 API 新契约。
- `pyproject.toml`：版本号从 `0.5.9` 提升到 `0.5.10`。
- `docs/archived/task-packages/git-owner-task-package-creation/`：记录本轮需求、设计、验证策略和实现证据。

## 测试结果

RED 阶段：

- `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
  - 退出码：1
  - 摘要：4 个失败，暴露 `<GIT OWNER>` 未替换、`--owner` 仍被接受，以及直接调用 `new_package()` 时 owner 默认值仍是 Typer `OptionInfo`。

GREEN 阶段：

- `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
  - 退出码：0
  - 摘要：`17 passed`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
  - 退出码：0
  - 摘要：`17 passed`
- `uv run pytest tests/openharness_cases/test_yaml_quoting.py -q`
  - 退出码：0
  - 摘要：`1 passed`
- `uv run pytest tests/openharness_cases -q`
  - 退出码：0
  - 摘要：`55 passed`
- `uv run openharness check-tasks`
  - 退出码：2
  - 摘要：当前 CLI 不存在 `check-tasks` 命令，因此验证策略已改为当前可执行的 `task-package list/view` smoke。
- `uv run openharness task-package list`
  - 退出码：0
  - 摘要：列出 `TASK-022 [implementing] Git Owner Task Package Creation`。
- `uv run openharness task-package view TASK-022`
  - 退出码：0
  - 摘要：显示任务包详情，Owner 为 `Shaokun.Tang`，并注入 implementing 阶段指令。

最终实现阶段复跑：

- `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
  - 退出码：0
  - 摘要：`17 passed`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
  - 退出码：0
  - 摘要：`17 passed`
- `uv run pytest tests/openharness_cases -q`
  - 退出码：0
  - 摘要：`55 passed`
- `uv run openharness task-package list`
  - 退出码：0
  - 摘要：列出 `TASK-022 [implementing] Git Owner Task Package Creation`。
- `uv run openharness task-package view TASK-022`
  - 退出码：0
  - 摘要：显示任务包详情，Owner 为 `Shaokun.Tang`，并注入 implementing 阶段指令。

## 验证结果

结论：通过。

verifying 阶段实际执行结果：

| 命令 | 实际退出码 | 输出摘要 |
|------|------------|----------|
| `uv run pytest tests/openharness_cases/test_task_package_core.py -q` | 0 | `17 passed` |
| `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` | 0 | `17 passed` |
| `uv run pytest tests/openharness_cases -q` | 0 | `55 passed` |
| `uv run openharness task-package list` | 0 | 列出 `TASK-022 [verifying] Git Owner Task Package Creation` |
| `uv run openharness task-package view TASK-022` | 0 | 显示任务包详情，Owner 为 `Shaokun.Tang`，并注入 verifying 阶段指令 |

所有验证命令实际退出码均符合 `verification-design.md` 的期望退出码。

## 验收标准覆盖表

| 验收标准 | 证据 | 结果 |
|----------|------|------|
| 新建任务包把 `<GIT OWNER>` 替换成 Git author | `test_new_package_injects_git_owner_from_effective_git_config`，读取生成的 `task-info.yaml` 断言 owner 为 `Temp Owner`，且文本不含 `<GIT OWNER>` | 通过 |
| CLI 不再允许 `--owner` | `test_new_package_rejects_owner_option`，传入 `--owner codex` 退出非零且不创建目标包 | 通过 |
| `task-package new --help` 不展示 `--owner` | `test_cli_commands_resolve` 断言帮助文本不包含 `--owner` | 通过 |
| 核心创建 API 不再依赖外部 owner 入参 | `test_create_task_package_from_templates` 和 `test_create_task_package_quotes_yaml_sensitive_status_fields` 使用无 owner 入参的新调用路径 | 通过 |
| 现有 OpenHarness case 不退化 | `uv run pytest tests/openharness_cases -q` | 通过 |
| 当前任务包仍能被 CLI 发现和查看 | `uv run openharness task-package list` 与 `uv run openharness task-package view TASK-022` | 通过 |

## 残余风险

- 历史归档任务包中已有的 `owner: <GIT OWNER>` 没有批量修复；这是需求中明确排除的历史数据清理。
- 没有单独模拟 Git 全局配置层级；OpenHarness 调用的是 `git config user.name`，该命令由 Git 自身解析本地、全局和系统有效配置，本轮只验证 OpenHarness 使用返回值。
- Typer 未知参数的完整错误文案没有被固定；测试只依赖退出非零和不创建任务包，避免绑定第三方库文案。

## 后续事项

无必须后续事项。若未来要清理历史归档包 owner 占位符，应单独建任务包处理历史事实迁移。
