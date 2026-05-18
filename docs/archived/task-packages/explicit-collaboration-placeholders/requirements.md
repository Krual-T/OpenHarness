# 需求

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 为什么现在要做这件事，而不是以后再做？
> - 当前痛点、缺口、冲突或风险具体是什么？
> - 本轮必须交付哪些结果？这些结果的验收标准是什么？
> - 本轮明确不做什么？哪个 counterexample 看起来相似，但仍然不属于这个任务包？
> - 目标用户是谁？核心场景是什么？单一成功指标是什么？
> - 本轮允许付出的 cost cap 是什么？
> - 有哪些不能违反的约束？
>
> **写法建议**：先写问题陈述（当前到底哪里痛），再写必须交付的结果（准备交付什么），不要倒过来。模板里的每个标题都是必答题。如果你写完后仍然无法解释"为什么不是另一个问题包"，说明需求还没收敛。

## 目标
让 `task-info.yaml` 模板显式展示需要填写的枚举字段，并用 `<候选值|>` 形式表达“可选枚举或留空”，避免 `collaboration: {}` 或空字符串让字段形状和可选值依赖模型猜测。

单一成功指标：新建任务包的 `task-info.yaml` 中包含 `collaboration.task_type`、`collaboration.design_review_mode` 和 `verification.verify_by` 键，且它们的值是包含候选枚举和空选项的占位符。

## 问题陈述
目标用户是创建和维护 OpenHarness 任务包的协作者。核心场景是新建任务包后填写 `task-info.yaml` 中的协作分叉字段。

当前模板写成 `collaboration: {}`，虽然注释说明了两个字段，但 YAML 结构里没有字段键。`verification.verify_by` 虽有字段键，但只写空字符串，候选值放在注释里。维护者或模型需要根据注释推断要补哪些值，容易漏写或写错层级。枚举占位符能同时表达字段、候选值和可留空。

## 必须交付的结果
1. 修改 `collaboration` 模板：
   - 验收标准：`collaboration.task_type` 为 `<mechanical|standard development|protocol/architecture|>`。
   - 验收标准：`collaboration.design_review_mode` 为 `<stepwise|auto|>`。
2. 保持未确认语义：
   - 验收标准：枚举占位符不会被解析为已确认值，requirements gate 仍能提示需要填写 `task_type` 和 `verify_by`。
3. 更新测试：
   - 验收标准：创建任务包测试断言生成的 `collaboration` 和 `verification` 结构包含枚举占位符。
4. 同步 `verification.verify_by`：
   - 验收标准：`verification.verify_by` 为 `<unit_test|qualitative|rwp|>`。

## 非目标
- 不改变 `collaboration` 字段枚举值。
- 不自动填入 `mechanical`、`auto`、`unit_test` 或其他确认结果。
- Counterexample：根据任务内容自动推断 `task_type`，属于新功能，不属于本轮模板修正。

## 约束
- 协议边界：字段键和候选值可以显式存在，但占位符不得被当成确认结果。
- 兼容性约束：现有 `CollaborationInfo.from_dict` 和 `VerificationInfo.from_dict` 对非法枚举占位符应继续解析为 `None`。
- 依赖限制：不新增依赖。
- Cost cap：模板、相关测试和任务包文档的一次小改动。
