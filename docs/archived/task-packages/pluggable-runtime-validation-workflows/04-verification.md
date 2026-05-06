# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先用 TDD 锁住 `openharness rwp` parser、`list/show/run` 行为和 `openharness.rwp.get_logger()` runtime API；再把 runtime capability 文档从旧 helper/surface 术语迁移到 RWP；最后执行 `uv run pytest` 与 `uv run openharness check-tasks` 作为本轮 command-backed verification。
- Executed Path: 已先运行针对 RWP 的红灯测试，确认缺少 `rwp` 命令、`cmd_rwp` 和 `openharness.rwp` 包时测试失败；实现后执行 targeted pytest，确认 RWP CLI/API 测试通过；随后执行 `uv run pytest`，结果为 201 个测试全部通过。
- Path Notes: 当前验证覆盖 CLI 行为、runtime API、协议文档和 task package 校验。没有执行真实 Lark/飞书 runtime workflow，因为本轮目标是 OpenHarness RWP 协议与最小执行外壳，不实现具体下游 workflow。

## Required Commands
- `uv run pytest`
  - 已执行，结果为 201 passed。
- `uv run openharness check-tasks`
  - 已通过 `openharness verify pluggable-runtime-validation-workflows` 执行，结果为通过。

## Expected Outcomes
- `openharness` parser 暴露 `rwp` 子命令。
- `openharness rwp list` 能从 `.harness/rwp/workflows/*/workflow.md` 读取 `name`、`description` 和路径。
- `openharness rwp show <workflow>` 能输出完整 `workflow.md`。
- `openharness rwp run <workflow> <script.py> [args...]` 显式运行 workflow `scripts/` 下的 Python 脚本，并加载 `.harness/.env` 与 `.harness/rwp/.env`。
- `from openharness.rwp import get_logger` 可用，且 `get_logger()` 返回标准 logger。
- 核心文档以 RWP 作为 runtime workflow 主概念，不再把旧 helper/surface 作为主路径。

## Traceability
- `01-requirements.md` 要求 RWP 能被 agent 渐进发现、读取详情、执行并写回 task package；`tests/openharness_cases/test_rwp_workflows.py` 覆盖 `list/show/run` 和 `get_logger()`。
- `02-overview-design.md` 要求 RWP 不走 `SKILL.md`，由 OpenHarness CLI 控制披露；`runtime-workflow-packages.md` 和 `runtime-capability-contract.md` 已记录该协议。
- `03-detailed-design.md` 要求先测 parser/CLI/runtime API，再迁移文档；本轮执行顺序按该路径完成。

## Risk Acceptance
- 本轮没有提供真实项目的 RWP 样例目录；后续可以由具体项目在 `.harness/rwp/workflows/` 下接入。
- 本轮只支持 `.py` 脚本；其他语言或跨语言 runner 需要后续任务包另行设计。
- `get_logger()` 当前只返回标准 logger，不负责日志落盘策略；日志组织由具体 workflow 决定。

## Latest Result
- Latest Result: `uv run openharness verify pluggable-runtime-validation-workflows` 已 fresh 执行并通过；artifact 记录 `uv run pytest` 与 `uv run openharness check-tasks` 均为 exit code 0。
- Latest Artifact: `.harness/artifacts/OH-040/verification-runs/20260506T054719836818Z.json`
