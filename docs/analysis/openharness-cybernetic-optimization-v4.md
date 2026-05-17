# OpenHarness 工程控制论优化 v4

> 基于钱学森《工程控制论》第一性原理，综合18路并行调研（13个skill深度审计、CLI全量分析、3个归档任务复盘、5类写作指南审计、7大外部系统设计哲学、工程控制论文献与SDD实践调研），重新发现OpenHarness的SDD本质并给出优化方案。

---

## 零、v3的根本问题：没认出SDD

v3做了大量有价值的诊断（信息访问模式、反馈回路开环、软硬约束失衡），但它犯了一个根本性的认识错误：**把OpenHarness当作"技能系统"来优化，而不是"控制论驱动的规范系统"来设计。**

OpenHarness的五文档流水线（01-requirements → 02-overview-design → 03-detailed-design → 04-verification → 05-evidence），配合10阶段状态机、写作指南的门禁退出检查、以及 `openharness transition` 的硬性预置条件，**本身就是一套完整的SDD（Specification-Driven Development）控制论系统。**

### SDD的证据

1. **规范先于代码**：`proposing` → `overview_designing` → `detailed_designing` → `implementing` 的顺序不可逆。机械任务可跳过设计阶段，但不可跳过需求。
2. **规范是合约**：反合理化表反复驳回"需求很清楚不需要写"、"先写代码后面补"——规范必须是显式写入文件的。
3. **验证追溯规范**：`04-verification.md` 的 Traceability 部分要求将需求→设计决策→验证证据可追溯映射。
4. **规范驱动自动化**：`STATUS.yaml` 的 `verification.required_commands`、`task_type`、`design_review_mode` 是机器可读的规范元素，直接驱动CLI行为。
5. **规范包含边界**：Non-Goals with counterexamples、System Boundary exclusion scope、Decision Closure（accepted/rejected/deferred）是硬性要求的章节。

**工程控制论视角**：规范就是控制论系统中的"目标函数"。OpenHarness不是在"管理任务"，而是在**将Agent行为持续校正到规范定义的目标状态**。

---

## 一、工程控制论第一性原理（重述与深化）

v3提出了4条原理，本次调研深化为5条可操作原理：

### 原理1：反馈闭合（Feedback Closure）

> 任何关键流程，如果缺少自动闭合的反馈回路，就一定存在质量风险。

**控制论定义**：传感器→比较器→执行器→被控对象→传感器。断环=失控。

**OpenHarness现状**：4个关键回路中，verifying→debugging回路已被v3提出但仅作为CLI警告（`_check_verifying_rollback_preconditions`中的软阻止）。code review回路**完全开环**——两个技能（requesting/receiving）不连接路由表、不连接彼此、不产生持久化产物。

**归档任务实际验证**：OH-038发现 `openharness verify` 是全局验证（一个包损坏阻塞所有包）——这意味着验证反馈回路存在结构性单点故障。

### 原理2：分层控制（Hierarchical Control）

> 复杂系统必须按抽象层级分解。层间通信只能通过明确定义的接口。

**OpenHarness现状**：using-openharness的路由表混合了三层信息（战略层"状态是什么"、战术层"读什么指南"、操作层"执行什么命令"）。Agent的访问路径是线性遍历——先读SKILL.md（47行）→ 被告知读session-routing.md → 被告知读state-routing-table.md（200+行）→ 为当前1个状态读了全部10个状态的信息。

**实际改进**：v3提出的"按状态快速索引"是一个好的开始，但本质问题是：**信息没有按Agent当前所处的控制层级过滤**。

### 原理3：必要变异度（Requisite Variety）

> 控制器的变异度必须 ≥ 被控对象的变异度。

**OpenHarness现状**：13个skill的description当前写了工作流摘要而非触发条件。调研发现大量skill的description是"当[状态]时使用——做什么"而非"当[状态/场景]时使用——[触发症状]"。

**Superpowers的CSO原则**：description必须是触发器而不是摘要。实测证明：写工作流摘要→Agent把description当完整指令跳过body。写触发条件→Agent正确读取完整skill。这是必要变异度的直接应用：description必须覆盖所有触发场景的表述变体。

### 原理4：结构可靠性（不可靠元件组成可靠系统）

