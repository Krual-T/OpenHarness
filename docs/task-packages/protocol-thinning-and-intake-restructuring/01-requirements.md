# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
基于 `OH-036` 的评估结果，对 OpenHarness 做一轮聚焦重构：削减重复协议表面、重组入口层与用户可见阶段播报的关系，同时保留 task package、状态、verification 和 archive 构成的核心工程闭环。

单一成功指标是：重构后 OpenHarness 的协议主路径更短、更集中，新进入者和代理不需要在多个表面之间比对同一套规则，且项目不会重新退回到“假完成难以识别”的状态。

## Problem Statement
`OH-036` 已经把 OpenHarness 当前的主要矛盾收敛出来：

- 真正有价值的结构主要集中在 task package、`STATUS.yaml`、verification / evidence writeback 和 archive protocol。
- 高风险负担主要来自 skills、guidance、README、task package 和测试之间对同一仓库协议的重复解释。
- 入口阶段播报与 `bootstrap` 可见性虽然提高了流程透明度，但也带来了前台流程感偏重、首轮回复不够自然、入口行为边界不清的问题。
- 多个历史 package 显示 OpenHarness 经常是通过“收紧语义、删除重复解释、重组入口”来前进，而不是通过永久兼容旧表面来前进。

目标用户是 OpenHarness 的维护者和高频协作者。核心场景是：维护者已经接受 OpenHarness 需要继续演化，但不希望再通过叠加更多 guidance、更多制度说明和更多兼容桥来推进，而是要做一轮更直接的结构减重和入口重组。

之所以现在做，是因为评估包已经把“保留 / 削减 / 重组”的候选边界明确出来。如果不尽快承接，OpenHarness 很容易又回到“继续补说明而不是改结构”的惯性上。

## Required Outcomes
1. 明确哪些仓库级协议表面是唯一权威源，哪些重复承载面应被删除、合并或降级为引用。
   `acceptance criteria`: 至少能对 `AGENTS.md`、README、skills、guidance、CLI 输出之间的职责边界给出清晰结论。
2. 重组 intake 行为与阶段可见性，使入口体验更自然，但不丢失当前阶段、下一步和活跃任务上下文的可观察性。
   `acceptance criteria`: 能明确回答何时应前台展示阶段信息，何时只在后台使用 `bootstrap` 或其他上下文工具。
3. 保留并强化 OpenHarness 的核心闭环，即 task package、机器可读状态、verification / evidence writeback 和 archive 语义。
   `acceptance criteria`: 任何删减或重组方案都不能把项目退回到“完成声明没有证据约束”的状态。
4. 明确本轮不默认保留兼容性，并列出哪些旧表面如果要保留，必须单独证明其价值。
   `acceptance criteria`: 设计结论中不能出现“为了兼容先都保留”的默认策略。

## Non-Goals
- 本轮不重做 task package 核心文件结构，不把 OpenHarness 改写成完全不同的系统。
- 本轮不扩展新的 runtime helper、维护命令或额外 stage。
- 本轮不把所有外部对照项目的方法都引进来；只围绕 `OH-036` 已经收敛出的结构问题动手。
- `counterexample`: 如果只是继续给 skills、guidance 或 README 增补更多解释文字，却不真正删除重复表面或重组入口行为，那不属于这轮任务的完成结果。

## Constraints
- 本轮依赖 `OH-036` 已经收敛出的边界，不重新回到“OpenHarness 值不值得存在”的泛评估。
- 本轮默认不做兼容性保留；如果需要兼容，必须把兼容对象、兼容价值和兼容成本写成显式决定。
- 必须保留证据优先于完成声明这一基本方向，不允许为了减轻流程感而放弃 verification / evidence / archive 闭环。
- `cost cap`: 本轮只做一轮聚焦重构，不同时重开新的生态调研、runtime 产品化或额外协议升级。
