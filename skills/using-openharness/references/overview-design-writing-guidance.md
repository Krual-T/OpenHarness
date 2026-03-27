# Overview Design Writing Guidance

本说明只负责 `02-overview-design.md`。

它不负责替代方案探索，也不负责决定是否进入详细设计；这些事情由 `exploring-solution-space` 负责。

## Purpose

在多个可能方案中收敛总体方向，说明系统边界、主结构、关键流程和主要取舍。

## Questions This Document Must Answer

- 这轮设计覆盖哪些表面，明确不覆盖哪些表面？
- 推荐方案的主结构是什么？
- 关键模块边界、接口边界或流程边界是什么？
- 主路径是怎么走的？
- `key failure modes` 是什么？如何识别？
- 失败时如何降级、回滚或收缩？
- 为什么选这个方向，而不是另一个可行方向？
- 这轮反思后，哪些挑战被纳入约束，哪些被拒绝，哪些被延期，也就是 `challenge closure` 是什么？

## Section Mapping

- `System Boundary`
  - 写覆盖范围和明确排除范围。
  - 边界要落到仓库表面、模块、接口责任或流程范围，不接受只有抽象原则的表述。
- `Proposed Structure`
  - 写推荐方案的层次、关键边界和边界两侧各自负责什么。
  - 结构必须能被指到具体对象，例如模块、文档面、流程节点、责任面。
- `Key Flows`
  - 写主路径经过哪些步骤，关键决定发生在哪一步，失败信号在哪里出现。
- `Stage Gates`
  - 把 overview 进入下一阶段前必须满足的硬条件写清楚。
  - 至少覆盖关键约束、边界与接口决定、`key failure modes`、降级或回滚方向。
- `Trade-offs`
  - 至少写一个可行备选方案，说明为什么没选它。
  - 不只写优点，还要写代价和放弃了什么。
- `Overview Reflection`
  - 写真正挑战过什么。
  - 反思结论必须带 `challenge closure`，也就是接受、拒绝或延期，而不是只写“考虑过”。

## Boundary With Adjacent Documents

- 这里写“整体怎么组织”，不写“每个文件具体改什么实现细节”。
- 如果你已经开始列函数、类、命令细节、迁移步骤或测试清单，说明内容已经落到 `03-detailed-design.md`。
- 这里也不应该重写需求背景；背景只需引用需求结论。

## Common Failure Modes

- `System Boundary` 只有一句“本轮修改 X”，没有写覆盖面和排除面。
- `Proposed Structure` 只是抽象口号，没有说明边界与主路径。
- `Trade-offs` 只有优点，没有写代价和为什么不选别的方向。
- `Overview Reflection` 只是重复主结论，没有真正挑战备选方案。

## Minimum Acceptable Shape

- `System Boundary` 至少同时写清覆盖范围与不纳入范围。
- `Proposed Structure` 至少解释方案层次、主边界和关键约束，并能指向具体责任对象。
- `Key Flows` 至少让后续读者能快速建立主流程模型，并知道失败信号会在哪出现。
- `Stage Gates` 必须写成进入下一阶段的判定条件，不能只是把前文换个说法再写一遍。
- `Trade-offs` 至少比较一个替代方向，并写出为什么不选。
- `Overview Reflection` 至少记录一次真实挑战，并带上 `challenge closure`。

## Exit Check

离开 overview 阶段前，至少能明确回答下面 5 个问题：

- 这轮设计到底覆盖哪些表面，明确不覆盖哪些表面？
- 推荐方案具体由哪些责任边界构成？
- 主路径如何走，`key failure modes` 如何暴露？
- 如果这个方向失败，准备如何降级、回滚或收缩？
- 至少一个备选方向为什么没被采用，且这个挑战是如何关闭的？

如果这些问题还答不清，就不要进入 `03-detailed-design.md`。

## How To Use The Template

- 写 `System Boundary` 时，优先用“覆盖什么 / 不覆盖什么”两类句子。
- 写 `Trade-offs` 时，不要怕写代价；没有代价的方案通常只是没想清楚。
- 写 `Proposed Structure` 时，优先点名具体仓库表面、模块或接口责任，不要只写抽象原则。
- 写完后检查：一个不了解上下文的人，能不能靠这份文档知道“这一轮设计到底包多大、为什么这样分、失败时怎么办”。
