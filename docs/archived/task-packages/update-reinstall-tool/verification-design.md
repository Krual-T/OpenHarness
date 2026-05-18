# Verification Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
本轮使用 `unit_test`。通过 monkeypatch `subprocess.run` 验证 `openharness update --mode pull` 先执行 `git pull`，再执行 `uv tool upgrade --reinstall openharness`。

## Required Commands
1. 命令：`uv run pytest tests/openharness_cases/test_entrypoint.py -q`
   - 期望退出码：0
   - 期望输出：entrypoint/update 相关测试通过。

2. 命令：`uv run pytest tests/openharness_cases -q`
   - 期望退出码：0
   - 期望输出：OpenHarness case 测试通过。

## Expected Outcomes
- update 的工具刷新 subprocess 参数包含 `--reinstall`。
- help 文本和顶层 entrypoint 仍正常。
- 不实际执行 git pull 或 uv tool upgrade。

## Traceability
- Required Outcome 1 → `test_update_reinstalls_existing_tool_source`。
- Required Outcome 2 → 全量 OpenHarness case 测试。

## Risk Acceptance
- 不在测试中真实更新全局 tool，避免测试修改开发者环境。
