# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 用中文列出将执行的验证路径，命令本身保持英文原样；先写主验证路径，再写 fallback。
- Fallback Path:
- 用中文说明如果主验证路径被阻塞时如何处理，以及何时不能宣称完成。
- Planned Evidence:
- 用中文写明预计要产出的证据、产物或观察结果，并说明后续 `04-verification.md` 需要收什么。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
本轮只修改 live protocol / guidance / tests，不修改 archived task packages，不新增 CLI、Runtime Workflow Package 或测试框架。

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
  - 补充协议文档测试，只锁定关键边界：TDD 不替代 design、pytest floor 不等于所有任务都必须 pytest、detailed guidance 必须表达“测试或验证”。
  - 不写只证明长文本片段存在的形式主义断言。

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
