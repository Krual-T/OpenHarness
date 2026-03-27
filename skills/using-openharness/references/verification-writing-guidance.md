# Verification Writing Guidance

本说明只负责 `04-verification.md`。

它不负责替代真实验证；如果没有新鲜证据，这个文档只能诚实记录“尚未验证完成”。

## Purpose

记录这轮工作本来打算如何验证、实际上如何验证、结果如何，以及验证证据和需求设计之间是否对得上。

## Questions This Document Must Answer

- 计划验证路径是什么？
- 实际执行了什么？
- 偏差、阻塞和限制是什么？
- 预期结果与实际结果是否匹配？
- 需求、设计和验证证据如何对应？
- 还接受了哪些残余风险？
- 本轮证据是否足够支撑当前状态或完成主张？
- 哪条证据是最新的，也就是 `fresh` verification evidence？

## Section Mapping

- `Verification Path`
  - `Planned Path` 写准备怎么验证。
  - `Executed Path` 写实际执行了什么，什么时候执行，看到什么结果。
  - `Path Notes` 写偏差、限制、阻塞，以及为什么当前路径足够或不足够。
- `Required Commands`
  - 写本包声明必须执行的命令。
  - 要能看出哪些已经执行，哪些还没执行，缺口是什么。
- `Expected Outcomes`
  - 写每条关键验证路径本来应该观察到什么。
- `Traceability`
  - 把核心需求、设计决策和验证证据逐项对上。
  - 不接受“基本对应”“大体覆盖”这种泛化句。
- `Risk Acceptance`
  - 写当前仍接受哪些盲区或残余风险，以及触发重新审查的条件。
- `Latest Result`
  - 写最近一次验证结果是否足以支撑当前状态。
  - `Latest Artifact` 写最新、最权威的验证产物；没有就明确写无。

## Boundary With Adjacent Documents

- 这里写“验证发生了什么”，不是重新设计方案。
- 这里也不应该替代 `05-evidence.md` 去列完整改动清单；证据文件更适合沉淀命令、文件和产物路径。

## Common Failure Modes

- 只写 `Required Commands`，不写 `Executed Path`。
- 把“还没验证”伪装成“应该没问题”。
- `Traceability` 缺失，导致测试过了但没人知道它证明了哪条需求。
- `Risk Acceptance` 缺失，导致盲区被静默吞掉。
- 没有标出哪条证据是最新的 `fresh` evidence，导致状态和证据脱节。

## Minimum Acceptable Shape

- `Verification Path` 至少有计划路径与实际执行路径，并说明当前路径足够或不足够。
- `Required Commands` 不能只抄配置，必须能看出实际执行缺口。
- `Expected Outcomes` 不能省略，否则无法比较预期与实际。
- `Traceability` 至少说明核心需求和关键证据的对应关系。
- `Risk Acceptance` 不能缺失，否则盲区会被静默吞掉。
- `Latest Result` 至少明确最近一次验证结果，不允许空泛成功表述。
- `Latest Artifact` 没有时也要明确写无。

## Exit Check

离开 verification 阶段前，至少能明确回答下面 6 个问题：

- 哪些 `Required Commands` 已执行，哪些没执行？
- 最近一次验证是否是 `fresh` 的，而不是旧结果复用？
- 这次验证的预期结果和实际结果是否一致？
- 哪条核心需求由哪条证据支撑？
- 当前还接受哪些残余风险？
- 这次结果是否真的足以支撑当前状态或完成主张？

如果这些问题还答不清，就不要把包推进到 `archived`。

## How To Use The Template

- 先记计划，再补执行，不要等到最后凭记忆倒推。
- 明确标出哪条结果是最新、最权威的验证结果。
- 如果验证不足，要明确写“不足”，不要用模糊措辞掩盖。
