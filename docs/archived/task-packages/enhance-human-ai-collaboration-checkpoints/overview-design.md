# 总体设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 系统边界

**覆盖范围**：四个阶段 skill 文件（`skills/using-openharness/states/` 下）：

| 文件 | 阶段 | 改动性质 |
|------|------|---------|
| `exploring-solution-space/SKILL.md` | overview_designing | 逐项设计确认改强制、准则 #1/#4 落地、术语统一 |
| `detailed-design/SKILL.md` | detailed_designing | 同上 |
| `verification-designing/SKILL.md` | verification_designing | 新增验证策略确认停点、准则 #1/#4 落地、术语统一 |
| `verifying/SKILL.md` | verifying | 扩展人审范围到全部 verify_by 模式、循环验证、术语统一 |

**不纳入范围**：

- `brainstorming/SKILL.md` — 已在 commit `722f9d2` 完成增强
- `implementing/SKILL.md` — 由 TASK-021 独立处理
- CLI 层代码（`workflows.py`、`transition_engine.py`、`task_status.py`）— 不新增 gate 状态或 gate_preconditions
- mechanical 工作流 — 跳过 overview/detailed 阶段，不需要这些停点
- `references/templates/` 下的模板文件 — 模板标题不受本轮约束
- 准则 #2（简洁优先）和 #3（精准修改）— TASK-020 只落地 #1 和 #4

## 推荐结构

### 改动层次

```
skills/using-openharness/states/
├── exploring-solution-space/SKILL.md  ← 三点改动
├── detailed-design/SKILL.md           ← 三点改动
├── verification-designing/SKILL.md    ← 三点改动
└── verifying/SKILL.md                ← 两点改动
```

### 每个文件的改动模式

统一的改动模式：

1. **停点增强**：在关键决策步骤后插入命名停点（格式复用 brainstorming 的"X 确认停点"）
2. **准则落地**：
   - 准则 #1 → 存在多个合理选择时列出选项+代价，不得默选
   - 准则 #4 → 阶段结束检查从 AI 自答改为要求引用具体产物（文档章节号、文件路径、接口签名）
3. **术语统一**：`Exit Check` → `阶段结束检查`

### 模块职责

| 模块 | 职责 |
|------|------|
| exploring-solution-space SKILL.md | 指导 AI 在方案探索阶段的行为：架构决策前有确认停点、多方案显式展示、证据引用 |
| detailed-design SKILL.md | 指导 AI 在详细设计阶段的行为：接口精度决策前有确认停点、多选一显式展示、产物引用 |
| verification-designing SKILL.md | 指导 AI 设计验证策略时的行为：验证命令清单+风险接受需人类确认 |
| verifying SKILL.md | 指导 AI 执行验证时的行为：最终结论+残余风险需人类确认（扩展到全部 verify_by），循环验证 |

### 关键约束

- `design_review_mode: auto` 时，逐项设计确认的停点保持为可选（不阻塞 AI 自主推进）
- `design_review_mode: stepwise` 时，逐项设计确认的停点为强制
- 所有改动保持现有章节结构（步骤 → 退出检查 → 要点 → 边界 → 失败模式 → 反合理化）不变

## 关键流程

### 主路径（以 verification-designing 为例）

```
AI 读需求 → 确定验证方式 → 写 verification-design.md
    → [停点] 向用户展示验证命令清单 + 覆盖矩阵 + 不覆盖风险
    → 用户确认 → 继续
    → 用户否定 → 修正验证策略
    → [可选] 提前跑一次验证命令确认能正确失败（验证 RED）
    → 阶段结束检查（引用具体产物）
    → transition
```

### 关键失败信号

| 信号 | 出现位置 | 含义 |
|------|---------|------|
| 用户拒绝停点确认 | 各阶段停点 | 设计方案或验证策略需调整 |
| Exit Check 答不上来 | 各阶段退出前 | 产出物不完整，阻塞推进 |
| design_review_mode: auto 时 AI 自行跳过停点 | 设计阶段 | 符合预期——auto 模式下允许 |

## 阶段门禁

进入 `detailed_designing` 前必须确定：

1. exploring-solution-space 的停点模式和准则 #1/#4 落地方式已确认
2. 四个文件的术语统一方案已确认
3. `design_review_mode` 对停点强制性的控制逻辑已明确

## 取舍

### 推荐方案：纯 skill 指令层面改动

**收益**：
- 不引入 CLI 复杂度，不新增 gate 状态
- 可以立即生效（skill 文件是 AI 行为的直接指令源）
- 向后兼容——`auto` 模式保持现有行为

**代价**：
- 停点依赖 AI 遵循 skill 指令，CLI 层无强制力
- 不如 CLI gate 那样有硬性的前置条件检查

**回退空间**：如果纯 skill 层面的停点效果不够，后续可以在 gate_next 状态前增加 gate_preconditions 作为硬门禁

### 备选方案：CLI 层新增 gate 状态

**未被采用的原因**：
- 需要修改 `task_status.py`（新增枚举值）、`workflows.py`（新增 `gate_next` 和 `gate_preconditions`）、`transition_engine.py`
- 引入向后兼容风险——现有任务包的状态迁移路径被改变
- 过度工程——停点是人类和 AI 之间的交互，不是状态机逻辑，CLI 管不到聊天行为

## 推荐图示

本轮改动结构简单（四个文件的统一模式），不需要 PlantUML 图。文字描述已足够表达改动边界和流程。

## 总体设计反思

**挑战 1：停点是否应该做成 CLI 硬门禁？**

- 结论：拒绝
- 理由：停点是人机交互行为，CLI 无法感知聊天层面的"用户确认"。CLI gate 适合检查文件存在性和字段完整性（如现有的 `_check_requirements_gate`），不适合检查"用户是否确认了某个设计方向"。如果未来需要强化，可以在 `gate_preconditions` 中增加对文档内容的检查（如是否存在"确认"标记），但本轮不做。

**挑战 2：是否应该把准则 #2 和 #3 也一起落地？**

- 结论：延期（到 TASK-021 或后续任务）
- 理由：准则 #2（简洁优先）和 #3（精准修改）更偏向 implementing 阶段的行为指导，与 TASK-020 的设计/验证阶段关注点不同。将 #2/#3 放入 TASK-021 的实现引导技能中更合理。

**挑战 3：verification-designing 的"提前跑验证命令"是否应该是强制步骤？**

- 结论：接受为可选步骤
- 理由：强制运行验证命令需要环境（Python、pytest、依赖等），不同任务包的环境差异大，不能假设 AI 能在设计阶段就执行验证命令。标为可选建议更务实。如果后续 CLI 支持沙箱验证环境，可以升级为强制。
