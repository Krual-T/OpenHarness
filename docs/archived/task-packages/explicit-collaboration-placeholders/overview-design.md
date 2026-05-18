# 总体设计

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 这轮设计覆盖哪些表面，明确不覆盖哪些表面？
> - 推荐方案的主结构是什么？关键模块边界、接口边界或流程边界是什么？
> - 关键数据/状态模型是什么？哪些全局语义会影响后续实现？
> - 主路径是怎么走的？架构级安全、一致性、权限或兼容性约束是什么？
> - key failure modes 是什么？失败时如何降级、回滚或收缩？
> - 为什么选这个方向，而不是另一个可行方向？至少一个备选为何没被采用？
> - 哪些关系最好通过 PlantUML 图示来稳定表达？
>
> **写法建议**：写 System Boundary 时优先用"覆盖什么 / 不覆盖什么"两类句子；写 Trade-offs 时不只写优点还要写代价和放弃了什么；写 Proposed Structure 时优先点名具体模块、接口责任和关键数据/状态模型，不要只写抽象原则。写完后检查：一个不了解上下文的人能不能靠这份文档知道"这一轮设计到底包多大、为什么这样分、关键数据怎么流、失败时怎么办"。

## 系统边界
覆盖范围：
- `task-package.task-info.yaml` 模板中的 `collaboration` 和 `verification.verify_by` 结构。
- 创建任务包测试中对模板输出结构的断言。

不纳入范围：
- 不改变 `CollaborationInfo` 解析逻辑。
- 不改变 `requirements_designed` gate 的校验规则。
- 不自动推断或填写 `task_type`、`design_review_mode`。

## 推荐结构
推荐方案：
- 模板将 `collaboration: {}` 改为嵌套结构：
  - `task_type: <mechanical|standard development|protocol/architecture|>`
  - `design_review_mode: <stepwise|auto|>`
- 模板将 `verification.verify_by` 改为 `<unit_test|qualitative|rwp|>`。
- 模型解析保持不变：这些占位符不是合法枚举，会被解析为未确认。

## 关键流程
主流程：
1. 新建任务包时模板写出显式 `collaboration` 键。
2. 用户或模型能直接看到应填写的两个字段。
3. 字段为枚举占位符时，`package.task_type`、`package.design_review_mode` 和 `package.verify_by` 仍为空。
4. requirements gate 继续要求确认 `task_type` 和 `verify_by`。

失败信号：
- 新模板仍是 `collaboration: {}`。
- 枚举占位符被误解析为有效枚举，导致 gate 错误通过。

## 阶段门禁
进入详细设计前必须确认：
- 显式字段值使用枚举候选占位符，不使用真实单一枚举值。
- 测试覆盖生成后的 YAML 结构。
- 测试覆盖枚举占位符仍触发 gate 提示。

## 取舍
收益：模板结构和候选值都更明确，减少靠注释猜字段层级和枚举值。

代价：模板多两行，但这两行是当前流程真实需要填写的字段。

被拒绝方案：继续使用 `collaboration: {}`。拒绝原因是字段形状不在 YAML 结构里，容易漏写。

被拒绝方案：填入 `task_type: mechanical`、`design_review_mode: auto` 和 `verify_by: unit_test`。拒绝原因是这会伪造确认结果，破坏需求阶段门禁。

## 推荐图示
不需要图示。

## 总体设计反思
挑战 1：枚举占位符会不会绕过 gate？
- 结论：拒绝该风险。现有解析逻辑只接受精确枚举值，占位符会返回 `None`，gate 仍会提示缺少 `task_type` 和 `verify_by`。

挑战 2：是否也要同步 `verification.verify_by`？
- 结论：接受。它和 `collaboration` 字段一样是必填分叉字段，应该采用同一种占位符表达。
