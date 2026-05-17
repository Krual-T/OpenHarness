# OpenHarness Skill 调用链路独立审计

> 独立分析，不从 v5 结论出发。关注 Agent 实际执行路径上的结构性张力，而非文件缺失或 schema 不一致。

---

## 一、理想调用链路

一个 Agent 使用 OpenHarness 处理标准开发任务的完整路径：

```
AGENTS.md → using-openharness → bootstrap → STATUS.yaml → 路由表 → 当前状态的skill

   proposing           overview_designing    detailed_designing     implementing        verifying          archived
   ┌──────────┐        ┌──────────────┐     ┌──────────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐
   │brainstorm│   →    │ exploring-   │  →  │ detailed-    │  →   │ TDD /    │   →   │ verif-   │   →   │finishing │
   │  ing     │        │ solution-    │     │ design       │      │ subagent │       │ ication  │       │ -branch  │
   │          │        │ space        │     │              │      │ / debug  │       │          │       │          │
   │01-req.md│        │02-overview.md│     │03-detail.md  │      │  代码    │       │04+05.md  │       │ 合并/PR  │
   └──────────┘        └──────────────┘     └──────────────┘      └──────────┘       └──────────┘       └──────────┘
        │                     │                     │                   │                  │                  │
   [7项Exit Check]      [6项Exit Check]       [7项Exit Check]      [代码审查?]       [6+5项Exit Check]   [4选项]
        │                     │                     │                   │                  │                  │
   transition →        transition →          transition →         transition →      transition →        终态
   reqs_designed       overview_designed     detailed_designed    implemented       archived
```

中间 4 个 `_designed` / `implemented` 是 gate 状态——按设计，Agent 只需执行 `openharness transition`，不调用任何 skill。

### 每个阶段的上下文加载量

| 阶段 | 加载内容 | 估算行数 |
|------|---------|---------|
| 入口 | AGENTS.md + using-openharness SKILL.md + 4个reference文件 | ~270 |
| proposing | brainstorming SKILL.md + 模板 | ~140 |
| overview_designing | exploring-solution-space SKILL.md + 模板 | ~160 |
| detailed_designing | detailed-design SKILL.md + 模板 | ~170 |
| implementing | TDD/subagent/debug SKILL.md（择一） | ~80 |
| verifying | verification-before-completion SKILL.md + 模板×2 | ~240 |
| archived | finishing-a-development-branch SKILL.md | ~55 |

完整标准流程累计加载 ~1100 行 skill/reference 内容，加上实际任务包文档。

---

## 二、发现的结构性问题

### 问题 1：Gate 状态是标签，不是门禁

`lifecycle.py` 的 `_ensure_transition_allowed` 只检查三件事：
- 目标状态是否在合法流中
- 是否跳过了中间状态
- 是否从正确状态归档

它不检查任何 Exit Check 内容。`requirements_designed`、`overview_designed`、`detailed_designed`、`implemented` 四个 gate 状态的门禁，完全依赖 Agent 自觉读完 skill 里的 6-7 个 Exit Check 问题并诚实回答。

这本身不是 bug——Exit Check 问题本质上是定性的（"能不能明确回答目标用户是谁？"），CLI 无法自动验证。但路由表把它叫做"gate"，实际行为却是"pass-through"。Agent 如果跳过 Exit Check 直接 transition，CLI 不会阻止。

**建议**：在路由表中明确标注哪些检查是 CLI 硬门禁、哪些是 Agent 自律门禁。不要让 Agent 在"这个会被挡下来吗"的猜测中做决策。

### 问题 2：`implemented` 状态语义矛盾

路由表说 `implemented` 是 gate 状态——不用调 skill，只做 transition。

但 `lifecycle.py` 的 `_next_step` 对 `implemented` 说：

```python
"implemented": (
    "Run declared verification, refresh `04-verification.md` and `05-evidence.md`, "
    "then transition to `verifying`."
),
```

这告诉 Agent 在 `implemented` 状态就开始跑验证、刷新 04 和 05 文档。但 04 和 05 按路由表是 `verifying` 状态的产出，由 `verification-before-completion` skill 负责。到底在哪个状态开始验证？两边说法矛盾。

**建议**：`_next_step` 的 `implemented` 提示不应建议跑验证和刷新验证文档，应只说"确认实现完成，然后 transition 到 verifying"。

### 问题 3：反合理化表——位置对了，时机错了

每个 skill 都有反合理化表。以 brainstorming 为例：

