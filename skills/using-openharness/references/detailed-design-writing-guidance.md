# Detailed Design Writing Guidance

本说明只负责 `03-detailed-design.md`。

它不负责重新选择总体方向；如果你还在争论方向，应返回 `02-overview-design.md` 继续收敛。

## Purpose

把总体方案收敛成可执行实施计划，明确验证路径、改动落点、接口边界、错误处理与迁移顺序。

## Questions This Document Must Answer

- 准备怎么验证这轮工作真的成立？
- 如果主验证路径走不通，降级路径是什么？
- 哪些文件会新增或修改，为什么？
- 涉及哪些接口、契约和稳定边界？
- `testing-first` 的实施顺序是什么？
- `observability` 要求是什么？要靠什么看见失败或退化？
- 失败路径、误用风险和静默出错风险是什么？
- 迁移顺序和回滚注意事项是什么？
- 还有哪些挑战被接受、拒绝或延期？

## Section Mapping

- `Runtime Verification Plan`
  - 先写主验证路径，再写 fallback，再写预期证据。
  - 这里必须体现 `testing-first`：先准备哪些测试或验证，再落实现。
- `Files Added Or Changed`
  - 写实现将落在哪些文件或文档面，以及为什么这些落点合理。
  - 不接受只有文件清单、没有承载理由的写法。
- `Interfaces`
  - 写接口、契约、稳定边界和边界两侧责任。
  - 这里也要交代关键 `observability` 入口，例如日志、状态、测试观察点、验证产物。
- `Stage Gates`
  - 写 detailed 进入实施前必须已经确定的硬条件。
  - 至少覆盖测试策略、`observability` 要求、实现落点、迁移顺序、预期证据类型。
- `Decision Closure`
  - 写关键挑战如何被接受、拒绝或延期，以及各自理由。
- `Error Handling`
  - 写主要失败路径、误用方式、静默出错风险，以及如何发现这些问题。
- `Migration Notes`
  - 写实施顺序、兼容策略、切换点、回滚触发点。
- `Detailed Reflection`
  - 再次挑战测试策略、接口边界、迁移顺序、预期证据是否足够支撑实施。

## Boundary With Adjacent Documents

- 这里写“怎么落地”，不是重新争论总体方向。
- 如果你还在讨论方案一还是方案二，说明 overview 还没真正收敛。
- 如果你已经开始记录实际执行结果，那部分应进入 `04-verification.md` 或 `05-evidence.md`。

## Common Failure Modes

- 只有文件列表，没有解释为什么这些落点合理。
- `Runtime Verification Plan` 只写一个命令，没有说明不足时怎么办。
- `Interfaces` 缺失，导致改动边界不清。
- `Decision Closure` 没有明确接受、拒绝或延期，挑战一直悬空。
- `Migration Notes` 缺失，默认认为“改完就自然生效”。

## Minimum Acceptable Shape

- `Runtime Verification Plan` 至少写主验证路径、阻塞时的 fallback 和预期证据。
- `Files Added Or Changed` 至少说明每类改动文件的作用。
- `Interfaces` 至少定义稳定边界和暴露契约，并能说清怎么观察失败或退化，也就是 `observability`。
- `Stage Gates` 至少覆盖测试策略、`observability`、实现落点、迁移顺序和证据类型。
- `Decision Closure` 至少记录一个被接受、拒绝或延期的关键挑战。
- `Error Handling` 至少写出主要失败路径和静默出错风险。
- `Detailed Reflection` 至少再次挑战测试、接口、迁移和预期证据假设。

## Exit Check

离开 detailed 阶段前，至少能明确回答下面 6 个问题：

- 如果现在开始实施，是否已经知道先写什么测试或验证，也就是 `testing-first` 顺序？
- 是否已经知道失败会通过什么信号暴露，也就是 `observability` 从哪里来？
- 是否已经知道实现会落到哪些文件或模块，以及为什么是这些地方？
- 是否已经知道主要接口边界和误用风险？
- 是否已经知道迁移顺序、切换点和回滚触发点？
- 是否已经知道后续 `04-verification.md` 需要收什么证据？

如果这些问题还答不清，就不要进入 `in_progress`。

## How To Use The Template

- 先写验证路径，再写文件落点；否则很容易做出无法验证的设计。
- `Files Added Or Changed` 不只是改动清单，更是“为什么这些地方承载本轮实现”的解释。
- 先把 exploration 阶段已经确定的事实落到对应章节，再补推论；不要重新从空白开始发明 detailed。
- 如果你写完后还不能直接开始实施，说明 detailed 还不够具体。
