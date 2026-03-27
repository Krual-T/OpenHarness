# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先撰写 `OH-033` 的需求、总体设计和详细设计，使其达到 `detailed_ready`。
  - 再运行 `uv run openharness check-tasks`，确认新包在设计完成但尚未实现时仍满足当前 task package 校验。
  - 后续真正实施方法论时，再把验证扩展到 reference 新文档、模板调整和必要测试。
- Fallback Path:
  - 如果 `check-tasks` 暴露出当前设计文档缺失语义锚点，就先修正 task package 自身，而不是跳过状态推进。
  - 如果后续实施阶段发现“一份总指南”过长到难以维护，可以在不改变总体职责分层的前提下拆成多份 reference。
  - 如果实施阶段发现某些 child skill 仍然需要保留少量本地写作提示，应优先以链接和一句职责提醒解决，而不是重新复制整套方法论。
- Planned Evidence:
  - `OH-033` 完整的 `01`、`02`、`03` 设计文档。
  - 后续新增或修改的分阶段 guidance reference 文档。
  - 模板中保留但被收紧的简短提示。
  - `check-tasks` 通过结果，以及必要时补充的测试。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `docs/task-packages/task-package-writing-methodology/README.md`
  - 更新本包摘要和当前状态，让入口页反映这轮真实目标。
- `docs/task-packages/task-package-writing-methodology/STATUS.yaml`
  - 记录状态、完成标准和后续验证命令。
- `docs/task-packages/task-package-writing-methodology/01-requirements.md`
  - 写清用户背景、问题陈述和需求门槛。
- `docs/task-packages/task-package-writing-methodology/02-overview-design.md`
  - 固化推荐的信息架构分层和 OpenSpec 借鉴策略。
- `docs/task-packages/task-package-writing-methodology/03-detailed-design.md`
  - 把实施顺序、接口边界和失败路径写具体。
- `skills/using-openharness/references/requirements-writing-guidance.md`
- `skills/using-openharness/references/overview-design-writing-guidance.md`
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
- `skills/using-openharness/references/verification-writing-guidance.md`
- `skills/using-openharness/references/evidence-writing-guidance.md`
  - 计划新增的五份分文档 guidance，分别承载各阶段静态写作 contract。
- `skills/using-openharness/references/templates/task-package.01-requirements.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.04-verification.md`
- `skills/using-openharness/references/templates/task-package.05-evidence.md`
  - 计划做轻量收紧，只保留最短写作提示，必要时加简短“必答问题”而不是长篇说明。
