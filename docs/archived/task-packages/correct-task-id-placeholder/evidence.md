# 验证证据

## 文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：将模板第一行修正为 `id: <TASK_ID>`。
- `openharness_cli/core/task_packages.py`：新增 `<TASK_ID>` 替换，并保留 `<DESIGN_ID>` 兼容替换。
- `tests/openharness_cases/test_task_package_core.py`：把创建路径测试样例改为 `<TASK_ID>`，并断言生成后的 `id` 等于分配的 `task_id`。
- `tests/openharness_cases/test_yaml_quoting.py`：把 YAML quoting 测试样例改为 `<TASK_ID>`，并断言生成后的 `id` 等于分配的 `task_id`。
- `docs/task-packages/correct-task-id-placeholder/requirements.md`：记录纠错需求和字段评估边界。
- `docs/task-packages/correct-task-id-placeholder/overview-design.md`：记录总体方案和不删除字段的范围控制。
- `docs/task-packages/correct-task-id-placeholder/detailed-design.md`：记录实现落点、接口语义和迁移顺序。
- `docs/task-packages/correct-task-id-placeholder/verification-design.md`：记录验证命令和预期结果。

## 测试结果
- RED 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 退出码：`0`
  - 输出摘要：`2 passed`。当时测试尚未断言 `id == task_id`，未暴露错误。
- RED 命令：`rg -n '^id: <TASK_ID>$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：无输出。
- RED 命令：`! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 退出码：`1`
  - 输出摘要：测试样例中仍有 `<DESIGN_ID>`。
- RED 命令：`rg -n '"<TASK_ID>"|<TASK_ID>' openharness_cli/core/task_packages.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 退出码：`1`
  - 输出摘要：无输出。

- GREEN 命令：`uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 退出码：`0`
  - 输出摘要：`2 passed in 0.13s`。
- GREEN 命令：`rg -n '^id: <TASK_ID>$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：`1:id: <TASK_ID>`。
- GREEN 命令：`! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 退出码：`0`
  - 输出摘要：无输出。
- GREEN 命令：`rg -n '"<TASK_ID>"|<TASK_ID>' openharness_cli/core/task_packages.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 退出码：`0`
  - 输出摘要：创建逻辑和测试样例中均存在 `<TASK_ID>` 使用点。

## 验收标准覆盖表
- 模板使用 `<TASK_ID>`：由 `rg -n '^id: <TASK_ID>$' ...` 覆盖，结果通过。
- 创建逻辑替换 `<TASK_ID>`：由聚焦 pytest 和 `rg` 检查 `openharness_cli/core/task_packages.py` 覆盖，结果通过。
- 测试样例不再使用 `<DESIGN_ID>`：由反向 `rg` 覆盖，结果通过。
- 字段实际作用评估：由最终答复覆盖。

## 验证结果

最终结论：通过。

最终验证命令：
- `uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`2 passed in 0.07s`。
- `rg -n '^id: <TASK_ID>$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`1:id: <TASK_ID>`。
- `! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：无输出。
- `rg -n '"<TASK_ID>"|<TASK_ID>' openharness_cli/core/task_packages.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：创建逻辑和测试样例中均存在 `<TASK_ID>` 使用点。

## 残余风险

- 未覆盖风险：未运行完整测试套件。
  - 接受理由：本轮改动集中在任务包创建模板替换路径，已运行覆盖该路径的聚焦测试。
- 未覆盖风险：仍保留 `<DESIGN_ID>` 的兼容替换。
  - 接受理由：这是有意兼容外部旧模板，不影响当前模板语义。
- 未覆盖风险：未删除 `done_criteria`、`depends_on`、`scope.areas`。
  - 接受理由：这是 schema 精简问题，需要单独任务包设计迁移和验证。

## 后续事项

后续如决定精简 `task-info.yaml` schema，应单独评估并删除或迁移 `done_criteria`、`depends_on`、`scope.areas`。
