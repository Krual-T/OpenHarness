# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 本轮不新增专门的 `pytest` 文档字符串测试。逐项设计确认主要改变 agent 协作协议，硬性断言某些文档片段存在容易锁死措辞，却不能证明真实协作行为合理。
- 主验证路径改为协议审查加仓库检查：
  - 运行 `uv run openharness check-tasks`，确认 task package 结构与状态有效。
  - 主智能体完成 skill 与 writing guidance 改造后，分配子智能体从使用者视角审查：遇到非机械开发任务时，是否会主动提出任务分类确认、是否会进入逐项设计确认、是否会按 `N/M` 推进、是否会把已确认设计点写回 task package。
  - 子智能体需要给出通过或不通过结论，并列出具体协议缺口。
- Fallback Path:
- 如果子智能体审查发现协议仍不清楚，不能宣称完成；需要回到对应 skill 或 guidance 修改后重新审查。
- 如果只能运行结构检查、无法完成子智能体审查，则只能记录为验证阻塞，不能把行为协议改造视为已验证。
- Planned Evidence:
- `04-verification.md` 需要记录 `uv run openharness check-tasks` 的结果、子智能体审查结论、发现的问题、修正动作与剩余风险。
- `05-evidence.md` 需要记录实际修改的 skill/guidance 文件、审查摘要和最终确认结论。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/SKILL.md`
  - 增加入口级规则：进入开发任务时先判断任务分类；非机械任务进入设计阶段前，主动提出逐项设计确认。
- `skills/brainstorming/SKILL.md`
  - 增加需求收敛后的任务分类建议规则：agent 提出 `mechanical` / `standard development` / `protocol/architecture`，但必须由人类确认后才作为后续触发依据。
- `skills/exploring-solution-space/SKILL.md`
  - 增加逐项设计确认执行规则：一次一个设计点、`N/M` 进度、推荐方案、理由、影响范围、确认问题、用户响应解释、写回 task package。
- `skills/using-openharness/references/overview-design-writing-guidance.md`
  - 增加 `02-overview-design.md` 应记录 overview 级已确认设计点的写作要求。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
  - 增加 `03-detailed-design.md` 应记录 detailed 级已确认设计点的写作要求。
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
  - 增加 `collaboration` 字段示例，用于表达已确认的任务类型和设计协作模式。
- `docs/archived/task-packages/design-decision-review-mode/STATUS.yaml`
  - 写入本任务已经确认的 `collaboration.task_type` 与 `collaboration.design_review_mode`，避免后续会话只能依赖聊天记录恢复协作上下文。

本轮不新增 skill、不新增 CLI、不新增 task package Markdown 文件。`STATUS.yaml` 增加可选机器可读字段，但不改变 `status:` 阶段状态机。

## Interfaces
本轮暴露的是 agent 协作协议接口，不是代码 API：

- 入口接口：`using-openharness` 负责告诉 agent 何时应进入任务分类与逐项设计确认。
- 需求阶段接口：`brainstorming` 负责提出任务分类建议，并要求人类确认分类。
- 设计阶段接口：`exploring-solution-space` 负责逐项推进设计点、解释用户响应、把确认结果写回 task package。
- 文档写作接口：overview 与 detailed writing guidance 负责约束 `02` 和 `03` 中的记录位置与记录内容。
- 状态接口：`STATUS.yaml.collaboration` 负责保存已确认的任务类型和设计协作模式，供 agent 读取任务状态时理解当前协作上下文。

稳定边界是：逐项设计确认属于现有设计阶段协议，不形成新的独立入口、独立 skill 或独立 task package 层级。

## Module Internals
职责分解：

- 编排：`using-openharness` 只判断是否进入该协作模式，并把后续执行交给阶段 skill。
- 分类确认：`brainstorming` 在 requirements 收敛后提出分类，且必须获得人类确认。
- 执行规则：`exploring-solution-space` 维护逐项确认的单点格式、进度语义、用户响应语义和写回规则。
- 写回约束：两个 writing guidance 只说明 `02` 与 `03` 分别记录哪些级别的 confirmed decision points。
- 状态更新：仍沿用 task package 当前状态流转；本轮不新增状态值。
- 协作状态：任务分类和设计协作模式写入 `STATUS.yaml.collaboration`，但不写入 `STATUS.yaml.status`。
- 副作用：唯一副作用是修改 task package 文档内容，不引入新的运行时副作用。

## Data Semantics
任务分类语义：

- `mechanical`
  - 指格式、命名、路径、局部文本、简单配置等低判断成本改动。
  - 不默认逐项确认，agent 可以直接执行并验证。
- `standard development`
  - 指常规功能、修复、文档协议调整、测试策略调整等需要设计但不是长期架构重塑的任务。
  - 进入 `02` 或 `03` 前，agent 主动建议逐项设计确认；用户可以调粗粒度或授权自主推进。
- `protocol/architecture`
  - 指会影响长期协议、skill 行为、目录结构、公共接口、agent 路由、验证路径或跨任务复用方式的任务。
  - 默认逐项设计确认；除非用户明确授权跳过，否则关键设计点逐项确认。

一致性约束：

- 任务分类由 agent 提出，但必须经过人类确认后，才作为后续设计阶段触发强度依据。
- 人类确认分类前，agent 不能把任务直接归类为 `mechanical` 并绕开必要设计讨论。
- 分类只决定协作触发强度，不改变 task package 状态机。
- 用户授权自主推进时，只降低确认粒度，不取消关键 decision points 写回要求。

`STATUS.yaml.collaboration` 字段语义：

```yaml
collaboration:
  task_type: protocol/architecture
  design_review_mode: stepwise
