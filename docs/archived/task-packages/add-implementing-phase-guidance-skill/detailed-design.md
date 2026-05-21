# 详细设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 可观察性与验证准备

- **验证路径**：qualitative — 子 Agent 审核新 SKILL.md 的 14 个章节完整性 + 人类审阅者逐项确认。审核维度：章节结构对齐、Karpathy 准则融入深度、人机协同停点格式、与其他阶段技能一致性
- **降级路径**：子 Agent 审核结论与人类审阅者存在分歧时，以人类审阅者意见为准并在结论中记录分歧点。如果主审核维度不够具体导致结论模糊，回到 verification-design 补充判定准则
- **预期证据**：子 Agent 审核矩阵（每个章节 → 审核维度 → 发现 + 严重程度 + 闭合状态）+ 人类审阅者逐项反馈（同意/异议/补充）+ 综合结论（通过/有条件通过/不通过）

## 新增或修改文件

| 文件 | 操作 | 作用 |
|------|------|------|
| `skills/using-openharness/states/implementing/SKILL.md` | 重写 | 唯一的改动文件。以 Karpathy 四项准则为主干，补齐全部标准章节 |

为什么这是唯一落点：implementing 阶段引导由 CLI 的 `output_state_hook` 通过 `TaskStatus.IMPLEMENTING.hook` 路径注入，重写此文件即可生效，无需修改任何 Python 代码。

## 接口

本轮改动的"接口"是 SKILL.md 的章节结构——它定义了 implementing 阶段 agent 的完整行为契约。

### 前条件

- CLI 已将任务状态推进到 `implementing`（来自 `verification_designed` 的 gate 自动推进）
- `verification-design.md` 已就绪，包含可复制粘贴执行的验证命令
- `detailed-design.md`（如果存在）已收敛实现落点和数据语义

### 后条件

- agent 完成全部验证命令并亲眼看到通过
- `evidence.md` 包含中间事实（变更文件 + 测试命令 + 执行结果）
- 用户已审阅并确认 evidence.md
- 任务状态已推进到 `implemented`

### 行为契约（14 个章节的指令精度）

每个章节输出明确的行为指令，不给 agent 留自由裁量空间：

| 章节 | 指令类型 | 精度要求 |
|------|---------|---------|
| 入口分流 | 条件分支 | 两个分支明确互斥：首次进入走完整流程，从 verifying 回退走增量修复 |
| Think Before Coding | 强制检查点 | 停止→陈述假设/暴露歧义→询问—通过后才能继续 |
| Simplicity First | 约束规则 | 5 条否定式规则 + 1 条自检问题 |
| Surgical Changes | 约束规则 | 4 条否定式规则 + 1 条检验标准 |
| Goal-Driven Execution | 执行循环 | 按 verify_by 三分支：unit_test 走 TDD（RED→GREEN→REFACTOR）、qualitative 对照审核矩阵逐项写→自检→修正、rwp 修改→运行工作流→观察输出→修正 |
| 完成后 | 写入指令 | evidence.md 中间事实的精确格式（文件名、命令、退出码、输出摘要） |
| 文档审阅停点 | 人机交互 | 告知路径→等待确认→确认后 transition |
| 阶段结束检查 | 条件门禁 | 3 条二值判定（命令全部通过？evidence 非空？文件全部列出？） |
| 工具命令参考 | 参考表 | 5 个可复制粘贴执行的命令 |
| 重入指南 | 条件分支 | 3 个入口的场景→行为映射 |
| 要点 | 约束摘要 | 通用约束 + 按 verify_by 分列的约束 |
| 相邻文档边界 | 边界声明 | 3 个相邻文档的职责边界 |
| 常见失败模式 | 故障表 | 8 条（3 条编码行为故障 + 2 条定性/rwp 特有故障 + 3 条 unit_test TDD 故障） |
| 反合理化 | 反驳表 | 6 条借口→反驳 |

## 模块内部设计

单文件改动的"模块"即 14 个章节，按职责分为四层：

### 编排层（控制流）

- **入口分流**：判断场景，决定后续走向
- **重入指南**：定义回退路径
- **阶段结束检查**：门禁判定
- **文档审阅停点**：人机协同阻塞点

### 行为准则层（编码约束）

- **Think Before Coding**：认知前置——不确定时停、问、陈述
- **Simplicity First**：代码量约束——否定式规则
- **Surgical Changes**：改动范围约束——否定式规则

### 执行层（验证循环）

- **Goal-Driven Execution**：按 verify_by 三分支——`unit_test` 走 TDD（RED→GREEN→REFACTOR）、`qualitative` 对照审核矩阵逐项写→自检→修正、`rwp` 修改→运行工作流→观察输出→修正。三个分支共享多步计划模板
- **完成后**：evidence.md 中间事实写入

### 参考层（辅助信息）

- **项目工具命令参考**：可复制粘贴的命令
- **要点**：约束摘要
- **与相邻文档边界**：职责边界声明
- **常见失败模式**：故障诊断表
- **反合理化**：借口反驳表

依赖方向：编排层 → 执行层 → 参考层（参考层不依赖其他层）。行为准则层贯穿执行层的每一步。

## 数据语义

本轮不涉及数据结构变更。关键概念语义：

| 概念 | 语义 | 来源 |
|------|------|------|
| 首次进入 | 任务从 `verification_designed` gate 首次到达 `implementing` | CLI 状态机 |
| 从 verifying 回退 | 验证失败后，verifying 阶段 agent 执行 `transition <task> implementing` 回退 | CLI 命令 |
| 中间事实 | 命令字面量、退出码、输出摘要、变更文件列表。不包含通过/失败结论 | evidence.md 模板 |
| 增量目标 | 回退时声明的有限范围："上次失败的是 X，本轮只验证 X 是否修复 + 已有通过的 Y 不退化" | verifying SKILL.md 循环验证逻辑 |

