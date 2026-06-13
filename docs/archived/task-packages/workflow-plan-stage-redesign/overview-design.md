# 总体设计

## 系统边界

本轮覆盖 OpenHarness 任务包工作流的四个表面：

1. **CLI 工作流定义**：`openharness_cli/workflows.py` 中三类任务的状态序列、门禁跳转、自动创建文件、当前阶段工作文件、阶段描述和下一步提示。
2. **任务包文档模型**：`openharness_cli/models/task_package_document.py` 中任务包文档枚举、文件名和章节要求。
3. **skill 阶段指令与模板**：`skills/using-openharness/states/` 下的 proposing、overview、detailed、verification/plan、implementing、verifying 指令，以及 `skills/using-openharness/references/templates/` 下对应模板。
4. **回归测试**：`tests/openharness_cases/` 中覆盖任务包创建、状态流转、文档章节校验和协议文档锚点的测试。

本轮不覆盖以下表面：

- 不为 `docs/archived/` 下的历史任务包提供旧协议兼容逻辑。历史文件可以作为静态证据保留，但 CLI、skill 和测试不继续支持旧阶段作为当前协议。
- 不实现 OpenSpec 兼容层，不把任务包格式改成 `proposal.md`、`design.md`、`tasks.md`。
- 不引入 Superpowers 式子 Agent 调度系统。`plan.md` 可以借鉴可勾选子任务和分步验证表达，但不新增调度引擎。
- 不删除总体设计和详细设计。它们从默认 standard 路径中移出，但仍是 `structural` 任务的必要设计阶段。

## 推荐结构

推荐结构是“一个统一计划阶段，三条任务复杂度工作流”。计划阶段应在语言上完整成立：状态名、阶段说明、模板、工作文件和后续消费方都使用 `planning` / `planned` 与 `plan.md`，不再把旧的 `verification_designing` 包装成计划阶段。

任务类型边界：

- `mechanical`：需求收敛后直接进入实现，再进入验证和归档。它不创建 `plan.md`，也不创建 `overview-design.md` 或 `detailed-design.md`。适用条件是改动判断成本低、执行步骤可以由需求直接推出、失败验证方式明确、通常不跨模块。
- `standard`：需求收敛后进入计划阶段，再进入实现、验证和归档。它创建 `plan.md`，但不默认创建总体设计和详细设计。适用条件是需要拆实施步骤或分步验证，但不需要先设计模块结构、接口边界或状态模型。
- `structural`：需求收敛后进入总体设计、详细设计、计划、实现、验证和归档。适用条件是任务涉及模块复杂性、跨模块边界、长期协议、公共接口、状态或数据语义，需要先从整体到局部设计。

文档职责边界：

- `requirements.md` 回答“为什么做、做完什么事实成立、边界在哪里”。
- `overview-design.md` 只在 `structural` 中出现，回答“系统如何拆分、模块责任和主流程如何组织、哪些架构约束会影响后续实现”。
- `detailed-design.md` 只在 `structural` 中出现，回答“关键部件如何落地、接口和数据语义如何精确、错误与迁移如何处理”。
- `plan.md` 在 `standard` 和 `structural` 中出现，回答“按什么顺序做、每个子任务怎么验、最终怎么判定完成”。它消费需求和设计结论，不重新做结构设计。
- `evidence.md` 回答“实际执行了什么、结果是什么、剩余风险是什么”。

实现层新增 `TaskStatus.PLANNING` / `planning` 和 `TaskStatus.PLANNED` / `planned`，替换当前工作流中的 `verification_designing` / `verification_designed`。本轮不做“旧状态名内部保留、新阶段名外部展示”的兼容折中，因为这会让协议继续残留旧语义，后续读者也会困惑为什么计划阶段仍叫 verification design。

迁移策略是硬切换：当前 CLI 新建、流转、提示和校验只支持 `plan.md` 与 `planning` / `planned`。本轮不为旧 `verification_designing` / `verification_designed` 状态或旧 `verification-design.md` 文件提供兼容读取。现有活跃任务包如果仍停在旧状态，必须迁移为新协议状态与文件，或者由维护者按新协议重建任务包；它们不作为本轮实现需要兼容的运行时路径。