```
| "需求已经很清楚了，直接开始设计吧" | 清楚到能写下来 ≠ 实际上写下来了... |
| "用户只问了一个小功能" | 小功能也可能有隐式假设... |
| "先写代码，需求后面补" | 后面不会补的... |
```

三个问题：

**a) 跨 skill 重复。** "先写代码再补文档"这个借口在 brainstorming、exploring-solution-space、detailed-design 三个 skill 中反复出现，措辞不同但论证相同。这是上下文膨胀的纯冗余。

**b) 加载时机与决策时机错位。** Agent 在进入 skill 时读到这些，但合理化倾向发生在想跳过步骤的那一刻——这时反合理化表早就在上下文窗口远处，甚至可能已被压缩。Agent 不会在决策点回查。

**c) 语调是"训诫另一个 Agent"，不是"指导当前 Agent"。** 写法是第二人称反驳句式（"这不是例外，是借口"），本质是对过去犯过错的 Agent 喊话。对于当前 Agent，有效信息是正面的规则陈述，不是驳论。

**建议**：将反合理化内容从 skill 正文中分离。两种可行方式：
- 提取为独立文件，在 Exit Check 中引用（"如果有以下想法，读 X 文件"）
- 将反例转化为正面的约束陈述（"不清楚到能写下来的需求 = 不存在"→ 不如直接写规则："所有需求必须在 01 中写下来才能 transition"）

### 问题 4：RWP 是全空协议

整个 RWP 机制有四层，只有三层存在：

```
runtime-capability-contract.md   ✓ 协议定义
runtime-workflow-packages.md     ✓ 使用说明
openharness rwp list/show/run    ✓ CLI 实现
.harness/rwp/workflows/          ✗ 零个实际工作流
```

`exploring-solution-space` 的步骤 5 要求 Agent 运行 `openharness rwp list` 检查候选 RWP。结果永远是空列表 → Agent 记录"RWP gap" → 流程继续。

**这不是"缺少 RWP"的问题，而是"协议从未被端到端验证过"的问题。** CLI 命令存在、文档存在、模板存在，但没有任何项目实际走过 RWP 发现→选择→执行→写回的完整路径。当第一个真正的 RWP 被创建时，这个流程大概率会发现设计假设与实际情况不匹配——例如：
- RWP 选择需要子 agent 执行，但 overview_designing 阶段是否已经有足够的上下文给子 agent？
- `openharness rwp run` 的日志写回路径设计为 `.harness/rwp/logs/`，但 verification 阶段的 `05-evidence.md` 期望在 task package 目录下找到产物——两者如何关联？

**建议**：要么为 OpenHarness 自身创建一个 RWP（狗粮自用），验证端到端流程；要么在协议文档中标注"此功能尚未有生产使用，设计假设待验证"。

### 问题 5：brainstorming "快通道"与 task_type 分类的循环依赖

brainstorming 定义了两条路径：

- **快通道**：任务清晰 → 3-5 行确认用户和动机 → 直接写 01
- **完整流程**：任务模糊 → 挑战前提 → 收集信息 → 提出多方案

但 task_type 的分类时机在 brainstorming **完成之后**：`task-classification.md` 明确说"brainstorming 完成后、需求已收敛时，对 task_type 做最终确认"。

Agent 在 brainstorming 开始时并不知道这是 `mechanical` 还是 `standard development`。快通道和 mechanical 流程都意味着"更少的文档开销"，但它们是两个独立的决策点。文档没有说明：

- 快通道的"清晰任务"和 task_type 的 `mechanical` 是否等效？
- 如果走快通道写完 01 后发现应该是 `standard development`，此时需要补完整流程的步骤 2-4 吗？
- 如果走完整流程发现其实很简单，可以降级为 `mechanical` 吗？

**建议**：在 brainstorming 文档中明确：快通道/完整流程的选择是 brainstorming 内部的方法论选择，task_type 是产出 01 之后的状态机选择。两者独立决策，但快通道产出的 01 不排斥后续走标准流程。

### 问题 6：Skill 内部引用路径对子 Agent 不可用

多个 skill 引用模板文件时使用从项目根目录出发的路径：

```
brainstorming:          skills/using-openharness/references/templates/task-package.01-requirements.md
exploring-solution-space: skills/using-openharness/references/templates/task-package.02-overview-design.md
```

这些路径对主 Agent（已读过 AGENTS.md 即仓库地图）不是问题。但如果一个子 agent 只拿到 skill 内容就被调度去写文档，它无法从 skill 内提供的路径找到模板——因为子 agent 可能不知道项目根目录在哪，或者 working directory 不同。

