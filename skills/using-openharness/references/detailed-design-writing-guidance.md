# Detailed Design Writing Guidance

本说明只负责 `03-detailed-design.md`。

它不负责重新选择总体方向；如果你还在争论方向，应返回 `02-overview-design.md` 继续收敛。

## Purpose

把总体方案收敛成可执行实施计划，明确验证路径、改动落点、模块内部职责、接口边界、数据语义、错误处理与迁移顺序，让人类维护者和 agent 都能按同一组硬约束实施。

## Questions This Document Must Answer

- 准备怎么验证这轮工作真的成立？
- 如果主验证路径走不通，降级路径是什么？
- 哪些文件会新增或修改，为什么？
- 涉及哪些接口、契约和稳定边界？精度需要细到什么程度？
- 模块内部职责如何拆分？谁负责状态变化、校验、编排和副作用？
- 关键数据结构、字段语义或状态转换约束是什么？
- `testing-first` 的实施顺序是什么？
- `observability` 要求是什么？要靠什么看见失败或退化？
- 失败路径、误用风险和静默出错风险是什么？
- 迁移顺序和回滚注意事项是什么？
- 还有哪些挑战被接受、拒绝或延期？
- 哪些交互关系最适合用 `PlantUML` 表达，且图不能替代文字里的契约？

## Section Mapping

- `Runtime Verification Plan`
  - 先写主验证路径，再写 fallback，再写预期证据。
  - 这里必须体现 `testing-first`：先准备哪些测试或验证，再落实现。
- `Files Added Or Changed`
  - 写实现将落在哪些文件或文档面，以及为什么这些落点合理。
  - 不接受只有文件清单、没有承载理由的写法。
- `Interfaces`
  - 写接口、契约、稳定边界和边界两侧责任。
  - 这里要明确接口精度，例如参数语义、输入输出约束、边界条件、错误传播或兼容性要求。
  - 这里也要交代关键 `observability` 入口，例如日志、状态、测试观察点、验证产物。
- `Module Internals`
  - 写模块内部职责分解，说明编排、校验、状态更新、副作用和适配层分别落在哪里。
  - 这里是把 overview 的结构边界下沉到足够支撑编码的层次，但仍不记录执行结果。
- `Data Semantics`
  - 写关键数据结构、字段语义、状态转换和一致性约束。
  - 如果数据关系复杂，优先补一张 `PlantUML` 状态图、类图或关系图。
- `Stage Gates`
  - 写 detailed 进入实施前必须已经确定的硬条件。
  - 至少覆盖测试策略、`observability` 要求、实现落点、模块内部职责、接口精度、数据语义、迁移顺序、预期证据类型。
- `Decision Closure`
  - 写关键挑战如何被接受、拒绝或延期，以及各自理由。
- `Error Handling`
  - 写主要失败路径、误用方式、静默出错风险，以及如何发现这些问题。
  - 如果异常处理或回退路径跨模块传播，应该写清传播链。
- `Migration Notes`
  - 写实施顺序、兼容策略、切换点、回滚触发点。
- `Recommended Diagrams`
  - 写哪些实现关系适合用 `PlantUML` 表达，例如时序图、状态图、数据关系图。
  - 图只负责帮助协作，不替代文字里的接口、数据语义和异常说明。
- `Detailed Reflection`
  - 再次挑战测试策略、接口边界、迁移顺序、预期证据是否足够支撑实施。

## Boundary With Adjacent Documents

- 这里写“怎么落地”，不是重新争论总体方向。
- 如果你还在讨论方案一还是方案二，说明 overview 还没真正收敛。
- 这里要把 overview 已经确定的结构下沉到可编码粒度，但不要把 `04-verification.md` 的实际执行结果提前写进来。
- 如果你已经开始记录实际执行结果，那部分应进入 `04-verification.md` 或 `05-evidence.md`。

## Common Failure Modes

- 只有文件列表，没有解释为什么这些落点合理。
- `Runtime Verification Plan` 只写一个命令，没有说明不足时怎么办。
- `Interfaces` 缺失，导致改动边界不清。
- 没有模块内部职责，导致实现顺序和落点只能靠临场决定。
- 没有数据语义，导致字段、状态或缓存语义在不同实现点上各写各的。
- `Decision Closure` 没有明确接受、拒绝或延期，挑战一直悬空。
- `Migration Notes` 缺失，默认认为“改完就自然生效”。
- 画了图但没有写明接口、数据语义或异常约束，也属于失败。

## Minimum Acceptable Shape

- `Runtime Verification Plan` 至少写主验证路径、阻塞时的 fallback 和预期证据。
- `Files Added Or Changed` 至少说明每类改动文件的作用。
- `Interfaces` 至少定义稳定边界、接口精度和暴露契约，并能说清怎么观察失败或退化，也就是 `observability`。
- `Module Internals` 至少说明一个关键模块的内部职责分解。
- `Data Semantics` 至少说明一个关键数据结构、字段语义或状态转换约束。
- `Stage Gates` 至少覆盖测试策略、`observability`、实现落点、模块内部职责、数据语义、迁移顺序和证据类型。
- `Decision Closure` 至少记录一个被接受、拒绝或延期的关键挑战。
- `Error Handling` 至少写出主要失败路径和静默出错风险。
- 如果图示能显著减少歧义，应给出 `PlantUML` 推荐图类型或图示位置。
- `Detailed Reflection` 至少再次挑战测试、接口、迁移和预期证据假设。

## Exit Check

离开 detailed 阶段前，至少能明确回答下面 6 个问题：

- 如果现在开始实施，是否已经知道先写什么测试或验证，也就是 `testing-first` 顺序？
- 是否已经知道失败会通过什么信号暴露，也就是 `observability` 从哪里来？
- 是否已经知道实现会落到哪些文件或模块，以及为什么是这些地方？
- 是否已经知道主要接口边界、接口精度和误用风险？
- 是否已经知道模块内部职责和关键数据语义如何拆分？
- 是否已经知道迁移顺序、切换点和回滚触发点？
- 是否已经知道后续 `04-verification.md` 需要收什么证据？

如果这些问题还答不清，就不要进入 `in_progress`。

## How To Use The Template

- 先写验证路径，再写文件落点；否则很容易做出无法验证的设计。
- `Files Added Or Changed` 不只是改动清单，更是“为什么这些地方承载本轮实现”的解释。
- 先把 exploration 阶段已经确定的事实落到对应章节，再补推论；不要重新从空白开始发明 detailed。
- 模块内部职责、数据语义和异常边界要写到 agent 能直接据此落实现，而不是只留下抽象口号。
- 如果一张图能明显压缩歧义，优先用 `PlantUML` 补时序图、状态图或数据关系图，但图旁边仍要写文字契约。
- 如果你写完后还不能直接开始实施，说明 detailed 还不够具体。
