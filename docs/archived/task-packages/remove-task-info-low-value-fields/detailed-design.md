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
- **验证路径**：用 `rg` 检查模板和常量中字段已移除；用聚焦 pytest 检查创建、验证和流程命令在缺少 `done_criteria` 时仍可运行。
- **回退路径**：如果测试失败，先判断是测试夹具仍写旧字段、校验仍要求旧字段，还是模型读取兼容被破坏；对应回到实现修正。
- **预期证据**：模板不含字段、`REQUIRED_STATUS_KEYS` 不含 `done_criteria`、新建任务包不生成字段、缺少 `done_criteria` 的任务包能通过基础验证。

## 新增或修改文件
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：删除新任务包默认字段。
- `openharness_cli/constants.py`：从必填字段集合删除 `done_criteria`。
- `openharness_cli/models/task_info.py` 和 `openharness_cli/models/task_package.py`：删除 `done_criteria` 一等模型字段和包装属性。
- `tests/openharness_cases/test_task_package_core.py`：更新最小仓库模板和校验测试，覆盖缺少 `done_criteria` 的合法性。
- `tests/openharness_cases/test_cli_workflows.py`：更新 CLI 流程测试夹具，避免继续表达旧必填假设。
- `docs/task-packages/remove-task-info-low-value-fields/*`：记录本轮协议精简过程。

## 接口
稳定边界：
- 新 `task-info.yaml` 不要求 `done_criteria`、`depends_on`、`scope.areas`。
- `TaskInfo.from_dict` 仍通过 `_extra` 接受旧字段，这是兼容边界。
- `validate_task_package` 的必填判断以 `REQUIRED_STATUS_KEYS` 为准；删除 `done_criteria` 后不应再报缺失。

可观察性：
- `rg` 直接观察模板和常量。
- pytest 观察 CLI 创建和验证行为。

## 模块内部设计
`constants.py` 承载必填 schema；从这里删除 `done_criteria` 会让 `validate_task_package` 自动停止要求该字段。

`TaskInfo` 不再显式解析 `done_criteria`；该字段如果存在于旧 YAML，会留在 `raw` 中并进入 `_extra`。这样历史任务包如果被读取后再写出，字段仍可保留，但它不再是一等协议字段。

测试夹具中的 `done_criteria` 删除只针对不依赖它的场景；如果某个测试特意验证旧包兼容，可以保留或新增专门断言。

## 数据语义
- `done_criteria`：从必填 schema 和一等模型字段删除，旧值通过 `_extra` 兼容。
- `depends_on`：从新模板删除；如果旧包存在，会作为 `_extra` 保留。
- `scope.areas`：从新模板删除；如果旧包存在，会作为 `_extra` 保留。
- `verification.verify_by`、`collaboration.task_type` 仍是当前阶段门禁消费字段，不受影响。

## 阶段门禁
进入实施前必须确定：
- 删除字段只影响新模板和必填校验。
- 兼容读取旧字段。
- 测试必须证明缺少 `done_criteria` 不再报必填缺失。
- 本任务包自身在旧校验阶段可临时保留 `done_criteria`，实现后删除。

## 决策闭合
- 接受：删除模板中的三个字段。理由是它们当前不是新任务包的必要输入。
- 接受：删除 `done_criteria` 必填校验。理由是它没有门禁语义，只增加填写负担。
- 接受：删除模型一等属性。理由是 `_extra` 已经覆盖旧字段保留，不需要专门属性。
- 拒绝：历史批量迁移。理由是超出本轮范围。

## 错误处理
静默出错风险：只删模板不删 `REQUIRED_STATUS_KEYS` 时，新建任务包会立刻被 validate 报缺失 `done_criteria`。

避免方式：同时更新常量和测试，新增或调整缺字段验证场景。

## 迁移说明
实施顺序：
1. 更新验证策略，先定义失败信号。
2. 删除模板字段。
3. 删除模型中的 `done_criteria` 一等字段和包装属性。
4. 删除 `REQUIRED_STATUS_KEYS` 中的 `done_criteria`。
5. 更新测试夹具和断言。
6. 从本任务包 `task-info.yaml` 删除临时 `done_criteria`。

切换点：新模板不再生成三个字段，validate 不再要求 `done_criteria`。

回滚触发点：如果缺字段任务包无法进入正常 workflow，回退常量或修复校验逻辑后重测。

## 推荐图示
不需要图示。

## 详细设计反思
测试策略挑战：只检查模板不够，因为 `done_criteria` 的主要实际作用在校验常量里；必须运行 validate 相关测试。

接口边界挑战：删除模型字段看起来更彻底，但会把旧任务包兼容问题混进本轮，因此拒绝。

迁移假设挑战：当前任务包由旧模板创建，先临时保留 `done_criteria` 通过旧校验，待实现后删除。
