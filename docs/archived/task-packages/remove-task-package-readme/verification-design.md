# Verification Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
本轮使用 `unit_test` 验证。主路径是定向运行任务包协议相关测试，再运行 OpenHarness 自身任务包校验。

验证覆盖四个行为面：

1. 新建任务包不再创建 `README.md`。
2. workflow required/scaffold/section 校验不再要求 README。
3. 旧 `entrypoints` 字段仍可被解析、校验和归档路径改写。
4. 删除 README 模板后，创建任务包的 YAML quoting 行为不退化。

## Required Commands
1. 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_yaml_quoting.py -q`
   - 期望退出码：0
   - 期望输出：所有定向测试通过。

2. 命令：`uv run pytest tests/openharness_cases -q`
   - 期望退出码：0
   - 期望输出：OpenHarness 自身 case 测试通过，表示任务包创建、推进、归档、校验和协议文档回归未受本轮改动破坏。

3. 命令：`rg -n "TaskPackageDocument\\.README|task-package\\.README|Current Status|Read This First" openharness_cli skills/using-openharness tests -g '!**/__pycache__/**'`
   - 期望退出码：1
   - 期望输出：无匹配，表示活跃协议、模板和测试不再引用 per-task README 模板或 README 状态章节。

## Expected Outcomes
- CLI 文档模型不再包含 README：定向测试不会引用 `TaskPackageDocument.README`，扫描命令无旧符号残留。
- 模板不再生成 README：创建任务包测试断言目标目录没有 `README.md`。
- 校验不再要求 README：overview 校验测试只关注 `overview-design.md` 的 `Overview Reflection` 等阶段章节。
- 历史兼容保留：归档测试中的已有 `entrypoints` 路径仍被改写到 archived 目录，但不再包含 README。
- `task-info.yaml` quoting 行为保留：YAML quoting 测试继续通过。

## Traceability
- Required Outcome 1 → 扫描命令、`test_task_package_core.py`、`test_cli_workflows.py`。
- Required Outcome 2 → 创建任务包测试、模板文件删除、YAML quoting 测试。
- Required Outcome 3 → 归档路径改写测试、`TaskInfo.entrypoints` 保留。
- Required Outcome 4 → CLI reference 内容扫描、定向 pytest、全量 `tests/openharness_cases`。

## Risk Acceptance
- 不验证 archived 历史包内容被批量迁移，因为本轮明确不迁移历史证据。
- 不删除并验证 `TaskInfo.entrypoints` 字段，因为本轮仅从默认任务包流程移除 README；字段完全删除属于单独兼容性任务。
- 不运行仓库外部集成或 RWP 作为硬门禁；本轮代码路径集中在任务包协议，定向 pytest 加全量 `tests/openharness_cases` 足以覆盖核心风险。