- `skills/using-openharness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
  - 计划补阶段信息采集要求、必答问题和对分阶段 guidance 的引用，避免复制静态方法论。

## Interfaces
本轮涉及的接口与稳定边界如下：

- `using-openharness` 与 child skills 的接口边界
  - skill 输出仍然是阶段动作、阶段门槛、产出物落点。
  - skill 不再承担完整的文档写作教材，但必须明确阶段信息采集要求，并在需要处链接到对应 guidance。
- 模板与作者的接口边界
  - 模板继续作为脚手架，保留短提示。
  - 模板不再承担系统化解释，避免“每个新包都复制半本手册”。
- 分阶段 guidance 与作者的接口边界
  - 每份 guidance 只负责一个 task package 文档，避免“当前阶段还要在总文档中定位自己”。
  - 每类文档至少要定义：文档目的、必答问题、与相邻文档的边界、常见误写、合格特征。
- 校验器与方法论的边界
  - `check-tasks` 继续只验证最低语义锚点，不提升为质量评分器。
  - 若未来需要更强校验，应单独开包讨论，不能在本包里隐式扩张。

每份 guidance 建议采用以下章节骨架：

1. `Purpose`
2. `Questions This Document Must Answer`
3. `Boundary With Adjacent Documents`
4. `Common Failure Modes`
5. `Minimum Acceptable Shape`
6. `How To Use The Template`

这样既借鉴 OpenSpec 的显式 contract，又保持 OpenHarness 自身文件体系，并把“当前阶段要看什么”收敛到最小范围。

## Stage Gates
- 必须把后续新增或修改的文件列清楚，不能只停留在抽象口号。
- 必须明确分阶段 guidance 的统一章节骨架，证明后续实现不是“边写边想”。
- 必须明确 skill、模板、reference、validator 四层边界，避免实施时再发生职责回流。
- 必须明确后续验证方式，至少包括 `uv run openharness check-tasks`。
- 必须说明迁移顺序，使实现时不会先改模板和 skill，后面才发现 guidance 结构还没定。

## Decision Closure
- 接受：把详细写作方法论放到 `references/`，并按文档拆成多份 guidance 作为首轮实现形态。
- 接受：`SKILL.md` 继续承担阶段动作指导，例如检索、反思、推进阶段的做法。
- 接受：模板只保留最短提示，不承担完整手册。
- 拒绝：把写作指南主内容塞进 `SKILL.md`。理由是会放大重复和分散。
- 拒绝：只靠模板增强来解决问题。理由是模板天然不是长文说明书。
- 拒绝：完全照搬 OpenSpec 文件布局。理由是会破坏 OpenHarness 现有 task package 和验证分层。
- 延期：是否把某些“必答问题”升级成更强校验规则。触发条件是未来继续出现大量形式化空转，且单靠 guide 与模板无法改善。

## Error Handling
主要失败路径和防错方式如下：

- 如果实现时把大量静态写作规则重新复制到多个 skill 中，会再次制造协议漂移。
  - 防错方式：skill 只保留阶段动作与引用，不承载完整静态说明。
- 如果某份 guidance 写成泛泛而谈的价值口号，维护者仍然无法据此写文档。
  - 防错方式：每类文档都必须包含必答问题、边界说明和常见误写。
- 如果模板被扩写过长，用户新建 task package 时会看到过量噪音。
  - 防错方式：模板只保留简短提示，把长解释留在 reference。
- 如果未来有人误以为 `check-tasks` 已经能判断文档质量，会过度信任自动化。
  - 防错方式：在写作指南和相关 skill 中明确声明校验器只做最低诚实性检查。

## Migration Notes
建议的落地顺序如下：

1. 先新增五份分文档 guidance 并确定统一章节骨架。
2. 再根据 guidance 内容精简或微调五个 task package 模板。
3. 再在 `using-openharness` 及相关 child skills 中补上阶段信息采集要求和对对应 guidance 的引用。
4. 如有必要，再补充最小测试或文档校验，确保仓库不会回到职责混杂状态。

兼容策略：

- 不修改现有 task package 文件名和状态流。
- archived task packages 不要求立刻重写，只在相关任务再次触及时按新指南修正。
- 现有 skill 仍可工作，只是后续应减少承担静态写作说明的负担。

回滚注意事项：

- 如果后续发现某份 guidance 结构设计失当，可以局部回退该 reference，再保留其他 guidance 和设计结论，避免同时回滚全部模板和 skill。
- 不应在没有替代入口的情况下直接删除模板提示或 skill 中现有有效说明。

## Detailed Reflection
- 我反思了“是否应该在本轮就设计更强的自动校验”。结论是不应该。当前真正缺的是写作 contract，而不是再提前发明质量评分机制。
- 我也反思了“分成五份 guidance 会不会导致事实源分散”。这个风险有，但它小于总指南把所有阶段糊在一起的风险；只要每个 skill 只指向自己负责的 guidance，使用路径仍然清晰。
- 我再次检查了接口边界：skill 讲动作和必收集信息、guidance 讲写法、template 讲最短提示、validator 讲最低诚实性。这个分层是本轮最核心的稳定边界，实施时不能破坏。
- 我检查了迁移假设是否过强。当前假设是现有模板和 skill 都可以做渐进式调整，不需要大爆炸重写；这个假设与仓库现状相符，也更符合当前任务边界。
- 当前验证路径已经足够支持 `detailed_ready`，因为本轮目标是完成设计并让新包通过校验，而不是宣称实现已经完成。
