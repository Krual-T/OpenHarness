# Verification

## Verification Path
- Planned Path: 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认任务包与 live docs 满足仓库协议；执行 `uv run pytest`，确认新增协议文案与模板断言通过。
- Executed Path: 已创建任务包并补全文档；已补做一轮有边界的多智能体设计评审，并将评审结论吸收到 `02-overview-design.md` 与 `03-detailed-design.md`；已把阶段门禁、角色注入、挑战闭环和收敛判据落到核心 skills、skill hub 与任务包模板；已执行 `uv run pytest skills/using-openharness/tests/test_openharness.py -q`、`uv run python skills/using-openharness/scripts/openharness.py check-tasks`、`uv run pytest` 与 `uv run python skills/using-openharness/scripts/openharness.py verify gstack-methodology`。
- Path Notes: 本轮虽然没有业务代码实现，但已经修改了 skill 文档、模板与仓库测试，因此必须运行测试而不是只做 task-package 校验；这轮验证的重点是任务包结构、live skill surface、模板结构与仓库断言一致性；中途发现 `STATUS.yaml.verification.last_run_result` 误写为 `pending`，已改为仓库接受的状态值后重新执行校验；设计验证不以“是否所有角色都发言”为标准，而以“是否补齐阶段门禁、挑战闭环、收敛判据”为标准。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- `gstack-methodology` 任务包被识别为有效 task package。
- 新增的 skill 协议文案与模板结构断言通过。
- 仓库全量测试不因本轮 productization 回归。

## Traceability
- `01-requirements.md` 要求把方法论真正落地到 skills，并为每个阶段补足门禁与收敛规则。
- `02-overview-design.md` 定义了按阶段组织、按角色注入的总体结构。
- `03-detailed-design.md` 把这些要求映射到具体 skill、模板与测试文件。
- 本节的验证命令用于确认这些文档与 live skill surface 已经一致。

## Risk Acceptance
- 当前接受的风险是：新的门禁与挑战闭环锚点尚未被 task-package validator 强制应用到全部历史包。
- 接受理由是：本轮目标是先把协议 productize 到 live skills、templates 与 tests，而不是连带发起一次历史任务包迁移。
- 重新触发审查的条件是：后续如果要把这些锚点升级为仓库级机械约束，必须单独开包迁移现有 task packages。

## Latest Result
- 已通过。`uv run python skills/using-openharness/scripts/openharness.py check-tasks` 成功验证 18 个任务包；`uv run pytest` 全量通过，共 56 个测试通过。
- Latest Artifact:
- `.harness/artifacts/001/verification-runs/20260324T142726186543Z.json`
