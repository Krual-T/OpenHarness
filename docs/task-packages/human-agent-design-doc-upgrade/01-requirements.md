# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 OpenHarness 的 `02-overview-design.md` 与 `03-detailed-design.md` 从“偏流程治理的设计说明”增强为“同时适合人类维护者和 agent 执行实现”的设计文档 contract。

单一成功指标：维护者或 agent 仅阅读新的 overview/detailed guidance 与模板，就能明确回答边界、模块、接口、数据、异常、验证与回滚问题，而不必主要依赖历史 archived package 猜写法。

## Problem Statement
目标用户是使用 OpenHarness 维护 task package 的作者，以及依据 task package 落地开发的 agent。

核心场景是：作者已经完成需求收敛，准备写 `02-overview-design.md` 和 `03-detailed-design.md` 来支撑后续实现。当前协议能表达边界、主流程、验证路径和证据链，但对下面这些信息约束不够硬：

- `02` 对模块划分、接口边界、核心数据/状态模型、安全与一致性约束的提示不够系统。
- `03` 对模块内部职责、接口精度、数据语义、异常处理和实现顺序的提示不够接近可直接编码的粒度。
- 图示目前没有正式落点，导致文字很容易写成抽象结论，agent 仍要自行脑补结构关系。

现在做这件事，是因为这类缺口已经影响到“让 OpenHarness 更适合人和 agent 协作开发”的目标；如果继续只强调流程和验证，设计文档会越来越像治理记录，而不是可执行设计输入。

## Required Outcomes
1. 更新 `overview-design-writing-guidance.md`，让它不仅要求边界、主结构、主路径和 trade-off，还明确要求支持人机协作所需的模块关系、接口责任、关键数据/状态模型、架构级安全/一致性约束和图示建议。
   `acceptance criteria`: guidance 的“必答问题”“章节映射”“最小合格形态”里都能看到这些要求。
2. 更新 `detailed-design-writing-guidance.md`，让它明确要求模块内部职责、接口精度、数据语义、异常/边界处理、实现顺序与测试优先执行信息。
   `acceptance criteria`: guidance 明确把这些内容落到对应章节，而不是只停留在验证路径与文件落点。
3. 更新 `task-package.02-overview-design.md` 与 `task-package.03-detailed-design.md` 模板，使作者能在脚手架层面看到新的写作提示。
   `acceptance criteria`: `openharness new-task` 生成的模板中包含新的章节或更强提示，并通过测试。
4. 为 `PlantUML` 增加仓库内正式建议用法，说明 overview 与 detailed 分别适合放哪些类型的图，且强调图不能替代文字约束。
5. 扩展协议测试，保证新的 guidance/template contract 可持续验证。

## Non-Goals
- 本轮不重写整个 task package 协议，不新增新的固定 task package 文件。
- 本轮不引入必须渲染图片或校验图语法的工具链；`PlantUML` 只作为正式推荐的文本图示方法进入 guidance/template。
- 本轮不批量回填所有 archived packages 的旧文档。
- `counterexample`: 如果有人提议直接把所有设计规则做成强 schema 校验或自动图生成，这看起来相关，但不属于本轮范围。

## Constraints
- 必须保持现有 task package 固定文件集合和状态流不变。
- 必须兼容当前 `using-openharness`/`exploring-solution-space` 的阶段边界，不能把 `02` 与 `03` 合并成一个总设文档。
- 必须保持中文正文、英文标题与路径的现有仓库写作约定。
- `cost cap`: 本轮只改 guidance、模板和必要测试，不扩展到新的 CLI 子命令或新的仓库级校验器。
- 新增约束必须足够清晰，但不能把模板膨胀成冗长教程。
