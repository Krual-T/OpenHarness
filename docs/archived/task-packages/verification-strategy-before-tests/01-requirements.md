# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
目标是调整 OpenHarness 的测试与验证指导原则：agent 在进入实现前，必须先在 `03-detailed-design.md` 中明确验证策略，再决定是否需要自动测试。

单一成功指标：新会话 agent 面对一个开发任务时，能根据验证对象选择合适证据路径，而不是默认把“写 pytest”套用到文档、协作协议、skill 语义或非可执行行为上。

## Problem Statement
目标用户是使用 OpenHarness 维护 task package、skill 和项目工作流的 agent 与人类维护者。

核心场景来自 OH-042：在实现“逐项设计确认”时，最初倾向于给协议文档新增 pytest 字符串断言。用户指出这会变成形式主义，因为测试只能证明某些文档片段存在，不能证明 agent 会按协议行动。随后任务改用“子智能体协议审查 + `openharness check-tasks`”，实际效果更贴近验证对象。

当前缺口是：`test-driven-development` skill 和 detailed design guidance 容易被理解成“任何改动都必须先写自动测试”，但真实工程里验证对象不同：

- 可执行代码逻辑适合自动测试和 TDD。
- CLI 行为、解析器、校验器、状态机适合自动测试。
- 文档语义、协作协议和 skill 行为规则更适合协议审查、子智能体 dry run 或场景复盘。
- runtime 行为更适合 Runtime Workflow Package 或项目自己的运行时验证流程。
- 机械改动只需要最小结构检查、格式检查或目标命令验证。

为什么现在要做：OH-042 已经把问题暴露成真实流程摩擦。如果不修正，后续 agent 可能继续把 TDD 误用成形式化 pytest 要求，既增加维护成本，又给人一种“测了但没真正验证”的假安全感。

## Required Outcomes
1. OpenHarness 文档明确“验证策略先于测试实现”。
   - Acceptance criteria: `03-detailed-design.md` guidance 或相关 skill 明确要求先定义验证对象、证据路径和适用验证方式，再决定是否写自动测试。
2. `test-driven-development` skill 的适用边界被修正或补充。
   - Acceptance criteria: 它不再被解释为所有文档、协议、配置和非可执行行为都必须先写 pytest；它应明确自动测试适用于可执行行为和可观察代码契约。
3. OpenHarness 能表达不同验证方式。
   - Acceptance criteria: 文档能区分自动测试、协议审查、子智能体 dry run、runtime workflow、人工场景验证、结构检查等路径，并说明各自适用对象。
4. agent 不应因为跳过不合适的 pytest 就违反工作流。
   - Acceptance criteria: 当 detailed design 选择非自动测试验证方式并给出理由时，工作流视为合规。
5. 验证证据仍然必须严肃记录。
   - Acceptance criteria: 即使不用自动测试，`04-verification.md` 和 `05-evidence.md` 仍必须记录执行过的验证路径、观察结果、限制和残余风险。

## Non-Goals
- 不废除 TDD。TDD 对可执行代码、CLI、解析器、校验器、状态机仍然有效。
- 不取消验证要求。相反，本轮要让验证更贴合对象，而不是用形式化测试替代真实证据。
- 不为所有任务设计复杂测试矩阵；本轮只定义协议和指导原则。
- 不新增 runtime workflow 本身；runtime 验证路径仍由 RWP 或项目具体 workflow 承担。
- Counterexample: 修改一个纯 Markdown 协作协议时，强行写 pytest 断言某几句话存在，不应被视为本轮鼓励的验证方式。

## Constraints
- 必须兼容现有 task package 阶段流：`requirements_ready`、`overview_ready`、`detailed_ready`、`in_progress`、`verifying`、`archived`。
- 必须保留 `verification-before-completion` 的 fresh evidence 要求，不能把“选择非自动测试”变成免验证。
- 必须避免和 OH-042 刚引入的逐项设计确认冲突；该任务应默认按逐项设计确认推进。
- 建议任务分类：`protocol/architecture`，但需要新会话中由人类确认后再写入 `STATUS.yaml.collaboration.task_type`。
- Cost cap: 本轮优先改 skill 和 writing guidance，不引入新 CLI、不重构测试框架、不新增大型自动化系统。