**建议**：skill 中引用路径时加注"从项目根目录"或在 AGENTS.md 中增加一条子 agent 路径约定。

### 问题 7：verification-before-completion 承载过多

这个 skill 有 135 行，混合了三件事：

1. **流程指令**（怎么验证）：确认路径 → 执行 → 读取 → 确认 → 写回
2. **文档规范**（怎么写 04 和 05）：两个 Exit Check 组（6+5 个问题）、阶段写回规则、边界定义
3. **反合理化护城河**（最大的那张表）：声称-需要-不够的映射表，10 种常见错误声明 + 12 条借口反驳

如果 Agent 在 verifying 阶段同时需要：执行 `openharness verify`、调度 `reviewing-task-package` 做文档审核、处理验证失败的路由——这个 skill 列出了"验证失败时"的路由表，但没有说明正常流程中这些步骤的先后顺序。

Agent 可能的困惑：先调 `reviewing-task-package` 还是先跑 `openharness verify`？文档审核是阻塞的还是并行的？

**建议**：在 verification-before-completion 开头增加一个步骤顺序表，明确正常流程中的串行/并行关系。

---

## 三、结构性张力总结

以上 7 个问题指向三个深层结构性张力，而非表面 bug：

### 张力 A：Skill 身份过载

每个 Skill 同时是：
- 流程说明书（步骤 1-2-3）
- 质量护城河（Exit Check）
- 反合理化手册（常见借口反驳）
- 边界定义（与相邻文档的关系）
- 失败模式目录

五种内容混在一个文件里，Agent 每次调用都要全量加载。当 Agent 只是需要查"下一步 transition 到哪"时，也要加载 100 行反合理化内容。

### 张力 B：硬门禁与软门禁的边界未文档化

哪些检查是 CLI 强制、哪些依赖 Agent 自律——这个区分没有在任何地方明确写出来。对 Agent 的行为影响巨大：
- Agent 不确定某个检查是否会被 CLI 挡住，可能过度谨慎（反复确认）或过度冒险（赌 CLI 不检查）
- 路由表用"gate"一词同时指代 CLI 硬门禁和 Agent 自律门禁，加剧混淆

### 张力 C：RWP 协议是"先有答案再找问题"

定义了一个完整的运行时验证框架，但没有任何项目使用它。设计假设（渐进式发现、子 agent 选择、写回流程）从未被验证。这不是"功能未完成"的问题，而是"架构未验证"的问题。

---

## 四、与 v5 的差异

| 维度 | v5 结论 | 本审计 |
|------|--------|--------|
| STATUS.yaml 缺 `code_review` | 声称缺失 | **已存在**（模板第40-44行），v5 诊断过时 |
| Code review 回路断裂 | P0 严重 | 存在但不严重。`_warn_code_review_gap` 是 warn 不是 block——这是有意设计。问题是路由表没标注这个可选入口 |
| Gate 状态软门禁 | 应加强 | 软门禁本身不是问题——Exit Check 的定性本质决定了它无法被 CLI 硬校验。真正的问题是 `implemented` 状态语义矛盾 |
| Guidance 删除 | 正确决策 | 同意，但遗留问题是 Skill 变得臃肿。反合理化表跨 Skill 重复是 v5 遗漏的 |
| RWP 空转 | 未提及 | 最被低估的问题——定义了完整协议但没有一条端到端验证过的执行路径 |
| 反合理化表 | 认为是正优化 | 结构性问题的核心——加载时机与决策时机错位，跨 skill 重复 |

---

## 五、优先级建议

| 优先级 | 问题 | 理由 |
|--------|------|------|
| P1 | 问题 2：`implemented` 语义矛盾 | 影响 Agent 行为——Agent 不知道该不该在 implemented 状态开始验证 |
| P1 | 问题 5：快通道/分类循环依赖 | 影响 brainstorming 阶段的决策质量 |
| P2 | 问题 3：反合理化表结构 | 不是功能 bug，但持续造成上下文膨胀 |
| P2 | 问题 7：verification 承载过多 | 影响 verifying 阶段的执行效率 |
| P2 | 问题 4：RWP 空协议 | 当前无实际影响，但协议设计假设未验证是个定时炸弹 |
| P3 | 问题 1：Gate 标签歧义 | 文档措辞问题，不影响功能 |
| P3 | 问题 6：Skill 路径对子 Agent 不可用 | 边界场景，影响范围有限 |