> 系统的可靠性不是元器件的加和，而是结构的涌现属性。

**OpenHarness现状**：绝大多数约束是软约束（文字指令），极度依赖Agent自律。只有 `transition` 命令的预置条件检查是真正的硬约束。

**Superpowers的对抗设计**：Rule说"不要做X"（可合理化绕过），Gate说"不满足条件不能前进"（机械阻止）。OpenHarness需要在架构层面**假设Agent会尝试绕过约束，然后使其不可能**。

**Hermes的经验教训**：即使Hermes的自进化技能系统报告"92%的人类质量"，8%的差距仍然意味着不可靠。自进化是未解决的挑战——先做好一阶控制。

### 原理5：前馈控制（新增，v3遗漏）

> 与其等错误发生后再纠正，不如在执行前主动加载纠错信息。

**控制论定义**：前馈通道在干扰进入系统前就进行补偿。

**在Agent系统中的映射**：
- Superpowers的反合理化表 = 前馈控制：在Agent产生合理化念头之前就驳斥常见借口
- Hermes的frozen memory snapshots = 前馈加载：会话开始时注入关键约束
- OpenHarness现状：反合理化表分散在SKILL.md和各writing-guidance中，Agent必须读到那一步才看到——缺少顶层前馈注入

---

## 二、18路并行调研的核心发现

### 2.1 13个Skill的结构性审计

| Skill | 核心问题 | 严重程度 |
|-------|---------|---------|
| **brainstorming** | 快通道仍要求完整01-requirements.md；反合理化表跨SKILL.md和guidance重复50% | 中 |
| **exploring-solution-space** | 模板路径错误（缺task-package.前缀）；exit check计数错误（声称5项实列6项）；重新调用detailed_designing时无跳过步骤1-4的指引 | 高 |
| **test-driven-development** | "必须删除代码"规则过于刚性；SKILL.md未引用自己的testing-anti-patterns.md；无快速路径 | 中 |
| **verification-before-completion** | 步骤4"修改文档后返回步骤2"对纯文档修改不合理；验证失败路由不覆盖"需要重新实现"场景；19个反合理化陷阱分布在3个文件中过于碎片化 | 中 |
| **finishing-a-development-branch** | 不处理合并冲突；`$BRANCH_NAME`变量未定义；步骤1与CLI预置条件重复检查 | 中 |
| **systematic-debugging** | `references/defense-in-depth.md`引用路径损坏（实际在技能根目录）；阶段4计数器作用域不明确；压力测试无文档化答案标准 | 高 |
| **requesting-code-review** | `allow_implicit_invocation: false`与description声称的触发条件矛盾；路由表中完全不存在；差异范围硬编码`HEAD~1..HEAD` | 严重 |
| **receiving-code-review** | next_skills为空→反馈处理后无定义；缺references/目录；内部/外部审查者场景混杂 | 严重 |
| **reviewing-task-package** | references/目录为空；审核报告写回被审核文档可能造成自引用循环；隐式调用与路由表不匹配 | 低 |
| **subagent-driven-development** | "子代理"抽象层不明确（如何实例化？）；快速/标准/最强模型未定义；异步编排的上下文持续性未说明 | 中 |
| **dispatching-parallel-agents** | **60-70%内容与subagent-driven-development冗余**；缺references/目录；缺模型选择、状态处理、包级关闭 | 严重 |
| **using-git-worktrees** | `$BRANCH_NAME`和`$path`变量未定义；与using-openharness/subagent-driven-development的集成仅单向声明（对方skill不提及worktree）；无命名规范 | 高 |
| **using-openharness** | 快速索引导入后仍存在4步链接阅读；runtime相关4个文件概念重叠可合并；CLI参考与路由表列出的命令逐字重复 | 低 |

### 2.2 CLI分析核心发现

1. **code_review_gap是软警告**（`_warn_code_review_gap`仅打印不阻塞）——这正是code review回路开环的技术根因
2. **verifying→implementing回退已是硬阻止**（`_check_verifying_rollback_preconditions`）——但只在verification result是"failed"时阻止，且要求"先调用systematic-debugging"
3. **transition命令无并发锁**——两个并发transition可能竞争STATUS.yaml
4. **`shell=True`无输入转义**——`required_commands`中的用户输入是潜在的shell注入向量
5. **`auto_archive`在discover时运行**——这是一个读操作中的副作用

