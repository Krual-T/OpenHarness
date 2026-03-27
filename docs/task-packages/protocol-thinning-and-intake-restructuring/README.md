# OH-037 Protocol Thinning And Intake Restructuring

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮任务承接 `OH-036` 的评估结论，目标是对 OpenHarness 做一轮聚焦重构：减轻重复协议表面，重组入口行为与用户可见阶段播报，同时保留 task package、状态、verification 和 archive 形成的核心闭环。
- 本轮默认不为了兼容旧结构而保留重复承载面；是否保留某个旧表面，必须由本包重新证明其必要性。

## Current Status
- 当前处于 `verifying`：第一波实现已经落地，当前正在核对入口减重、协议文案收口和仓库回归是否都成立；后续如继续推进，将进入下一波对 entry skill 和 child skills 的进一步减重。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
