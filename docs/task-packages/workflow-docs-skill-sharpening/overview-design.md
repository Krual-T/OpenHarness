# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 OpenHarness 主工作流的文档说明面：

- `skills/using-openharness/SKILL.md`：入口协议、核心命令、gate 流转、受保护文件和全局输出语言约定。
- `skills/using-openharness/states/*/SKILL.md`：各阶段动作、阻塞条件、失败分流、transition 目标和阶段边界。
- `skills/using-openharness/references/templates/task-package.*`：任务包文档模板的章节、最低要求、写法质量标准和内容边界。
- `skills/using-openharness/references/runtime-*.md`：仅当 RWP 写回规则与阶段文档职责冲突时同步边界表达。

本轮不覆盖 CLI 状态机、hook 实现、任务包数据模型、状态值、文件名、archived 历史包批量重写，也不移动、归档或删除现有阶段 skill。`finishing-a-development-branch` 不作为本轮迁移对象。

## Proposed Structure
推荐采用“三层职责边界”：

1. 入口 skill 层：`using-openharness/SKILL.md` 只维护全局协议，包括任务包入口判断、核心命令、gate 流转、受保护文件和输出语言约定。它不展开每个文档模板的写法。
2. 阶段 skill 层：`states/*/SKILL.md` 只回答“当前阶段怎么行动、什么情况阻塞、失败如何分流、完成后 transition 到哪个 gate”。它可以引用模板路径，但不重复模板里的长篇章节写法。
3. 模板层：`references/templates/task-package.*` 只回答“这个文件有哪些章节、每章最低写到什么程度、文档质量怎么判断”。模板不解释完整工作流，也不承担状态机教学。

关键状态模型保持不变：`task-info.yaml.status` 仍由 CLI 管理，gate 状态仍由 CLI 自动推进；文档只描述 agent 应如何配合这些状态，不改变状态语义。

关键内容模型按文档职责收敛：

- `requirements.md` 写问题、目标、验收结果、反例和约束。
- `overview-design.md` 写系统边界、总体结构、主路径、取舍和挑战闭合。
- `detailed-design.md` 写落地设计、文件承载理由、接口精度、数据语义、预期证据和 fallback。
- `verification-design.md` 写计划验证命令、期望退出码、期望输出、Traceability 和 Risk Acceptance。
- `evidence.md` 写实际执行结果、最终结论、残余风险和 follow-up。
- `task-info.yaml` 写元信息和机器可读字段；自然语言字段用中文，YAML 键、状态值、枚举值和路径保持英文。

## Key Flows
主流程是：

1. agent 通过 CLI 进入任务包，CLI 注入当前状态对应的阶段 skill。
2. 阶段 skill 指挥 agent 完成本阶段动作，并引用对应模板。
3. agent 按模板把阶段产物写入任务包文档。
4. 阶段 Exit Check 通过后，agent transition 到对应 gate 状态，由 CLI 自动推进。
5. 后续阶段只读取前一阶段已写清的决策，不把职责倒灌回前一文档。

关键失败信号包括：

- 同一条规则同时出现在阶段 skill 和模板中，且措辞不一致。
- 阶段 skill 要求写入某个章节，但对应模板没有该章节。
- `implementing` 对 `evidence.md` 写最终结论，和 `verifying` 的最终证据职责冲突。
- `task-info.yaml` 模板继续承载状态流教学，导致元信息文件变成流程说明文档。
- Markdown 章节标题语言不统一，导致新任务包继续复制混合标题。

收缩路径：如果某一类规则无法在本轮内安全收敛，优先保留阶段 skill 的门禁和失败分流，只压缩重复写法说明；模板变更只做与已确认职责直接相关的章节调整。

## Stage Gates
进入 `detailed_designing` 前必须满足：

- 覆盖范围与排除范围已经明确，包括不移动 `finishing-a-development-branch`。
- 已确认三层职责边界：入口 skill、阶段 skill、模板分别承担什么。
- 已确认文档职责模型：`detailed-design.md`、`verification-design.md`、`evidence.md` 的验证相关内容不再混写。
- 已确认语言规则：Markdown 章节标题用英文，正文和 `task-info.yaml` 自然语言字段用中文，枚举和路径保持英文。
- 已确认失败处理原则：保留阶段 skill 的门禁和回退动作，只压缩重复写作指导。
- 已确认本轮验证方式是 `qualitative`，不需要 RWP 运行时验证。

## Trade-offs
推荐方案的收益是边界清楚：agent 先看阶段 skill 决定“现在怎么走”，再看模板决定“文档怎么写”。这能降低重复文本，也能减少因为多处维护同一规则造成的冲突。

代价是本轮需要同时检查多个阶段 skill 和模板，不能只改一个文件。详细设计阶段需要逐项列出具体落点，避免用总体原则替代实际编辑计划。

备选方案一：只改模板，不改阶段 skill。拒绝理由：当前冲突来自两边同时解释流程，只改模板不能消除阶段 skill 中的重复或不一致。

备选方案二：只改阶段 skill，不改模板。拒绝理由：模板仍会被新任务包复制，章节标题语言和验证职责混写会继续扩散。

备选方案三：把所有说明集中到一个大文档，阶段 skill 和模板只放链接。拒绝理由：CLI 的渐进式注入依赖阶段 skill 能当场给出行动门禁；把阶段动作移到远端大文档会降低可执行性。

## Recommended Diagrams
本轮不需要 PlantUML 图。三层职责边界和文档职责模型可以用文字与表格稳定表达；增加图示反而会提高后续同步成本。若详细设计发现 RWP 写回路径仍有歧义，可在 `detailed-design.md` 中补一张简单流程图建议，但不是 overview 阶段的硬要求。

## Overview Reflection
挑战一：是否应该把 `finishing-a-development-branch` 移出主工作流文档面。结论：拒绝。用户已明确指出该方向是错的，本轮只处理文档职责和模板表达，不移动现有阶段 skill。

挑战二：是否应该要求所有阶段 skill 都只保留一句话，模板承担全部指导。结论：拒绝。阶段 skill 仍需要保留门禁、失败分流和 transition 目标，否则 CLI 注入后无法直接指导 agent 行动。

挑战三：是否需要 RWP 验证。结论：拒绝。本轮是文档与协议表达收敛，不验证运行时行为；`verify_by: qualitative` 足够覆盖需求。

挑战四：是否把语言规则只写在模板，不写入口 skill。结论：拒绝。入口 skill 是全局输出约定的权威位置，模板是具体文档的局部执行位置，两边可以保留同一规则的不同粒度表达，但不能维护相互冲突的扩展说明。
