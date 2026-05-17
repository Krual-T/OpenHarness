# OpenHarness 工程控制论优化 v5

> v5的核心发现：Guidance是三层架构中的冗余中间层，删除后内容分别流向Skill（流程控制）和Template（产出标准），形成工程控制论意义上的干净两层控制回路。

---

## 零、v4 vs v5：差异总览

| 维度 | v4 | v5 |
|------|----|----|
| 核心认知 | OpenHarness是控制论驱动的SDD系统 | 同，但进一步识别**三层架构中Guidance是冗余中间层** |
| Guidance定位 | 未质疑其存在 | **应删除，内容流向Template和Skill** |
| 调研深度 | 18路并行 | 12路并行（每个skill一个子Agent + 外部调研 + 归档复盘 + CLI/Guidance/Template深度审计） |
| SDD完整性检查 | 未涉及 | **逐状态、逐文档检查，发现4个缺失** |
| 具体性 | 方向性方案 | **行号级定位每个硬错误、每条重复内容** |

---

## 一、SDD系统完整性检查：缺失状态与文档

按照Spec-Driven Development的规范完整性要求，逐状态检查当前系统：

### 1.1 当前状态机（10状态标准流）

```
proposing → requirements_designed → overview_designing → overview_designed →
detailed_designing → detailed_designed → implementing → implemented → verifying → archived
```

对应5份规范文档：
```
01-requirements.md   (proposing → requirements_designed)
02-overview-design.md   (overview_designing → overview_designed)
03-detailed-design.md   (detailed_designing → detailed_designed)
04-verification.md      (verifying)
05-evidence.md          (verifying → archived)
```

### 1.2 发现的4个缺失

#### 缺失1：Code Review回路在状态机中不存在

`requesting-code-review` 和 `receiving-code-review` 两个skill完全不在路由表中。`implemented` 状态被定义为"gate状态，不需调用skill，只执行transition"。但 `_warn_code_review_gap`（lifecycle.py:250）检查 `evidence.code_review` 是否存在——这个字段**模板中没有定义**，两个code review skill也**不写入它**。

**症状**：
- 路由表 `implemented` 行无code review入口
- STATUS.yaml模板无 `evidence.code_review` 字段
- `_warn_code_review_gap` 永远空转（字段不存在 → 永远警告 → 永远不阻塞）
- receiving-code-review 的 `next_skills` 为空

**结论**：Code review是一个完全缺失的控制论回路——传感器（`_warn_code_review_gap`）连接到不存在的执行器（skill不写入产物）。

#### 缺失2：4个Gate状态无独立退出检查

`requirements_designed`、`overview_designed`、`detailed_designed`、`implemented` 这4个gate状态的定义是"前一阶段已完成，等待推进"。但：

- `proposing → requirements_designed`：`transition` 验证 `01-requirements.md` 全部section有实际内容
- `overview_designed → detailed_designing`：**仅检查文件存在**，不检查内容质量
- `detailed_designed → implementing`：**仅检查文件存在**
- `implemented → verifying`：仅检查 `STATUS.yaml` 字段，**不检查code review**

`transition` 的 `validate_task_package` 对gate状态只检查"文件是否存在+section是否有内容"，不检查Exit Check问题。Exit Check完全依赖Agent自律。

**结论**：Gate状态是"软门禁"——依赖Agent读了guidance并自律回答Exit Check问题。如果Agent跳过guidance（三层加载链导致的可能性），gate状态形同虚设。

#### 缺失3：STATUS.yaml模板缺少 `evidence.code_review` 字段

CLI `lifecycle.py:250-265` 检查 `evidence.code_review`，但模板 `task-package.STATUS.yaml` 中只有：
```yaml
evidence:
  docs: [...]
  code: []
  tests: []
```

没有 `code_review` 子字段。这是**schema与代码不一致**。

#### 缺失4：`verifying` 状态产出两份文档但状态机只要求一份

`04-verification.md` 在 `STATUS_REQUIRED_FILES["verifying"]` 中，但 `05-evidence.md` 只在 `archived` 才required。实际使用中，两个文档在verifying阶段同时产出（OH-043、OH-045都如此），但状态机定义的文档累积边界与实际工作流不匹配。

---

## 二、Guidance删除论证：三层→两层

### 2.1 当前三层架构的实际内容分布

经过12路子Agent对全部5份guidance、8份template、13个skill的逐文件审计：

