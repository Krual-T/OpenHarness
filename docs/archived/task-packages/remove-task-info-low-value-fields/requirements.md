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
从当前任务包 `task-info.yaml` 模板和 CLI 必填 schema 中删除低价值字段 `done_criteria`、`depends_on`、`scope.areas`，让新建任务包元数据只保留当前流程实际消费的字段。

单一成功指标：新建任务包模板不再包含这三个字段，且缺少 `done_criteria` 的任务包不再被 `validate_task_package` 判为缺失必填项。

## 问题陈述
目标用户是维护 OpenHarness 任务包协议和创建流程的协作者。核心场景是运行 `openharness task-package new` 创建任务包，以及维护者阅读 `task-info.yaml` 判断哪些字段必须填写。

当前模板包含 `done_criteria`、`depends_on`、`scope.areas`，但其中 `depends_on` 和 `scope.areas` 没有被 CLI 显式消费；`done_criteria` 只作为必填校验存在，没有参与阶段门禁、归档或验证执行。它们增加了填写负担，也会误导维护者以为这些字段具有更强执行语义。

## 必须交付的结果
1. 删除模板字段：
   - 验收标准：`skills/using-openharness/references/templates/task-package.task-info.yaml` 中不再出现 `done_criteria`、`depends_on`、`scope` 或 `areas`。
2. 删除 `done_criteria` 必填校验：
   - 验收标准：`openharness_cli/constants.py` 的 `REQUIRED_STATUS_KEYS` 不再包含 `done_criteria`。
3. 保持旧任务包读取兼容：
   - 验收标准：已有包含这些字段的任务包仍能被 `TaskInfo.from_dict` 读取，旧字段作为 `_extra` 保留，不要求历史归档任务包批量迁移。
4. 更新测试：
   - 验收标准：相关测试夹具不再为了通过校验而写入 `done_criteria`，并新增或调整测试覆盖缺少 `done_criteria` 时验证通过的行为。

## 非目标
- 不批量改写 `docs/archived/task-packages/` 中历史任务包的 `task-info.yaml`。
- 不批量改写旧任务包中已经存在的这些字段。
- Counterexample：为 `depends_on` 增加依赖排序能力，虽然与字段相关，但属于新增功能，不属于本轮删除。

## 约束
- 协议边界：新模板和新校验不再要求这三个字段。
- 兼容性约束：历史任务包包含这些字段时不应导致读取失败。
- 依赖限制：不新增依赖。
- Cost cap：一次模板/schema/test 精简，一轮聚焦测试和一次提交。
- 如果要设计新的依赖管理或 scope 展示能力，就不再是本任务包范围。
