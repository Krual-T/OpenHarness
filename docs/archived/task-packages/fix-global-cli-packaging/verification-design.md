# Verification Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
本轮使用 `unit_test` 加安装态 smoke test 验证。核心是确认 wheel/tool 安装后的全局 Python 环境包含 `openharness_cli` 子包，并且全局 `openharness` 从仓库外执行 transition 不再使用旧 README scaffold。

## Required Commands
1. 命令：`uv tool install --force .`
   - 期望退出码：0
   - 期望输出：全局 `openharness` 从当前仓库重新安装成功。

2. 命令：`/home/Shaokun.Tang/.local/share/uv/tools/openharness/bin/python3 - <<'PY' ...`
   - 期望退出码：0
   - 期望输出：可以导入 `openharness_cli.models`，`TaskPackageDocument` 不包含 `README.md`，`scaffold_files(proposing)` 只包含 `task-info.yaml` 和 `requirements.md`。

3. 命令：`tmpdir=$(mktemp -d); cd "$tmpdir" && openharness --repo /home/Shaokun.Tang/Projects/openharness task-package transition TASK-004 overview_designing`
   - 期望退出码：0
   - 期望输出：transition 成功，不出现 `task-package.README.md` 缺失。
   - 验证后动作：将 `docs/task-packages/workflow-docs-skill-sharpening/task-info.yaml` 的 `status` 恢复为 `requirements_designed`。

4. 命令：`uv run pytest tests/openharness_cases -q`
   - 期望退出码：0
   - 期望输出：OpenHarness case 测试通过。

## Expected Outcomes
- 全局安装包包含 `openharness_cli.models`、`openharness_cli.core`、`openharness_cli.commands`。
- 全局 CLI 不再加载旧 skill-hub 克隆里的代码。
- 全局 transition 不再尝试补建 README 模板。
- 本地测试不因 packaging 配置变更退化。

## Traceability
- Required Outcome 1 → 全局 Python 导入 smoke test。
- Required Outcome 2 → 全局 Python 输出 `openharness_cli.__file__` 和文档枚举。
- Required Outcome 3 → 仓库外全局 transition smoke test。

## Risk Acceptance
- 不修改 `openharness update` 逻辑；本轮只确保重新安装出来的全局工具可用。
- 不删除旧 skill-hub 克隆；只验证全局工具不再加载它。
