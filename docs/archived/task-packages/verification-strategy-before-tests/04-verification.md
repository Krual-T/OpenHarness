# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 主路径是先完成 live wording 实现，再用协议审查、子 Agent dry run、人工复核和 `uv run openharness check-tasks` 验证。pytest 不是主验证路径；仅维护已有 README 协议文档测试的短边界断言，作为辅助防回归证据。
- Executed Path: 已修改 `skills/test-driven-development/SKILL.md`，把 TDD 限定为 detailed design 之后、适用于可执行行为和可观察代码契约的实现内循环；已修改 `skills/using-openharness/references/detailed-design-writing-guidance.md`，明确 detailed design 先写实现设计，再推导验证对象、验证路径和预期证据；已修改 `skills/using-openharness/SKILL.md`，把 `03-detailed-design.md` 的职责改成实现设计加对象适配的测试或验证顺序，明确这不代表 detailed design 前先写测试；已修改 `README.md`，把 `uv run pytest` 表述为 testable code behavior 的默认自动化基线，并说明它不证明文档语义、协作协议、skill 行为或 agent workflow；已同步维护 `tests/openharness_cases/test_protocol_docs.py` 中既有 README 防回归测试，使其断言新的短边界；已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`，结果为 `52 passed`；已执行 `uv run openharness check-tasks`，结果为校验 45 个 task package 通过；已执行旧误导 wording 扫描，未发现 `default minimum automated verification floor`、`detailed testing-first design`、旧 TDD iron law 文本或相关旧短语残留；已完成两个只读子 Agent 验证：
  - 协议审查 Agent 结论：通过；未发现阻塞性误导 wording；当前 live wording 不会明显诱导 TDD 提前到 design 之前，也没有把 pytest 表达成所有任务的默认主验证路径。
  - dry run Agent 结论：通过；面对“不涉及可执行代码的协作协议或 skill 行为规则修改”，会先完成 task package design，并选择协议审查、dry run、人工复核和 `check-tasks`，不倾向 pytest-first。
- Path Notes: pytest 本轮只证明 README 协议文档的短边界没有回归，不证明 agent 行为本身。子 Agent 审查和 dry run 是本轮最关键证据，因为验证对象是协议 wording 与 agent 行为引导。`check-tasks` 只证明 task package 结构有效，不证明协议语义正确；该限制已在风险中接受并记录。

## Required Commands
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run openharness check-tasks
- rg -n "default minimum automated verification floor|detailed testing-first design|NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST|Need to explore first|Production code →|先写 pytest|所有任务.*pytest|pytest-first" README.md skills/test-driven-development/SKILL.md skills/using-openharness/SKILL.md skills/using-openharness/references/detailed-design-writing-guidance.md docs/archived/task-packages/verification-strategy-before-tests

## Expected Outcomes
- 目标协议文档测试应通过，说明已有 README 协议测试已更新到新的短边界。
- `check-tasks` 应通过，说明 active / archived task package 结构和状态写回没有破坏仓库协议。
- 旧误导 wording 扫描不应命中 live wording 中的旧表达。
- 协议审查 Agent 应确认 TDD 不再替代 design，pytest 不再被表达为所有任务默认主路径。
- dry run Agent 应在非可执行协议或 skill 行为任务中选择协议审查 / dry run / 人工复核 / `check-tasks`，而不是 pytest-first。

## Traceability
- 需求 1 “验证策略先于测试实现”已按 corrected design 落成“先完成 detailed design 的实现设计，再按验证对象选择测试或验证”。证据是 `detailed-design-writing-guidance.md` 的 wording、协议审查 Agent 结论和 dry run Agent 结论。
- 需求 2 “TDD 只适用于可执行行为等适合自动测试的对象”由 `skills/test-driven-development/SKILL.md` 的触发边界、do-not-use 列表和 dry run 结论支撑。
- 需求 3 “文档语义、协作协议、skill 行为规则等可采用协议审查、子 Agent dry run、runtime workflow 或人工场景验证”由 README、TDD skill、detailed guidance 的 object-appropriate evidence 表述，以及两次子 Agent 结论支撑。
- 需求 4 “跳过不合适 pytest 不违反工作流”由 `03-detailed-design.md` 的主验证路径、live wording 和 dry run 结果支撑；dry run 明确不倾向 pytest-first。
- 需求 5 “非自动测试仍必须记录严肃证据”由本页、`05-evidence.md`、子 Agent 记录和 `check-tasks` 结果支撑。

## Risk Acceptance
- 接受残余风险：agent 如果只粗读 TDD skill 的强硬段落，仍可能被 TDD 语气带偏。但 skill 前置边界已经限定为 executable behavior，协议审查 Agent 判断该风险非阻塞。
- 接受残余风险：`01-requirements.md` 仍有“先明确验证策略”的短表达，但 `02` 和 `03` 已纠正为“先实现设计，再推导验证路径”。后续若发现 agent 只读 `01` 并复用旧简称，应再补一轮 requirements wording cleanup。
- 接受残余风险：`check-tasks` 不能证明协议语义或 agent 行为。该风险通过子 Agent 审查和 dry run 补足；后续若 dry run 缺失或失败，不能宣称协议行为充分验证。

## Latest Result
- 最近一次验证结果：通过。目标协议文档测试通过，`check-tasks` 通过，两个子 Agent 均给出通过结论。
- Latest Artifact: 子 Agent `019dfde4-a43c-7cd3-8cb8-db5c3a9c1bc5` 协议审查结论；子 Agent `019dfde4-a4a6-7ff1-9f15-d488b654ec67` dry run 结论；stdout from `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` and `uv run openharness check-tasks`
