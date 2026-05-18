# 验证策略

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **本文件在 `verification_designing` 阶段编写（TDD 红阶段，先于实现）**。
> 定义验证策略——计划怎么验证、用什么命令、期望什么结果。
> 实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。
>
> **使用前先确认你能回答这些问题**：
> - 每项 Required Outcome 是否有对应的验证方法？
> - 验证命令是否具体到可以直接复制粘贴执行？
> - 是否有边界或错误场景的验证？
> - 哪些风险本轮不覆盖，接受理由是什么？
> - 计划路径和回退路径分别是什么？

## 验证路径
- **计划路径**：运行任务包创建相关单元测试，确认 `<TASK_ID>` 模板会生成实际 `TASK-xxx`；同时用文本检查确认模板事实源和测试样例不再使用 `<DESIGN_ID>` 作为创建路径占位符。
- **回退路径**：如果 pytest 失败，先判断是占位符生成失败还是测试环境失败；如果文本检查失败，回到实现阶段同步模板、替换逻辑或测试样例。
- **路径说明**：本轮改动是可编程输入输出行为，`unit_test` 能自动判定核心结果；`rg` 用于补充检查模板事实源和旧语义残留。

## 必需命令
1. `uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
   - 期望退出码：`0`
   - 期望输出：两个测试通过。
2. `rg -n '^id: <TASK_ID>$' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：显示目标模板第一行。
3. `! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
   - 期望退出码：`0`
   - 期望输出：无输出。
4. `rg -n '"<TASK_ID>"|<TASK_ID>' openharness_cli/core/task_packages.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py`
   - 期望退出码：`0`
   - 期望输出：显示创建逻辑和测试样例中的 `<TASK_ID>` 使用点。

## 预期结果
- 模板第一行是 `id: <TASK_ID>`。
- 创建任务包时，生成文件的 `id` 是实际分配到的 `TASK-xxx`。
- 相关创建路径测试样例使用 `<TASK_ID>`。
- 旧的 `<DESIGN_ID>` 不再出现在本轮目标模板和测试样例中。

## 可追溯性
- 需求结果 1 由命令 2 覆盖。
- 需求结果 2 由命令 1 和命令 4 覆盖。
- 需求结果 3 由命令 1、命令 3、命令 4 覆盖。
- 需求结果 4 由最终答复中的字段评估结论覆盖。

## 风险接受
- 接受风险：不删除 `done_criteria`、`depends_on`、`scope.areas`。理由是本轮目标是纠正占位符；字段删除需要 schema 迁移设计。
- 接受风险：保留 `<DESIGN_ID>` 的代码兼容替换。理由是这不会影响新模板语义，且降低旧模板兼容风险。
- 接受风险：不改写历史任务包中关于上一轮错误提交的证据文本。理由是归档证据应保留当时事实。

## 验证执行计划
- 执行人：当前实现者。
- 执行时机：实现前运行命令 1 观察失败；实现后运行全部命令；验证阶段再次运行全部命令。
- 执行环境：仓库根目录 `/home/Shaokun.Tang/Projects/openharness`，按仓库约定使用 `uv run`。
- **Fallback**：验证失败则回到 `implementing` 修正；如果发现命令不能代表验收标准，则回到 `verification_designing` 修正策略。
