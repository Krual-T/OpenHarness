# OpenHarness 工程控制论优化分析 v2

> 基于钱学森《工程控制论》的系统工程视角，结合对 13 个 skill、CLI 运行时、写作指导体系的深度审计，以及对 superpowers/gstack/Hermes/Claude Code/OpenCode/Codex 六大外部系统的设计哲学调研。

---

## 一、工程控制论核心原理框架

钱学森《工程控制论》提出了几个对 AI Agent 系统设计至关重要的原理：

| 原理 | 控制论定义 | 在 Agent 系统中的映射 |
|------|-----------|---------------------|
| **分层控制** | 复杂系统必须按抽象层级分解，每层只处理本层信息 | Skill 不应跨抽象层混合职责 |
| **负反馈稳定** | 系统偏差通过反向信号自动修正 | 验证失败 → 自动触发调试，而非等待人工 |
| **信息流完整性** | 控制信号必须从传感器到执行器无中断传递 | Skill 间的前置/后置条件必须显式声明 |
| **必要变异度** | 控制器的变异度必须 ≥ 被控对象的变异度 | Skill 路由系统必须能覆盖所有任务类型 |
| **可靠性冗余** | 关键回路需要备用路径 | 单一 skill 失败不可阻塞整条流水线 |
| **自适应** | 系统应根据环境变化自动调整参数 | Skill 内容应根据执行效果自我改进 |

本报告以此六原理为诊断框架。

---

## 二、当前系统控制论模型

### 2.1 三层控制架构

```
┌──────────────────────────────────────────────────────────────┐
│  战略层 (Strategic) — 决定做什么                                │
│  AGENTS.md → using-openharness → brainstorming                │
│  → exploring-solution-space (overview + detailed)              │
│  控制变量: task_type, design_review_mode, scope boundary       │
├──────────────────────────────────────────────────────────────┤
│  战术层 (Tactical) — 决定怎么做                                 │
│  subagent-driven-development / TDD / systematic-debugging     │
│  dispatching-parallel-agents / using-git-worktrees             │
│  控制变量: 实现策略选择, 子代理分配, 测试覆盖                   │
├──────────────────────────────────────────────────────────────┤
│  操作层 (Operational) — 验证和闭环                              │
│  verification-before-completion / reviewing-task-package       │
│  requesting-code-review / receiving-code-review                │
│  finishing-a-development-branch                               │
│  控制变量: 验证证据, 代码审查结果, 分支处理决策                  │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 信息流与状态机

```
用户请求 → AGENTS.md → using-openharness (路由中枢)
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
        proposing    overview/      implementing
        (brain-      detailed       (TDD/subagent/
        storming)    (exploring)     debugging)
            │              │              │
            ▼              ▼              ▼
        STATUS.yaml  ←── gate ──→  STATUS.yaml
            │                          │
            └──────────┬───────────────┘
                       ▼
                 verifying
            (verification-before-
              completion)
                       │
                       ▼
                  archived
            (finishing-a-branch)
