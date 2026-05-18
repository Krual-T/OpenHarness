# Verification Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
本轮使用 `unit_test` 验证。核心路径是 `validate_task_package()` 对含 stale `entrypoints` 的任务包不再报 `missing referenced path`，同时保留其他校验能力。

## Required Commands
1. 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py -q`
   - 期望退出码：0
   - 期望输出：`test_validate_task_package_rejects_unknown_status_but_allows_stale_entrypoints` 通过，且文件内其他任务包核心测试通过。

2. 命令：`uv run pytest tests/openharness_cases -q`
   - 期望退出码：0
   - 期望输出：OpenHarness case 测试通过。

3. 命令：`rg -n "missing referenced path|_referenced_path_exists" openharness_cli`
   - 期望退出码：1
   - 期望输出：无匹配，表示生产代码不再生成 entrypoints 路径存在性错误。

## Expected Outcomes
- 含 `docs/task-packages/<task>/README.md` stale entrypoint 的 active package 校验不再产生 `missing referenced path`。
- 未知状态等其他校验仍然生效。
- `TaskInfo.entrypoints` 字段未被删除，兼容读取和序列化仍保留。

## Traceability
- Required Outcome 1 → `test_validate_task_package_rejects_unknown_status_but_allows_stale_entrypoints`。
- Required Outcome 2 → 不修改 `TaskInfo.entrypoints`，全量 case 测试通过。
- Required Outcome 3 → 定向 pytest 和 `rg` 扫描。

## Risk Acceptance
- 不验证所有历史任务包，因为本轮行为是放宽可选字段路径校验，历史数据无需迁移。
- 不删除 `entrypoints` 字段；字段完全移除属于另一个兼容性决策。
