# 计划

## 目标与上下文

修复 `openharness update` 的源码同步失败体验：同步命令失败时自动最多尝试 3 次，并把每次失败的命令、退出码、stdout 和 stderr 摘要打印出来。

## 输入文档

- `requirements.md`

## 实施步骤

- [x] 增加带重试的同步命令执行 helper
  - 修改对象：`openharness_cli/commands/update.py`、`openharness_cli/main.py`
  - 完成条件：`git pull`、`git fetch --prune`、`git reset --hard @{u}` 都通过 helper 执行，失败最多重试 3 次。
  - 验证方式：单元测试模拟 subprocess 返回码。

- [x] 增加失败详情输出
  - 修改对象：`openharness_cli/commands/update.py`、`openharness_cli/main.py`
  - 完成条件：每次失败输出 attempt、命令、返回码、stdout 摘要、stderr 摘要。
  - 验证方式：测试断言 stdout 包含失败详情。

- [x] 更新 update 命令测试
  - 修改对象：`tests/openharness_cases/test_cli_workflows.py`、`tests/openharness_cases/test_entrypoint.py`
  - 完成条件：覆盖重试后成功、三次失败后退出、force-sync 命令重试、依赖缺失兜底入口失败时不继续升级。
  - 验证方式：运行聚焦测试。

## 文件修改计划

- `openharness_cli/commands/update.py`：承载更新命令行为；新增 helper 避免 pull 和 force-sync 分叉重复。
- `openharness_cli/main.py`：承载依赖缺失时的 `openharness update` 兜底入口；同步改为失败重试并阻断升级。
- `tests/openharness_cases/test_cli_workflows.py`：已有 update 行为测试所在地，继续在此覆盖重试和错误输出。
- `tests/openharness_cases/test_entrypoint.py`：覆盖兜底入口的失败重试和阻断升级行为。
- `pyproject.toml`：提交前 patch bump。
- `docs/task-packages/update-retry-error-reporting/evidence.md`：记录验证证据。

## 验证设计

- **必需命令**：
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py -v`
  - `uv run pytest tests/ -v`
- **预期结果**：
  - 聚焦测试通过。
  - 全量测试通过。
  - 失败路径输出包含失败详情。

## 进度记录

- [x] 需求已写入。
- [x] 实现重试和报错输出。
- [x] 测试通过。

## 决策与发现

- 本轮只重试源码同步命令，不重试 `uv tool upgrade`。升级失败通常不是 GitHub 同步抖动，保留现有直接失败行为。
- 不自动代理。代理选择依赖用户环境，CLI 不应隐式改变网络路径。

## 风险接受

- 重试之间不增加 sleep。接受理由：本轮需求是显示报错和自动重试 3 次，避免引入等待配置和测试时间成本。

## 完成判定

- `update.py` 同步命令失败时会输出每次失败详情并重试。
- 3 次失败后不执行工具升级。
- 聚焦测试和全量测试通过。