模块责任：

- `TaskPackageDocument` 用 `PLAN = "plan.md"` 替换 `VERIFICATION_DESIGN = "verification-design.md"` 在新工作流中的职责，章节要求围绕实施步骤、验证设计和完成判定。
- `workflows.py` 增加独立的 `STRUCTURAL_WORKFLOW`，并把 `workflow_for(TaskType.STRUCTURAL)` 显式映射到 structural；`TaskType.STANDARD` 映射到 standard；`TaskType.MECHANICAL` 映射到 mechanical。
- `STANDARD_WORKFLOW` 改为 `requirements -> plan -> implement -> verify -> archive`。
- `MECHANICAL_WORKFLOW` 改为 `requirements -> implement -> verify -> archive`，不再进入计划阶段。
- `STRUCTURAL_WORKFLOW` 使用现有 overview、detailed 阶段后进入计划阶段。
- `TaskStatus` 新增 `PLANNING` / `PLANNED`，并移除新工作流对 `VERIFICATION_DESIGNING` / `VERIFICATION_DESIGNED` 的依赖。
- 阶段指令负责解释何时进入对应阶段，模板负责给文档提供稳定章节，测试负责防止 CLI 和 skill 再次分叉。

## 关键流程

主状态流：

```text
mechanical:
proposing -> requirements_designed -> implementing -> implemented -> verifying -> verified -> archived

standard:
proposing -> requirements_designed -> planning -> planned -> implementing -> implemented -> verifying -> verified -> archived

structural:
proposing -> requirements_designed -> overview_designing -> overview_designed -> detailed_designing -> detailed_designed -> planning -> planned -> implementing -> implemented -> verifying -> verified -> archived
```

任务创建和流转的信息流：

1. `proposing` 阶段确认 `collaboration.task_type`。
2. `workflow_for()` 根据 `task_type` 选择三条实际工作流之一。
3. `transition requirements_designed` 通过需求门禁后，CLI 自动跳到对应任务类型的下一个活跃阶段。
4. 进入计划阶段时，CLI 创建或要求 `plan.md`；进入实现阶段时，implementing 指令消费 `plan.md` 中的子任务和验证设计。
5. 进入 verifying 阶段时，verifying 指令根据 `plan.md` 的最终验证清单执行或审核，并把实际结果写入 `evidence.md`。

关键失败信号：

- `standard` 仍自动进入 `overview_designing`，说明工作流分流未改干净。
- `mechanical` 仍进入计划或验证设计阶段，说明“低判断成本任务”仍被额外门禁拖住。
- `structural` 被映射到 standard，说明复杂任务丢失总体设计和详细设计。
- CLI 工作文件变成 `plan.md`，但模型仍要求 `verification-design.md` 的章节，说明文档模型与工作流不一致。
- implementing/verifying 指令仍只引用 `verification-design.md`，说明计划阶段无法真正被消费。
- 新任务包仍出现 `verification_designing` / `verification_designed` 状态，说明旧阶段语言没有真正移除。

## 阶段门禁

进入详细设计前，以下设计条件必须成立：

1. **三类任务分流可判定**：
   - `mechanical` 的判定标准是执行路径短、改动局部、无需跨模块协调、无需单独拆执行步骤。典型例子是修正拼写、改一个明确配置、调整单个测试期望或替换一个稳定命名。
   - `standard` 的判定标准是需要计划，但不需要结构设计。任务可能涉及多个文件或多个步骤，但模块边界、接口方向和状态语义都已存在，不需要重新拆系统结构。
   - `structural` 的判定标准是需要从整体到局部设计。只要任务改变长期协议、公共接口、模块责任、跨模块依赖、状态模型、数据语义或迁移策略，就应进入总体设计和详细设计。