| 内容类型 | 当前所在层 | 应属层 | 占比 |
|---------|-----------|--------|------|
| Exit Check（5-7个阻塞问题） | Guidance | Skill | 每份guidance ~15% |
| Anti-Rationalization（4条借口） | Guidance + Skill（重复） | Skill | 每份guidance ~10% |
| Common Failure Modes（5-9条） | Guidance | Skill | 每份guidance ~10% |
| Boundary With Adjacent Documents | Guidance | Skill | 每份guidance ~8% |
| Section Mapping（怎么写每章） | Guidance | Template | 每份guidance ~30% |
| Minimum Acceptable Shape | Guidance | Template | 每份guidance ~10% |
| Questions This Document Must Answer | Guidance | Template | 每份guidance ~10% |
| How To Use The Template | Guidance | Template | 每份guidance ~5% |
| Purpose声明 | Guidance | 冗余（Skill已隐含） | 每份guidance ~2% |

**核心结论**：Guidance中约55%的内容本质是流程控制（应归Skill），约55%的内容本质是产出标准（应归Template），两者有10%重叠。Guidance作为一个独立层没有提供任何独特价值——它只是把Skill和Template各自缺失的内容暂存在了一个中间文件里。

### 2.2 工程控制论五原理的论证

**原理1：反馈闭合**

Guidance的Exit Check是"传感器"，但它在Guidance文件中——Agent必须主动加载Guidance才能看到。Skill流程中没有强制读取Guidance的节点。这导致：Agent执行Skill → 跳过Guidance → Exit Check从未执行 → 反馈回路未闭合。

删除Guidance后：Exit Check嵌入Skill流程步骤中，Agent执行流程必经。

**原理2：分层控制**

当前三层之间通信模糊：
- Skill引用Guidance（"对照guidance的Exit Check"）但不列出具体问题
- Guidance引用Template（"按模板各章节填写"）但章节规则分散在Section Mapping
- Template完全不自包含，必须配合Guidance才能产出合格文档

删除Guidance后：两层间接口清晰——Skill定义"何时阻塞"，Template定义"何谓合格"。

**原理3：必要变异度**

13个skill的description当前写了工作流摘要（如"当任务状态是verifying时使用——负责验证..."），这是CSO反模式。Superpowers实践证明：description写摘要→Agent把摘要当完整指令，跳过body。

**原理4：结构可靠性**

Guidance的反合理化表和Exit Check都是软约束（文字）。删除Guidance不是去掉这些约束，而是把它们嵌入正确的层：
- Exit Check → Skill中，配合CLI `transition` 硬门禁
- Anti-Rationalization → Skill中，配合AGENTS.md前馈注入

**原理5：前馈控制**

反合理化表分散在5个Guidance + 多个Skill中，Agent无法预加载。删除Guidance后：反合理化统一在Skill和AGENTS.md中，会话启动时预加载。

### 2.3 具体流向表

以`requirements-writing-guidance.md`（95行）为例：

| 原始位置（guidance行号） | 内容 | 流向 | 目标位置 |
|------------------------|------|------|---------|
| L7-9 Purpose | "定义这轮任务为什么存在" | 删除 | SKILL.md已隐含 |
| L11-22 Questions (10问) | 驱动问题清单 | → Template | 01-template.md文件头部 |
| L24-40 Section Mapping | 每章怎么写 | → Template | 01-template.md各章节下方注释 |
| L42-46 Boundary | 与02/03的边界 | → Skill | SKILL.md步骤间说明 |
| L48-54 Common Failure Modes (5条) | 典型失败 | → Skill | SKILL.md"警示信号" |
| L56-62 Minimum Acceptable Shape | 每章最低标准 | → Template | 01-template.md每章"最低要求" |
| L64-76 Exit Check (7问) | 阻塞检查 | → Skill | SKILL.md步骤6 |
| L78-87 Anti-Rationalization (4条) | 借口反驳 | → Skill | SKILL.md反合理化表（去重合并） |
| L89-94 How To Use (4条) | 使用建议 | → Template | 01-template.md开头 |

5份guidance同理。总计节省约4500行guidance内容，其中~55%流入Skill（约2500行等效约束），~45%流入Template（约2000行等效标准），实际Skill和Template各行数增加远小于此（因为有大量结构性重复可去重）。

---

## 三、P0：立即可修复的硬错误

### 3.1 路径错误

| 文件:行号 | 错误值 | 正确值 |
|----------|--------|--------|
| `exploring-solution-space/SKILL.md:59` | `using-openharness/references/templates/02-overview-design.md` | `using-openharness/references/templates/task-package.02-overview-design.md` |
| `exploring-solution-space/SKILL.md:59` | `03-detailed-design.md` | `task-package.03-detailed-design.md` |
| `systematic-debugging/SKILL.md:45` | `references/defense-in-depth.md` | `defense-in-depth.md` |

