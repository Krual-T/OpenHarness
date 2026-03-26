# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先为 `update` 增加 parser 和 command 行为测试，验证命令解析、执行顺序、repo root 和失败中断。
  - 再更新文档测试，确认 `INSTALL.codex.md` 提到了 `openharness update`。
  - 最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Fallback Path:
  - 如果真实 `git pull` 不适合在当前工作树执行，则以 monkeypatch 的自动化测试作为主验证路径；如果顺序、参数和失败路径没有被测试覆盖，就不能宣称完成。
- Planned Evidence:
  - `test_cli_workflows.py` 中关于 `update` 的新增测试。
  - 更新后的安装文档与技能文档。
  - `check-tasks` 通过记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/cli.py`：声明 `update` 子命令。
- `openharness_cli/commands.py`：实现 `cmd_update`。
- `openharness_cli/main.py` 与兼容脚本导出：暴露新命令。
- `skills/using-openharness/tests/openharness_cases/test_cli_workflows.py`：新增命令行为测试。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`、`INSTALL.codex.md`、`skills/using-openharness/SKILL.md`：更新文档与断言。

## Interfaces
新增用户接口：

- `openharness update`

内部契约：

- handler 必须只依赖统一 `_run_command(repo_root, command)` 执行外部命令。
- `repo_root` 必须指向 OpenHarness 自身仓库根。

## Stage Gates
- 先有失败测试，再写实现。
- 需要验证成功顺序、失败中断和 repo root。
- 文档必须把原手工更新步骤收敛为 `openharness update`。

## Decision Closure
- 接受：对外命名用 `update`。
- 接受：内部继续调用 `uv tool upgrade openharness`，因为这是刷新工具环境的现有底层命令。
- 拒绝：把当前 `cwd` 当更新目标仓库。

## Error Handling
- `git pull` 失败时直接返回非 0，并打印失败步骤。
- 不尝试吞掉错误或自动继续。
- 若仓库根定位异常，应返回明确错误，而不是在错误目录执行更新。

## Migration Notes
- 已安装用户升级到包含本功能的版本后，可以直接用 `openharness update` 替代旧手工更新命令。
- 旧手工命令仍然可用，但文档不再作为首选路径。

## Detailed Reflection
反思结论：

- 真实更新命令不适合在测试里直接跑，因此测试必须聚焦行为契约，而不是依赖外部网络和 git 状态。
- `update` 是安装层命令，不应该读取 task package 或 repo manifest；它只关心 OpenHarness 自身仓库位置和执行顺序。
