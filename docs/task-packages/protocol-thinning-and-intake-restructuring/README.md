# OH-037 Protocol Thinning And Intake Restructuring

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮任务承接 `OH-036` 的评估结论，目标是对 OpenHarness 做一轮聚焦重构：减轻重复协议表面，重组入口行为与用户可见阶段播报，同时保留 task package、状态、verification 和 archive 形成的核心闭环。
- 本轮默认不为了兼容旧结构而保留重复承载面；是否保留某个旧表面，必须由本包重新证明其必要性。

## Current Status
- 当前处于 `verifying`：第二波实现已经把 `using-openharness` 收回到入口路由与归档协议，把 `skill-hub` 收回到技能目录与引用索引，并用协议测试锁住“不再重复讲角色注入、stage gate、runtime 总述”的边界。
- 当前验证重点是确认这一波减重没有破坏 CLI、协议文档和 task package 校验；child skills 本轮经复查后维持 stage-local 动作定位，没有继续额外收缩。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
