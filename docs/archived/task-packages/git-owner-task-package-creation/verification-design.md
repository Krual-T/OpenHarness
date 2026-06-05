# 验证策略

## 验证路径

- **计划路径**：用 pytest 覆盖核心创建和 CLI 参数表面，再运行 OpenHarness case 回归和任务包校验。
- **回退路径**：如果未知参数错误文本不稳定，测试不依赖完整文案，只断言退出非零和目标任务包未创建；如果生成 owner 或帮助文本不能自动断言，则不能完成本包。
- **路径说明**：本轮是 CLI 与模板替换的可编程行为，`unit_test` 能直接判断输入、输出和错误路径。已执行 `uv run openharness rwp list`，没有可用 RWP，也不需要端到端运行工作流。

## 必需命令

1. `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
   - 期望退出码：0
   - 期望输出：核心任务包测试通过，包含 Git owner 注入和 `--owner` 拒绝场景。

2. `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
   - 期望退出码：0
   - 期望输出：协议文档和 CLI 帮助表面测试通过，`task-package new --help` 不包含 `--owner`。

3. `uv run pytest tests/openharness_cases -q`
   - 期望退出码：0
   - 期望输出：OpenHarness case 回归通过。

4. `uv run openharness task-package list`
   - 期望退出码：0
   - 期望输出：列出当前活跃任务包，包含 `TASK-022`。

5. `uv run openharness task-package view TASK-022`
   - 期望退出码：0
   - 期望输出：显示当前任务包详情和当前阶段指令。

## 预期结果

- 新建任务包时，`task-info.yaml.owner` 等于临时仓库中 `git config user.name` 设置的值。
- 生成文本不包含 `<GIT OWNER>`。
- `openharness task-package new --help` 不显示 `--owner`。
- `openharness task-package new ... --owner someone` 退出非零，且不会创建目标任务包。
- 当前任务包能通过 `task-package list` 和 `task-package view TASK-022` 被 CLI 发现和查看。

## 可追溯性

- 需求“模板继续使用 `<GIT OWNER>`，代码负责替换”对应 `test_task_package_core.py` 中生成文件 owner 和占位符残留断言。
- 需求“CLI 不允许 `--owner` 参数”对应 CLI 帮助文本断言和未知参数拒绝测试。
- 需求“Git 本地未配置时读取有效配置链”对应临时仓库只设置 Git 配置后创建任务包的自动化测试；Git 命令本身负责本地、全局、系统配置解析。
- 需求“不影响现有任务包流程”对应 OpenHarness case 回归、`task-package list` 和 `task-package view TASK-022`。

## 风险接受

- 不覆盖历史归档任务包 owner 批量修复，因为本轮明确只修新建路径。
- 不覆盖所有 Git 配置层级的矩阵测试；`git config user.name` 是 Git 自身行为，本轮只验证 OpenHarness 调用该命令并使用返回值。
- 不覆盖 Typer 具体错误文案，避免测试绑定第三方库文案。

## 验证执行计划

实现前先修改或新增聚焦测试，确认当前行为失败；实现后立即执行必需命令。任何必需命令失败，都回到 `implementing` 修改实现或回到 `verification_designing` 修正验证策略。
