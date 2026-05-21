# 证据

## 变更文件

- `skills/using-openharness/states/implementing/SKILL.md` — 端到端重写：以 Karpathy 四项准则为主干章节（Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution），按 verify_by 三分支，补齐入口分流、证据审阅停点、工具命令参考、重入指南、相邻文档边界、常见失败模式、反合理化等标准章节。verifying 阶段反馈后修正三处：rwp 增加 unit_test 前置步骤并收窄边界到退出码+stderr、完成后 rwp 描述同步、阶段结束检查 rwp 增加单元测试项。verifying 阶段人类审阅者反馈后移除 YAML frontmatter 以与其他阶段技能格式一致。
- `skills/using-openharness/states/verification-designing/SKILL.md` — 要点新增一条：三阶段闭环呼应（设计验证 → 执行验证 → 判定验证）；RWP 选择与设计约束新增：预期结果必须可逐项比对（verifying 阶段子 Agent 观察需要）；常见失败模式新增：rwp 预期结果模糊导致双轨审核空转
- `skills/using-openharness/states/verifying/SKILL.md` — 开头新增职责声明：implementing 已记录中间结果，verifying 职责是判定正确性；步骤新增 rwp 双轨审核流程（执行工作流 → 子 Agent 观察 → 人类反馈 → 综合结论）；evidence.md checklist rwp 增加子 Agent 观察条目；验证失败处理表增加 rwp 子 Agent 观察模糊条目；常见失败模式增加 rwp 双轨审核缺失条目

## 语义审核

### implementing 阶段完整性确认

对照 `verification-design.md` 中的 16 条审核矩阵，确认所有审核对象已写完、内容非空。

审核对象覆盖：
- #1-5: 入口分流 + 四项 Karpathy 准则可操作性和分支正确性 — 已写完
- #6-8: evidence.md 中间事实、审阅停点、阶段结束检查 — 已写完
- #9-10: 工具命令、重入指南 — 已写完
- #11-12: 要点 verify_by 标注、相邻文档边界 — 已写完
- #13-14: 常见失败模式 9 条、反合理化 6 条 — 已写完
- #15-16: 结构一致性、语言规则 — 已写完

中间发现：所有章节按 detailed-design 的设计内容写入，14 个章节齐全，内容非空。正确性判定留给 verifying 阶段。

### verifying 阶段双轨审核

#### 子 Agent 审核结论（16 条审核矩阵）

| # | 审核对象 | 结论 | 发现 | 严重程度 |
|---|---------|------|------|---------|
| 1 | 入口分流 | 通过 | 首次进入 vs 从 verifying 回退两个场景分支明确 | — |
| 2 | Think Before Coding | 通过 | 包含"陈述假设""暴露歧义""不确定时主动问"等具体行为指令 | — |
| 3 | Simplicity First | 通过 | 6 条否定式约束规则，每条具象可判定 | — |
| 4 | Surgical Changes | 通过 | "不顺手改进""匹配现有风格""清理自己遗留"规则到位 | — |
| 5 | Goal-Driven Execution | 通过 | 按 verify_by 三分支正确，含 rwp unit_test 前置 | — |
| 6 | 完成后 | 通过 | 中间事实字段完整，明确不含最终结论 | — |
| 7 | 文档审阅停点 | 通过 | "告知路径→审阅→确认后 transition"流程完整 | — |
| 8 | 阶段结束检查 | 通过 | 二值判定，按 verify_by 区分检查项 | — |
| 9 | 工具命令参考 | 通过 | 5 条可复制粘贴命令 | — |
| 10 | 重入指南 | 通过 | 三个入口场景全部覆盖 | — |
| 11 | 要点 | 通过 | verify_by 约束标注适用条件正确 | — |
| 12 | 相邻文档边界 | 通过 | implementing / verification-designing / verifying 三方边界清晰 | — |
| 13 | 常见失败模式 | 通过 | 9 条覆盖编码行为 + 验证循环故障两类 | — |
| 14 | 反合理化 | 通过 | 6 条借口→反驳，覆盖所有常见借口 | — |
| 15 | 整体结构 | 不通过 | YAML frontmatter 与其他五个阶段技能格式不一致 | 建议 |
| 16 | 整体内容 | 通过 | 中文正文 + 英文命令/状态值/文件名 | — |

**子 Agent 汇总：通过 15 / 不通过 1**

#### 人类审阅者逐项反馈

| # | 反馈 | 处置 |
|---|------|------|
| 1-14 | 同意 | — |
| 15 | 移除 YAML frontmatter | 已移除，与其他阶段技能对齐 |
| 16 | 同意 | — |

### 验证过程中新增的设计变更

verifying 阶段人类审阅者提出三个架构问题，经讨论后实施：

1. **rwp 增加 unit_test 前置步骤** — implementing SKILL.md Goal-Driven Execution rwp 分支增加"先运行单元测试（如有）"步骤
2. **rwp implementing 边界收窄** — 从"输出是否符合预期"收窄到"退出码 0、stderr 无报错"，输出语义正确性留给 verifying
3. **rwp verifying 启用子 Agent 双轨审核** — verifying SKILL.md 新增 rwp 双轨审核流程（Shell 执行 → 子 Agent 逐项比对 → 人类反馈 → 综合结论），verification-designing SKILL.md 新增预期结果必须可逐项比对的约束

## 验证结果

**通过**

所有 16 条审核矩阵已闭合，无严重未闭合项。#15（YAML frontmatter 格式不一致）经人类审阅者确认后移除，已闭合。

变更范围从单文件（implementing/SKILL.md）扩展到三文件，增加的 verification-designing 和 verifying 改动是实现 rwp 双轨审核闭环的必要前提，属于已验证设计范围内的合理扩展。

## 残余风险

| 风险 | 接受理由 | 重新审查触发条件 |
|------|---------|----------------|
| 审核矩阵未覆盖"Skill 指令在实际 implementing 阶段的效果" | 本轮验证对象是 SKILL.md 文档本身的质量，运行时效果需在实际任务中观察 | 后续有 implementing 阶段 agent 行为退化的反馈时 |
| rwp 双轨审核流程尚未在实际 rwp 任务中验证 | 当前仓库无活跃 rwp 任务，流程设计已通过 qualitative 审核 | 首个 rwp 任务执行 verifying 阶段后，收集反馈并修正 |

## 后续事项

无。所有审核条目已闭合，交付结果均已达到 requirements.md 中定义的完成标准。