### 2.3 归档任务复盘发现

从OH-038、OH-039、OH-016三个任务包的实际使用中：

1. **全局验证是单点故障**：OH-038发现不相关包的损坏YAML阻塞了整仓验证
2. **无"需要更新什么"的自动化分析**：OH-039中agent必须手动发现所有引用project-memory脚本的位置
3. **文档测试是浅层文本断言**：无法验证正确性——只能验证"字符串存在"
4. **推迟的技术债无后续机制**：所有三个包都有诚实的残余风险记录，但无系统机制强制未来解决
5. **三个包都展示了强SDD实践**：先写需求→验收标准→测试断言→验证证据，决策闭合明确列出accepted/rejected/deferred

### 2.4 外部系统设计哲学

| 系统 | 核心哲学 | 对OpenHarness最可操作的借鉴 |
|------|---------|--------------------------|
| **Superpowers** | Gates > Rules | 硬门禁机制（1% Rule、反合理化表、验证门禁）可编码进OpenHarness runtime |
| **gstack** | Thin Harness, Fat Skills | 角色隔离＞多Agent；每个skill只在一个认知轨道上 |
| **SpecKit** | 规范是持久化制品 | Constitution→Spec→Plan→Tasks的制品链；多Agent对抗验证 |
| **Claude Code** | 基础设施必须愚蠢 | 3层渐进加载、断路器（3次失败→降级） |
| **Hermes** | 自进化能力 | 自进化仍是不成熟技术（92%人类质量），暂不借鉴 |
| **OpenCode/Codex** | 平台可移植性 | 多模型支持是趋势但非当前优先级 |

### 2.5 工程控制论与SDD的连接

调研确认了一个关键认知：**工程控制论与SDD的关系不是"两个不同的东西"，而是"理论与其工程实践"**。

- 系统思维回答"系统在做什么"
- 工程控制论回答"**我想让它做什么，以及怎么纠正偏差**"
- SDD是实现工程控制论的**具体工程方法**：规范=目标函数，验证=传感器，transition门禁=比较器，修复循环=执行器

钱学森1954年《工程控制论》的核心洞察——"将工程实践中的设计原则加以整理、取其共性、提升为科学理论"——恰好是OpenHarness正在做的事：将Agent开发中的约束模式抽象为可复用的控制论结构。

---

## 三、优化方案：5个结构性变化

### 变化1：在架构层面承认并强化SDD（认知升级）

**不是加代码，而是改认知框架。**

当前OpenHarness的自我描述是"skill-based agent harness"。更准确的描述应该是：

> **OpenHarness是一个控制论驱动的规范系统**（Cybernetic Specification-Driven Development harness）。它通过不可变的五文档规范制品+10阶段状态门禁+机器可验证的退出检查，将不可靠的LLM Agent行为持续校正到规范定义的目标状态。

**具体改动**：
- AGENTS.md、README.md中的自我描述从"skill系统"改为"控制论规范系统"
- using-openharness/SKILL.md的入口描述增加一句："OpenHarness的每个skill不是一个'功能'，而是一个控制论回路——它定义了目标状态（规范）、偏差检测（退出检查）、和执行修正（transition门禁）"
- 13个SKILL.md的description从"当[状态]时使用——做什么"改为"当[触发症状]时使用——这个skill闭合了什么控制论回路"

### 变化2：闭合4个关键反馈回路（解决缺陷B）

#### 回路1：代码审查 ← 严重开环

**当前状态**：requesting-code-review和receiving-code-review完全不连接路由表、不连接彼此、不产生持久化产物、不阻塞transition。

**修复方案**：
1. 在路由表 `implemented` 行增加退出条件：`code_review.completed = true`
2. 在CLI `_warn_code_review_gap` 中：将软警告升级为硬阻止（非mechanical任务从implemented→verifying时，STATUS.yaml必须包含code_review.completed字段）
3. requesting-code-review的 `allow_implicit_invocation` 改为 `true`
4. receiving-code-review增加退出后行动：修复完成后→重新请求审查（闭合回路）
5. STATUS.yaml增加 `evidence.code_review` 的结构化字段：`{completed: bool, reviewer: string, result: "approved"|"changes_requested", artifact_path: string}`

#### 回路2：验证失败→自动调试→再验证

**当前状态**：CLI已有 `_check_verifying_rollback_preconditions` 硬阻止，但仅检查verification result是否为"failed"。

**修复方案**：
1. 保留现有硬阻止
2. 在 `_check_verifying_rollback_preconditions` 中增加：如果从verifying回退到implementing，且失败类型为代码行为→要求STATUS.yaml中记录debugging session引用
3. systematic-debugging增加修复后的显式步骤："修复完成后→transition到verifying→重新运行openharness verify"

#### 回路3：实现多次受阻→设计审查

**当前状态**：systematic-debugging有"3次失败→质疑架构"的规则，但计数器不持久、不跨skill调用、不自动触发设计阶段回退。

**修复方案**：
1. 在STATUS.yaml中增加 `debugging.failed_attempts` 计数器（持久化）
2. CLI `transition implementing` 时检查该计数器≥3→阻止transition，要求先回退到 `detailed_designing`
3. systematic-debugging的阶段4步骤4增加：每次失败后写入STATUS.yaml

#### 回路4：技能执行效果→技能改进

**当前状态**：无任何度量。Hermes的自进化是未解决挑战，但可以从不那么野心的地方开始。

**修复方案**（最低可行）：
1. 在归档任务的05-evidence.md中增加一个可选section：`## Skill Feedback`——记录执行过程中的skill改进建议
2. 这个section不是自动化的，而是给人类维护者看的
3. 不搞自动化skill蒸馏（Hermes证明这仍是未解决挑战）

### 变化3：消除冗余、修复硬错误（清理）

以下问题直接导致Agent行为异常或增加认知负担：

#### 3.1 两个subagent skill合并

**问题**：dispatching-parallel-agents的60-70%内容与subagent-driven-development重复。前者缺少模型选择、状态处理、包级关闭。独立使用不安全，作为子技能又完全冗余。

**方案**：将dispatching-parallel-agents的独特内容（按独立问题域分组、prompt结构要求）合并到subagent-driven-development的并发部分。删除dispatching-parallel-agents SKILL.md，保留agents/openai.yaml作为subagent-driven-development的并发变体入口。

#### 3.2 修复引用路径错误

| 位置 | 错误 | 修复 |
|------|------|------|
| exploring-solution-space/SKILL.md:59 | `using-openharness/references/templates/02-overview-design.md` | `using-openharness/references/templates/task-package.02-overview-design.md` |
| exploring-solution-space/SKILL.md:59 | `03-detailed-design.md` | `task-package.03-detailed-design.md` |
| systematic-debugging/SKILL.md:45 | `references/defense-in-depth.md` | `defense-in-depth.md`（文件在技能根目录） |
| overview-design-writing-guidance.md:89 | "5 项退出检查"实有6项 | 更新计数为6 |
| state-routing-table.md overview_designing行 | "指南 5 项退出检查" | 改为6项 |

#### 3.3 定义using-git-worktrees的变量

```bash
# 当前：未定义
git worktree add "$path" -b "$BRANCH_NAME"

# 修复后：
BRANCH_NAME="task-${TASK_ID}-$(date +%Y%m%d-%H%M)"
path=".worktrees/${BRANCH_NAME}"
git worktree add "$path" -b "$BRANCH_NAME"
```

并在using-openharness路由表的implementing决策树中增加入口：`需要隔离工作空间？→ using-git-worktrees`

#### 3.4 消除skill间重复的反合理化表

brainstorming的SKILL.md和requirements-writing-guidance.md中的反合理化表50%重复。方案：SKILL.md只保留1-2个最关键的陷阱，其余引用guidance。**原则**：反合理化表只写在一个地方——写作指南。

### 变化4：skill内容质量优化

#### 4.1 所有skill增加"何时跳过"判断

每个skill在步骤列表前增加条件分叉：

```
如果 [具体可检查的条件] → 跳到步骤N
如果不满足 → 完整流程
```

| Skill | 快通道条件 |
|-------|----------|
| brainstorming | 改动范围明确、无架构决策、指令可直接转化为验收标准 |
| exploring-solution-space | 当重新调用且处于detailed_designing时→从步骤7（详细设计）开始 |
| test-driven-development | 如果是bug修复且bug已被复现→直接GREEN |
| verification-before-completion | 如果是纯文档任务→跳过命令验证步骤 |

#### 4.2 brainstorming：加强前提挑战

当前步骤2（挑战前提）比gstack的/office-hours弱。gstack有完整的"Premise Challenge"阶段。建议：
- 将步骤2拆分为独立的挑战阶段："为什么现在做？不做会怎样？这真的是问题还是症状？当前矛盾具体是什么？"
- 禁止只写模糊的"体验差"——必须有可操作的矛盾陈述

#### 4.3 exploring-solution-space：加入重入指南

SKILL.md顶部增加：
```
## 重入指南
- overview_designing → 从步骤1开始（完整流程）
- detailed_designing → 从步骤7开始（跳过问题重述、本地探索、网络搜索、总结）
```

#### 4.4 TDD：放宽"必须删除代码"规则

当前："测试立即通过→必须删除代码"过于刚性。改为：
```
测试立即通过：
  1. 先确认：测试是否因正确的已有行为而通过？（回归测试场景）
     是 → 保留
     否 → 修正测试（测试的是已有行为而非新行为）
  2. 测试有误（测错了东西）→ 修正测试后重新进入RED
```

### 变化5：建立三层渐进式技能加载 + 前馈注入

#### 5.1 三层加载（与v3一致，但强化执行）

| 层 | 内容 | Token预算 | 加载时机 |
|---|------|----------|---------|
| L1 发现 | name + trigger-condition-only description | ~50 token/skill | 会话启动时全部加载 |
| L2 激活 | SKILL.md 完整正文 | <5000 token/skill | 路由表判定触发后加载 |
| L3 资源 | references/、templates/、scripts/ | 按需 | SKILL.md中显式引用时才加载 |

**具体执行**：
- 所有13个SKILL.md的description重写为**纯触发条件**：`"当[触发症状1/2/3]时使用"`，删除所有工作流摘要
- 各skill的references/自包含所需资源
- 在AGENTS.md中增加前馈指令："读任何skill前先检查：我当前的状态是[从STATUS.yaml读取的状态]？这个skill的description是否匹配？如匹配则读L2正文；正文中显式引用了references/再读L3"

#### 5.2 前馈注入

在会话启动时（通过AGENTS.md或session-routing），注入一条浓缩的前馈指令：

```
## 前馈约束（执行前必读）
1. 任何退出检查问题答不上来 → 不能transition
2. 合理化借口（"需求很清楚""改动很小""先写代码"等）→ 自动驳回，返回skill
3. 验证必须fresh（上次运行不算，子Agent报告不算）
4. 状态唯一来源是STATUS.yaml
5. 设计决策写入文档，不留在聊天里
```

这是对反合理化表的顶层压缩——不需要Agent读到具体skill才知道"不能跳过"。

---

## 四、实施优先级

### 立刻做（零风险高收益）

1. **修复硬错误**：模板路径、exit check计数、引用路径、using-git-worktrees的未定义变量
2. **合并dispatching-parallel-agents到subagent-driven-development**：减少60-70%冗余
3. **重写13个SKILL.md的description为纯触发条件**：CSO原则
4. **在AGENTS.md中增加前馈约束**：5条核心约束的顶层注入

### 短期（2周内）

5. **闭合code review回路**：CLI硬阻止 + 路由表注册 + STATUS.yaml结构化字段
6. **闭合debugging反馈回路**：持久化计数器 + CLI transition前检查
7. **消除反合理化表跨文件重复**：brainstorming和exploring-solution-space优先
8. **所有skill增加"何时跳过"判断**：从brainstorming和exploring-solution-space开始

### 中期（1个月内）

9. **闭合3次失败→设计审查回路**：STATUS.yaml计数器 + CLI transition阻止
10. **exploring-solution-space增加重入指南**
11. **TDD放宽"必须删除代码"规则**
12. **在路由表implementing决策树中增加using-git-worktrees入口**
13. **CLI shell注入修复**：`_run_command`使用shlex.join或列表参数

