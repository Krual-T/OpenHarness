# 执行验证

implementing 阶段 agent 已在 `evidence.md` 中记录了中间执行结果（变更文件、执行的命令、退出码、输出摘要）。你的职责是判定这些结果的正确性，而非重新执行——除非需要复现验证失败。

## 步骤

{% set n = namespace(cnt=1) %}
{{ n.cnt }}. **执行验证命令（如有）**：运行 `verification-design.md` 中声明的全部验证命令；若 `## 必需命令` 明确无必需命令，只记录原因并进入后续审核流程
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **判断命令结果（如有）**：逐条对比期望退出码 vs 实际退出码和输出
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **处理失败**：见下方"验证失败处理"
{% if verification_method == "qualitative" %}
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **定性审核双轨流程**：
   - **准备审核交接包**：读取 `verification-design.md` 的 `## 审核交接包` 和审核矩阵，确认审核对象、任务背景、审核目标、非审核范围和输出格式齐全
   - **启动子 Agent 审核**：启动一个独立子 Agent（`subagent_type: general-purpose`），将完整审核交接包交给子 Agent。子 Agent 必须逐项覆盖审核矩阵，输出结构化发现；不能只给整体观感
   - **征集人类审阅者反馈**：将子 Agent 的逐项审核结论呈现给人类审阅者，请人类审阅者对每项结论给出同意 / 异议 / 补充。只有整体同意不足以闭合审核
   - **综合两方结论**：将子 Agent 审核结果和人类反馈合并写入 `evidence.md` 的 `## 语义审核` 章节；双方存在分歧时，以人类审阅者意见为准，并记录分歧点、采纳或拒绝理由
   - **处理未闭合项**：子 Agent 发现被拒绝时写明拒绝理由；人工反馈缺失或未逐项对应时，最终结论只能是有条件通过或不通过
{% endif %}
{% if rwp_enabled == "true" %}
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **RWP 双轨审核流程**：
   - **执行工作流**：按 `verification-design.md` 中声明的工作流命令执行，收集 stdout、stderr、产物路径
   - **启动子 Agent 观察**：将工作流输出（stdout/stderr/产物）、预期结果和判定标准交给独立子 Agent（`subagent_type: general-purpose`），子 Agent 逐项比对后输出结构化发现
   - **征集人类审阅者反馈**：将子 Agent 的观察结论呈现给人类审阅者，请人类审阅者逐项给出反馈（同意 / 异议 / 补充）
   - **综合两方结论**：将子 Agent 观察结果和人类反馈合并写入 `evidence.md` 的 `## 运行时观察` 章节；双方存在分歧时，以人类审阅者意见为准并在结论中注明分歧点
{% endif %}
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **补充 `evidence.md`**：
   - 补充实际执行的命令和结果；若无必需命令，写明未执行命令的原因
   - 补充验收标准覆盖表
   - 标记残余风险和延后事项
   - 写入最终 `## 验证结果`，明确通过 / 有条件通过 / 不通过
{% set n.cnt = n.cnt + 1 %}
{{ n.cnt }}. **自检 阶段结束检查**

完成后：`openharness task-package transition <task-name>|<task-id> verified`

（`verified` 是 gate 状态，CLI 检查 evidence.md 存在且非空后自动归档）

## 验证失败处理

不是所有失败都意味着"回去改代码"。按失败原因分流：

| 失败类型 | 判定 | 动作 |
|---------|------|------|
| 命令执行报错（找不到文件、权限拒绝、环境变量缺失） | 验证环境问题，非代码问题 | 修复环境后重新执行 |
| 退出码与期望不符（期望 0，实际 1） | 代码未通过验证 | 回到 `implementing` 修复代码 |
| 输出内容与预期不符，但退出码为 0 | 验证命令不够精确——期望输出写得太宽 | 回到 `verification-design.md` 收紧期望输出 |
| rwp 脚本超时或挂起 | 工作流脚本有资源泄漏或死循环 | 回到 `implementing`，同时检查工作流脚本自身的 bug |
| qualitative 审核结论模糊（"差不多""基本可以"） | 审核判定准则不够具体 | 回到 `verification-design.md` 补充判定准则 |
| qualitative 审核交接包缺字段 | 子 Agent 或人类审阅者无法按同一输入逐项审核 | 回到 `verification-design.md` 补齐审核对象、背景、目标、矩阵、非审核范围和输出格式 |
| 人类审阅者只给整体反馈 | 定性审核证据没有逐项闭合 | 继续征集逐项反馈；无法获得时记录为有条件通过或不通过 |
| rwp 子 Agent 观察结论模糊（"输出看起来正常"） | 预期结果不够具体，子 Agent 无法逐项比对 | 回到 `verification-design.md` 将预期结果写为可逐项比对的条目 |