### 3.2 计数错误

| 文件:行号 | 错误 | 修复 |
|----------|------|------|
| `overview-design-writing-guidance.md:88` | "5 个问题"实有6个 | 改为6 |
| `detailed-design-writing-guidance.md:101` | "6 个问题"实有7个 | 改为7 |
| `state-routing-table.md:39` (overview_designing) | "指南 5 项退出检查" | 改为6项 |
| `state-routing-table.md:41` (detailed_designing) | "指南 7 项退出检查" | 改为7项（数字对但guidance标错了） |

### 3.3 Schema不一致

| 位置 | 问题 | 修复 |
|------|------|------|
| `task-package.STATUS.yaml` | 缺少 `evidence.code_review` 字段 | 增加 `code_review:` 子字段 |
| `lifecycle.py:250-265` | 检查 `evidence.code_review` 但模板无此字段 | 模板补字段后生效 |
| `STATUS_REQUIRED_FILES["verifying"]` | 不包含 `05-evidence.md` | 实际使用中verifying已写05，建议补入 |

---

## 四、P1：删除Guidance的实施计划

### 4.1 改动范围

涉及5个skill的SKILL.md修改 + 5个template文件修改 + 5个guidance文件删除：

| Skill | 删除的Guidance | SKILL.md增加 | Template增加 |
|-------|---------------|-------------|-------------|
| brainstorming | `requirements-writing-guidance.md` | Exit Check 7问 + 反合理化4条 + Common Failure Modes 5条 + Boundary | Questions 10问 + Section Mapping + Minimum Acceptable Shape + How To Use |
| exploring-solution-space | `overview-design-writing-guidance.md` | Exit Check 6问（修正后）+ 反合理化 + Common Failure Modes + Boundary | 同上结构 |
| exploring-solution-space | `detailed-design-writing-guidance.md` | Exit Check 7问（修正后）+ 反合理化 + Common Failure Modes + Boundary | 同上结构 |
| verification-before-completion | `verification-writing-guidance.md` | Exit Check 6问 + 反合理化 + Common Failure Modes + Boundary | 同上结构 |
| verification-before-completion | `evidence-writing-guidance.md` | Exit Check 5问 + 反合理化 + Common Failure Modes + Boundary | 同上结构 |

### 4.2 反合理化去重策略

当前5份guidance共有20条反合理化借口，skill中共有~14条。去重后预计保留~25条唯一借口，全部集中在各Skill中。

brainstorming的SKILL.md和requirements-guidance中4条有3条直接重复（措辞不同，意思相同），合并后取更完整版本。

### 4.3 `writing-guide` CLI命令处理

删除guidance文件后，`openharness writing-guide list` 和 `writing-guide read` 将找不到文件。两个选项：
- **方案A**：直接删除 `writing-guide` 命令（内容已并入skill+template，不再需要独立命令）
- **方案B**：将命令重定向到template文件（`writing-guide read requirements` → 读取 `task-package.01-requirements.md` template）

建议方案A——删除模板文件不是"指南"，template已自包含写作指导，不需要独立的CLI入口。

---

## 五、P2：闭合4个控制论回路

### 5.1 Code Review回路（当前完全开环）

```
当前：requesting-code-review ──✗── receiving-code-review ──✗── transition
      (无连接)                (无连接)              (无阻塞)
```

修复：
1. STATUS.yaml模板增加 `evidence.code_review` 字段：
   ```yaml
   evidence:
     code_review:
       completed: false
       reviewer: ""
       result: ""
       artifact_path: ""
   ```
2. 路由表 `implemented` 行增加：先调用 `requesting-code-review`，审查通过后才允许transition
3. receiving-code-review 增加 `next_skills: [verification-before-completion]`
4. `_warn_code_review_gap` 升级为硬阻止（非mechanical任务）
5. requesting-code-review 的 `allow_implicit_invocation` 改为 `true`

### 5.2 Debugging回路（当前软规则无持久化）

修复：
1. STATUS.yaml增加 `debugging.failed_attempts` 计数器
2. CLI `transition implementing` 检查计数器≥3 → 阻止，要求回退到 `detailed_designing`
3. systematic-debugging阶段4步骤4增加：每次失败后写入STATUS.yaml

### 5.3 验证失败→重新实现回路（当前路由不完整）

修复：verification-before-completion的验证失败路由增加：
- "需要重新实现" → 路由到implementing
- "验证环境故障" → 路由到环境修复
- "需求不合理" → 路由回proposing

