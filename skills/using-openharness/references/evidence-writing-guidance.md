# Evidence Writing Guidance

本说明只负责 `05-evidence.md`。

它不负责判定任务是否完成；它负责把本轮真实落地过的痕迹沉淀下来，供后续复核和追溯。

## Purpose

沉淀这一轮真正落地过的文件、命令、产物路径、人工步骤、残余风险和后续事项。

## Questions This Document Must Answer

- 这一轮实际改了哪些文件？
- 实际跑了哪些命令？
- 哪条是 `final verification command`，也就是最终支撑完成主张的验证命令或人工验证步骤？
- 证据产物放在哪里？
- 有没有需要人工执行的步骤？
- 还有哪些残余风险和未覆盖面？
- 哪些后续事项被明确延后了？
- 这些文件、命令和产物分别支撑哪项验证结论或完成主张？

## Section Mapping

- `Residual Risks`
  - 写本轮之后仍存在的盲区、未覆盖面和已知风险。
- `Manual Steps`
  - 只写已经执行过或明确待执行的人工作业。
  - 不要把一般性改进建议写到这里。
- `Files`
  - 列关键变更文件或关键证据文件。
  - 如果某个文件重要，最好说明它支撑什么结论。
- `Commands`
  - 列本轮实际执行过的关键命令。
  - 必须能看出哪条是 `final verification command`。
- `Artifact Paths`
  - 列关键产物、日志或证据位置。
  - 最好能说明它由什么产生、为什么值得看。
- `Follow-ups`
  - 写明确延后的后续动作、剩余决策或后续包。

## Boundary With Adjacent Documents

- 这里写“落地证据是什么”，不是重新描述需求、设计或验证理论。
- 如果某段内容在解释验证是否充分，应放进 `04-verification.md`；这里更适合记录证据位置和剩余事项。

## Common Failure Modes

- 只列文件名，不说明是否真的改过或为什么相关。
- `Commands` 留空，导致无法复盘本轮做过什么。
- `Artifact Paths` 缺失，后续无法找到日志或产物。
- `Follow-ups` 缺失，导致延期事项再次隐形消失。
- 没有标出 `final verification command`，导致读者不知道哪条命令真正支撑完成主张。
- 把一般性建议写进 `Manual Steps`，导致人工操作和后续计划混在一起。

## Minimum Acceptable Shape

- `Files` 至少列出关键变更文件或关键证据文件；如果没有相关文件，也应明确写无。
- `Commands` 至少列出本轮实际执行过的关键命令，并标出 `final verification command`。
- `Artifact Paths` 没有时也应明确写无；有时应尽量说明它由什么产生。
- `Manual Steps` 没有时也应明确写无。
- `Residual Risks` 与 `Follow-ups` 至少各写一轮真实结论，而不是占位句。

## Exit Check

离开 evidence 收尾前，至少能明确回答下面 5 个问题：

- 哪条命令或人工步骤是 `final verification command`？
- 如果删掉 `04-verification.md`，别人还能不能靠本页定位到关键命令、关键产物和关键文件？
- `Manual Steps` 里写的是实际人工操作，而不是后续建议吗？
- `Artifact Paths` 是否真的能带人找到该看的产物？
- `Follow-ups` 是否已经把延期事项单独写清，而不是混在别的章节？

如果这些问题还答不清，这页就还不是高价值 evidence 索引。

## How To Use The Template

- 这里优先写事实，不写评价。
- 如果某项证据不存在，就明确写无，不要留空。
- 先列主证据，再补背景痕迹；不要让低价值清单淹没真正关键的证据入口。
- 把它当成“复盘索引页”，而不是第二份验证报告。
