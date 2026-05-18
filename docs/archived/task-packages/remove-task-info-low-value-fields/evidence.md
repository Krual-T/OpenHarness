# 验证证据

## 文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：删除低价值 task-info 字段。
- `openharness_cli/constants.py`：从必填字段集合删除旧完成条件字段。
- `openharness_cli/models/task_info.py`：删除旧完成条件的一等模型字段，旧 YAML 字段改由 `_extra` 通用机制保留。
- `openharness_cli/models/task_package.py`：删除旧完成条件的包装属性。
- `tests/openharness_cases/test_task_package_core.py`：更新任务包核心测试夹具，并断言新建任务包不生成已删除字段。
- `tests/openharness_cases/test_cli_workflows.py`：更新 CLI workflow 测试夹具，移除旧必填字段假设。
- `docs/task-packages/remove-task-info-low-value-fields/requirements.md`：记录本轮删除目标和兼容边界。
- `docs/task-packages/remove-task-info-low-value-fields/overview-design.md`：记录新 schema 表面和历史兼容策略。
- `docs/task-packages/remove-task-info-low-value-fields/detailed-design.md`：记录实现落点、接口语义和迁移顺序。
- `docs/task-packages/remove-task-info-low-value-fields/verification-design.md`：记录验证命令和预期结果。

## 测试结果
- RED 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py -q`
  - 退出码：`0`
  - 输出摘要：`27 passed`。当时测试夹具仍按旧 schema 写字段，未暴露模板和 schema 残留。
- RED 命令：`! rg -n 'done_criteria|depends_on|scope:|areas:' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：目标模板中仍有旧字段。
- RED 命令：`! rg -n '"done_criteria"' openharness_cli/constants.py`
  - 退出码：`1`
  - 输出摘要：必填字段集合中仍有旧完成条件字段。
- RED 命令：`rg -n 'done_criteria' openharness_cli/models/task_info.py`
  - 退出码：`0`
  - 输出摘要：模型中仍有旧完成条件一等字段。

- GREEN 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py -q`
  - 退出码：`0`
  - 输出摘要：`27 passed in 0.65s`。
- GREEN 命令：`! rg -n 'done_criteria|depends_on|scope:|areas:' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：无输出。
- GREEN 命令：`! rg -n '"done_criteria"' openharness_cli/constants.py`
  - 退出码：`0`
  - 输出摘要：无输出。
- GREEN 命令：`! rg -n 'done_criteria|depends_on|scope:|areas:' openharness_cli tests/openharness_cases skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：无输出。

## 验收标准覆盖表
- 模板不再包含三个低价值字段：由模板反向 `rg` 覆盖，结果通过。
- 旧完成条件不再是必填字段：由 constants 反向 `rg` 和核心测试覆盖，结果通过。
- 新建任务包不生成已删除字段：由 `test_new_package_creates_with_auto_id` 和 `test_create_task_package_from_templates` 覆盖，结果通过。
- CLI workflow 不依赖旧字段：由 `test_cli_workflows.py` 覆盖，结果通过。

## 验证结果

最终结论：通过。

最终验证命令：
- `uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py -q`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`27 passed in 0.57s`。
- `! rg -n 'done_criteria|depends_on|scope:|areas:' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：无输出。
- `! rg -n '"done_criteria"' openharness_cli/constants.py`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：无输出。
- `! rg -n 'done_criteria|depends_on|scope:|areas:' openharness_cli tests/openharness_cases skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：无输出。

## 残余风险

- 未覆盖风险：历史归档任务包仍可能包含已删除字段。
  - 接受理由：本轮删除新 schema 表面，不重写历史证据。
- 未覆盖风险：外部用户如果依赖 `TaskPackage.done_criteria` 属性会受到影响。
  - 接受理由：用户明确要求删除该字段；仓库内已搜索并移除一等字段引用。

## 后续事项

无必须跟进事项。