**关键约束**：不要看到失败就自动跳回 implementing。先判断失败属于代码问题、环境问题还是验证策略问题——三者回退路径不同。

## 验证结论确认停点

`evidence.md` 写完最终结论（通过/有条件通过/不通过 + 残余风险清单）后，必须向用户展示并获确认后才可 transition。

回退修复后重新进入 verifying 时，先明确本轮验证的增量目标（"上次失败的是 X，本轮只验证 X 是否修复 + 已有通过的 Y 不退化"），再执行验证命令。

## evidence.md 完整性检查

在 transition 到 verified 之前，evidence.md 必须包含以下内容（按 `verification.method` 和 RWP 开关）：

{% if verification_method == "unit_test" %}
- [ ] 每条验证命令的实际执行结果（命令、退出码、输出摘要）
- [ ] 变更文件清单（一个文件一行，附带改动说明）
- [ ] 验收标准覆盖表（每条标准 → 对应测试函数名 → 结果）
- [ ] 残余风险（本轮未覆盖的边界 + 接受理由）

{% elif verification_method == "qualitative" %}
- [ ] `verification-design.md` 中的审核交接包已用于子 Agent 和人类审阅者
- [ ] 子 Agent 审核已执行（审核对象、审核维度、通过标准逐项覆盖）
- [ ] 子 Agent 审核结论已呈现给人类审阅者并已获得逐项反馈
- [ ] 每项发现（来源 + 问题描述 + 严重程度 + 采纳/拒绝/延后 + 处理理由 + 是否闭合）
- [ ] 最终结论（通过 / 有条件通过 / 不通过），注明子 Agent 与人类审阅者是否存在分歧
- [ ] 未闭合问题的 follow-up 计划

{% else %}
- [ ] 验证命令的实际执行结果
- [ ] 变更文件清单（一个文件一行，附带改动说明）
- [ ] 验收标准覆盖表
- [ ] 残余风险和后续事项
{% endif %}
{% if rwp_enabled == "true" %}
- [ ] 工作流名称和调用命令
- [ ] stdout 中的结构化输出（不要截断或改写）
- [ ] stderr 是否有异常日志
- [ ] 产物路径（输出文件、日志、截图等）
- [ ] 子 Agent 观察已执行（工作流输出逐项比对预期结果）
- [ ] 子 Agent 观察结论已呈现给人类审阅者并已获得逐项反馈
- [ ] 每项发现（来源 + 比对结果 + 严重程度 + 是否闭合）
- [ ] 盲区说明（工作流无法覆盖的场景 + 为什么可接受）
{% endif %}

如果 checklist 有缺项，先补充再 transition。

## 阶段结束检查

1. `verification-design.md` 中声明的验证命令（如有）是否已执行？
2. evidence.md 是否包含了实际运行的命令和结果，或无必需命令的原因？
3. 验收标准是否全部有对应的证据覆盖？
4. 是否有验证失败的条目？如果有，是否已分流到正确的回退路径？

全部能回答 → `openharness task-package transition <task-name>|<task-id> verified`

## 要点

- verifying 阶段不是"跑一遍测试就过"——必须逐条对比期望退出码和实际输出
- `evidence.md` 的 checklist 是硬门禁：缺一项就不能 transition
- 验证失败时先诊断再跳转，不要默认回到 implementing

## 常见失败模式

- 有声明验证命令时跳过命令直接写 evidence.md——evidence 必须基于实际执行结果
- verification-design.md 中声明了 N 条命令，但 verifying 只跑了 N-1 条——遗漏的命令不声不响
- rwp 工作流执行后只看了 stdout，忽略了 stderr 中的异常日志
- rwp 审核只有人类执行了工作流，缺少子 Agent 逐项比对预期结果——双轨审核缺一不可
- rwp 子 Agent 观察未对照 `verification-design.md` 中的预期结果逐项比对，仅写"输出看起来正常"
- qualitative 审核写成"代码看起来不错"——没有任何判定准则可对照
- qualitative 审核没有传递完整交接包，只让子 Agent “帮我看一下”
- qualitative 审核只有 AI 子 Agent 结论，缺少人类审阅者逐项反馈——双轨审核缺一不可
- 人类审阅者反馈未逐项对应审核矩阵，仅写"整体同意"——必须落实到每个审核维度
- 主 Agent 用自己的判断替代子 Agent 或人类审阅者结论，导致 evidence 失去独立审核证据
- 验证失败后直接改代码而不先判断失败根因，导致反复 RED-GREEN 空转
