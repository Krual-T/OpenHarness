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
- **计划路径**：直接审查 `skills/using-openharness/references/templates/task-package.task-info.yaml` 的 `id` 行，并用命令确认 `<DESIGN_ID>` 已移除、`id: TASK_ID` 已存在。
- **回退路径**：如果命令未通过，回到 `implementing` 阶段修正目标模板；如果发现实际协议仍需要 `<DESIGN_ID>`，回到需求阶段重新定义本任务。
- **路径说明**：本轮只修改一个 YAML 模板占位符，定性审查加精确文本搜索足以覆盖必须交付结果。无需单元测试或运行时工作流。

## 必需命令
1. `rg -n '^id: TASK_ID$' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：显示目标模板文件中的 `id: TASK_ID` 行。
2. `! rg -n '<DESIGN_ID>' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：无输出。

## 预期结果
- 目标模板文件的 `id` 字段为 `TASK_ID`。
- 目标模板文件中不再出现 `<DESIGN_ID>`。
- 目标模板的其他字段保持原有结构和语义。

## 可追溯性
- 需求结果 1 对应必需命令 1：证明 `id:` 行已经使用 `TASK_ID`。
- 需求结果 2 对应必需命令 2 和人工审查：证明旧占位符不存在，且没有扩大到流程、状态机或 CLI 变更。

## 风险接受
- 本轮不验证 CLI 生成任务包的完整行为，因为用户要求只修改模板文件，且目标验收标准是模板文本本身。
- 本轮不搜索整个仓库中的其他 `<DESIGN_ID>`，因为批量迁移历史命名属于非目标；只有发现新建任务包仍复制旧占位符时，才重新触发更大范围审查。

## 验证执行计划
- 执行人：当前实现者。
- 执行时机：模板修改完成后立即执行。
- 执行环境：仓库根目录 `/home/Shaokun.Tang/Projects/openharness`，需要可用的 `rg`。
- **Fallback**：验证失败则回到 `implementing` 修改模板；如果验证策略与实际需求不匹配，则回到 `verification_designing` 修正策略。
