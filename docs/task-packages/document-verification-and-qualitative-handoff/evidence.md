# 证据

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 验证结果

- **verify_by**: qualitative
- **Result**: 待 `verifying` 阶段最终判定

## 变更文件

- `skills/using-openharness/states/verification-designing/instructions.md` — 明确验证设计阶段消费并校验需求阶段确定的 `verify_by`，补充文档字符级断言边界和 `qualitative` 审核交接包要求。
- `skills/using-openharness/states/verifying/instructions.md` — 补充定性审核交接包执行、子 Agent 逐项审核、人工逐项反馈、分歧处理和证据完整性要求。
- `skills/using-openharness/references/templates/task-package.verification-design.md` — 增加 `## 审核交接包` 和 `### 审核矩阵` 模板结构。
- `skills/using-openharness/references/templates/task-package.evidence.md` — 扩展 `## 语义审核`，增加交接包摘要、逐项人工反馈和发现处理结构。
- `docs/anti-patterns/skill-writing.md` — 增加“对自然语言文档默认使用 pytest”和“定性审核交接不完整”两个反模式。
- `tests/openharness_cases/test_protocol_docs.py` — 增加模板稳定章节的最小结构断言，不断言自然语言完整句子。
- `docs/task-packages/document-verification-and-qualitative-handoff/requirements.md` — 记录本轮需求。
- `docs/task-packages/document-verification-and-qualitative-handoff/overview-design.md` — 记录总体设计。
- `docs/task-packages/document-verification-and-qualitative-handoff/detailed-design.md` — 记录详细设计。
- `docs/task-packages/document-verification-and-qualitative-handoff/verification-design.md` — 记录验证计划和审核交接包。
- `docs/task-packages/document-verification-and-qualitative-handoff/task-info.yaml` — 记录任务状态和分叉字段。
- `pyproject.toml` — 本轮协议修正提交前将版本号从 `0.5.10` 递增到 `0.5.11`。

## 测试结果

辅助结构测试已执行：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

结果：`17 passed in 0.24s`。

用户指出 `verification-designing/instructions.md` 中 `## verify_by 选择约束` 仍会误导阶段职责，且文档字符级断言边界不应对所有 `verify_by` 暴露。已增量修正为：

- 标题改为 `## verify_by 一致性校验`。
- 按 Jinja 条件只渲染当前 `verify_by` 的一致性规则。
- `## 文档与字符级断言边界` 和 `## qualitative 审核交接包` 只在 `verify_by == "qualitative"` 时渲染。
- 定性审核相关失败回退、要点和常见失败模式也改为 `qualitative` 条件渲染。

修正后重新执行：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

结果：`17 passed in 0.20s`。

用户继续指出 Jinja 分支内不应输出“当前 `verify_by: ...`”这类自报分支的文字。已增量修正为直接写该分支的校验要求，并删除 RWP 小节中的 `当 verify_by == rwp 时`。

修正后重新执行：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

结果：`17 passed in 0.21s`。

说明：该命令只覆盖模板新增稳定章节和协议结构锚点，不作为自然语言语义正确性的证据。

用户要求修正四个实现审查问题后，已增量修改：

- `verifying/instructions.md`：将验证命令步骤改为“如有”，允许无必需命令的 `qualitative` 任务直接进入定性审核；将最终 `evidence.md` 写回步骤移到定性审核和 RWP 审核之后。
- `verifying/instructions.md`：阶段结束检查和常见失败模式同步改成“声明了命令才必须执行”，并要求无必需命令时写明原因。
- `verification-designing/instructions.md`：将 `verify_by` 冲突回退动作统一为回退需求阶段，修正 `requirements.md` 和 `task-info.yaml` 后再进入验证设计。
- `docs/anti-patterns/skill-writing.md`：把“用脆弱字符断言替代语义审核”拆成独立反模式。

修正后执行：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

结果：`17 passed in 0.27s`。

## 语义审核

`verifying` 阶段按 `verification-design.md` 的审核交接包执行。

### 实施阶段自查

| 审核对象 | 自查项 | 结果 |
|----------|--------|------|
| `verification-designing/instructions.md` | 是否仍暗示本阶段可静默重新选择 `verify_by` | 未发现静默切换要求；新增说明要求冲突时回退需求阶段 |
| `verification-designing/instructions.md` | 是否仍以“选择约束”展示全量 verify_by 分流规则 | 已改为 `## verify_by 一致性校验`，并按 Jinja 条件渲染当前类型 |
| `verification-designing/instructions.md` | 是否说明字符级断言适用和不适用边界 | 已新增对应章节 |
| `verifying/instructions.md` | 是否要求完整交接包和人工逐项反馈 | 已新增对应流程和失败处理 |
| `task-package.verification-design.md` | 是否有审核交接包和审核矩阵位置 | 已新增稳定章节 |
| `task-package.evidence.md` | 是否能记录交接包、反馈和处理理由 | 已扩展语义审核结构 |
| `docs/anti-patterns/skill-writing.md` | 是否覆盖文档默认 pytest 和交接不完整反模式 | 已新增两个反模式 |
| `test_protocol_docs.py` | 是否只断言稳定模板结构 | 新增断言只覆盖章节锚点 |

## 残余风险

待 `verifying` 阶段填写。

## 后续事项

待 `verifying` 阶段填写。
