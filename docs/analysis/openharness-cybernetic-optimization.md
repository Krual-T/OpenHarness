# OpenHarness 工程控制论优化分析

> 基于钱学森《工程控制论》的系统工程视角，结合对 13 个 skill、CLI 运行时、以及 superpowers/gstack/Hermes/Claude Code/OpenCode 等外部参考的深度调研。

---

## 一、当前系统控制论模型

### 1.1 三层控制架构

```
┌─────────────────────────────────────────────────────────┐
│  战略层 (Strategic) — 决定做什么                           │
│  AGENTS.md → using-openharness → brainstorming            │
│  → exploring-solution-space (overview + detailed)         │
├─────────────────────────────────────────────────────────┤
│  战术层 (Tactical) — 决定怎么做                            │
│  subagent-driven-development / TDD / systematic-debugging │
│  dispatching-parallel-agents / using-git-worktrees        │
├─────────────────────────────────────────────────────────┤
│  操作层 (Operational) — 验证和闭环                         │
│  verification-before-completion / reviewing-task-package  │
│  requesting-code-review / receiving-code-review           │
│  finishing-a-development-branch                          │
└─────────────────────────────────────────────────────────┘
```

### 1.2 信息流模型

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

### 1.3 反馈回路

当前系统识别到两类反馈：

| 回路 | 类型 | 触发 | 机制 |
|------|------|------|------|
| 验证失败 → 重新实现 | 负反馈 | `verifying` 验证不通过 | 手动 `transition` 回退 |
| 设计卡住 → 重新讨论 | 负反馈 | 设计不可行 | 手动 `transition` 回退到 `proposing` |
| 详设发现总设问题 | 负反馈 | 详设阶段发现方向错误 | 手动 `transition` 回退 |

**缺失的关键反馈回路**：验证失败 → 自动触发调试（无）；代码审查发现 → 自动更新证据文件（无）；运行时验证失败 → 通知设计层（无）。

---

## 二、系统性缺陷诊断（按控制论维度）

### 2.1 控制中枢过度集中

**问题**：`using-openharness/SKILL.md` 承担了路由、分类、状态管理、CLI 参考、回退处理、写作指南引用等 6 项职责，形成"上帝对象"。

```
using-openharness 当前承载 (~170 行):
├── 入口判断 (是否需要任务上下文)
├── bootstrap 结果处理 (3 种分支)
├── 新建任务包流程
├── 任务分类 (task_type + design_review_mode)
├── 状态路由表 (标准 10 状态 + 机械 5 状态)
├── 实现阶段 skill 选择 (3 种场景 + 组合使用)
├── 回退与异常处理 (4 种回退场景)
├── CLI 速查 (8 个命令)
└── 关键约束 (5 条规则)
```

**控制论原理违反**：在工程控制论中，单个控制单元应只负责一层抽象的决策。多层决策集中在单一单元会导致：信息过载、决策延迟、修改风险放大。

### 2.2 信息流断裂（共 8 处已确认断裂）

| 编号 | 断裂位置 | 表现 | 影响 |
|------|---------|------|------|
| F1 | exploring-solution-space ↔ RWP | 设计阶段不引用运行时工作流 | 运行时验证在设计阶段未被考虑 |
| F2 | brainstorming ↔ task_type 确认 | writing guidance exit check 不含 task_type 确认 | 可能跳过关键分类步骤 |
| F3 | verification-before-completion ↔ systematic-debugging | 验证失败后无自动调试触发 | 需人工判断下一步 |
| F4 | TDD ↔ systematic-debugging | 单向引用（debugging→TDD，TDD 无反引） | GREEN 阶段失败无指引 |
| F5 | AGENTS.md ↔ AGENTS.example.md | 文件编号不一致（05/06 vs 04/05） | 代理读取不同文件会产生冲突认知 |
| F6 | skill SKILL.md ↔ 模板文件 | brainstorming/exploring 不引用模板路径 | 代理不知模板存在 |
| F7 | finishing-a-branch ↔ code-review | 合并前不强制执行代码审查 | 可能跳过审查直接合并 |
| F8 | defense-in-depth ↔ debugging 主流程 | 防御层是独立文档，不被主流程引用 | 修复后缺少防御增强步骤 |

### 2.3 反馈回路缺失

工程控制论强调负反馈是系统稳定性的核心。当前系统缺失以下关键回路：

