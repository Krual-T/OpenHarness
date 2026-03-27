# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
- 用中文写预期验证路径，命令或路径保持英文原样。
- Executed Path:
- 用中文记录本轮实际执行了什么，明确哪些已执行、哪些未执行。
- Path Notes:
- 用中文说明偏差、限制、阻塞点和为什么这条路径足够或不足够。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- 用英文命令逐条列出本包要求执行的命令。

## Expected Outcomes
- 用中文写出执行后应当观察到的结果，用于对比预期与实际。

## Traceability
- 用中文说明需求、设计、验证证据之间如何对应；若仍有缺口，明确写出缺口与接受理由，不要只写“基本覆盖”。

## Risk Acceptance
- 用中文说明本轮仍然接受了哪些残余风险、为什么可以接受，以及这些风险后续应由什么事件或证据重新触发审查。

## Latest Result
- 用中文记录最近一次验证结果；若尚未执行，明确写待验证原因。
- Latest Artifact:
