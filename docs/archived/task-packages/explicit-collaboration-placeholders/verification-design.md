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
- **计划路径**：运行创建任务包测试和 gate 测试，确认生成的 YAML 保留枚举候选占位符，且这些占位符不会被解析为已确认值；用文本检查确认模板事实源写入预期占位符。
- **回退路径**：如果测试失败，回到实现阶段修正模板或测试；如果占位符被 gate 当作有效值，回到模型解析逻辑。
- **路径说明**：本轮是模板输出行为，可用单元测试自动判定；文本检查覆盖事实源。

## 必需命令
1. `uv run pytest tests/openharness_cases/test_task_package_core.py::test_create_task_package_from_templates tests/openharness_cases/test_task_package_core.py::test_gate_precondition_failure_does_not_persist_intermediate_status tests/openharness_cases/test_yaml_quoting.py::test_create_task_package_quotes_yaml_sensitive_status_fields -q`
   - 期望退出码：`0`
   - 期望输出：三个测试通过。
2. `rg -n 'task_type: <mechanical\\|standard development\\|protocol/architecture\\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：显示 `task_type` 占位符行。
3. `rg -n 'design_review_mode: <stepwise\\|auto\\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：显示 `design_review_mode` 占位符行。
4. `rg -n 'verify_by: <unit_test\\|qualitative\\|rwp\\|>' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：显示 `verify_by` 占位符行。

## 预期结果
- 新模板含有 `collaboration.task_type` 和 `collaboration.design_review_mode` 的枚举候选占位符。
- 新模板含有 `verification.verify_by` 的枚举候选占位符。
- 新建任务包生成的 YAML 保留这些占位符。
- requirements gate 仍提示 `task_type is not confirmed` 和 `verify_by is not determined`。

## 可追溯性
- 需求结果 1 由命令 1、2、3 覆盖。
- 需求结果 2 由命令 1 覆盖。
- 需求结果 3 由命令 1 覆盖。
- 需求结果 4 由命令 1、4 覆盖。

## 风险接受
- 接受风险：占位符格式不是 YAML schema 标准。理由是该仓库模板已经使用 `<TASK_ID>` 等占位符，保持一致。
- 接受风险：不新增专门解析逻辑。理由是现有枚举解析已能把占位符当作未确认。

## 验证执行计划
- 执行人：当前实现者。
- 执行时机：实现前观察失败，实现后和 verifying 阶段重复执行。
- 执行环境：仓库根目录 `/home/Shaokun.Tang/Projects/openharness`，使用 `uv run`。
- **Fallback**：验证失败回到 `implementing`；验证命令不准确则回到 `verification_designing`。
