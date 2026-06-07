# 验证策略

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 本文件在实现前编写。定义验证策略——计划怎么验证、用什么命令、期望什么结果。实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。

## 验证路径

- **主路径**：`verify_by: qualitative`。实施完成后，主 Agent 按本文件的审核交接包启动子智能体审核，再将子智能体结论交给人类审阅者逐项反馈。两方结论和分歧处理写入 `evidence.md`。
- **辅助路径**：如实施中新增了稳定模板章节或固定协议锚点，可运行最小化协议结构测试。该测试只证明稳定文本契约存在，不证明自然语言语义正确。
- **回退路径**：如果人工审阅者无法逐项反馈，不能宣称完整通过；如果子智能体审核输出模糊，应回退本文件收紧审核矩阵；如果发现 `verify_by` 与验证对象冲突，应回退需求阶段修正 `task-info.yaml`。
- **路径说明**：本轮验证对象是协议文档的语义边界和审核交接方法，主证据应来自定性审核。`pytest` 只能作为结构辅助证据，不能替代语义审核。

## 必需命令

本轮没有用于证明自然语言语义正确的必需命令。

实施后必须执行定性审核流程：

1. 主 Agent 按“审核交接包”启动子智能体审核。
2. 主 Agent 将子智能体结论呈现给人类审阅者。
3. 人类审阅者逐项反馈同意、异议或补充。
4. 主 Agent 将两方结论、采纳或拒绝理由、残余风险写入 `evidence.md`。

可选辅助命令：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

期望退出码：`0`。

使用条件：仅当实施阶段新增或调整了稳定模板章节、固定协议锚点或既有协议结构断言时执行。若没有新增稳定结构断言，可不执行该命令，并在 `evidence.md` 写明原因。

该命令不得作为自然语言语义正确性的证据。

## 预期结果

定性审核预期结果：

- 子智能体按审核矩阵逐项输出结论，不只给整体评价。
- 人类审阅者对每项子智能体结论给出同意、异议或补充。
- 主 Agent 对每项发现记录处理状态：采纳、拒绝或延后。
- 拒绝子智能体发现时必须记录理由。
- 最终结论明确为通过、有条件通过或不通过。
- 如存在未闭合问题，写入残余风险或后续事项。

辅助结构测试预期结果：

