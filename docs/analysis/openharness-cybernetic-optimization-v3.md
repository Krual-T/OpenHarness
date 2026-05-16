# OpenHarness 工程控制论优化 v3

> 基于钱学森《工程控制论》第一性原理，综合 9 路并行调研（13个skill审计、CLI分析、3个归档任务复盘、6大外部系统设计哲学），对 v2 方案的简化重构。

---

## 零、v2 的问题

v2 报告做了详尽诊断（14处信息流断裂、5个反馈回路缺失、3阶段路线图），但犯了**过度设计**的错误：

- **把症状当根因**。14处断裂是因为缺少底层结构约束，逐个修补只会增加复杂度。
- **往系统上加东西，而不是减东西**。HARD GATE、依赖图、执行轨迹记录——每一个都合理，但加起来让系统更重。
- **外部参考变成了特性清单**。Superpowers的1%法则、Hermes的自进化、Claude Code的渐进式加载全堆进去了，但没有统一的设计哲学。

v3 回到工程控制论第一性原理，只做**减法和结构化**。

---

## 一、工程控制论第一性原理

钱学森《工程控制论》的核心不是理论公式，而是**将工程实践中的设计原则加以整理、取其共性、提升为科学理论**。这是元方法论：工程师每天都在做控制，但不知道自己"在做什么"——钱学森让他们意识到自己在做控制论。

从这个立场出发，为 AI Agent 技能系统提取4条可操作的第一性原理：

### 原理1：反馈回路必须闭合（Feedback Closure）

> 任何关键流程，如果缺少自动闭合的反馈回路，就一定存在质量风险。

**控制论定义**：传感器→比较器→执行器→被控对象→传感器，形成闭环。断环=失控。

**在Agent系统中的映射**：
- 编译器 = 语法层的反馈闭合（传感器=词法分析器，执行器=报错）
- 单元测试 = 行为层的反馈闭合
- CI/CD = 部署层的反馈闭合

**判断标准**：任何一个流程，问三个问题——谁检测偏差？谁比较目标值？谁执行修正？缺一不可。

### 原理2：分层控制（Hierarchical Control）

> 复杂系统必须按抽象层级分解，每层只处理本层信息。层间通信只能通过明确定义的接口。

**控制论定义**：高层管策略（做什么），中层管协调（怎么做），底层管执行（做）。层间不跨级控制。

**在Agent系统中的映射**：
- 战略层（Strategic）：决定做什么——路由、分类、范围界定
- 战术层（Tactical）：决定怎么做——设计、实现策略选择
- 操作层（Operational）：验证和闭环——测试、审查、归档

**判断标准**：一个skill如果同时做路由、做实现指导、做验证检查，它就是跨层混淆。

### 原理3：必要变异度（Requisite Variety）

> 控制器的变异度必须 ≥ 被控对象的变异度。简单控制器控制不了复杂系统。

**控制论定义**（艾什比定律）：只有多样性才能吸收多样性。

**在Agent系统中的映射**：
- 路由系统必须覆盖所有任务类型
- 如果一个skill的description不能让模型准确判断触发时机，变异度就不够
- 约束机制（减少自由度）比增加智能（扩大控制器状态空间）更经济

**判断标准**：存在多少种任务类型是路由表覆盖不到的？description能在多少种不同表述下被正确触发？

### 原理4：不可靠元件组成可靠系统（Reliability through Structure）

> 系统的可靠性不是元器件的加和，而是结构的涌现属性。

**控制论定义**：承认每个部件不可靠，通过系统结构获得整体可靠性。

**在Agent系统中的映射**：
- AI Agent 天然不可靠（会合理化、会跳步、会忘记约束）
- 不能靠"让Agent更聪明"来保证质量，只能靠结构约束
- "减少自由度，比增加智能更能让系统稳定"

**判断标准**：如果Agent在某一步犯了错，系统能否自动检测并阻止错误传播？