```

- `task_type`
  - 可选值：`mechanical`、`standard development`、`protocol/architecture`。
  - 只有在人类确认分类后才写入。
  - 字段缺失表示任务分类未确定，不能当作已确认事实。
- `design_review_mode`
  - 可选值：`stepwise`、`auto`。
  - `stepwise` 表示逐项设计确认。
  - `auto` 表示用户授权 agent 自主推进，但仍需记录关键 decision points。
  - 字段缺失表示协作模式未确定，需要澄清或提出建议。

OpenHarness 文档只解释字段含义和写入时机，不新增额外恢复流程。agent 读取任务状态时按这些字段理解当前任务的协作上下文。

逐项确认执行语义：

- 每次只提出一个设计点。
- 每个设计点包含 `设计点 N/M`、推荐方案、理由、影响范围和确认问题。
- `N/M` 是协作进度，不是 stage gate 完成度。
- 如果发现新设计点，可以更新 `M`，但要说明新增原因。
- 用户说 `确认` / `ok` / `可以` / `继续` / `下一个`，只确认当前设计点。
- 用户说 `自主推进` / `你决定` / `不用每点确认`，写入 `collaboration.design_review_mode: auto`，但仍要记录关键 decision points。
- 用户修改当前设计点时，agent 先复述最终版，再写回 task package。
- 用户推翻前序设计点时，agent 先更新已有 `02` 或 `03`；如果影响 overview 边界，先同步 `02` 再继续 `03`。
- 每个确认后的设计点应及时写回 task package，不积攒到最后。

## Stage Gates
detailed 进入实现前必须具备：

- 已确认验证策略不新增 pytest 文档字符串测试，而使用子智能体协议审查加 `uv run openharness check-tasks`。
- 已确认文件改造边界覆盖 5 个现有协议文档文件、`STATUS.yaml` 模板和当前任务包 `STATUS.yaml`，不新增 skill、CLI 或 task package Markdown 文件。
- 已确认任务分类包含 `mechanical`、`standard development`、`protocol/architecture`，且分类必须经过人类确认。
- 已确认 `STATUS.yaml.collaboration.task_type` 只有在人类确认分类后才写入。
- 已确认 `STATUS.yaml.collaboration.design_review_mode` 只有 `stepwise` 与 `auto` 两个值，字段缺失表示未确定。
- 已确认 `using-openharness` 负责非明显 mechanical 任务进入 overview 或 detailed 设计阶段前的主动触发。
- 已确认 `brainstorming` 负责需求收敛后的分类建议与人类确认。
- 已确认 `exploring-solution-space` 负责逐项确认的完整执行规则。
- 已确认用户授权自主推进时仍需写回关键 decision points。

## Decision Closure
用中文记录关键挑战如何被处理，只允许写清楚接受、拒绝或延期，以及对应理由、替代方案或触发条件。

设计点 1/6：验证策略。

结论：接受“不要新增 pytest 文档字符串测试，改用子智能体协议审查加 `openharness check-tasks`”。

理由：本轮核心是 agent 协作协议，不是可执行业务逻辑。针对文档写 pytest 断言固定措辞，容易变成形式主义；子智能体按使用者视角审查更接近真实触发路径，也能检查逐项确认是否会被主动纳入任务流程。

设计点 2/6：文件改造边界。

结论：先接受只改 5 个现有协议文档文件：`using-openharness`、`brainstorming`、`exploring-solution-space`、overview writing guidance、detailed writing guidance。后续设计点 4/6 确认需要增加 `STATUS.yaml` 模板与当前任务包 `STATUS.yaml` 的协作状态字段。

理由：入口判断、需求后分类、设计阶段逐项推进和文档写回分别落在对应现有层级，可以避免新增一套平行工作流，也避免把同一段规则重复塞进所有 skill。

设计点 3/6：任务分类与触发规则。

结论：接受三类任务分类与两层触发写法。`brainstorming` 负责提出并获得人类确认的分类；`using-openharness` 负责非明显 mechanical 任务进入 `02` 或 `03` 前主动提出逐项设计确认。

理由：分类属于需求收敛后的判断，触发属于入口和阶段路由。两者分开能避免把需求判断、协作话术和设计执行规则混在同一个 skill 中。

设计点 4/6：任务协作状态字段。

结论：接受在 `STATUS.yaml` 增加可选 `collaboration` 字段，包含 `task_type` 与 `design_review_mode`，不保留 `task_type_confirmed`，不设置 `none` 模式。

理由：`STATUS.yaml` 是机器可读状态源，适合保存跨会话需要读取的协作状态。`task_type` 只在人类确认后写入，因此不需要额外 confirmed 字段；`design_review_mode` 只保留 `stepwise` 和 `auto`，字段缺失表示未确定。

设计点 5/6：逐项确认执行规则。

结论：接受把完整执行规则主要写入 `exploring-solution-space`，由它负责设计阶段的一次一个设计点、`N/M` 进度、用户响应解释、模式切换和写回规则。

理由：`using-openharness` 负责触发，`brainstorming` 负责分类；真正推进 overview 与 detailed 设计的是 `exploring-solution-space`，执行细节放在这里边界最清楚。

设计点 6/6：迁移与落地顺序。

结论：接受按 `STATUS.yaml` 模板、`using-openharness`、`brainstorming`、`exploring-solution-space`、两个 writing guidance、验证与证据写回的顺序落地。

理由：先明确机器可读状态字段，再改入口触发、分类确认、设计执行和写作落点，可以降低文档之间互相引用但语义尚未定义的风险。旧任务缺失 `collaboration` 字段仍有效，回滚也可以优先调整 skill 触发强度而不是改变任务包状态机。

## Error Handling
主要失败路径：

- 静默出错风险：用户说“继续”后，agent 把它误解为后续所有设计点都自动通过。处理方式是在 `exploring-solution-space` 明确规定“继续/下一个”只确认当前设计点。
- 协作模式误写风险：用户授权自主推进后，agent 没有写入 `collaboration.design_review_mode: auto`，导致后续任务状态不完整。处理方式是在执行规则中说明授权后要写入字段。
- 分类绕过风险：agent 在人类确认前写入 `collaboration.task_type`。处理方式是在 `brainstorming` 说明只有人类确认后才写入。
- 文档积压风险：agent 等所有设计点都确认后才写回 task package，导致中途新会话丢上下文。处理方式是要求每个设计点确认后及时写回。

## Migration Notes
落地顺序：

1. 先改 `skills/using-openharness/references/templates/task-package.STATUS.yaml`
   - 增加可选 `collaboration` 字段示例。
   - 说明 `task_type` 只有人类确认后写入。
   - 说明 `design_review_mode` 只有 `stepwise` 和 `auto`。
2. 再改 `skills/using-openharness/SKILL.md`
   - 说明读取任务状态时要理解 `STATUS.yaml.collaboration`。
   - 说明非明显 mechanical 任务进入设计阶段前，主动提出逐项设计确认。
   - 只放触发和路由，不放完整执行规则。
3. 再改 `skills/brainstorming/SKILL.md`
   - 说明 requirements 收敛后提出任务分类。
   - 人类确认后写入 `collaboration.task_type`。
4. 再改 `skills/exploring-solution-space/SKILL.md`
   - 写入逐项确认完整执行规则。
   - 用户选择逐项确认时写入 `design_review_mode: stepwise`。
   - 用户授权自主推进时写入 `design_review_mode: auto`。
5. 最后改两个 writing guidance
   - `02` 记录 overview 级 confirmed decision points。
   - `03` 记录 detailed 级 confirmed decision points。
6. 验证
   - 运行 `uv run openharness check-tasks`。
   - 分配子智能体做协议审查。
   - 把结果写入 `04-verification.md` 与 `05-evidence.md`。

兼容策略：

- 已有旧任务没有 `collaboration` 字段时不报错。
- 字段缺失只代表未确定，不代表 `none`。
- 不改变 `status:` 阶段流转。

回滚策略：

- 如果协议审查认为规则太重或触发过度，先回滚 skill 文档中的触发强度，不需要回滚 task package 结构。
- 如果 `collaboration` 字段引起歧义，保留 `status:` 不变，只调整字段说明。

## Recommended Diagrams
本轮不需要补图。任务分类、协作模式、逐项确认与写回规则已经可以用字段语义和执行规则表达清楚。

## Detailed Reflection
测试策略反思：本轮确认不新增 pytest 文档字符串测试，避免把协议文档验证变成固定措辞断言。行为验证改为子智能体协议审查加 `uv run openharness check-tasks`。

接口边界反思：逐项设计确认没有新增独立 skill，也没有新增 task package Markdown 文件；它扩展现有 `using-openharness`、`brainstorming`、`exploring-solution-space` 与 writing guidance 的职责。

迁移假设反思：`STATUS.yaml.collaboration` 是可选字段，旧任务缺失该字段仍有效。字段只保存协作状态，不承载具体设计内容。

验证路径反思：协议审查必须从使用者视角检查触发、分类确认、`N/M` 推进、`stepwise` / `auto` 模式写入和 task package 写回，不能只检查文档是否包含关键词。