```
缺失回路 1：验证失败 → 自动调试
  当前：verifying 失败 → 手动 transition → implementing
  应有：verifying 失败 → 自动触发 systematic-debugging → 修复 → 重新验证

缺失回路 2：实现受阻 → 设计审查
  当前：implementing 卡住 → 需要人工判断
  应有：3次以上修复失败 → 自动触发设计审查 → 判断是设计问题还是实现问题

缺失回路 3：技能执行质量 → 技能改进
  当前：技能执行后无质量度量
  应有：每次技能执行后记录效果 → 定期审查 → 改进技能内容
```

### 2.4 自适应能力缺失

Hermes 系统展示了三个关键的自适应机制，而 OpenHarness 全部缺失：

1. **技能自创建**：从执行轨迹中自动提取可复用模式
2. **技能自修补**：发现技能缺陷时自动修补
3. **后台 Nudge 引擎**：异步审查和优化记忆/技能

### 2.5 渐进式信息披露不完整

Claude Code 使用 3 层渐进式加载（元数据 → 技能体 → 支持文件），预期节省 60-84% 令牌。OpenHarness 的 RWP 系统已实现了此模式（list → show → run），但 **skill 系统本身没有**：

```
RWP (已有): list (摘要) → show (详情) → run (执行)
Skill (缺失): 元数据 → 技能体 → 参考文件  ← 全量加载
```

### 2.6 门禁 (Gate) 机制弱化

Superpowers 明确区分了三层约束机制：

| 机制 | Superpowers | OpenHarness |
|------|-------------|-------------|
| Rule (规则) | "过马路前看路" | AGENTS.md 约定 |
| Gate (门禁) | "硬性门禁：先看左边，再看右边，再迈步" | writing guidance Exit Check |
| Hook (钩子) | 确定性软件触发器 | CLI `openharness check-tasks` |

OpenHarness 的 Exit Check 是"软门禁"——依赖代理自觉执行。缺少 Superpowers 的"1% 法则"（即使只有 1% 可能性适用也必须调用）和反合理化表。

---

## 三、优化建议：先整体后局部

### 3.1 整体架构优化（系统工程层面）

#### 建议 1：将 using-openharness 拆分为三层路由

**原理**：控制论中的分层控制——每层只处理本层抽象

```
当前:
  using-openharness (单文件, 170 行, 6 项职责)

优化后:
  using-openharness/SKILL.md (~40 行)
    ├── 入口判断 → 引用 session-routing.md
    ├── 任务分类 → 引用 task-classification.md
    ├── 状态路由 → 引用 state-routing-table.md
    └── CLI 速查 → 引用 cli-reference.md
```

**效果**：降低单文件认知负担，各模块可独立演进。

#### 建议 2：建立技能依赖图 (Skill Dependency Graph)

**原理**：控制论中的信息流显式化——每个技能声明其前置/后置条件

```yaml
# 在 SKILL.md frontmatter 中增加
---
name: verification-before-completion
requires: [task-package-ready]
on-failure: systematic-debugging
on-success: finishing-a-development-branch
provides: [verification-evidence]
---
```

**效果**：代理可自动发现调用链，减少路由表的人工维护。

#### 建议 3：实现技能执行的三层渐进式加载

**原理**：与 RWP 的 list→show→run 模式对齐

```
Layer 1 (始终加载): 技能名 + 单行描述 + 触发条件
Layer 2 (按需加载): 完整 SKILL.md 工作流
Layer 3 (延迟加载): references/ agents/ templates/
```

**效果**：减少上下文占用 60-84%（参考 cc-polymath 数据）。

#### 建议 4：增加自适应反馈回路

```
技能执行 ──→ 记录执行结果 ──→ 定期审查 ──→ 改进技能内容
                  │
                  └── 执行失败 ──→ 区分：技能缺陷 vs 执行失误
                                     │
                        技能缺陷 → 自动修补 SKILL.md
                        执行失误 → 改进代理执行策略
```

**参考**：Hermes 的自改进循环在同一任务上从 12 次工具调用 + 2 次错误降到 6 次 + 0 次错误。

### 3.2 技能层优化（局部逐个优化，按优先级）

#### 优先级 P0 — using-openharness（入口重构）

**现状问题**：
- 上帝对象，6 项职责混在一起
- 状态路由表是线性文本，难以扩展
- 技能选择缺少决策树
- 子代理的 SUBAGENT-STOP 与 RWP 子代理路由冲突

