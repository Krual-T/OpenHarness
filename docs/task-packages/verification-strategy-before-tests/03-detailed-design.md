# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
Verification Path:

1. 先完成本 `03-detailed-design.md`，把实现落点、接口边界、行为契约、误用风险、迁移顺序和证据路径写清楚；在 detailed design 未完成前，不安排 pytest-first 或 live docs 改动。
2. Implementation 阶段按 detailed design 修改 live protocol / guidance / README wording。
3. Verification 阶段以协议审查和子 Agent dry run 为主证据，检查新 wording 是否仍会诱导 agent 把 TDD 提前到 design 之前，或对非可执行对象硬写 pytest。
4. 执行 `uv run openharness check-tasks`，只用于证明 task package 结构和状态写回没有破坏仓库协议。
5. 人工复核关键 wording，确认它表达的是“先设计，再按验证对象选择证据路径”，而不是“先测试再设计”。

Fallback Path:

- 如果子 Agent dry run 无法执行，不能宣称协议行为已经充分验证；`04-verification.md` 必须把缺失 dry run 记录为 residual risk，并用人工协议审查 + `uv run openharness check-tasks` 作为不足但可追溯的 fallback。
- 如果后续发现某个旧误导性 wording 很容易回归，可以追加极薄的 `tests/openharness_cases/test_protocol_docs.py` 文本边界测试；该测试只能作为辅助防回归，不作为主验证路径，也不能替代协议审查。
- 如果 `check-tasks` 失败，先修复 task package 结构或状态写回，再继续实施；不能把失败结构作为已知风险带入完成状态。

Planned Evidence:

- 子 Agent 协议审查或 dry run 的结论摘要，重点观察是否还会选择 pytest-first 来验证协议、skill 行为或 agent 工作流。
- 人工复核记录，说明关键 live wording 是否符合“detailed design 先行、证据路径按对象选择”的结论。
- `uv run openharness check-tasks` 的 fresh 输出。
- 如果采用可选薄文本测试，记录该测试只覆盖防回归 wording，不覆盖 agent 行为本身。
- `04-verification.md` 需要写清 traceability：每条核心需求由哪类证据支撑，哪些证据不足，以及残余风险是什么。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
本轮只修改 live protocol / guidance / README，不修改 archived task packages，不新增 CLI、Runtime Workflow Package 或测试框架。测试文件不是计划主改动面；只有发现具体 wording 回归风险值得自动锁定时，才追加极薄的辅助文本边界测试。

- `skills/test-driven-development/SKILL.md`
  - 修正 TDD 的触发边界，把它定义成 detailed design 之后、implementation 之前的实现内循环。
  - 明确 TDD 适用于可执行行为、CLI、解析器、校验器、状态机和可观察代码契约。
  - 改写“所有 feature / behavior change 都必须无条件 TDD”的绝对口径，避免 agent 把文档语义、协作协议、skill 行为或 agent 工作流也硬套 pytest。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
  - 修正 `testing-first` 的含义：`03` 必须先完成实现设计，再从设计推导验证对象和证据路径。
  - 把“先准备测试或验证，再落实现”明确成按对象选择测试、协议审查、dry run、runtime workflow、人工场景验证或结构检查，而不是默认先写 pytest。
- `skills/using-openharness/SKILL.md`
  - 调整入口协议里关于 `03-detailed-design.md` owns `testing-first` 的 wording，避免 agent 误读成 detailed design 之前先写测试。
  - 保留现有 task package 阶段流、runtime capability routing 和 fresh verification writeback 要求。
- `README.md`
  - 保留 Python-first `uv run pytest` 自动化基线，但说明它主要覆盖代码类改动，不是所有任务的唯一验证路径。
  - 明确 runtime、协议、skill 行为和 agent 工作流仍需要在 task package 中设计更贴合对象的证据路径。
- `tests/openharness_cases/test_protocol_docs.py`
  - 默认不改。
  - 仅当 implementation 过程中发现某个短 wording 边界存在高回归风险时，才补充极薄的辅助文本测试。
  - 即使补充测试，也只证明防回归 wording，没有资格作为协议行为的主证据。

确认的非改动范围：

- 不改 `skills/verification-before-completion/SKILL.md` 的核心门槛；它已经支持 command-backed verification、manual runtime verification 和 insufficient verification。
- 不改 `openharness check-tasks` 逻辑。
- 不修改 archived task packages。

## Interfaces
这轮没有运行时代码接口，主要接口是 agent 可读的协议契约。

- `skills/test-driven-development/SKILL.md`
  - 输入前提：task package 已经完成足够 detailed design，且验证对象是可执行行为、CLI、解析器、校验器、状态机或可观察代码契约。
  - 输出行为：进入 red-green-refactor，实现前先写能失败的测试，再写最小实现，再重构。
  - 禁止解释：TDD 不能替代 `01-requirements.md`、`02-overview-design.md` 或 `03-detailed-design.md`；不能因为任务有“变更”二字就对协议、文档语义、skill 行为或 agent 工作流硬写 pytest。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
  - 输入前提：overview 已收敛，正在把总体方向落到可执行设计。
  - 输出契约：`03` 先写实现落点、接口边界、行为契约、失败模式、误用风险和迁移顺序，再从这些设计结论推导验证对象与证据路径。
  - `testing-first` 精度：表示“先准备适合对象的测试或验证，再落实现”，不是“先写 pytest”。
