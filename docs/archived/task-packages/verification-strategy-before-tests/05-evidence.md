# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- TDD skill 仍保留强硬 red-green-refactor 语气；如果 agent 粗读并忽略前置边界，仍可能误用。当前通过显式适用对象和子 Agent 审查降低风险。
- `01-requirements.md` 保留“先明确验证策略”的短表达；`02` 和 `03` 已纠正为“先实现设计，再推导验证路径”。后续如果出现 agent 只读 `01` 的误用，应补 requirements wording cleanup。
- `check-tasks` 只证明任务包结构，不证明协议语义或 agent 行为；本轮用协议审查和 dry run 补足。

## Manual Steps
- 已人工复核 live wording diff，确认 `uv run pytest` 被限定为 testable code behavior 的自动化基线，TDD 被限定为 executable behavior 的实现内循环。
- 无待执行人工步骤。

## Files
- `skills/test-driven-development/SKILL.md`：收窄 TDD 适用边界，明确不替代 requirements / overview / detailed design。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`：明确 detailed design 先完成实现设计，再推导验证对象和证据路径。
- `skills/using-openharness/SKILL.md`：调整 `03-detailed-design.md` 对 testing / verification order 的职责表述。
- `README.md`：调整 Python-first pytest floor 的对外说明。
- `tests/openharness_cases/test_protocol_docs.py`：维护已有 README 协议测试的短边界断言。
- `docs/archived/task-packages/verification-strategy-before-tests/04-verification.md`：记录实际验证路径、traceability 和风险接受。
- `docs/archived/task-packages/verification-strategy-before-tests/05-evidence.md`：沉淀证据索引。
- `.project-memory/decisions/openharness_design_and_evidence_driven_verification.yaml`：保存本轮可复用决策。

## Commands
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- `uv run openharness check-tasks`
- `rg -n "default minimum automated verification floor|detailed testing-first design|NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST|Need to explore first|Production code →|先写 pytest|所有任务.*pytest|pytest-first" README.md skills/test-driven-development/SKILL.md skills/using-openharness/SKILL.md skills/using-openharness/references/detailed-design-writing-guidance.md docs/archived/task-packages/verification-strategy-before-tests`
- `uv run openharness project-memory save-decision openharness_design_and_evidence_driven_verification ...`
- `uv run openharness check-tasks`  # final verification command

## Artifact Paths
- `019dfde4-a43c-7cd3-8cb8-db5c3a9c1bc5`  # protocol review sub-agent result
- `019dfde4-a4a6-7ff1-9f15-d488b654ec67`  # dry run sub-agent result
- stdout from `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- stdout from `uv run openharness check-tasks`

## Follow-ups
- 如果后续发现 agent 只读 `01-requirements.md` 并复用“先明确验证策略”的短表达导致误用，应新增小修任务清理 requirements wording。
- 如果后续新增更强的 agent dry run harness，可以把当前子 Agent 手工 dry run 升级为可重复 runtime workflow；本轮不新增 RWP。