### 核心区分：控制论思维 vs 系统思维

系统思维回答"系统在做什么"，控制论思维回答"**我想让它做什么，以及怎么纠正偏差**"。控制论思维比系统思维多了一个**目标函数**和一个**调节机制**。对于OpenHarness，这意味着不是去描述"What skills exist and how they connect"，而是设计"How does the system steer agent behavior toward task completion goals"。

---

## 二、当前系统的结构性缺陷

用上述4条原理诊断，当前系统有**3个结构性缺陷**，不是14个表面问题：

### 缺陷A：信息访问模式低效（违反原理2）

> 反驳：using-openharness 承载的所有信息（路由表、写作指南、模板、CLI参考、RWP协议）都是**必要的**。再怎么优化，Agent 仍然需要读这些。不能因为"信息量大"就诊断为"架构问题"。

真正的问题不是"using-openharness管太多"，而是**Agent访问这些信息的模式太低效**。

当前 Agent 的访问路径是**线性遍历**：

```
读 SKILL.md (47行) →
  被告知需要读 session-routing.md →
    被告知需要读 state-routing-table.md (200+行，覆盖全部10个状态) →
      为当前1个状态，读了全部10个状态的信息 →
        被告知需要读 task-classification.md →
          被告知需要读对应的 writing-guidance →
            被告知需要查看 cli-reference →
              ...
```

**根因不是"职责过多"，而是"没有按状态的读取索引"**。Agent 必须读取 state-routing-table.md 的全部200+行才能找到自己当前状态对应的那一行。writing-guidance 全部挂在 using-openharness 下，Agent 要间接跳转多次才能拿到当前状态需要的文件。

这与分层控制原理的关系是：**不是职责跨层，而是信息没有按"当前所处层次"过滤**。同一个路由表里混合了战略层信息（状态是什么）、战术层信息（该读什么指南）、操作层信息（该执行什么命令），但没有告诉Agent"对你当前的状态，只需要看这几行"。

### 缺陷B：反馈回路开环（违反原理1）

当前系统有4个关键开环回路：

| 回路 | 当前 | 缺失 |
|------|------|------|
| 验证失败→修复→再验证 | 手动判断→transition implementing | 无自动触发机制 |
| 实现受阻→设计审查 | 需人工判断 | debugging的"3次失败→质疑架构"信号不回流到设计层 |
| 代码审查发现→修复→再审查 | requesting→receiving线性链 | 无强制重审查 |
| 技能执行效果→技能改进 | 无任何度量 | 无执行轨迹记录 |

**根因**：当前系统用"transition命令"模拟反馈——这是手动开环操作。真正的反馈需要：偏差检测→自动触发纠正动作→重新进入验证。

### 缺陷C：软约束为主，硬约束缺失（违反原理4）

OpenHarness几乎所有约束都是"软建议"（文字指令），极度依赖Agent自律：

```
软约束（Agent可能跳过）：
├── Exit Check（"必须"通过，但无强制检查器）
├── 反合理化表（Agent能看到，但可以选择忽略）
├── 门禁规则（"答不上来就阻塞"，但无机械阻止）
└── CSO原则（description写触发条件，但目前写了工作流摘要）

硬约束（架构层面强制执行）：
└── transition命令中archive预置条件（唯一的硬门禁）
```

对比Superpowers：Rule → Gate → Hook，三层约束逐级硬化。OpenHarness只有Rule层。

**根因**：系统设计时假设Agent会遵守指令。工程控制论的立场是：**假设Agent会尝试绕过约束，然后在架构层面使其不可能。**

---

## 三、外部系统的设计哲学参考

调研了6个系统，提取对OpenHarness最有用的3个设计原则：

### 来自 Superpowers：技能是代码，不是文档

> "Skills are not prose — they are code that shapes agent behavior."
> "每一行描述要么是行为信号，要么是浪费的token。"

三个可操作的模式：