## 阶段门禁

进入 implementing（开始写 SKILL.md）前必须确定：

1. 14 个章节的完整内容已在 detailed-design 中逐项确认 ✅（4 个设计点全部用户确认）
2. 四个 Karpathy 准则章节的内容边界已定稿 ✅（设计点 1/4）
3. 入口分流和重入指南的场景覆盖已定稿 ✅（设计点 2/4）
4. evidence.md 中间事实记录格式已定稿 ✅（设计点 3/4）
5. 常见失败模式和反合理化表已定稿 ✅（设计点 4/4）
6. 工具命令清单已确认 ✅（设计点 3/4）

## 决策闭合

| 决策 | 结论 | 理由 |
|------|------|------|
| 四项 Karpathy 准则是否作为顶层章节 | 接受 | 用户确认结构方案（设计点 1/4）。准则作为主干而非子项，agent 进入后按线性顺序推进 |
| 是否保留 evidence.md 中间事实写入 | 接受 | 用户确认保留中间事实记录。implementing 记录事实（命令、退出码、文件），verifying 写最终结论 |
| 是否把 Karpathy 准则放在独立引用文件 | 拒绝 | 碎片化引导，增加遗漏概率。替代方案：全部融入 implementing SKILL.md |
| 是否修改 verifying SKILL.md 以适配新边界 | 拒绝 | 改动范围应限 implementing 单文件。verifying 已有的 evidence.md 完整性检查逻辑不需要调整 |
| Goal-Driven Execution 是否按 verify_by 分流 | 接受 | 用户指出 TDD 循环（RED→GREEN→REFACTOR）对 qualitative/rwp 任务无效。`unit_test` 保留完整 TDD；`qualitative` 循环变为"对照审核矩阵逐项写→自检→修正"；`rwp` 循环变为"修改→运行工作流→观察输出→修正" |

## 错误处理

### 静默出错风险

| 风险 | 如何暴露 | 防止措施 |
|------|---------|---------|
| agent 跳过 Think Before Coding 直接开始写代码 | 没有显式的阻塞点——skill 指令靠 agent 自觉执行 | 入口分流后第一段文字即"停止—先做以下检查"，用粗体强调"不确定时阻塞" |
| agent 在 Simplicity First 阶段顺手建了抽象 | 实现完成后无从发现——代码能通过测试但结构过度复杂 | "如果你写了 200 行但 50 行就够，重写"这条可作为 evidence.md 审阅时的检查项 |
| agent 在 Surgical Changes 阶段重构了无关代码 | diff 中包含任务范围外的改动 | 用户审阅 evidence.md 变更文件清单时逐文件核对 |
| evidence.md 中间事实事后补写而非逐轮追加 | evidence 条目时间顺序不对或不完整 | "每轮循环写完立即追加"在完成后和要点两个章节各强调一次 |
| qualitative/rwp 任务照搬 TDD 循环（RED→GREEN→REFACTOR） | 无测试可跑，agent 在 RED 阶段空转或编造测试 | Goal-Driven Execution 入口处按 verify_by 显式分流，qualitative/rwp 分支无 RED 步骤 |
| qualitative 任务"先让测试失败"规则被机械执行 | 定性任务没有测试，agent 困惑或跳过关键验证 | 要点中"先让测试失败"标注仅 unit_test 适用 |

### 失败传播

implementing 阶段的失败不自动消化——每个失败模式对应明确的回退目标状态（verification-designing / detailed-designing / requirements.md），避免在 implementing 阶段空转。

## 迁移说明

### 实施顺序

1. 在仓库根目录打开 `skills/using-openharness/states/implementing/SKILL.md`
2. 端到端重写：YAML frontmatter → 14 个章节按设计内容写入
3. 自检：对照 `requirements.md` 的 8 项交付结果逐项验收
4. 提交前：运行 `uv run ruff check .` 确认无格式问题

### 切换点

- 旧 SKILL.md 被覆盖后立即生效——CLI 在下次 `transition` 到 `implementing` 时注入新内容
- 无中间兼容状态：单文件替换，不涉及 API 版本或数据迁移

### 回滚触发点

- 回滚方式：`git checkout HEAD -- skills/using-openharness/states/implementing/SKILL.md`
- 触发条件：新 skill 在 implementing 阶段导致 agent 行为退化（如跳过 TDD 循环、不写 evidence.md）

## 推荐图示

本轮改动是单文件的线性章节结构，无需图示。14 个章节的层级关系已在"模块内部设计"的四层职责分解中充分表达。

## 详细设计反思

| 检查项 | 结论 |
|--------|------|
| 验证策略（qualitative 双轨审核）是否与设计内容匹配？ | 是——14 个章节形成 14 个审核对象，每个可对照"是否存在、内容是否可操作、是否与其他阶段技能对齐"三个维度审核 |
| 接口边界是否可能与其他阶段技能产生矛盾指令？ | 与相邻文档边界章节明确声明了三方职责：implementing 写中间事实、verification-designing 写验证计划、verifying 写最终结论。不存在重叠 |
| 14 个章节的迁移是否可能遗漏原有逻辑？ | TDD 循环保留在 Goal-Driven Execution，evidence.md 写法约束保留在"完成后"章节。原有的 TDD 故障处理表合并到常见失败模式中 |
| 文件长度是否合理？ | 预计 150-200 行，与 brainstorming（129 行）、detailed-design（114 行）同类技能体量一致 |
