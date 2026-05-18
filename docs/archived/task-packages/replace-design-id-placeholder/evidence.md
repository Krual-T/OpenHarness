# 验证证据

## 文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：将 `id` 占位符从 `<DESIGN_ID>` 改为 `TASK_ID`。
- `docs/task-packages/replace-design-id-placeholder/requirements.md`：记录本轮需求、边界和验收标准。
- `docs/task-packages/replace-design-id-placeholder/task-info.yaml`：记录任务分类、验证方式和完成标准。
- `docs/task-packages/replace-design-id-placeholder/verification-design.md`：记录验证路径、命令和预期结果。

## 语义审核
- RED 命令：`rg -n '^id: TASK_ID$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：无输出，说明修改前目标行不存在。
- RED 命令：`! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`1`
  - 输出摘要：`1:id: <DESIGN_ID>`，说明修改前旧占位符仍存在。
- GREEN 命令：`rg -n '^id: TASK_ID$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：`1:id: TASK_ID`。
- GREEN 命令：`! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 退出码：`0`
  - 输出摘要：无输出。

## 验证结果

最终结论：通过。

最终验证命令：
- `rg -n '^id: TASK_ID$' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：`1:id: TASK_ID`
- `! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 期望退出码：`0`
  - 实际退出码：`0`
  - 输出摘要：无输出。

审核对象：
- `skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 审核维度：`id` 占位符语义是否为任务标识。
  - 发现：旧占位符 `<DESIGN_ID>` 已闭合，严重程度低。
- `docs/task-packages/replace-design-id-placeholder/requirements.md`
  - 审核维度：需求、边界、验收标准是否完整。
  - 发现：无未闭合问题。
- `docs/task-packages/replace-design-id-placeholder/verification-design.md`
  - 审核维度：验证命令是否可执行，期望结果是否明确。
  - 发现：无未闭合问题。

验收标准覆盖：
- `id:` 行从 `id: <DESIGN_ID>` 变为 `id: TASK_ID`：由最终验证命令 1 覆盖，结果通过。
- 目标模板中不再出现 `<DESIGN_ID>`：由最终验证命令 2 覆盖，结果通过。
- 不引入流程、状态机或 CLI 变更：由变更文件清单和审核对象覆盖，结果通过。

## 残余风险

- 未覆盖风险：未运行 CLI 新建任务包的端到端流程。
  - 接受理由：本轮目标是模板文本替换，不修改 CLI 行为；验证命令已直接覆盖用户指定文件。
- 未覆盖风险：仓库其他位置可能仍有历史命名。
  - 接受理由：批量迁移被需求明确列为非目标；如后续发现其他模板仍误导新任务包语义，应另开任务包处理。

## 后续事项

无必须跟进事项。