```

### 2.3 反馈回路现状

| 回路 | 类型 | 触发条件 | 当前机制 | 工程控制论评估 |
|------|------|---------|---------|--------------|
| 验证失败 → 重新实现 | 负反馈 | verifying 不通过 | 手动 transition 回退 | ❌ 无自动触发 |
| 设计卡住 → 重新讨论 | 负反馈 | 设计不可行 | 手动 transition 到 proposing | ❌ 依赖代理判断 |
| 详设发现总设问题 | 负反馈 | 详细设计暴露方向错误 | 手动 transition | ❌ 信息不回流到总设 |
| TDD GREEN 失败 → 调试 | 负反馈 | 测试写完后代码无法通过 | 单句引用 systematic-debugging | ❌ 返回路径未定义 |
| 代码审查发现 → 修复 | 正反馈 | 审查报告有 Critical 问题 | requesting → receiving 线性链 | ⚠️ 无强制重审查 |

---

## 三、系统性缺陷诊断（按控制论六原理深度审计）

### 3.1 违反"分层控制"——控制中枢过度集中

**`using-openharness` 上帝对象问题（9 项职责，SKILL.md 47 行 + 14 个引用文件）：**

```
using-openharness 当前承载:
├── 入口判断 (是否需要任务上下文) → references/session-routing.md
├── bootstrap 结果处理 (3 种分支)
├── 新建任务包流程
├── 任务分类 (task_type + design_review_mode) → references/task-classification.md
├── 状态路由表 (标准 10 状态 + 机械 5 状态) → references/state-routing-table.md
├── 实现阶段 skill 选择 (4 分支决策树)
├── 回退与异常处理 (4 种回退场景)
├── 写作指导体系 (5 份指南 + Exit Check + 反合理化表)
├── 运行时能力合约 (3 层架构 + 4 路路由) → runtime-capability-contract.md
├── 项目运行时表面地图 → project-runtime-surface-map.md
├── RWP 工作流包系统 → runtime-workflow-packages.md
├── CLI 速查 (9 个命令) → cli-reference.md
├── 9 个模板文件 → templates/
├── SUBAGENT-STOP 子代理豁免逻辑
└── 关键约束 (5 条规则)
```

**深层问题**：SKILL.md 本身是薄的路由入口（47行），实际逻辑分散在 14 个引用文件中。`next_skills: [brainstorming]` 声明严重过度简化——实际可路由到 7 个不同 skill。`state-routing-table.md` 成为事实上的第二级调度器，但与 session-routing.md 之间的职责边界模糊。

**审计发现**：
- `session-routing.md` 和 `state-routing-table.md` 各自独立定义了状态转换逻辑，存在部分重复
- 实现阶段 4 分支决策树仅存在于路由表中，SKILL.md 无直接引用
- RWP 路由（runtime-capability-contract.md）是完全独立的子系统，但在 SKILL.md 中无直接链接
- `next_skills` 元数据字段与实际路由图严重不一致

### 3.2 违反"信息流完整性"——信息流断裂（扩展至 14 处）

经逐个 skill 审计，确认以下信息流断裂：

| 编号 | 断裂位置 | 具体表现 | 影响等级 |
|------|---------|---------|---------|
| F1 | exploring-solution-space ↔ RWP | Step 4.5 插入 RWP 检查，但与 runtime-capability-contract.md 对"谁执行 RWP 检查"存在矛盾（主代理 vs 子代理） | 高 |
| F2 | brainstorming ↔ task_type | Exit Check 含 task_type 确认（第7项），但状态路由表引用计数为 6 项（实为 7 项），overview 引用为 5 项（实为 6 项） | 中 |
| F3 | verification ↔ systematic-debugging | 验证失败后说"调用 debugging"，但无自动触发机制，debugging 的 `next_skills` 指向 TDD 而非 verification，回环路径缺失 | 高 |
| F4 | TDD ↔ systematic-debugging | 单向引用（debugging → TDD），TDD 的 GREEN 失败处理仅一句，调试后如何回到 TDD 循环未定义 | 高 |
| F5 | AGENTS.md ↔ AGENTS.example.md | 文件编号不一致（05/06 vs 04/05） | 低 |
| F6 | skill ↔ 模板文件 | brainstorming 引用 `templates/01-requirements.md` 但实际为 `templates/task-package.01-requirements.md` | 中 |
| F7 | finishing-a-branch ↔ code-review | 选项 1/2 前说"确认代码审查已完成"但无检查机制——无引用 receiving-code-review，无读取审查工件的指令 | 高 |
| F8 | defense-in-depth ↔ debugging 主流程 | 防御层引用 `references/defense-in-depth.md` 但文件位于 skill 根目录，且防御层在阶段 4 末尾作为"附加步骤"，未集成到阶段 1-3 的数据流追溯中 | 中 |
| F9 | writing-guidance Exit Check 计数 | state-routing-table.md 中 requirements 引用为 6 项（实为 7 项），overview 引用为 5 项（实为 6 项） | 低 |
| F10 | using-git-worktrees 清理 | 完全依赖 finishing-a-development-branch 清理 worktree，但两者无 `requires`/`next_skills` 声明，元数据均为空 | 中 |
| F11 | reviewing-task-package 触发冲突 | 与 verification-before-completion 共享 `triggers_on: [verifying]`，但前者的 exit 条件未写入状态路由表 | 中 |
| F12 | receiving-code-review 下游断裂 | `next_skills: []`，审查反馈处理后的下一步未定义 | 中 |
| F13 | requesting-code-review 单 commit 假设 | 硬编码 `HEAD~1..HEAD` 作为 diff 范围，无法处理多 commit 分支和未提交变更 | 中 |
| F14 | subagent-driven-development 审查员提示 | code-quality-reviewer-prompt.md 依赖外部 `../requesting-code-review/references/code-reviewer.md` 的传递引用 | 中 |

### 3.3 违反"负反馈稳定"——反馈回路缺失（扩展至 5 个）

```
缺失回路 1：验证失败 → 自动调试 → 重新验证
  当前：verifying 失败 → 手动判断 → transition implementing
  应有：verifying 失败 → 自动触发 systematic-debugging → 修复 → 自动 transition verifying
  阻碍：debugging 的 next_skills 指向 TDD（而非 verification），回环断裂

缺失回路 2：实现受阻 → 设计审查
  当前：implementing 阶段多次失败 → 需人工判断
  应有：3次以上修复失败 → 自动 transition detailed_designing → 重新审查设计
  参考：systematic-debugging 已定义"3次失败→质疑架构"，但该信号不回流到设计层

缺失回路 3：技能执行质量 → 技能内容改进
  当前：技能执行后无任何度量
  应有：每次执行记录工具调用次数、错误数、人工干预次数 → 定期审查 → 改进技能
  参考：Hermes 自改进循环从 12 次工具调用 + 2 次错误 → 6 次 + 0 次错误

缺失回路 4：代码审查发现 → 防御层增强
  当前：review 发现的问题修复后不更新防御层
  应有：每次 Critical 审查发现 → 自动检查 defense-in-depth 是否需要补充

缺失回路 5：子代理执行质量 → 父代理调度策略
  当前：子代理 DONE/CONCERNS/BLOCKED 状态仅用于当次判定
  应有：累积子代理执行质量数据 → 调整模型选择（快速模型 vs 强模型）
```

### 3.4 违反"必要变异度"——路由覆盖不完整

当前 `implementing` 阶段有 4 分支决策树，但以下场景未被覆盖：
- 纯文档变更任务（无需 TDD 也无需子代理）
- 配置变更（需特殊验证路径）
- 依赖升级任务（需特殊测试策略）
- 跨多个任务包的协调工作

### 3.5 违反"可靠性冗余"——单点故障

- **路由中枢单点**：using-openharness 是所有会话的唯一切入点
- **写作指导单点**：5 份写作指导是 Exit Check 的唯一来源
- **CLI 单点**：状态转换完全依赖 `openharness transition` CLI
- **模板单点**：模板路径硬编码在 skill 中

### 3.6 违反"自适应"——静态技能系统

与六大外部系统的自适应能力对比：

| 能力 | Superpowers | Hermes | Claude Code | gstack | OpenCode | Codex | **OpenHarness** |
|------|------------|--------|-------------|--------|----------|-------|----------------|
| 技能自创建 | 间接(/skillify) | ✅ 从执行轨迹生成 | ❌ | ✅ /skillify 命令 | ✅ lore 蒸馏 | ❌ | ❌ |
| 技能自修补 | ✅ 压力场景→补反合理化 | ✅ fuzzy_find_and_replace | ❌ | ❌ | ❌ | ❌ | ❌ |
| 后台审查 | ❌ | ✅ Nudge 引擎 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 渐进式加载 | ✅ 3 层 | ✅ index → skill_view | ✅ 3 层 | ✅ 3 层 | ❌ | ✅ 3 层 | ⚠️ RWP 有 / Skill 无 |
| 执行轨迹记录 | ❌ | ✅ | ❌ | ❌ | ✅ lore | ✅ compaction | ❌ |
| 反合理化 | ✅ 核心机制 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ writing guidance 有 |

---

## 四、六大外部系统设计哲学对比

### 4.1 Superpowers (obra/superpowers) — "硬性约束优先"

**核心哲学**：AI 代理类比为"热情但缺乏判断力的初级工程师"。行为约束优于建议，机械不可能性优于口头警告。

**关键机制**：
- **三层约束架构**：Rule（软建议，会被合理化跳过）→ Gate（硬门禁，下一步被机械阻止）→ Hook（确定性软件触发器）
- **1% 法则**：即使只有 1% 可能性适用也必须调用 skill。将代理的主观判断权降为零
- **反合理化表**：每个约束配对一份"代理可能用的借口 vs 为什么借口不成立"表格。通过先让代理无 skill 执行任务、记录其 verbatim 合理化语句、然后写 skill 逐条反驳来生成
- **CSO (Claude Search Optimization)**：description 必须是触发器而非摘要。写"Use when [症状]"而非"这个 skill 做 X, Y, Z"→ 防止代理把 description 当完整指令跳过 body
- **TDD 用于 Prompt Engineering**：RED（压力场景 + 无 skill → 记录合理化）→ GREEN（写 skill 逐条反驳）→ REFACTOR（测试，补新漏洞）

**对 OpenHarness 的启示**：反合理化表已在 writing guidance 中使用，但未扩展到 skill 级别。Exit Check 仍是软门禁。CSO 原则完全未应用。

### 4.2 Hermes (NousResearch) — "自进化为核心"

**核心哲学**：Agent 从"静态工具"变为"动态进化的数字伙伴"。真正的护城河是 Agent 通过工作积累的领域知识。

**关键机制**：
- **三子系统闭环**：Memory（2200 字符硬限制）→ Skill（从执行轨迹蒸馏）→ Nudge（后台异步触发）
- **技能自创建**：任务涉及 5+ 工具调用、遇到并克服错误 → 自动蒸馏为 SKILL.md
- **技能自修补**：fuzzy_find_and_replace + 安全扫描 + 原子回滚
- **容量限制作为反思工具**：Memory 写满时 `add` 失败并返回全部条目 → 强迫代理主动决定删除什么
- **实际效果**：Session 1（12 工具调用 + 2 错误）→ Session 3（6 次 + 0 错误）

**对 OpenHarness 的启示**：OpenHarness 已有 task-package 完成后的自然闭环点。可在 archived 后增加自动蒸馏步骤。

### 4.3 Claude Code (Anthropic) — "Harness Engineering"

**核心哲学**：**Agent = Model + Harness**。65% 的 Agent 失败源于 harness 缺陷。

**关键机制**：
- **TAOR 循环**（约 50 行代码）：Think → Act → Observe → Repeat。故意"蠢"——所有推理委托给模型
- **三层渐进披露**：元数据层（始终加载，~30-50 token/skill）→ 指令层（触发时加载）→ 资源层（按需加载）
- **29 个生命周期钩子**：Hook 占用**零上下文 token**（作为副作用执行）
- **上下文压缩 + 断路器**：连续 3 次失败 → 断路器断开
- **子代理作为上下文防火墙**：隔离上下文中消耗 token，仅返回结论

**对 OpenHarness 的启示**：渐进式加载是最紧迫的架构改进。Hook 系统可用于实现硬性门禁。

### 4.4 gstack (garrytan) — "角色化技能组织"

**核心哲学**：**Thin Harness, Fat Skills**。约 90% 的价值在 SKILL.md 文件中。

**关键机制**：
- **角色隔离而非多代理**：23+ 角色，每个角色只看到其需要的上下文
- **7 阶段冲刺循环**：THINK → PLAN → BUILD → REVIEW → TEST → SHIP → REFLECT
- **/skillify 元技能**：观察刚完成的工作流 → 提取可重复模式 → 自动生成 SKILL.md
- **Boil the Lake 原则**：AI 使完整性的边际成本趋近于零 → 默认选择完整方案

**对 OpenHarness 的启示**：角色隔离模式可应用于子代理。/skillify 概念可映射到 task-package → skill 蒸馏。

### 4.5 OpenCode (SST/anomalyco) — "架构级权限分离"

**核心哲学**：Provider-agnostic（75+ 提供商）、终端优先。Plan 与 Build 之间的分离是架构强制。

**关键机制**：
- **硬性权限级策略/执行分离**：Plan Agent（edit: deny 全局阻止）物理上无法写入文件
- **扁平团队架构**：1 个 lead + N 个 teammate，通过名称通信
- **蒸馏而非摘要**：保留文件路径、错误信息、确切决策——准确率从 50% → 85%

**对 OpenHarness 的启示**：架构级权限分离是 OpenHarness 最缺乏的。

### 4.6 Codex (OpenAI) — "Shell-First + Compaction"

**核心哲学**：模型优先，harness 应随模型变强而变薄。Shell 是最通用的 Agent 接口。

**关键机制**：
- **Shell-First Training**：模型训练时偏好 shell 工具
- **Compaction as First-Class Primitive**：25 小时 session 经历 13 次 compaction，消费 12.7M tokens
- **Append-Only 状态管理**：保持 prefix 不变性，最大化 prompt cache 命中率
- **防御纵深安全**：3 层（Sandbox + OS 隔离 + 审批策略）

**对 OpenHarness 的启示**：Compaction 是 OpenHarness 完全缺失的能力。

---

## 五、优化建议：先整体后局部

### 5.1 整体架构层

#### 建议 1：实现 Skill 三层渐进式加载

```
Layer 1 — 元数据层 (始终加载，~50 token/skill):
  name + description → 作为路由键

Layer 2 — 指令层 (触发时加载，<500 行):
  完整 SKILL.md 主体

Layer 3 — 资源层 (按需加载):
  references/ agents/ templates/ scripts/
```

**效果预估**：13 个 skill 的发现成本从全量加载降为 ~650 tokens（13 × 50），节省 90%+ 上下文。

#### 建议 2：建立技能依赖图

在 SKILL.md frontmatter 增加 `on-success`/`on-failure`/`provides`/`subagent_behavior` 字段，使依赖关系机器可读。

#### 建议 3：实现硬性门禁系统

三层门禁架构（借鉴 Superpowers）：
- Layer 1 — Hook：确定性软件触发器（零上下文）
- Layer 2 — Gate：架构级阻止（`HARD GATE:` 声明）
- Layer 3 — Rule：约定（可能被合理化跳过）

#### 建议 4：增加自适应反馈回路

执行轨迹记录 → Task-Package → Skill 蒸馏 → 后台定期审查。

---

### 5.2 信息流修复（14 处断裂的修复方案）

| 编号 | 修复方案 | 优先级 |
|------|---------|--------|
| F1 | 明确 exploring-solution-space Step 4.5 的 RWP 检查由主代理执行 | P1 |
| F2 | 修正 state-routing-table 中 Exit Check 计数 + 增加 task_type 确认项 | P1 |
| F3 | verification 失败分支增加 HARD GATE 自动调用 debugging；修改 debugging 的 next_skills | P0 |
| F4 | TDD GREEN 失败处理扩展为完整闭环（调用 debugging → 修改 → 重新测试） | P0 |
| F5 | 统一 AGENTS.md 和 AGENTS.example.md 的文件引用编号 | P2 |
| F6 | 更新 brainstorming 和 exploring 中的模板路径 | P1 |
| F7 | finishing 选项 1/2 前增加 HARD GATE 代码审查检查 | P0 |
| F8 | 修复 defense-in-depth 引用路径 + 集成到阶段 1-3 的数据流追溯 | P1 |
| F9 | 修正 state-routing-table 中的 Exit Check 计数 | P2 |
| F10 | using-git-worktrees 增加 next_skills，finishing 增加 requires | P2 |
| F11 | reviewing-task-package 的 exit 条件写入状态路由表 | P2 |
| F12 | receiving-code-review 增加 next_skills + 写入审查裁决到 evidence | P2 |
| F13 | requesting-code-review 支持多 commit 范围 | P2 |
| F14 | 消除传递依赖或增加存在性检查 | P2 |

---

### 5.3 局部优化：逐个 Skill

#### P0 优先级

- **verification-before-completion**：增加验证失败自动触发 debugging；明确文档语义审查子代理 dispatch 指令
- **finishing-a-development-branch**：选项 1/2 前增加 HARD GATE 代码审查检查；增加状态写回
- **test-driven-development**：GREEN 失败闭环扩展；REFACTOR 阶段增加具体 Exit Check 清单

#### P1 优先级

- **brainstorming**：视觉头脑风暴改为按需启动；spec-document-reviewer 衔接明确化
- **exploring-solution-space**：Step 4.5 提升为 Step 5；模板路径修正；mechanical 任务跳过
- **systematic-debugging**：防御层集成到主流程；压力测试文件增加 DISCUSSION.md
- **subagent-driven-development**：增加冲突解决策略和超时/重试策略

#### P2 优先级

- **dispatching-parallel-agents**：增加子代理失败处理和合并策略
- **requesting-code-review**：支持多 commit 范围；结构化输出格式
- **receiving-code-review**：增加审查裁决记录模板和冲突反馈处理
- **reviewing-task-package**：输出格式标准化；触发优先级明确化
- **using-git-worktrees**：增加清理逻辑和隔离状态指导
- **CLI**：修复 10 个 skip 测试；补充 writing-guide 和 RWP 错误路径测试

---

## 六、实施路线图

### 第一阶段：基础设施 + 关键信息流修复（当前）

```
范围:
  1. SKILL.md frontmatter 增加依赖图字段 (on-success/on-failure/provides/subagent_behavior)
  2. CLI 增加 openharness check-skills 命令
  3. F3, F4, F7 修复（验证失败→自动调试；TDD↔debugging 双向；合并前强制审查）
预计影响: 关键反馈回路闭环，技能依赖图可自动验证
```

### 第二阶段：门禁强化 + 剩余信息流修复

```
范围:
  1. F1, F2, F6, F8, F10-F14 修复
  2. 反合理化表扩展到所有 skill
  3. HARD GATE 声明规范建立
预计影响: 信息流断裂从 14 处降至 <3 处
```

### 第三阶段：渐进式加载 + 自适应

```
范围:
  1. Skill 三层渐进式加载
  2. 执行轨迹记录到 .harness/artifacts/skill-traces/
  3. Task-Package → Skill 蒸馏实验
预计影响: Skill 上下文占用降低 90%+
```

---

## 七、关键度量指标

| 指标 | 当前 | 阶段1 目标 | 最终目标 |
|------|------|-----------|---------|
| 信息流断裂数 | 14 | <8 | 0 |
| 技能交叉引用完整度 | ~25% 双向 | ~60% | 100% |
| 有反合理化表的 skill | 仅 writing guidance | 全部 P0 skill | 全部 skill |
| Skill 上下文加载量 | 全量 | 全量 | 元数据层 |
| 验证失败→自动调试 | 无 | 手动但明确指引 | 半自动 |
| 有 HARD GATE 覆盖的阶段 | 0 | 3 | 全部活跃状态 |

---

## 八、外部参考设计哲学总结

| 系统 | 核心哲学 | 关键机制 | 借鉴优先级 |
|------|---------|---------|-----------|
| **Superpowers** | 硬性约束 > 软性建议 | 1% 法则、反合理化表、CSO | **P0** |
| **Hermes** | 自进化为核心 | 技能自创建/自修补、Nudge 引擎 | **P2** |
| **Claude Code** | Agent = Model + Harness | 3 层渐进披露、29 Hook、断路器 | **P0** |
| **gstack** | Thin Harness, Fat Skills | 角色隔离、/skillify、7 阶段循环 | **P1** |
| **OpenCode** | 架构级权限分离 | Plan/Build agent 权限隔离 | **P2** |
| **Codex** | Shell-First + Compaction | Compaction API、Append-Only 状态 | **P2** |