1. **CSO（Claude Search Optimization）**：description必须是**触发器而不是摘要**。实测证明：description写工作流摘要→Agent把description当完整指令跳过body。description写触发条件→Agent正确读取完整skill。

2. **Gate > Rule**：Rule说"不要做X"（可以合理化绕过），Gate说"不满足条件就不能前进"（机械阻止）。1%法则就是Gate："哪怕1%可能适用，也必须调用这个skill。"

3. **反合理化表从失败中提取**：先让Agent无skill执行任务，记录verbatim合理化语句，然后写skill逐条反驳。不是"未雨绸缪"地写约束，而是"从实际错误中"提取约束。

### 来自 gstack：Thin Harness, Fat Skills

> "把智能往上推到skill里，把执行往下推到确定性工具里。Harness保持薄。"

三个可操作的模式：

1. **角色隔离 > 多Agent**：每个skill只在一个认知轨道上。`/plan-ceo-review`不关心怎么实现，`/review`不关心产品策略。

2. **CLAUDE.md是路由表**（~200行），不是指令堆（20,000行）。"如果我需要让你做两遍同样的事，就是我失败了"——意味着该写成skill。

3. **确定性问题用确定工具，判断问题用skill**：浏览器自动化200ms CLI vs 15秒MCP——75x效率差距。

### 来自 Claude Code：基础设施必须愚蠢

> "不要让你的基础设施有'想法'，让它只有'肌肉记忆'。"

三个可操作的模式：

1. **三层渐进式加载**：元数据层（~50 token/skill，始终加载）→ 指令层（触发时加载，<5000 token）→ 资源层（按需加载）。13个skill的发现成本从全量降为~650 tokens。

2. **断路器**："3次连续失败→跳闸→降级"。承认Agent一定会连续犯错，设计优雅降级而非祈祷不犯错。

3. **编排器上下文必须纯净**：所有"脏活"（大规模读文件、执行重型命令、浏览器操作）交给子Agent，编排器只收摘要。

---

## 四、优化方案：4个变化 + 1个原则约定

### 变化1：在路由表中加"按状态读取索引" + 写作指南就近存放（解决缺陷A）

**核心思路**：不拆分 using-openharness，而是在路由表中加一个**快速索引**，让Agent根据当前状态直接跳到需要的信息。

```
state-routing-table.md 顶部新增：

## 快速索引：按当前状态

| 当前状态 | 只需读 |
|---------|--------|
| proposing | brainstorming SKILL.md, requirements-writing-guidance.md |
| overview_designing | exploring-solution-space SKILL.md, overview-design-writing-guidance.md |
| detailed_designing | exploring-solution-space SKILL.md, detailed-design-writing-guidance.md |
| implementing | implementing阶段决策树（本文件第X行）, cli-reference.md |
| verifying | verification-before-completion SKILL.md, verification/evidence writing-guidance |
| archived | finishing-a-development-branch SKILL.md |
```