### 暂不做

- 自进化/自动化skill蒸馏（Hermes经验：92%质量，仍是未解决挑战）
- 全局验证改为包隔离（架构改动大，风险与收益不成比例）
- 多模型可移植性（当前Anthropic-first是合理的设计选择）
- GEPA式提示词进化（等Hermes经验更成熟后再考虑）
- 执行轨迹记录系统（先用归档任务的反思想法简单做）

---

## 五、核心原则速查（更新版）

| 工程控制论原理 | OpenHarness应用 | 现状 | v4目标 |
|--------------|----------------|------|--------|
| 反馈闭合 | code review→修复→再审查 | **完全开环** | CLI硬阻止闭合 |
| 反馈闭合 | 验证失败→调试→再验证 | 已硬阻止但无持久化追踪 | 增加session引用 |
| 反馈闭合 | 多次失败→设计审查 | 软规则无持久化 | STATUS.yaml计数器 |
| 分层控制 | 信息按控制层级过滤 | 线性遍历200+行 | 快速索引+前馈注入 |
| 必要变异度 | description覆盖触发场景 | 写了工作流摘要 | 纯触发条件 |
| 前馈控制 | 顶层约束注入 | 分散在3个文件 | AGENTS.md浓缩注入 |
| 结构可靠性 | 硬约束vs软约束 | 以软为主 | 4个回路硬阻闭合 |

---

## 六、与v3方案的关键差异

| 维度 | v3 | v4 |
|------|----|----|
| 核心认知 | OpenHarness是skill系统 | **OpenHarness是控制论驱动的SDD规范系统** |
| code review回路 | 提议在transition中加检查 | **具体方案**：CLI硬阻止+STATUS.yaml结构化字段+路由表注册 |
| debugging回路 | 提议区分失败类型 | **持久化计数器**：STATUS.yaml记录+CLI transition前检查 |
| dispatching-parallel-agents | 未涉及 | **合并到subagent-driven-development**，消除60-70%冗余 |
| 硬错误修复 | 未涉及 | **逐一修复**：模板路径、exit check计数、引用路径、未定义变量 |
| 前馈控制 | 未涉及 | **新增原理5**：AGENTS.md顶层前馈注入 |
| 反合理化表 | 未涉及 | **消除跨文件重复**：只写在一处（写作指南） |
| "何时跳过" | 仅brainstorming | **所有skill**增加快通道判断 |
| 外部调研深度 | 6个系统，宏观设计哲学 | 7个系统，**源码级细节+设计哲学+实际缺陷** |
| SDD认知 | 未识别 | **明确识别并作为设计基础** |

---

## 附录A：调研方法

### 内部审计（13+2+3+1+1=20路并行）
- 13个skill：每个skill一个独立Explore Agent，深度读取SKILL.md+references/全部文件
- CLI源码：1个Explore Agent，读取openharness_cli/全部9个Python文件
- 写作指南：1个Explore Agent，追踪5份guidance从using-openharness到各skill的迁移
- 归档任务：1个Explore Agent，随机抽取最近5个归档中的3个（OH-038、OH-039、OH-016）
- 路由表与模板：由using-openharness Agent覆盖

### 外部系统调研（2路并行）
- 工程控制论+SDD理论：1个general-purpose Agent，WebSearch x12次
- 外部技能系统：1个general-purpose Agent，WebSearch x15次，覆盖7大系统

### 关键文献
- 钱学森.《工程控制论》. McGraw-Hill, 1954.
- 郑楠、李耀东、戴汝为.《人机融合智慧涌现：AI大模型时代的综合集成研讨体系》. 清华大学出版社, 2024.
- "Agent Cybernetics Is the Missing Science of Foundation Agents" (arXiv 2605.10754, 2026)
- "AI Harness Engineering: A Runtime Substrate" (arXiv 2605.13357v1, 2026)
- "From Craft to Constitution" (arXiv 2510.13857)
- "Managing the Stochastic" (arXiv 2512.20660)
- kpiteira/spec-driven-development (GitHub)
- obra/superpowers (GitHub, ~170K stars)
- garrytan/gstack (GitHub, ~82K stars)
