# 详细设计

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 哪些文件会新增或修改，为什么是这些地方？
> - 涉及哪些接口、契约和稳定边界？精度需要细到什么程度？
> - 模块内部职责如何拆分？谁负责状态变化、校验、编排和副作用？
> - 关键数据结构、字段语义或状态转换约束是什么？
> - 准备怎么验证这轮工作真的成立？如果主验证路径走不通，降级路径是什么？
> - testing-first / verification-first 的实施顺序是什么？
> - observability 要求是什么？要靠什么看见失败或退化？
> - 失败路径、误用风险和静默出错风险是什么？
> - 迁移顺序和回滚注意事项是什么？
> - 还有哪些挑战被接受、拒绝或延期？
> - 哪些交互关系最适合用 PlantUML 表达？
>
> **写法建议**：先把实现设计写到足以判断验证对象，再写验证路径（否则容易让测试或命令替代真实设计）。Files Added Or Changed 不只是改动清单，更是"为什么这些地方承载本轮实现"的解释。模块内部职责、数据语义和异常边界要写到 agent 能直接据此落实现。如果你写完后还不能直接开始实施，说明 detailed 还不够具体。

## 可观察性与验证准备
- **验证路径**：运行创建任务包测试，读取生成后的 YAML，断言 `collaboration.task_type`、`collaboration.design_review_mode` 和 `verification.verify_by` 为枚举候选占位符；运行 gate 测试确认占位符仍未通过确认。
- **回退路径**：如果测试失败，回到模板结构或测试断言修正；如果占位符绕过 gate，需要回到模型解析逻辑。
- **预期证据**：模板文本、生成 YAML 结构、requirements gate 输出。

## 新增或修改文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：模板事实源，承载显式字段结构。
- `tests/openharness_cases/test_task_package_core.py`：创建任务包和 gate 测试，承载回归保护。
- `tests/openharness_cases/test_yaml_quoting.py`：同样使用临时模板创建任务包，需保持模板形状一致。
- `docs/task-packages/explicit-collaboration-placeholders/*`：记录本轮协议修正。

## 接口
稳定契约：
- `collaboration.task_type` 的枚举候选占位符表示未确认。
- `collaboration.design_review_mode` 的枚举候选占位符表示未确认。
- `verification.verify_by` 的枚举候选占位符表示未确认。
- 只有非空且合法枚举值才会被 `CollaborationInfo` 解析为有效值。

## 模块内部设计
不修改模块逻辑。现有 `CollaborationInfo.from_dict` 和 `VerificationInfo.from_dict` 只接受精确枚举值；本轮让模板输出非法枚举占位符，从而保持未确认语义。

## 数据语义
- `collaboration: {}`：旧模板形状，表达不出字段键。
- `collaboration.task_type: <mechanical|standard development|protocol/architecture|>`：字段存在、候选值存在、未确认。
- `collaboration.design_review_mode: <stepwise|auto|>`：字段存在、候选值存在、未确认。
- `verification.verify_by: <unit_test|qualitative|rwp|>`：字段存在、候选值存在、未确认。

## 阶段门禁
进入实施前必须确定：
- 只改模板和临时测试模板。
- 枚举候选占位符不代表确认。
- 测试要覆盖生成结构和 gate 行为。

## 决策闭合
- 接受：显式枚举候选占位符。理由是字段形状和候选值清晰，且不伪造确认。
- 拒绝：真实枚举占位。理由是会绕过或混淆确认语义。
- 拒绝：继续 `{}`。理由是结构信息不足。

## 错误处理
静默风险：字段显式存在后，维护者可能误以为占位符已经满足要求。避免方式是保留 gate 测试，确保占位符仍输出 `task_type is not confirmed` 和 `verify_by is not determined`。

## 迁移说明
实施顺序：
1. 更新测试临时模板和断言。
2. 更新模板事实源。
3. 运行聚焦测试和文本检查。

回滚触发点：如果占位符导致 gate 错误通过，回滚模板或调整解析逻辑。

## 推荐图示
不需要图示。

## 详细设计反思
测试策略挑战：只检查模板文本不够，必须读取生成 YAML，确认枚举占位符结构被保留。

接口边界挑战：不改解析逻辑是否足够。结论是足够，因为现有解析已经正确处理空字符串。