- `skills/using-openharness/SKILL.md`
  - 保持外层阶段流：`01 -> 02 -> 03 -> implementation -> 04 -> 05`。
  - `03-detailed-design.md` owns `testing-first` 的意思是 `03` 内写清 testing / verification order，不是 detailed design 之前先写测试。
- `README.md`
  - `uv run pytest` 是 Python-first 代码类改动的默认自动化基线。
  - 该基线不证明 runtime 行为、协议语义、skill 行为或 agent 工作流已经成立；这些对象必须在 task package 中选择更贴合的证据路径。

关键 observability 入口：

- 协议审查和子 Agent dry run 能观察 agent 是否仍把 TDD 提前到 design 之前，或对非可执行对象硬写 pytest。
- `uv run openharness check-tasks` 能观察 task package 结构和状态写回是否仍有效。
- 可选薄文本测试只能观察短 wording 是否回归，不能观察 agent 实际行为。

## Module Internals
这轮没有新增模块，内部职责按文档面分配：

- TDD skill 负责实现内循环边界：什么情况下进入 red-green-refactor，什么情况下不应调用 TDD。
- Detailed design guidance 负责实施前设计顺序：先把实现设计写清楚，再选择验证对象、证据路径和 expected evidence。
- OpenHarness entry skill 负责阶段编排：保持 task package 阶段流稳定，并把 detailed design、implementation、verification 的责任边界说清。
- README 负责产品级承诺：把 Python-first pytest floor 描述成代码类自动化基线，而不是全局验证制度。
- Verification / evidence guidance 保持原职责：记录 fresh evidence、traceability、manual steps、artifact paths 和 residual risks；本轮不改它们的核心行为。

## Data Semantics
核心数据不是代码结构，而是“验证对象类型 -> 证据路径”的语义映射：

- 可执行代码行为、CLI、解析器、校验器、状态机、可观察代码契约 -> TDD / 自动测试。
- 协作协议、skill 行为、agent 工作流、文档语义 -> 协议审查、子 Agent dry run、场景复盘或人工复核。
- runtime 行为 -> Runtime Workflow Package 或项目定义的 runtime 验证路径。
- task package 结构和状态写回 -> `uv run openharness check-tasks`。
- 机械改动 -> 最小目标命令、结构检查或格式检查。

一致性约束：

- 一个任务可以包含多个验证对象，因此可以组合多条证据路径。
- 自动测试是强证据之一，但不是所有对象的默认路径。
- `check-tasks` 只证明结构协议，不证明文档语义或 agent 行为。
- 子 Agent 审核是协议类对象的强候选证据，但如果无法执行，必须在 `04-verification.md` 中记录残余风险。

## Stage Gates
用中文写清楚 detailed 要进入下一阶段前必须具备哪些硬性产出，例如测试策略、可观测性要求、模块内部职责、数据语义、迁移顺序和预期证据类型。

## Decision Closure
用中文记录关键挑战如何被处理，只允许写清楚接受、拒绝或延期，以及对应理由、替代方案或触发条件。

## Error Handling
主要静默失败风险是 agent 看到 `testing-first`、`pytest floor` 或 TDD 的强硬语气后，继续误读成“所有任务先 pytest”。这类错误不会通过 `check-tasks` 暴露，因为任务包结构仍然可能有效。

处理方式：

- 在 TDD skill 和 detailed design guidance 中明确 forbidden interpretation：TDD 不替代 design，pytest 不覆盖所有验证对象。
- 在 README 和 using-openharness 中保留 Python-first 自动化基线，但补上适用边界。
- 在验证阶段使用协议审查和子 Agent dry run 专门观察该误读点。
- 如果 dry run 缺失，完成主张必须降级，并在 `04-verification.md` 和 `05-evidence.md` 写明 residual risk。

另一个失败路径是过度收缩 TDD，导致代码类改动也不写自动测试。处理方式是在 TDD skill 中保留 red-green-refactor 对可执行行为的强要求，只收窄适用对象，不削弱代码类验证纪律。

## Migration Notes
用中文描述迁移顺序、兼容策略、落地阶段和回滚注意事项，说明切换点与回滚触发点。

## Recommended Diagrams
如果关键交互、状态变化或数据关系仅靠文字容易歧义，用中文说明推荐补哪些 `PlantUML` 图，例如时序图、状态图或数据关系图；图不能替代文字里的接口、数据语义和异常说明。

## Detailed Reflection
用中文记录对测试策略、接口边界、迁移假设和验证路径的反思。
