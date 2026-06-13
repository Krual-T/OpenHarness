# 证据

## 验证结果

- **method**: unit_test
- **rwp_enabled**: false
- **Result**: passed

## 变更文件

- `skills/using-openharness/states/planning/instructions.md` — 重写 planning 阶段指令，移除任务类型校验，改为按 `task_type` 渲染输入文档和计划深度说明。
- `tests/openharness_cases/test_protocol_docs.py` — 增加 planning 指令协议测试，锁住 Jinja 分支和实现计划核心结构。
- `docs/task-packages/planning-instructions-methodology-fix/requirements.md` — 记录需求。
- `docs/task-packages/planning-instructions-methodology-fix/plan.md` — 记录实施计划。
- `docs/task-packages/planning-instructions-methodology-fix/task-info.yaml` — 记录任务分叉字段。

## 测试结果

```text
uv run pytest tests/openharness_cases/test_protocol_docs.py -v
结果：18 passed, 0 failed
```

```text
uv run pytest tests/ -v
结果：62 passed, 0 failed
```

## 验收标准覆盖

| 标准 | 证据 |
|------|------|
| planning 阶段不再校验任务类型 | `test_planning_instructions_render_by_task_type_and_focus_on_execution_plan` 断言不包含“校验任务类型” |
| 按 `task_type` 渲染 standard/structural 说明 | 同一测试断言包含 `task_type == "standard"` 与 `task_type == "structural"` 分支 |
| plan 保持一套模板，两类任务只改变说明深度 | planning 指令写明“一套 `plan.md` 模板即可” |
| plan 方法论覆盖核心结构 | 同一测试断言目标与上下文、输入文档、实施步骤、文件修改计划、验证设计、进度记录、决策与发现、风险接受、完成判定 |

## 运行时观察

未启用 RWP。

## 残余风险

本轮只修正 planning 指令，没有把 `task-package.plan.md` 模板同步扩展到完整推荐结构。接受理由：用户要求的是阶段指令方法论；模板扩展可在后续单独处理。

## 后续事项

无。