2. **计划阶段职责闭合**：`plan.md` 必须能承接 `standard` 和 `structural` 的执行，至少包含可勾选子任务、每个子任务的验证方式、最终验证清单、风险接受和完成判定。
3. **两阶段设计职责收窄**：`overview-design.md` 和 `detailed-design.md` 只为 `structural` 服务。它们不承担普通任务的执行清单职责，也不替代 `plan.md`。
4. **状态语言一致**：新协议中的状态、说明、模板、测试和指令必须使用 `planning` / `planned` 与 `plan.md`。旧的 `verification_designing` / `verification_designed` / `verification-design.md` 不能出现在新任务包主路径中。
5. **硬切换边界明确**：新 CLI 不兼容旧 `verification_designing` / `verification_designed` 状态和旧 `verification-design.md` 文件。历史归档只作为静态文本保留；活跃任务包必须迁移或重建，不进入兼容路径。
6. **RWP 缺口已记录**：本地执行 `uv run openharness rwp list` 的结果是无可用运行时工作流包。本轮验证依赖单元测试、CLI 流转测试和定性文档审阅，不依赖 RWP。

## 取舍

推荐方案：完整引入 `planning` / `planned` 和 `plan.md`，并重划三类工作流。

收益：

- 阶段语言更像人话。计划阶段就叫计划，不再用“验证设计”承载实施步骤。
- `standard` 不再被迫写总体设计和详细设计，普通任务的文档负担下降。
- `structural` 仍保留从整体到局部设计，避免把复杂模块任务压成简单 checklist。
- `plan.md` 把实施步骤和验证设计放在一起，能直接服务 implementing 和 verifying 阶段。

代价：

- 实现面比只改提示词更大，需要同步改状态枚举、工作流、模板、模型、阶段指令和测试。
- 旧的 `verification-design.md` 名称会退出新协议，当前活跃任务包如果使用旧状态或旧文件，需要迁移或重建。
- 测试更新面会扩大，尤其是依赖 `TaskPackageDocument.VERIFICATION_DESIGN` 和 `verification_designing` 的断言。

备选方案 A：只新增 `plan.md`，但保留 `verification_designing` 内部状态名。

拒绝理由：这个方案实现成本较低，但协议语言仍然分裂。使用者会看到计划阶段背后仍叫 verification design，智能体也容易继续把计划写成验证策略，无法解决“文档不像人话”的核心问题。

备选方案 B：完全采用 OpenSpec 风格，把任务包改成 `proposal.md`、`design.md`、`tasks.md`。

拒绝理由：OpenSpec 的 `tasks.md` 对本轮有启发，但完整换格式会把任务扩大成协议重构和迁移工程。OpenHarness 已有任务包状态机、skill 阶段指令和归档证据格式，本轮应保留这些资产，只调整阶段职责和计划表达。

备选方案 C：删除总体设计和详细设计，只保留 `plan.md`。

拒绝理由：这会过度简化。用户已明确指出总体设计和详细设计不是只有方案取舍才出现，模块复杂时仍需要从大到小设计。删除两阶段设计会让 `structural` 任务失去系统分解和局部机制设计的承载位置。

## 推荐图示

详细设计阶段建议补一张工作流对照图，展示三类任务从 `proposing` 到 `archived` 的状态序列，并标出每条路径会产生哪些文档。

建议补一张文档职责图，展示：

```text
requirements.md -> overview-design.md -> detailed-design.md -> plan.md -> evidence.md
                 \                         ^
                  \---- standard ----------/
```

图示要表达两个关键点：`standard` 从需求直接进入计划；`structural` 先经过总体设计和详细设计，再进入计划。`mechanical` 不进入计划，直接实现和验证。

## 反思

最初可选的低成本方向是保留 `verification_designing` 作为内部状态，只把外部文档改成 `plan.md`。这个方向能减少枚举和测试迁移，但用户反馈指出它“不够有语言”，也就是协议概念本身仍然不自然。

该挑战成立。OpenHarness 当前的问题不只是文件名不对，而是阶段语言让智能体以通过旧门禁为目标。若继续保留 `verification_designing`，新协议会从第一天开始背负旧语义，后续所有指令都要解释“这里虽然叫验证设计，但其实是计划”。这正是本轮要消除的形式主义。

结论：接受更大的实现面，完整引入 `planning` / `planned` 和 `plan.md`；拒绝内部旧名外部新名的折中方案，也拒绝为旧活跃任务包保留兼容路径。迁移风险通过硬切换后的状态一致性、必要的任务包手工迁移和测试控制，而不是通过保留旧概念控制。
