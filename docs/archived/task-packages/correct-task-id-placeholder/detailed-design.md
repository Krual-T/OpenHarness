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
- **验证路径**：先运行聚焦单元测试，确认当前实现对 `<TASK_ID>` 不闭合；实现后再次运行同一测试，并用 `rg` 检查模板和代码中旧占位符使用点。
- **回退路径**：如果单元测试失败但不是占位符问题，先收窄到相关测试；如果 CLI 生成路径仍残留占位符，回到实现阶段修正替换表。
- **预期证据**：测试命令退出码、模板第一行、创建逻辑替换 key、测试样例中的 `<TASK_ID>`。

## 新增或修改文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：协议模板事实源，必须表达 `<TASK_ID>` 占位符。
- `openharness_cli/core/task_packages.py`：创建任务包和补齐阶段文件的模板替换入口，必须支持 `<TASK_ID>`。
- `tests/openharness_cases/test_task_package_core.py`：覆盖创建任务包主路径和临时模板样例。
- `tests/openharness_cases/test_yaml_quoting.py`：覆盖 YAML quoting 的创建路径，样例占位符需同步。
- `docs/task-packages/correct-task-id-placeholder/*`：记录本轮设计、验证和证据。

## 接口
稳定契约：
- 模板中的 `<TASK_ID>` 表示待替换为实际任务编号。
- `create_task_package` 返回的 `task_id` 必须等于写入 `task-info.yaml.id` 的值。
- `ensure_task_package_stage_files` 使用相同替换语义，避免补齐文件时出现不同占位符体系。

兼容性要求：
- 替换表继续支持 `<DESIGN_ID>`，让旧外部模板仍能生成可用任务包。

可观察性入口：
- 单元测试读取生成后的 YAML，直接断言 `status["id"] == task_id`。
- 文本搜索确认事实源模板使用 `<TASK_ID>`。

## 模块内部设计
`openharness_cli/core/task_packages.py` 内部职责：
- `_create_task_package_unlocked` 负责分配后的创建编排，构造通用替换表。
- `_create_task_package_document` 负责读取模板、对 `task-info.yaml` 的 YAML 敏感字段做 quoting、执行替换并写文件。
- `ensure_task_package_stage_files` 负责后续阶段缺失文件的补齐，应沿用同一任务编号占位符语义。

实现方式：
- 通用替换表新增 `<TASK_ID>`，值为实际任务编号。
- 兼容保留 `<DESIGN_ID>`，值同样为实际任务编号。
- `task-info.yaml` quoting 分支对 `<TASK_ID>` 和 `<DESIGN_ID>` 都写入 JSON quoted task id。

## 数据语义
- `<TASK_ID>`：模板占位符，生命周期只存在于模板文件；生成后的任务包中不应残留。
- `TaskInfo.id`：生成后的实际任务编号，例如 `TASK-012`。
- `<DESIGN_ID>`：兼容旧模板的历史占位符，不再作为当前模板推荐语义。

## 阶段门禁
进入实施前必须确定：
- 实现落点是模板、创建逻辑和创建路径测试。
- 替换逻辑同时支持 `<TASK_ID>` 和 `<DESIGN_ID>`。
- 测试必须断言生成后的 `id` 是实际分配值。
- 本轮不删除元数据字段，只评估其作用。

## 决策闭合
- 接受：保留 `<DESIGN_ID>` 兼容替换。理由是兼容外部旧模板的成本很低。
- 拒绝：只改模板不改测试。理由是测试样例会继续传播旧语义，无法防回归。
- 延期：删除 `done_criteria`、`depends_on`、`scope.areas`。触发条件是单独发起 task-info schema 精简任务。

## 错误处理
静默出错风险：模板存在 `<TASK_ID>` 但替换表不包含它时，文件仍会写出且 YAML 可能可解析，错误会延迟到后续按任务编号解析时暴露。

避免方式：测试直接读取生成后的 `task-info.yaml`，断言 `id` 等于 `create_task_package` 返回的 `task_id`，而不是只检查文件存在。

## 迁移说明
实施顺序：
1. 先更新测试样例和断言，形成失败信号。
2. 更新模板为 `id: <TASK_ID>`。
3. 更新替换逻辑支持 `<TASK_ID>`，保留 `<DESIGN_ID>`。
4. 运行聚焦测试和文本检查。

切换点：模板事实源第一行变为 `id: <TASK_ID>`。

回滚触发点：如果新建任务包仍不能生成实际 `TASK-xxx` id，回滚模板或修正替换表后重新验证。

## 推荐图示
不需要图示。

## 详细设计反思
测试策略挑战：只用 `rg` 检查模板不足以证明 CLI 生成闭合，因此必须跑创建任务包测试。

接口边界挑战：是否移除 `<DESIGN_ID>` 替换。结论是暂不移除，因为保留兼容不影响当前目标。

迁移假设挑战：当前新建的 `TASK-012` 已被错误模板污染，需要在任务包元数据中手动修正为实际编号，避免后续 transition 失败。
