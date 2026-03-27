# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
这轮设计覆盖的是 OpenHarness 如何正式承载 task package 文档写作方法论，而不是直接重塑整个仓库协议。

纳入范围的表面包括：

- `skills/using-openharness/` 与相关 child skills 中对阶段职责和输出物的说明。
- `skills/using-openharness/references/templates/` 中的 task package 模板。
- `skills/using-openharness/references/` 下新增或改造的作者指南类参考文档。
- 现有 archived task packages 与 OpenSpec 公开资料中可借鉴的组织方式。

不纳入范围的部分包括：

- 修改 task package 固定文件列表或状态流。
- 为每个 skill 都单独写一套完整文档写作手册。
- 在本轮直接实现新的强校验规则去判断“文档质量好不好”。
- 用 OpenSpec 取代 OpenHarness，或把 OpenHarness 改造成同一套文件体系。

## Proposed Structure
推荐采用“三层职责 + 五份分文档 guidance”的结构。

1. `SKILL.md` 负责阶段动作指导
   - 回答“当前阶段该做什么、如何探索、从哪些角度挑战草案、什么时候进入下一阶段”。
   - 必须明确本阶段需要收集哪些信息、如何检索、需要从哪些角度思考，以及输出文档必须能回答哪些问题。
   - 不承担完整静态写作教材，但必须把作者推到正确的 guidance 上。
2. 模板负责最短写作提示
   - 每个章节保留一句到数句简洁说明，提醒作者这一节的主题与最低写作方向。
   - 模板不复制完整方法论，避免脚手架本身变成冗长正文。
3. `references/` 负责分阶段、分文档的正式写作方法论
   - 新增五份 reference，分别对应 `01-requirements.md`、`02-overview-design.md`、`03-detailed-design.md`、`04-verification.md`、`05-evidence.md`。
   - 每份 reference 都集中解释该文档的目的、必答问题、与相邻文档的边界、常见误写、合格标准和模板使用方式。
   - skill 负责告诉你“现在该做什么”，reference 负责告诉你“这个文档到底该怎么写才算合格”。

推荐的 guidance 布局如下：

- `references/requirements-writing-guidance.md`
- `references/overview-design-writing-guidance.md`
- `references/detailed-design-writing-guidance.md`
- `references/verification-writing-guidance.md`
- `references/evidence-writing-guidance.md`

这样做的原因不是为了“文件更多”，而是为了让每一阶段的真实问题和信息采集要求能被清楚绑定，避免再出现“一个总指南讲了很多话，但当前阶段到底该拿它看哪一段”这种认知负担。

从 OpenSpec 借鉴的点：

- 把每类产物要回答的问题写成显式 contract，而不是只给文件名。
- 把阶段动作和文档写法拆开：命令/动作负责推进流程，schema instruction 和模板负责约束具体产物。
- 让“如何写”落在稳定文档和模板提示中，而不是完全依赖历史样例。

不借鉴的点：

- 不照搬 OpenSpec 的文件布局。
- 不把本轮升级成完整 schema-first 规格系统。
- 不保留一个覆盖全部 task package 文档的总指南入口。
- 不让 reference 文档挤占 skill 的阶段动作空间。

## Key Flows
主流程如下：

1. 协作者从 `using-openharness` 进入仓库协议，确认当前阶段。
2. 进入 `brainstorming` 时，skill 明确要求收集需求信息，并把作者导向 `references/requirements-writing-guidance.md`。
3. 进入 `exploring-solution-space` 时，skill 先指导如何完成总体设计，再指导何时把结论下沉到详细设计，并分别导向 `references/overview-design-writing-guidance.md` 和 `references/detailed-design-writing-guidance.md`。
4. 进入 `verification-before-completion` 时，skill 指导如何建立验证链路、如何记录证据，并分别导向 `references/verification-writing-guidance.md` 和 `references/evidence-writing-guidance.md`。
5. 编写具体文档时，模板只提供该章节的最短提醒，帮助作者快速落笔。
6. `check-tasks` 继续只做最低诚实性约束，不负责承担写作教学。
7. 如果某份 guidance 后续改变了某些最小章节语义，相关模板和 skill 只做局部同步更新，不必牵动一份总文档。

这样形成的模型是：

- skill 负责“怎么做”
- guidance 负责“某个文档怎么写”
- template 负责“这里写什么”
- validator 负责“别空着或装完成”

## Stage Gates
- 必须明确三层职责边界，不能再把方法论含混地分散在 skill、模板和样例里。
- 必须说明为什么 guidance 应分文档放在 `references/`，而不是塞进 `SKILL.md` 或模板正文。
- 必须明确至少一种替代方案并说明不选原因。
- 必须定义失败模式：如果方案落地后维护者仍然需要主要靠 archived task packages 猜写法，说明设计仍然不够清晰。
- 必须给出降级方向：如果某个阶段 guidance 仍然过泛，就继续细化该 guidance 的问题清单，而不是重新回到总指南。

## Trade-offs
我考虑了三种主要方案：

- 方案一：把详细写作方法论写进 `SKILL.md`
  - 收益是用户在阶段内直接可见。
  - 代价是 `SKILL.md` 会膨胀成静态手册，阶段动作和文档写法混在一起，后续维护最容易重复与漂移。
- 方案二：把详细写作说明直接塞进模板
  - 收益是新建 task package 时立刻可见。
  - 代价是模板会变成长篇说明书，脚手架噪音大，还会把每个新包都变成半份教程。
- 方案三：在 `references/` 放按文档拆开的正式 guidance，skill 与模板只保留最小必要提示
  - 这是推荐方案。
  - 收益是职责边界清晰，阶段动作与静态写作 contract 同时可见，也最接近 OpenSpec “动作”和“artifact instruction”分开的优点。
  - 代价是 reference 文件数量增加，但每次只需打开当前文档对应的 guidance，实际认知负担更低。

回退面：

- 如果某份 guidance 仍然过长，可以继续在该 guidance 内按章节收敛，而不是重新合并成总文档。
- 如果模板提示被证明太短，可以补充 1 到 2 行“必答问题”而不是回退到长篇模板。

## Overview Reflection
- 我先挑战了“是不是应该把所有写作方法都放进 `SKILL.md`，因为 skill 本来就指导下一阶段要做什么”。结论是不应该。skill 适合指导阶段动作，但不适合承载大量稳定的静态写作规则，否则同一规则会在多个 child skill 重复出现。
- 我也挑战了“是否完全照搬 OpenSpec 的实现”。结论是不应该。OpenHarness 已经有 `04-verification.md`、`05-evidence.md` 以及状态流、归档模型，这些是 OpenSpec 之外的仓库特性，应该保留。
- 我检查了“是不是只靠模板多写几句就够了”。不够。模板适合提醒，不适合承担完整解释，尤其用户当前就是因为看不懂英文 skill、也不想靠历史样例自行推断。
- 我反过来挑战了“是不是应该保留总指南再加分阶段 guidance”。结论也不应该。总指南会重新变成上层概述，最后不是重复各份 guidance，就是制造新的事实源。
- 主要风险是分阶段 guidance 仍然写得太抽象，最后只是把空话拆成五份。为避免这一点，后续详细设计必须要求每类文档都写出必答问题、误写反例和边界说明。
- 本轮不需要有边界的子智能体讨论，因为核心决策是本仓库内的信息架构分层，而不是高不确定性的外部技术选择。
