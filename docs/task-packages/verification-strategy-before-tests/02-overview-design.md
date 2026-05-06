# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 OpenHarness 的“设计、测试与验证证据如何衔接”的协议面，重点解决 agent 把 TDD 误读成“任何改动都先写 pytest”的问题。

覆盖范围：

- `skills/test-driven-development/SKILL.md`：修正 TDD 的触发边界，明确它是适用于可执行行为和可观察代码契约的实现内循环，不是替代需求、overview design 或 detailed design 的总流程。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`：修正 `testing-first` 口径，明确 detailed design 必须先回答实现落点、接口边界、行为契约、数据语义、失败模式和迁移顺序，再从这些设计结论推导验证对象与证据路径。
- `skills/using-openharness/SKILL.md`、`README.md` 与相关 guidance：保留 Python-first 仓库的 `uv run pytest` 自动化基线，但明确这个基线不等于所有任务都必须写 pytest，也不等于 runtime、协议或 agent 行为已经被验证。
- `skills/verification-before-completion/SKILL.md`、`verification-writing-guidance.md`、`evidence-writing-guidance.md`：保持 fresh evidence 门槛，确保选择非自动测试路径时仍然要记录执行过的审查、dry run、runtime workflow、人工场景验证或结构检查证据。
- `tests/openharness_cases/test_protocol_docs.py`：只在需要锁定 live protocol wording 时补充协议文档测试，避免把测试写成无意义的文档片段存在性断言。

不覆盖范围：

- 不新增 CLI。
- 不新增 Runtime Workflow Package。
- 不重构 pytest 框架。
- 不把 `check-tasks` 升级成自然语言质量评分器。
- 不废除 TDD；TDD 对可执行代码、CLI、解析器、校验器、状态机等对象仍然是推荐的实现方法。
- 不把子 Agent 审核写成唯一默认；它是协议、skill 行为和 agent 工作流类对象的强候选证据路径，但最终仍由 detailed design 根据验证对象选择最强证据组合。

已确认设计点：OpenHarness 外层采用“设计与证据驱动开发”，内层按验证对象选择 TDD、ATDD/BDD 风格验收例子、子 Agent 协议审查、dry run、runtime workflow、人工场景验证或结构检查。TDD 不是“先测试再设计”；它发生在 detailed design 足够具体之后、实现之前。

## Proposed Structure
推荐结构分成三层：

1. 任务包阶段层：`01-requirements.md`、`02-overview-design.md` 和 `03-detailed-design.md` 先收敛要解决的问题、系统边界和实现设计。这个层次负责让 agent 和人类先知道“要做什么、为什么这样做、实现边界在哪里”。
2. 证据选择层：`03-detailed-design.md` 在实现细节足够清楚后，基于验证对象选择证据路径。验证对象可以是可执行代码行为、CLI 契约、解析器规则、文档语义、协作协议、skill 行为、agent 工作流或 runtime 观察。
3. 执行方法层：当验证对象适合自动化测试时，使用 TDD 的 red-green-refactor 内循环；当验证对象不适合 pytest 时，使用协议审查、子 Agent dry run、场景复盘、runtime workflow、人工验证记录或结构检查。

关键约束是依赖方向只能从设计推导验证，不能反过来让“必须先写 pytest”决定设计。测试是一类证据路径，不是 OpenHarness 唯一的合规入口。

## Key Flows
主流程仍然保持 OpenHarness 既有 task package 阶段：

1. `01-requirements.md` 定义问题、目标用户、验收标准、非目标和约束。
2. `02-overview-design.md` 定义系统边界、总体结构、关键取舍和架构级失败模式。
3. `03-detailed-design.md` 先完成实现设计，再从设计结论推导验证对象和证据路径。
4. Implementation 按 `03-detailed-design.md` 执行；如果验证对象适合 TDD，就先写失败测试再实现；如果不适合自动测试，就按已设计的协议审查、dry run、runtime workflow、人工场景验证或结构检查执行。
5. `04-verification.md` 记录实际执行了哪些验证、结果、偏差、限制、traceability 和残余风险。
6. `05-evidence.md` 沉淀变更文件、命令、子 Agent 审查结果、dry run 记录、人工步骤和产物路径。

`03-detailed-design.md` 内部有一个子流程，但它不是新的 task package 阶段：

1. 先回答实现设计问题：改动落点、接口边界、行为契约、数据语义、失败模式、误用风险和迁移顺序。
2. 再识别验证对象：可执行代码行为、CLI 契约、解析器规则、校验器逻辑、状态机、文档语义、协作协议、skill 行为、agent 工作流、runtime 观察或机械结构改动。
3. 再选择证据路径：TDD / 自动测试、ATDD/BDD 风格验收例子、协议审查、子 Agent dry run、runtime workflow、人工场景验证、结构检查或组合路径。
4. 最后写清 expected evidence，让 `04-verification.md` 和 `05-evidence.md` 知道后续必须收什么。

关键失败信号有三类：

- 在 `03-detailed-design.md` 之前就要求先写 pytest，说明 TDD 被错误提前成总流程入口。
- `03-detailed-design.md` 没有实现细节，只写“验证策略”，说明设计被证据选择替代。
- `04-verification.md` 只有 pytest 或 `check-tasks`，但没有证明协议、skill 行为、agent 工作流或 runtime 观察真的成立，说明证据路径与验证对象错配。

## Stage Gates
`02-overview-design.md` 进入 `03-detailed-design.md` 前，必须满足以下条件：

- 外层阶段流保持为 `01 -> 02 -> 03 -> Implementation -> 04 -> 05`，不新增“验证对象分类”这类并列 task package 阶段。
- TDD 被定义为适用于特定验证对象的实现内循环，不能提前到 detailed design 之前替代设计。
- `03-detailed-design.md` 必须先写清实现设计，再写验证对象、证据路径和 expected evidence。
- 证据路径必须匹配验证对象；不能用 pytest 字符串断言替代协议、skill 行为、agent 工作流或 runtime 观察的真实验证。
- 非自动测试路径仍必须产生 fresh evidence，包括审查结论、dry run 记录、runtime workflow 输出、人工场景观察、结构检查结果或这些证据的组合。
- Python-first 的 `uv run pytest` 可以继续作为代码类改动的自动化基线，但不能被解释成所有任务都必须新增 pytest。

如果后续 detailed design 仍无法回答“实现设计是什么”和“这些设计结论分别由什么证据证明”，就不能进入 `in_progress`。

## Trade-offs
推荐方案是“设计与证据驱动开发”：先按 task package 阶段完成需求、overview 和 detailed design，再按验证对象选择 TDD、自动测试、协议审查、子 Agent dry run、runtime workflow、人工场景验证或结构检查。

收益：

- 保留 TDD 对可执行行为的工程价值，同时避免把 TDD 误用到不适合自动测试的对象上。
- 让 agent 在写测试前先理解实现设计，减少形式主义 pytest 和错误抽象。
- 让非自动测试路径也有严肃证据，继续满足 `verification-before-completion` 的 fresh evidence 要求。

代价：

- detailed design 需要更明确地写出验证对象和 expected evidence，不能只列文件或命令。
- 某些协议或 agent 行为类任务需要子 Agent 审查、dry run 或场景复盘，验证成本比简单字符串断言更高。
- 自动化覆盖率数字不会覆盖全部工作，需要在 `04-verification.md` 和 `05-evidence.md` 里解释不同证据的 traceability。

拒绝的备选方案一：所有任务默认 pytest-first。

这个方案看似统一，但会把文档语义、协作协议、skill 行为和 agent 工作流降级成“文本片段存在性”测试，无法证明 agent 会按规则行动。它会制造假安全感，正是 OH-042 暴露的问题。

拒绝的备选方案二：非代码任务默认人工判断即可。

这个方案能避免无意义 pytest，但会削弱 OpenHarness 的证据纪律。没有 fresh evidence、traceability 和残余风险记录时，维护者无法复盘 agent 到底验证了什么，也和 `verification-before-completion` 冲突。

接受的中间方案：自动测试是强证据路径之一，不是唯一入口。设计先行，证据路径按对象选择；当对象不适合 pytest 时，必须用更贴合对象的审查、dry run、runtime 或人工场景证据补足。

## Recommended Diagrams
如果某些结构关系仅靠文字容易歧义，用中文说明推荐补哪些 `PlantUML` 图，例如系统上下文图、模块图或主流程图；图不能替代文字里的边界、约束和例外。

## Overview Reflection
用中文记录一轮反思，明确你挑战过哪些备选方案、风险假设和验证影响，并写明挑战是接受、拒绝还是延期。
