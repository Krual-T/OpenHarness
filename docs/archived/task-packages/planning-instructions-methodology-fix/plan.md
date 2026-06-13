# 计划

## 实施步骤

- [ ] 重写 planning 阶段步骤说明
  - 修改对象：`skills/using-openharness/states/planning/instructions.md`
  - 完成条件：移除“校验任务类型”；使用 Jinja 按 `task_type` 渲染 standard/structural 的输入文档和计划深度说明。
  - 验证方式：文本检查确认不再出现“校验任务类型”，并确认 Jinja 分支存在。

- [ ] 补充 plan 写作方法论
  - 修改对象：`skills/using-openharness/states/planning/instructions.md`
  - 完成条件：指令要求计划覆盖目标与上下文、输入文档、实施步骤、文件修改计划、验证设计、进度记录、决策与发现、风险接受、完成判定。
  - 验证方式：协议文档测试确认核心章节锚点存在。

- [ ] 更新协议测试和证据
  - 修改对象：`tests/openharness_cases/test_protocol_docs.py`、本任务 `evidence.md`
  - 完成条件：测试能防止 planning 指令回到任务类型校验；验证结果写入证据。
  - 验证方式：运行聚焦测试和全量测试。

## 验证设计

- **主要验证方式**：`unit_test`
- **必需命令**：
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py -v`
  - `uv run pytest tests/ -v`
- **预期结果**：
  - planning 指令不再包含“校验任务类型”。
  - planning 指令包含 `task_type == "standard"` 和 `task_type == "structural"` 的 Jinja 分支。
  - planning 指令包含计划写作的核心结构：目标与上下文、输入文档、实施步骤、文件修改计划、验证设计、进度记录、决策与发现、风险接受、完成判定。
- **边界或错误场景**：
  - 不新增第二套 `plan.md` 模板。
  - 不修改 workflow 状态机。

## 完成判定

- **进入实现的条件**：本计划列清修改文件、验证方式和不做事项。
- **实现完成的条件**：planning 指令和测试更新完成，聚焦测试通过。
- **验证完成的条件**：全量测试通过，`evidence.md` 记录结果。

## 风险接受

- 不对 OpenSpec/Superpowers/Codex/Claude/Cursor 的计划格式做完整兼容，只吸收共同方法论。接受理由：OpenHarness 需要保持自己的任务包协议。
