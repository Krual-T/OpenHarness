# 验证证据

## 文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：将 `collaboration` 和 `verification.verify_by` 改为枚举候选占位符。
- `tests/openharness_cases/test_task_package_core.py`：更新临时模板和断言，验证生成 YAML 保留占位符且 gate 不通过。
- `tests/openharness_cases/test_yaml_quoting.py`：更新临时模板和断言，验证 quoting 路径也保留占位符。
- `docs/task-packages/explicit-collaboration-placeholders/requirements.md`：记录枚举占位符需求。
- `docs/task-packages/explicit-collaboration-placeholders/overview-design.md`：记录总体设计和取舍。
- `docs/task-packages/explicit-collaboration-placeholders/detailed-design.md`：记录实现落点和数据语义。
- `docs/task-packages/explicit-collaboration-placeholders/verification-design.md`：记录验证命令和预期结果。

## 测试结果
- RED 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_task_package_core.py::test_gate_precondition_failure_does_not_persist_intermediate_status tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 退出码：`0`
  - 输出摘要：`3 passed`。当时测试尚未断言枚举占位符。
- RED 命令：`rg -n 'task_type: <mechanical\|standard development\|protocol/architecture\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：无输出。
- RED 命令：`rg -n 'design_review_mode: <stepwise\|auto\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：无输出。
- RED 命令：`rg -n 'verify_by: <unit_test\|qualitative\|rwp\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：无输出。

- GREEN 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_task_package_core.py::test_gate_precondition_failure_does_not_persist_intermediate_status tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 退出码：`0`
  - 输出摘要：`3 passed in 0.11s`。
- GREEN 命令：`rg -n 'task_type: <mechanical\|standard development\|protocol/architecture\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：`17:  task_type: <mechanical|standard development|protocol/architecture|>`。
- GREEN 命令：`rg -n 'design_review_mode: <stepwise\|auto\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：`18:  design_review_mode: <stepwise|auto|>`。
- GREEN 命令：`rg -n 'verify_by: <unit_test\|qualitative\|rwp\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：`20:  verify_by: <unit_test|qualitative|rwp|>`。

## 验收标准覆盖表
- `collaboration.task_type` 使用枚举候选占位符：由文本检查和创建任务包测试覆盖，结果通过。
- `collaboration.design_review_mode` 使用枚举候选占位符：由文本检查和创建任务包测试覆盖，结果通过。
- `verification.verify_by` 使用枚举候选占位符：由文本检查和创建任务包测试覆盖，结果通过。
- 占位符不被当作已确认值：由 gate 测试覆盖，结果通过。

## 验证结果

最终结论：通过。

最终验证命令：
- `uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_task_package_core.py::test_gate_precondition_failure_does_not_persist_intermediate_status tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`3 passed in 0.08s`。
- `rg -n 'task_type: <mechanical\|standard development\|protocol/architecture\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`17:  task_type: <mechanical|standard development|protocol/architecture|>`。
- `rg -n 'design_review_mode: <stepwise\|auto\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`18:  design_review_mode: <stepwise|auto|>`。
- `rg -n 'verify_by: <unit_test\|qualitative\|rwp\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`20:  verify_by: <unit_test|qualitative|rwp|>`。

## 残余风险

- 未覆盖风险：没有为占位符格式新增解析器或 schema 校验。
  - 接受理由：当前模板体系已经使用尖括号占位符；现有枚举解析会把这些值视为未确认。

## 后续事项

无必须跟进事项。