**具体改动**：
- state-routing-table.md 顶部加索引（5行表格），Agent 不需要读完整个200+行路由表
- 写作指南从 `using-openharness/references/` 移到**使用它的 skill 的 references/** 下：
  - `requirements-writing-guidance.md` → `skills/brainstorming/references/`
  - `overview-design-writing-guidance.md` → `skills/exploring-solution-space/references/`
  - `detailed-design-writing-guidance.md` → `skills/exploring-solution-space/references/`
  - `verification-writing-guidance.md` + `evidence-writing-guidance.md` → `skills/verification-before-completion/references/`
- 模板保留在 using-openharness/references/templates/（因为多个skill共用）
- CLI参考保留在 using-openharness/references/（因为所有状态都需要）

**为什么不是"拆分"**：using-openharness 承载的所有信息都是必要的。拆分到多个skill只会让Agent在不同skill间跳转来找同一份信息。正确的做法是让信息停留在一个地方，但提供更好的索引。

### 变化2：闭合关键反馈回路（解决缺陷B）

**核心思路**：不要在10个状态间加更多transition规则，而是在3个关键位置加硬性检查。

**位置1：verifying失败 → 自动触发 debugging**

```
当前：verifying失败 → Agent手动判断 → transition implementing
改为：verifying失败 → 区分失败类型 →
      代码行为失败 → 强制调用 systematic-debugging →
      修复后 → 重新进入 verifying（不经过implementing gate）
      文档质量不够 → 强制调用 reviewing-task-package
```

**位置2：implementing多次受阻 → 回流到设计审查**

```
当前：实现失败 → 继续尝试 → 无上限
改为：同一task连续3次transition implementing被退回 →
      强制回到 detailed_designing →
      重新审查03-detailed-design.md
      （借鉴Hermes的3次失败→质疑架构）
```

**位置3：code review在verifying前强制触发**

```
当前：requesting-code-review不在路由表中，可选
改为：implemented → verifying 的transition预置条件增加：
      STATUS.yaml必须包含code_review.completed字段
      或：implemented gate增加 "HARD CHECK: 代码审查是否完成？"
```

**注意**：这些不是"加一个HARD GATE标签"，而是让 `openharness transition` 命令的预置条件检查在对应场景下机械阻止前进。借鉴Claude Code的断路器模式：3次失败→强制降级，而不是让Agent自行判断。

### 变化3：建立三层渐进式技能加载（解决上下文效率）

**核心思路**：当前所有skill全量加载。改为三层：

| 层 | 内容 | Token预算 | 加载时机 |
|---|------|----------|---------|
| L1 发现 | name + description（SKILL.md frontmatter） | ~50 token/skill | 会话启动时全部加载 |
| L2 激活 | SKILL.md 完整正文 | <5000 token/skill | 路由表判定触发后加载 |
| L3 资源 | references/、templates/、scripts/ | 按需 | SKILL.md中显式引用时才加载 |

**具体改动**：
- 所有SKILL.md的description重写为**纯触发条件**（借鉴CSO）：`"当[状态/场景]时使用——[触发症状]"`，不写工作流摘要
- 各skill的references/子目录自包含所需资源，形成闭包
- 代理被告知：读L1 description判断是否触发 → 触发则读L2正文 → 正文中引用了references/才读L3

13个skill的初始发现成本：全量加载 → ~650 tokens（13×50）。节省90%+上下文。

### 变化4：优化skill内容流程灵活性（解决skill过于死板）

外部调研揭示了当前skill内容设计的两个结构性偏见：**先方案后质疑，以及无快通道**。

#### 以 brainstorming 为例

当前流程：Step1读上下文 → Step2提问 → Step3提2-3个方案 → Step4写需求 → Step5自检

对照 gstack 的 `/office-hours`：Phase1收集上下文 → Phase2区分模式 → **Phase3挑战前提** → Phase4生成替代方案 → Phase5输出设计文档

关键的差异：gstack 在生成方案之前，有一个完整的"Premise Challenge"阶段——先挑战"这真的是问题吗？"，再进入方案。而 OpenHarness 的 brainstorming 第三步就跳到"提出2-3个方案"——在充分质疑问题之前。gstack 的设计哲学来自 YC 创业方法论："大多数人在解决错的问题。"

对照 Superpowers：不强制2-3个方案，不强制一次一个问题。核心是"先得到用户对设计方向的确认"，而不是"完成特定数量的步骤"。

**建议的 brainstorming 流程调整**：

```
当前 brainstorming                        建议的 brainstorming
─────────────────                        ─────────────────
Step 1: 读上下文                         Step 1: 读上下文
Step 2: 提问（一次一个）     →           Step 2: 挑战前提
Step 3: 提出2-3个方案          →             "为什么现在做？不做会怎样？"
Step 4: 写需求                             "这真的是问题吗？还是问题的症状？"
Step 5: 自检                    →         Step 3: 判断任务清晰度
Step 6: 提议task_type                        清晰 → 快通道：直接写需求，一次确认
Step 7: 等待确认                              模糊 → 完整通道：
                                                a. 提问关键歧义（不强制一次一个）
                                                b. 提出方案（数量取决于不确定性）
                                         Step 4: 写需求
                                         Step 5: 自检 + 硬门禁
                                         Step 6: 提议task_type
```

关键变化：
1. **挑战前提前置**：在提方案之前，先质疑问题本身
2. **快通道**：机械性/高度明确的任务不强制走完整流程
3. **放弃强制2-3个方案**：不确定性高→多方案，不确定性低→一个推荐方案 + 一个被拒绝方案的简短说明即可
4. **保留Exit Check但加硬门禁**：transition预置条件检查requirements-writing-guidance的7个问题

#### 通用原则：skill内容设计标准

从调研中提取的3条原则，适用于所有skill的内容审视：

**原则1：步骤应声明"何时跳过"**
当前所有skill的步骤都是硬性列表（"Step1→Step2→Step3"），没有快速通道。每个skill应有一个判断逻辑：
```
如果 [条件] 满足 → 直接跳到 Step N
如果不是 → 继续完整流程
```
例如：TDD的"如果代码已是bug修复且bug已被测试复现 → 直接GREEN，跳过RED"

**原则2：反合理化表不应堵死所有合理跳过**
当前brainstorming的反合理化表：
```
"需求已经很清楚了，直接开始吧" → 不成立
"这次改动小，不需要完整需求分析" → 不成立
```
但确实存在"改动小且边界明确"的合理场景。反合理化表应该区分：
- 不可接受的理由（如"先写代码，需求后面补"） → 永远堵死
- 条件性可接受的理由（如"这次改动小"） → 列出可接受的条件

**原则3：skill间不应重复相同指令**
TDD Phase 4 Step 1（"先创建失败的测试用例来复现bug"）和 systematic-debugging Phase 4 Step 1 是同一句话。两个skill都在教Agent"写失败测试复现bug"，但用不同措辞。应该一个skill只写自己独有的指令，重复的概念用引用而不是重写。

### 约定1：技能写作必须从实际失败出发

**核心思路**：借鉴Superpowers的TDD for Prompt Engineering和Claude Code的"每一行指令必须对应一次真实Agent错误"。

- 新增或修改skill约束时，必须先记录：Agent在什么场景下做了什么错误行为？
- 反合理化表从verbatim合理化语句中提取，不是从想象中写
- 没有对应实际失败的约束 → 删除。"未雨绸缪"型的指令是浪费token

这比v2提出的"HARD GATE声明规范"、"执行轨迹记录系统"等基础设施要轻得多——先用简单约定开始。

---

## 五、与v2方案对比

| 维度 | v2 | v3 |
|------|----|----|
| 诊断方法 | 列举14处断裂 + 5个缺失回路 | 识别3个结构性缺陷（其中缺陷A经反驳后修正为访问模式问题） |
| using-openharness | 建议加依赖图字段、拆分为多skill | 不拆分，只在路由表中加快速索引 + 写作指南就近存放 |
| 反馈回路 | 建议加HARD GATE + 改next_skills | 在transition命令预置条件中加3个硬检查 |
| 渐进式加载 | 建议实现3层加载 | 同样的建议，但简化为description重写+references自包含 |
| skill内容质量 | 未涉及 | 挑战前提前置、快通道、反合理化表区分不可接受/条件性 |
| 新增机制 | on-success/on-failure/provides等字段 | 零新增元数据字段 |
| 软约束→硬约束 | 三层门禁架构（Hook/Gate/Rule） | 先在现有transition预置条件中加检查 |
| 自进化/自适应 | 执行轨迹→skill蒸馏→定期审查 | 暂不碰（Hermes经验：自进化仍是未解决挑战） |
| 技能度量 | 6个指标 | 先不做："能度量什么"之前先"做对了什么" |

---

## 六、实施优先级

### 立刻做（本周）

1. **重写所有13个SKILL.md的description**：改为纯触发条件格式，删除工作流摘要。CSO原则，零风险高收益。
2. **在state-routing-table.md顶部加快速索引**：5行表格，让Agent不读完200+行也能找到当前状态对应的信息。
3. **闭合verifying→debugging回路**：在 `openharness transition` 的预置条件中，增加"如果从verifying回退，检查最后一次verify是否failed→要求先调用debugging"。

### 短期（2周内）

4. **写作指南就近存放**：5份writing-guidance从using-openharness/references/移到使用它们的skill的references/下。
5. **implemented→verifying增加code review检查**：在transition预置条件中加。
6. **brainstorming流程调整**：挑战前提前置 + 快通道 + 放弃强制2-3方案数量。

### 中期（1个月内）

7. **实现3次实现失败→强制设计审查**：在transition命令中加计数器。
8. **所有skill加"何时跳过"判断逻辑**：不是只有brainstorming需要快通道。
9. **消除skill间重复指令**：TDD和systematic-debugging的重复指令用引用替代。

### 暂不做

- 执行轨迹记录→skill蒸馏（Hermes的经验表明这是未解决挑战）
- HARD GATE声明规范（先用transition预置条件解决问题，不够再加）
- on-success/on-failure/provides依赖图字段（增加元数据负担，收益不明确）
- 自适应/自改进回路（一阶控制做好了再考虑二阶）

---

## 七、核心原则速查

| 工程控制论原理 | OpenHarness 中的应用 | 现状 | 目标 |
|--------------|---------------------|------|------|
| 反馈闭合 | 验证失败→自动调试→再验证 | 开环 | 闭合 |
| 分层控制 | 按状态索引 → 只加载当前层需要的信息 | 线性遍历全部 | 按索引跳转 |
| 必要变异度 | description覆盖所有触发场景 | 写了工作流摘要 | 写触发条件 |
| 结构可靠性 | 硬约束（transition预置条件）> 软约束（skill文字） | 以软为主 | 硬约束补位 |
| 控制不确定性 | skill流程应声明"何时跳过" | 硬性步骤列表 | 条件性快通道 |

---

## 附录：调研来源

### 内部审计
- 13个SKILL.md + 全部references/子文件，深度审计（4个子Agent并行）
- openharness_cli/ 全部9个Python文件（1个子Agent）
- 3个归档任务包（OH-008、OH-038、OH-039）实践分析（1个子Agent）

### 外部系统调研
- **Superpowers** (obra/superpowers, ~170K stars)：GitHub源码 + RELEASE-NOTES.md + CLAUDE.md
- **gstack** (garrytan/gstack, ~88K stars)：GitHub源码 + THIN_HARNESS_FAT_SKILLS.md 设计文档
- **Hermes Agent** (NousResearch, ~100K stars)：GitHub源码 + DeepWiki + 社区分析
- **Claude Code** (Anthropic)：社区逆向分析(keli-wen/agentic-harness-patterns-skill) + Anthropic官方工程博客
- **OpenCode** (SST/anomalyco)：GitHub源码 + DeepWiki + 架构分析
- **Codex CLI** (OpenAI)：GitHub源码 + 架构分析

### 工程控制论文献
- 钱学森.《工程控制论》. McGraw-Hill, 1954.
- Gao, Z. "Engineering Cybernetics: 60 years in the Making." Control Theory and Technology, 2014.
- 钱学森、于景元、戴汝为.《一个科学新领域——开放的复杂巨系统及其方法论》. 自然杂志, 1990.
- 郑楠、李耀东、戴汝为.《人机融合智慧涌现：AI大模型时代的综合集成研讨体系》. 清华大学出版社, 2024.
