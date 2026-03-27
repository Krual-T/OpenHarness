# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 实现完成后运行 `uv run openharness check-tasks`。
  - 如果修改了 bootstrap 或相关测试表面，再运行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q` 与 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`。
  - 人工检查仓库入口、作者入口页、关键 stage skill 和模板是否形成一致导流。
- Executed Path:
  - 已实现中文作者入口页 `skills/using-openharness/references/author-entry.md`，并把它接入 `AGENTS.md`、`using-openharness`、关键 stage skill、`skill-hub`、五个模板和 `bootstrap` CLI。
  - 已执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`，结果为 `17 passed`。
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`，结果为 `48 passed`。
  - 已执行 `uv run openharness check-tasks`，确认实现后 task package 协议仍然通过。
- Path Notes:
  - 本轮的自动化验证已经覆盖 CLI 输出、协议文档表面和 task package 校验，足以支撑“入口优化已实现并通过仓库自测”的主张。
  - 仍未执行正式的人工中文使用者 walkthrough，因此残余风险要在 `Risk Acceptance` 中显式记录，而不是假装已经消失。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run openharness check-tasks`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`

## Expected Outcomes
- task package 协议保持通过。
- 中文作者入口与 guidance 导流在用户真实入口表面上可见。
- 模板提示更具体，但没有显著膨胀。

## Traceability
- `01-requirements.md` 要求解决中文入口不可见与 guidance 难发现的问题。
- `02-overview-design.md` 通过“单一中文作者入口 + 多表面导流 + 模板轻增强”定义总体方案。
- `03-detailed-design.md` 把实现落点约束为 `AGENTS.md`、关键 skill、模板、`skill-hub` 和可选 CLI 输出；这些改动已经全部落地。
- `test_cli_workflows.py` 证明 `bootstrap` 在作者入口存在时会把入口暴露到文本和 JSON 输出。
- `test_protocol_docs.py` 证明 `author-entry.md` 存在，并被关键 skill 与 `skill-hub` 共同引用。
- `check-tasks` 证明上述改动没有破坏 task package 协议表面。

## Risk Acceptance
- 当前接受“缺少正式人工 walkthrough 证据”的风险，因为本轮主要依赖仓库自动化验证与结构可见性来支撑完成主张。
- 如果后续仍有中文用户反馈 guidance 难发现，需要重新审查作者入口位置、CLI 输出文案和模板提示强度。

## Latest Result
- 最近一次结果是：`uv run pytest tests/openharness_cases/test_cli_workflows.py -q`、`uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 和 `uv run openharness check-tasks` 全部通过，足以支撑本轮实现进入归档收尾。
- Latest Artifact:
  - `.harness/artifacts/OH-034/verification-runs/20260327T025856540443Z.json`