### 5.4 Skill反馈回路（最低可行）

修复：05-evidence.md模板增加可选section `## Skill Feedback`，供人类维护者阅读。

---

## 六、P3：合并冗余skill

### 6.1 dispatching-parallel-agents → subagent-driven-development

**重复度**：~80%（经逐段对比确认）
**独特内容**：仅2-3行（负面清单"不要用于探索性调试、紧耦合重构"、prompt结构提醒"不要给模糊指令"）
**操作**：迁移独特内容 → 删除整个 `skills/dispatching-parallel-agents/` 目录

### 6.2 using-openharness加载链压缩

**当前**：SKILL.md(37行，5步链接) → session-routing.md → state-routing-table.md(200+行) → cli-reference.md
**"新建任务包"流程**在SKILL.md、session-routing.md、state-routing-table.md三处各写了一遍。

**优化**：
- 合并 session-routing + task-classification 为一个入口决策文件
- SKILL.md只保留精简路由表（3-5个最常见状态），完整表保留在state-routing-table.md
- cli-reference.md中已在路由表出现的命令移除

---

## 七、实施优先级总表

| 优先级 | 改动 | 类型 | 影响范围 |
|--------|------|------|---------|
| **P0** | 修复5个硬错误（路径×3 + 计数×4 + schema×3） | 修bug | 零风险 |
| **P0** | 合并dispatching-parallel-agents | 删冗余 | 零风险 |
| **P0** | 13个SKILL.md的description改为纯触发条件 | CSO原则 | 零风险 |
| **P1** | 删除5个Guidance，内容流入Skill+Template | 架构简化 | 需验证 |
| **P1** | 删除或重定向 `writing-guide` CLI命令 | 架构简化 | 需验证 |
| **P1** | 消除反合理化表跨文件重复 | 去重 | 零风险 |
| **P2** | 闭合code review回路 | 新功能 | 需测试 |
| **P2** | 闭合debugging回路（持久化计数器） | 新功能 | 需测试 |
| **P2** | AGENTS.md前馈约束注入 | 新功能 | 零风险 |
| **P2** | using-openharness加载链压缩 | 架构优化 | 需验证 |
| **P3** | 所有skill增加"何时跳过"快通道 | 效率优化 | 低风险 |
| **P3** | TDD放宽"必须删除代码"规则 | 行为修正 | 低风险 |

---

## 附录A：12路调研方法

| 路数 | 调研对象 | Agent类型 | 深度 |
|------|---------|----------|------|
| 1 | 外部调研：工程控制论 + Superpowers/gstack/SpecKit/Claude Code/Hermes/Codex | general-purpose | WebSearch x15次 |
| 2 | 5份Guidance全量审计 | Explore | 逐段分析，行号级 |
| 3 | 8份Template全量审计 | Explore | 逐文件分析 |
| 4 | CLI全量审计（9个Python文件） | Explore | 函数级 |
| 5 | 归档任务复盘（OH-002/OH-043/OH-045） | Explore | 全文件阅读 |
| 6 | brainstorming skill + requirements guidance | Explore | 逐行对照 |
| 7 | exploring-solution-space skill + 2 guidance | Explore | 逐行对照 |
| 8 | verification-before-completion skill + 2 guidance | Explore | 逐行对照 |
| 9 | using-openharness skill（枢纽skill） | Explore | 全文件阅读 |
| 10 | subagent + dispatching 重叠分析 | Explore | 逐段对比 |
| 11 | code review skills (requesting + receiving) | Explore | 回路线分析 |
| 12 | 其余5个skill（TDD/debug/finish/worktree/reviewing） | Explore | 结构审计 |

## 附录B：工程控制论五原理速查

| 原理 | 控制论定义 | OpenHarness应用 | v5动作 |
|------|-----------|----------------|--------|
| 反馈闭合 | 传感器→比较器→执行器→被控对象→传感器 | Code review回路完全开环 | CLI硬阻止闭合 |
| 分层控制 | 层间通信仅通过明确定义的接口 | Guidance混合了流程控制和产出标准 | 删除Guidance，两层各司其职 |
| 必要变异度 | 控制器变异度 ≥ 被控对象变异度 | Description写摘要而非触发条件 | 全部改为纯触发条件 |
| 结构可靠性 | 系统的可靠性是结构的涌现属性 | 以软约束为主，依赖Agent自律 | Exit Check从文字变为硬门禁 |
| 前馈控制 | 干扰进入系统前进行补偿 | 反合理化分散在5+文件中 | AGENTS.md浓缩前馈注入 |