- 如执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`，退出码为 `0`。
- 测试断言只覆盖稳定文本契约或模板结构，不包含自然语言完整句子断言。

## 审核交接包

### 审核对象

- `skills/using-openharness/states/verification-designing/instructions.md`
- `skills/using-openharness/states/verifying/instructions.md`
- `skills/using-openharness/references/templates/task-package.verification-design.md`
- `skills/using-openharness/references/templates/task-package.evidence.md`
- `docs/anti-patterns/skill-writing.md`
- 如实施阶段修改：`tests/openharness_cases/test_protocol_docs.py`

### 任务背景

OpenHarness 需要让 AI 协作者在文档类任务中区分稳定文本契约和自然语言语义。稳定文本契约可以用字符级断言防回归，自然语言语义应通过 `qualitative` 双轨审核。当前问题是 AI 容易对文档修改默认跑 `pytest`，或用脆弱字符串断言证明语义正确。

### 审核目标

- 判断阶段职责是否清楚：需求阶段确定 `verify_by`，验证设计阶段消费并校验，不重新选择。
- 判断字符级断言边界是否清楚：哪些场景可以断言，哪些场景不应断言。
- 判断自然语言审核交接包是否足以让子智能体和人工审阅者独立审核。
- 判断 evidence 写回要求是否能追溯子智能体发现、人工反馈、分歧和残余风险。
- 判断反模式说明是否能阻止“文档默认 pytest”和“脆弱字符断言替代语义审核”。

### 审核矩阵

| 审核对象 | 审核维度 | 通过标准 | 证据要求 |
|----------|----------|----------|----------|
| `verification-designing/instructions.md` | 阶段边界 | 明确 `verify_by` 由需求阶段确定；本阶段只校验一致性并设计路径 | 指出对应段落，并说明是否存在“重新选择验证方式”的误导 |
| `verification-designing/instructions.md` | 字符级断言边界 | 清楚区分稳定文本契约和自然语言语义 | 列出文档中“可断言”和“不可断言”规则是否完整 |
| `verification-designing/instructions.md` | 定性审核计划 | 要求写审核交接包、审核矩阵和非审核范围 | 检查是否足以指导后续 `verification-design.md` |
| `verifying/instructions.md` | 子智能体交接 | 要求把审核对象、目标、矩阵、输出格式完整交给子智能体 | 检查是否避免“帮我看一下”式模糊交接 |
| `verifying/instructions.md` | 人工反馈 | 要求人工逐项反馈同意、异议或补充 | 检查是否禁止只有整体同意就通过 |
| `verifying/instructions.md` | 分歧处理 | 明确人工意见优先，并记录拒绝子智能体发现的理由 | 检查证据写回规则是否闭合 |
| `task-package.verification-design.md` | 模板结构 | 为 `qualitative` 提供审核交接包和审核矩阵填写位置 | 检查模板不是只写抽象提醒 |
| `task-package.evidence.md` | 证据结构 | 能记录交接包摘要、子智能体发现、人工反馈、采纳/拒绝理由、残余风险 | 检查 evidence 能对应审核矩阵 |
| `docs/anti-patterns/skill-writing.md` | 反模式覆盖 | 覆盖文档默认 pytest、脆弱字符断言、定性审核交接不完整 | 检查反模式有错误特征、问题原因和正确做法 |
| `test_protocol_docs.py` | 测试边界 | 如有测试，只断言稳定文本契约，不断言自然语言语义 | 检查是否存在完整自然语言句子断言 |

### 非审核范围

- 不审核 CLI 状态机或新增命令行为。
- 不要求新增 `verify_by` 类型。
- 不评价所有历史任务包是否符合新规则。
- 不要求为自然语言语义新增 pytest。
- 不扩展为全仓库 Markdown 链接或格式治理。

### 输出格式

子智能体和人工审阅者均按以下结构输出：

- 结论：通过 / 有条件通过 / 不通过
- 逐项发现：审核对象、审核维度、问题、严重程度、建议处理
- 缺口：哪些维度证据不足
- 风险接受：哪些问题可以暂不处理及理由

## 可追溯性

| 需求交付物 | 验证方法 | 预期证据 |
|------------|----------|----------|
| 更新验证策略相关技能说明 | 审核矩阵检查 `verification-designing/instructions.md` 和 `verifying/instructions.md` | 子智能体和人工逐项确认阶段职责、交接和写回规则 |
| 补充字符级断言适用规则 | 审核矩阵检查“可断言/不可断言”边界 | 发现记录中列明规则是否完整、是否有误导 |
| 补充自然语言定性审核交接方法 | 审核矩阵检查交接包字段和输出格式 | evidence 记录交接包摘要和审核结论 |
| 补充审核结果写回要求 | 审核矩阵检查 `task-package.evidence.md` 和 `verifying/instructions.md` | evidence 能记录子智能体、人工反馈、分歧处理 |
| 更新反模式文档 | 审核矩阵检查反模式覆盖 | 子智能体和人工确认反模式是否具体可执行 |
| 必要时添加最小化测试 | 可选运行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` | 退出码 0；测试不覆盖自然语言语义 |

## 风险接受

- 接受不做全仓库历史文档迁移。本轮目标是修正后续协议入口，不追溯改写所有旧任务包。
- 接受辅助 pytest 可能不执行。若实施未新增稳定文本契约测试点，强行运行 pytest 对语义没有证明价值。
- 接受人工审阅者反馈成为完成门槛。定性审核的语义判断必须由人类确认，否则只能有条件通过或阻塞。
- 接受不新增 `verify_by` 类型。现有 `qualitative` 足以承载本轮文档审核。

## 验证执行计划

实施完成后立即执行：

1. 主 Agent 先自查是否存在自然语言完整句子 pytest 断言；如存在，实施阶段修正。
2. 如新增了稳定结构断言，执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`。
3. 主 Agent 按本文件“审核交接包”启动子智能体审核。
4. 主 Agent 将子智能体结论提交给人类审阅者逐项反馈。
5. 主 Agent 根据两方反馈修正文档或记录风险。
6. 主 Agent 将最终结果写入 `evidence.md`。

验证失败时：

- 发现协议文档仍暗示 `verification-designing` 可以重新选择 `verify_by`：回到 `implementing` 修正文档。
- 审核交接包不足以执行：回到 `verification_designing` 修正本文件。
- 子智能体或人工指出规则不可执行：回到 `implementing` 修正文档。
- 人工反馈缺失：不能进入 `verified`。
