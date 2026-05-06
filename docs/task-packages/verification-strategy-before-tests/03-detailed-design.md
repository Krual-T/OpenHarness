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
用中文写清楚这轮改动暴露或依赖的接口、契约和稳定边界，并说明关键 `observability` 入口、接口精度和边界条件。

## Module Internals
用中文说明关键模块的内部职责分解，至少写清编排、校验、状态更新、副作用或适配层分别落在哪里。

## Data Semantics
用中文说明关键数据结构、字段语义、状态转换或一致性约束；如果关系复杂，说明是否需要用 `PlantUML` 状态图、类图或关系图辅助表达。

## Stage Gates
用中文写清楚 detailed 要进入下一阶段前必须具备哪些硬性产出，例如测试策略、可观测性要求、模块内部职责、数据语义、迁移顺序和预期证据类型。

## Decision Closure
用中文记录关键挑战如何被处理，只允许写清楚接受、拒绝或延期，以及对应理由、替代方案或触发条件。

## Error Handling
用中文说明失败路径、误用风险、校验边界和如何避免静默出错，至少写出一个静默出错风险，并交代异常如何传播或回退。

## Migration Notes
用中文描述迁移顺序、兼容策略、落地阶段和回滚注意事项，说明切换点与回滚触发点。

## Recommended Diagrams
如果关键交互、状态变化或数据关系仅靠文字容易歧义，用中文说明推荐补哪些 `PlantUML` 图，例如时序图、状态图或数据关系图；图不能替代文字里的接口、数据语义和异常说明。

## Detailed Reflection
用中文记录对测试策略、接口边界、迁移假设和验证路径的反思。
