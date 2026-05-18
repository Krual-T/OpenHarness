# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 为什么现在要做这件事，而不是以后再做？
> - 当前痛点、缺口、冲突或风险具体是什么？
> - 本轮必须交付哪些结果？这些结果的 acceptance criteria 是什么？
> - 本轮明确不做什么？哪个 counterexample 看起来相似，但仍然不属于这个任务包？
> - 目标用户是谁？核心场景是什么？单一成功指标是什么？
> - 本轮允许付出的 cost cap 是什么？
> - 有哪些不能违反的约束？
>
> **写法建议**：先写 Problem Statement（当前到底哪里痛），再写 Required Outcomes（准备交付什么），不要倒过来。模板里的每个标题都是必答题。如果你写完后仍然无法解释"为什么不是另一个问题包"，说明需求还没收敛。

## Goal
优化 OpenHarness 的阶段 skill 与任务包模板文档，让 agent 在每个工作流阶段都能清楚判断：当前应该做什么、写入哪个文档、满足什么条件才能 transition。

单一成功指标：逐项确认后的改动完成后，阶段 skill 与模板不再互相冲突或重复承担同一职责，agent 按文档推进任务包时不会把设计、实现、验证计划和验证证据混写。

## Problem Statement
当前 CLI 状态机和 hook 框架已经基本稳定，主要问题转移到工作流文档本身。阶段 skill 与模板都在解释完整流程，导致部分要求重复、边界不清，少量内容还与当前流程不一致。

目标用户是使用 OpenHarness 的 agent 和维护者。核心场景是 agent 进入某个任务包阶段后，根据 CLI 注入的 skill 和模板写对应文档。现在的矛盾是：CLI 已经提供稳定阶段推进，但文档仍会让 agent 在多个位置读到相似甚至冲突的要求，例如 RWP 写回位置、验证设计与证据职责、实现阶段和验证阶段的 evidence 分工。

现在先做这件事，是因为继续优化 CLI hook 命令不会解决 agent 误写文档的问题；真正影响工作流质量的是 skill 与模板的职责边界。

## Required Outcomes
以下方向需要逐项确认；确认后才进入后续设计与修改：

1. 修正明确不一致的流程文档。
   - acceptance criteria：`task-package.task-info.yaml` 模板不再包含完整状态流教学注释；gate 流转说明由 `using-openharness` 入口 skill 或阶段 skill 承担；`brainstorming` 的阶段通过条件数量与列表一致，或改成不写死数量的中文表达。
2. 明确 skill 与模板的职责边界。
   - acceptance criteria：阶段 skill 主要描述阶段动作、阻塞条件和 transition 目标；模板主要描述各章节写法、最低要求和文档质量标准。
3. 收敛 `detailed-design.md`、`verification-design.md`、`evidence.md` 的验证职责。
   - acceptance criteria：`03` 写验证对象、观察点、预期证据和 fallback；`verification-design.md` 写计划命令、期望退出码、预期输出、Traceability 和 Risk Acceptance；`evidence.md` 写实际执行结果和最终证据。
4. 处理 implementing 与 verifying 对 `evidence.md` 的分工。
   - acceptance criteria：implementing 阶段只允许记录开发中事实草稿或中间观察；verifying 阶段负责最终证据、结果判断和残余风险。
5. 让 RWP 写回位置与模板章节一致。
   - acceptance criteria：如果 overview 阶段要求记录 RWP 候选或 gap，`overview-design.md` 模板必须有对应章节或该要求被移动到更合适阶段。
6. 统一 `task_type`、`verify_by` 的选择规则入口。
   - acceptance criteria：分类规则有清晰权威位置，其他 skill 只引用或做最小提醒，不重复维护多份规则。
7. 降低重复文本和上下文负担。
   - acceptance criteria：删除或压缩阶段 skill 中与模板重复的长篇写作指导，但不删除必要门禁、失败分流和回退动作。
8. 移除不再作为主工作流自动注入阶段的收尾 skill。
   - acceptance criteria：将 `skills/using-openharness/states/finishing-a-development-branch/` 移到 `.tmp/skills-backup/` 下保留备份；主工作流文档不再把它作为当前阶段优化对象。
9. 统一任务文档的章节标题语言。
   - acceptance criteria：任务包 Markdown 文档中的章节标题全部使用英文，例如 `Goal`、`Problem Statement`、`Required Outcomes`、`Constraints`；正文继续使用中文；命令、状态值、YAML 键、文件名和路径保持英文原样。
10. 规范 `task-info.yaml` 的自然语言字段。
   - acceptance criteria：`task-info.yaml` 保留 YAML 键、状态值、枚举值和路径的英文原样；非枚举的自然语言字段使用中文填写，例如 `title`、`summary`、`done_criteria` 中的描述文本。

## Non-Goals
- 不改 CLI 状态机、hook 触发实现、task package 数据模型或文件名。
- 不重新设计整个 OpenHarness 流程。
- 不把阶段 skill 简化成空壳；本轮目标是职责清晰，不是追求最短文本。
- 不在未确认方向上直接改 skill 正文。
- 不把所有文件名、状态值、命令和 YAML 键翻译成中文。
- 不把流程教学、阶段解释或写作指南塞进 `task-info.yaml`；`task-info.yaml` 只保留元信息和机器可读字段。

Counterexample：新增 `openharness task-package hook` 子命令看起来和 skill 触发相关，但本轮问题是文档内容质量，不属于本任务包。

## Constraints
- 必须保持 `using-openharness` 是唯一入口 skill。
- 必须保持现有 CLI 状态值、gate 流转和命令路径不变。
- `task-info.yaml` 的模板职责是提供元信息结构，不是解释 workflow。
- 任务包文档的章节标题使用英文；文档正文和 `task-info.yaml` 的自然语言字段使用中文；命令、状态值、枚举值、YAML 键、文件名和路径保持英文。
- 需要逐项确认改进方向；不能一次性把所有候选方向默认纳入。
- cost cap：本轮只处理 workflow skill 与模板文档，不扩张到 README 品牌叙述、安装文档或 archived 历史包批量重写。