**优化方案**：
1. 拆分 using-openharness 为多个职责明确的文件
2. 将状态路由表改为机器可读的 YAML（类似 RWP 的 workflow.md 元数据头）
3. 为 `implementing` 阶段添加技能选择决策树
4. 将 `<SUBAGENT-STOP>` 改为更精细的规则（按任务类型豁免，而非一刀切）
5. 增加反合理化表（参考 Superpowers 模式）

#### 优先级 P1 — 信息流修复

1. **F1 修复**：在 exploring-solution-space 中增加 RWP 选择步骤
2. **F2 修复**：在 requirements-writing-guidance Exit Check 中增加 task_type 确认项
3. **F3 修复**：在 verification-before-completion 失败分支中明确调用 systematic-debugging
4. **F4 修复**：TDD SKILL.md 增加"GREEN 失败时 → 调用 systematic-debugging"的引用
5. **F5 修复**：统一 AGENTS.md 和 AGENTS.example.md 的文件编号为 04/05
6. **F6 修复**：brainstorming 和 exploring-solution-space 中明确引用模板路径
7. **F7 修复**：finishing-a-development-branch 选项 1/2 前增加代码审查检查
8. **F8 修复**：systematic-debugging 阶段 4 增加"添加防御层"步骤

#### 优先级 P2 — 门禁强化

1. 为所有 Exit Check 增加反合理化表（参考 Superpowers 的 "It's just a quick fix" 模式）
2. 将 writing guidance 的 Exit Check 从"检查清单"升级为"硬性门禁"
3. 增加 `openharness gate-check <task> <stage>` CLI 命令自动化门禁检查

#### 优先级 P3 — 自适应机制

1. 技能执行轨迹记录（`.harness/artifacts/skill-traces/`）
2. 定期技能效果审查（后台代理）
3. 技能自修补实验性支持

---

## 四、实施路线图

### 第一阶段：using-openharness 入口优化（当前）

```
目标：降低入口复杂度，修复关键信息流断裂
范围：
  1. using-openharness 拆分（建议 1）
  2. F1, F5, F6 信息流修复
  3. 增加 implementing 阶段技能选择决策树
  4. 为 SKILL.md frontmatter 增加 depends/provides 字段（建议 2 基础设施）
预计影响：降低 ~60% 入口文件认知负担
```

### 第二阶段：反馈回路与门禁强化

```
范围：
  1. F2, F3, F4, F7, F8 信息流修复
  2. 反合理化表（所有 Exit Check）
  3. 硬性门禁 CLI 命令
预计影响：减少"跳过验证"类错误 ~70%
```

### 第三阶段：渐进式加载与自适应

```
范围：
  1. Skill 三层加载
  2. 技能执行轨迹记录
  3. 后台审查代理实验
预计影响：减少上下文占用 60-84%
```

---

## 五、关键度量指标

| 指标 | 当前状态 | 第一阶段目标 | 最终目标 |
|------|---------|-------------|---------|
| using-openharness 行数 | 170 | &lt;50 (主文件) | &lt;40 |
| 信息流断裂数 | 8 | &lt;4 | 0 |
| 技能交叉引用完整度 | ~30% 双向 | ~60% | 100% |
| 有反合理化表的门禁 | 0 | 3 | 全部 |
| Skill 上下文加载量 | 全量 | 全量 | 2 层渐进式 |
| 验证失败→自动调试 | 无 | 无 | 有 |

---

## 六、外部参考设计哲学总结

| 系统 | 核心设计哲学 | OpenHarness 可借鉴 |
|------|------------|-------------------|
| **Superpowers** | 硬性门禁 > 软性规则；1% 法则；反合理化表 | 门禁强化、反合理化表 |
| **Hermes** | 自进化：从工具到伙伴；后台 nudge 引擎 | 自适应回路、后台审查 |
| **Claude Code** | Harness Engineering；3 层渐进披露；17 个生命周期钩子 | 渐进式加载、钩子系统扩展 |
| **gstack** | 角色即技能；思考→计划→构建→评审→测试→发布→反思 | 角色化技能组织 |
| **OpenCode** | 提供商无关；战略与执行分离；文件是存储原语 | 多代理架构设计 |
| **AEGIS** | 治理优先；宪法式规则；强制性红队 | 治理层独立 |
