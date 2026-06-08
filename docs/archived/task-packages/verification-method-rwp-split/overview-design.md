# 总体设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 系统边界

本轮覆盖 OpenHarness 任务包验证配置的协议入口、CLI 数据模型、阶段指令、模板和测试。

覆盖面：

- `openharness_cli/models/verification_info.py`：验证配置的数据模型，负责读取和输出 `verification.method` 与 `verification.rwp`。
- `openharness_cli/models/task_package.py`：任务包对外暴露验证方法和 RWP 开关，供门禁、展示和模板渲染使用。
- `openharness_cli/workflows.py`、`openharness_cli/validate.py`、`openharness_cli/display.py`：消费验证配置的门禁、校验和阶段指令渲染上下文。
- `skills/using-openharness/references/templates/`：新任务包模板和验证文档模板。
- `skills/using-openharness/states/`：需求、验证策略、实现、验证执行阶段的说明。
- `tests/openharness_cases/`：覆盖新字段生成、门禁、校验和协议文档断言。

不覆盖面：

- 不改 `openharness rwp run`、`.harness/rwp/workflows/` 或运行时工作流脚本结构。
- 不提供旧 `verification.verify_by` 到新字段的自动迁移命令。
- 不批量迁移 `docs/archived/task-packages/` 下的历史任务包。
- 不把 TASK-023 的文档语义审核规则合并进本任务包；本轮只改验证配置模型。

## 推荐结构

推荐结构是把验证配置拆成两个独立问题：

```yaml
verification:
  method: <unit_test | qualitative>
  rwp:
    enabled: <true | false>
    reason: <启用或不启用的理由>
```

职责划分：

- `verification.method` 是主要验证方法，只表示最终验收主要依靠哪类判定机制。`unit_test` 覆盖可编程断言；`qualitative` 覆盖语义、协议、文档和设计判断。
- `verification.rwp.enabled` 是运行时证据开关，只表示本任务是否启用 RWP 作为额外运行时场景证据。
- `verification.rwp.reason` 是需求阶段的人类确认记录，启用和不启用都必须写理由。

模块依赖方向：

- `VerificationInfo` 负责解析和序列化新结构，不读取旧 `verify_by`。
- `TaskPackage` 提供 `verification_method`、`rwp_enabled`、`rwp_reason` 三个只读属性，避免上层直接解析 YAML。
- `workflows.py` 的需求门禁检查 `verification.method`、`verification.rwp.enabled`、`verification.rwp.reason` 是否已确认。
- `display.py` 把新字段传给 Jinja 模板，让阶段说明按 `verification_method` 与 `rwp_enabled` 分支渲染。
- 阶段指令只消费新字段，不再出现 `verify_by` 作为新任务包的协议入口。

## 关键流程

主路径：

1. 新任务包由 `task-package.task-info.yaml` 模板生成 `verification.method` 与 `verification.rwp` 占位符。
2. `proposing` 阶段向用户解释 `task_type`、`design_review_mode`、`verification.method`、`verification.rwp.enabled` 和 `verification.rwp.reason`，确认后写入 `task-info.yaml`。
3. `requirements_designed` 门禁检查 `method`、`rwp.enabled` 和 `rwp.reason`。任一缺失都阻塞推进。
4. `verification_designing` 阶段按 `method` 设计主要验证路径；如果 `rwp.enabled: true`，额外检查和选择 RWP，并把运行时工作流命令写进 `verification-design.md`。
5. `implementing` 阶段按 `method` 执行主要验证循环；如果启用 RWP，执行对应运行时工作流命令并记录中间结果。
6. `verifying` 阶段按 `method` 判定主要证据；如果启用 RWP，额外收集运行时观察、子 Agent 比对和人类确认。

关键失败信号：

- `verification.method` 缺失：需求阶段没有确认主要验证方法，门禁阻塞。
- `verification.rwp.enabled` 缺失：需求阶段没有确认是否启用运行时证据，门禁阻塞。
- `verification.rwp.reason` 缺失：启用或不启用没有人类确认理由，门禁阻塞。
- `verification.method: rwp`：新结构不支持，校验应报告未知方法。
- 阶段指令仍引用 `verify_by`：说明协议入口未清理干净，测试应失败。

已执行 `uv run openharness rwp list`，结果为 `No runtime workflow packages found.`。本任务已经确认 `rwp.enabled: false`，因此没有运行时验证缺口；这个结果只作为总体设计阶段的运行时能力检查记录。

## 阶段门禁

进入详细设计前必须满足：

- `verification.method` 是唯一主要验证方法字段，旧 `verification.verify_by` 不作为读取入口。
- `method` 的可选值只包含 `unit_test` 和 `qualitative`。
- RWP 只通过 `verification.rwp.enabled` 和 `verification.rwp.reason` 表达，不进入 `method` 枚举。
- 需求门禁必须阻止缺少 `method`、缺少 `rwp.enabled`、缺少 `rwp.reason` 的任务包进入后续阶段。
- 阶段指令和模板必须统一使用新字段名；如果保留 `verify_by`，只能作为历史反例或迁移说明出现，不能作为新任务包填写入口。
- 版本号必须按不兼容改造升级主版本号。

## 取舍

推荐方案的收益：

- 字段语义更稳定：`method` 表示主要验证方法，RWP 表示运行时证据开关。
- 避免长期双字段并存：旧 `verify_by` 不做兼容读取，减少后续任务包出现两套协议的风险。
- 更符合真实验证路径：单元测试、定性审核和 RWP 可以组合，而不是被单选枚举强行互斥。

代价：

- 这是不兼容改造，仍使用旧 `verify_by` 的活跃任务包会被新门禁视为未设置新字段。
- 需要同步修改 CLI、模板、阶段说明和测试，不能只改一个数据模型。
- 当前仓库已有 TASK-023 仍处于 `implementing` 且使用旧字段，后续继续推进时可能需要先按新结构更新它的 `task-info.yaml`。

被拒方案：保留 `verify_by` 并新增 `rwp.enabled`。

拒绝理由：这个方案能降低迁移成本，但会保留语义不准确的字段名。`verification.verify_by` 仍然不像“主要验证方法”，而且历史上它包含过 `rwp`，继续使用会让协作者误以为 RWP 仍可作为同维度选项。

被拒方案：新增 `verification.primary_method`。

拒绝理由：`primary_method` 语义更明确，但在 `verification` 作用域下显得重复。`verification.method` 已足够表达“验证方法”，也更易读。

## 推荐图示

本轮不需要图示。验证配置结构足够小，YAML 片段和模块职责表述已经能清楚表达边界。

## 反思

挑战：不兼容移除 `verify_by` 会不会过于激进？

结论：接受不兼容改造。用户已明确要求“不兼容读取”，并且本次问题的根源就是旧字段语义错误。如果为了平滑迁移继续双读，会把错误语义长期留在协议里，后续阶段说明和测试也必须继续处理旧分支，反而扩大维护成本。

挑战：RWP 是否应该完全从验证阶段说明中移除？

结论：拒绝。RWP 不应作为 `method` 的枚举值，但仍然是重要的运行时证据来源。正确做法是把它作为独立开关保留，并要求需求阶段启用或不启用都写明理由。
