# 需求

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 背景

OpenHarness 通过任务包驱动代码修改、设计决策和验证闭环。每个任务包的 `task-info.yaml` 当前使用 `verification.verify_by` 表示验证方式，可选值为 `unit_test`、`qualitative`、`rwp`。

这个字段会被需求阶段、验证策略设计阶段、验证执行阶段、任务包模板、CLI 数据模型和测试共同消费。现在的模型把单元测试、定性审核和运行时工作流包放在同一个单选维度里，已经影响后续协议表达。

## 问题陈述

`verify_by` 这个名字像是在问“由谁验证”，但实际值表达的是验证方法或验证载体。更大的问题是 `rwp` 与 `unit_test`、`qualitative` 不是同一层概念：单元测试和定性审核回答“主要如何判定结果”，RWP 回答“是否需要运行时场景证据”。

使用 OpenHarness 的 AI 协作者在需求阶段必须选择 `unit_test`、`qualitative` 或 `rwp` 之一。对于真实任务，RWP 往往只是运行时验证的可选证据来源：一个任务可以主要由单元测试判定，同时启用 RWP 观察端到端行为；也可以主要由定性审核判定，同时不启用 RWP。当前单选模型会迫使协作者把不同层级的判断混在一起。

这次改造需要现在完成，因为已有活跃协议正在强化文档验证和定性审核边界。如果继续保留 `verify_by: rwp` 这种表达，后续任务包会继续把“验证方法”和“运行时证据开关”混用，导致需求阶段确认、验证设计和 evidence 写回都不够清楚。

## 目标

完成后，OpenHarness 的任务包验证配置使用以下新结构：

```yaml
verification:
  method: <unit_test | qualitative>
  rwp:
    enabled: <true | false>
    reason: <启用或不启用的理由>
```

`verification.method` 表示主要验证方法。`verification.rwp.enabled` 表示是否启用运行时工作流证据，必须在需求阶段经过用户确认。新任务包不再生成、读取或推荐 `verification.verify_by`，也不再把 `rwp` 作为主要验证方法。

## 交付物

1. CLI 数据模型改造：`task-info.yaml` 的验证配置读取和输出改为 `verification.method` 与 `verification.rwp`；旧字段 `verification.verify_by` 不做兼容读取。
2. 任务包模板改造：新建任务包时生成新验证结构，不再出现 `verify_by` 占位符，也不再把 `rwp` 放进验证方法可选值。
3. 阶段指令改造：需求阶段必须解释并确认 `verification.method`、`verification.rwp.enabled` 和 `verification.rwp.reason`；验证策略设计和验证执行阶段按新字段消费配置。
4. RWP 语义改造：协议说明中明确 RWP 是可选运行时证据开关，不是和 `unit_test`、`qualitative` 并列的主要验证方法。
5. 测试改造：更新 YAML 生成、任务包流程和协议文档测试，断言新字段存在、旧字段不再作为新结构出现。
6. 版本号更新：由于本轮不兼容移除旧 `verify_by` 读取，提交前按项目要求提升 `pyproject.toml` 的主版本号。

## 非目标

- 不保留 `verification.verify_by` 的兼容读取，也不提供自动迁移旧任务包的命令。
- 不重写 RWP 的执行机制、工作流脚本目录结构或 `openharness rwp run` 的行为。
- 不新增第三种主要验证方法。`method` 本轮只支持 `unit_test` 和 `qualitative`。
- 不把所有历史归档任务包逐个迁移到新字段。历史归档只作为证据留存，不作为当前任务事实源。
- 不处理 TASK-023 的文档验证交接细节；本轮只处理验证配置模型。

## 约束

- 仓库内 Python 命令使用 `uv run ...`。
- 这是不兼容改造：如果为了兼容旧字段引入双读双写，就不再是本任务包。
- 新字段必须能被 CLI 模型、阶段模板和测试共同消费，不能只改文档说明。
- RWP 启用或不启用都必须有理由，不能让 Agent 静默默认选择。
- 本轮完成后需要一次聚焦提交，提交前必须更新 `pyproject.toml` 的版本号。

## 自检

提交前确认：

- [x] 不了解本轮对话的人，读完「背景」和「问题陈述」，能否知道当前需要做什么、为什么现在做？
- [x] 「目标」和「交付物」是否足够具体，不需要口头补充就能判断做完还是没做完？
- [x] 「非目标」是否写了具体的反例？
- [x] 「约束」是否写清了不可突破的边界？
