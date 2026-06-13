# 详细设计

## 可观察性与验证准备

主验证路径：

1. 先更新或新增单元测试，锁住三条工作流的状态序列、自动跳转、工作文件和必需章节。
2. 再更新协议文档测试，锁住 skill 指令和模板中的 `planning` / `planned` / `plan.md` 表达，防止旧 `verification_designing` 和 `verification-design.md` 回流到新协议主路径。
3. 实现后运行聚焦测试：
   - `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_protocol_docs.py -v`
4. 最后运行全量测试：
   - `uv run pytest tests/ -v`

降级路径：

- 如果协议文档语义无法用稳定字符串断言完整覆盖，`plan.md` 的章节锚点、状态名、文件名和旧名禁用点用单元测试覆盖；“是否像人话、是否便于执行”的判断保留给后续计划阶段的定性审核清单。
- 如果全量测试暴露大量历史归档旧名，本轮不为归档提供兼容。测试应只约束当前协议入口、当前模板、当前状态机和活跃任务处理，不把归档旧文件当作新协议失败。

预期证据：

- 测试能证明 `mechanical` 不经过计划阶段，`standard` 经过 `planning` 但不经过 overview/detailed，`structural` 经过 overview/detailed 后进入 `planning`。
- 测试能证明新建任务包不创建 `plan.md` 之外的计划文件，进入 `planning` 时创建 `plan.md`。
- 测试能证明 `TaskPackageDocument`、阶段指令、模板和 implementing/verifying 消费路径不再引用旧 `verification-design.md` 作为新协议文件。
- `evidence.md` 最终记录测试命令、退出码、覆盖范围和残余风险。

## 新增或修改文件

CLI 与模型：

- `openharness_cli/models/task_status.py`：新增 `PLANNING = ("planning", "skills/using-openharness/states/planning/instructions.md")` 和 `PLANNED = ("planned", "")`；移除或停止使用 `VERIFICATION_DESIGNING` / `VERIFICATION_DESIGNED`。
- `openharness_cli/models/task_package_document.py`：用 `PLAN = ("plan.md", False, (...))` 替换 `VERIFICATION_DESIGN = ("verification-design.md", False, (...))` 的新协议职责；章节要求改为计划文档所需锚点。
- `openharness_cli/workflows.py`：拆出 `MECHANICAL_WORKFLOW`、`STANDARD_WORKFLOW`、`STRUCTURAL_WORKFLOW` 三条真实工作流；更新描述、next step、文件添加、工作文件和 `workflow_for()`。
- `openharness_cli/__init__.py`：导出 `STRUCTURAL_WORKFLOW`，并移除不再存在的旧导出引用。
- `openharness_cli/core/rwp.py`：把文档职责说明中的 `verification-design.md` 改为 `plan.md`。

skill 指令与模板：

- `skills/using-openharness/states/proposing/instructions.md`：更新 `task_type` 分流说明。`mechanical` 不启用计划和两阶段设计；`standard` 启用计划；`structural` 启用总体设计、详细设计和计划。
- `skills/using-openharness/states/planning/instructions.md`：由当前 `verification-designing/instructions.md` 重写而来，职责改为计划设计，要求写 `plan.md`，包含实施步骤、验证设计、完成判定和风险接受。
- `skills/using-openharness/states/verification-designing/instructions.md`：删除或不再作为当前状态 hook 使用。若文件保留在仓库中，会误导协议；推荐删除目录。
- `skills/using-openharness/states/implementing/instructions.md`：入口从 `planned` 进入；所有 `verification-design.md` 引用改为 `plan.md`；执行循环按 `plan.md` 的子任务和验证清单推进。
- `skills/using-openharness/states/verifying/instructions.md`：所有验证命令、审核矩阵和预期结果来源改为 `plan.md`。
- `skills/using-openharness/references/templates/task-package.plan.md`：新增计划模板。
- `skills/using-openharness/references/templates/task-package.verification-design.md`：删除。新协议不再生成该模板。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：更新注释里的三条状态流，使用 `planning` / `planned`。

测试：

- `tests/openharness_cases/test_cli_workflows.py`：新增或更新状态流转测试，覆盖 `requirements_designed` 对三类 `task_type` 的自动跳转；更新旧 `VERIFICATION_DESIGN` 断言为 `PLAN`。
- `tests/openharness_cases/test_task_package_core.py`：更新模板最小仓库、`ALL_DESIGN_FILES` 预期、创建任务包断言和 vendored state 目录断言。
- `tests/openharness_cases/test_protocol_docs.py`：更新模板与阶段指令锚点，禁止当前协议继续要求 `verification-design.md`。
- `tests/openharness_cases/test_yaml_quoting.py`：更新测试模板文件列表。

任务包自身：

- `docs/task-packages/workflow-plan-stage-redesign/task-info.yaml`：本任务当前正在旧流程中运行，实施硬切换前需要把当前任务包状态迁移到新状态序列。详细做法在 `## 迁移说明` 中定义。
- `docs/task-packages/workflow-plan-stage-redesign/plan.md`：进入计划阶段后创建，不在详细设计阶段提前写。

## 接口

### `TaskStatus`

新状态值：

```python
class TaskStatus(StrEnum):
    PLANNING = ("planning", "skills/using-openharness/states/planning/instructions.md")
    PLANNED = ("planned", "")
```

接口语义：

- `TaskStatus.value` 是写入 `task-info.yaml.status` 的稳定协议值。
- `TaskStatus.hook` 是 CLI 在 `view`、`list` 或 `transition` 输出中注入阶段指令的路径。
- 新协议不接受 `verification_designing` 或 `verification_designed` 作为有效当前状态。`parse_status()` 对旧值返回 `None` 或无法映射到当前 workflow，`validate_task_package()` 报 unknown status。

误用风险：

- 如果只新增 `PLANNING` 但保留 workflow 对旧状态的引用，CLI 仍会把旧状态当成合法路径。
- 如果保留旧 enum 成员但“不使用”，测试和外部调用仍可能继续依赖它，硬切换不彻底。

推荐：移除旧 enum 成员，并修正所有引用点。历史归档如果包含旧状态，校验时按旧协议无效处理；归档发现与列表展示若因此报错，说明仍有旧协议输入进入当前 CLI，需要由维护者迁移或排除，不在代码里兼容。

### `TaskPackageDocument`

新文档条目：

```python
PLAN = ("plan.md", False, (
    "## 实施步骤",
    "## 验证设计",
    "## 完成判定",
    "## 风险接受",
))
```

章节语义：

- `## 实施步骤`：可勾选子任务；每个子任务要说明修改对象和完成条件。
- `## 验证设计`：验证方法、必需命令或审核矩阵、预期结果、边界场景。
- `## 完成判定`：实现阶段和验证阶段如何判断可以 transition。
- `## 风险接受`：本轮不覆盖的边界、接受理由和后续触发条件。

接口约束：

- `Workflow.required_files()`、`scaffold_files()` 和 `section_requirements()` 继续通过 `TaskPackageDocument` 计算文件与章节，不新增并行的文档规则系统。
- 模板文件名必须与 `TaskPackageDocument.value` 对齐，即 `task-package.plan.md`。

### `workflow_for(task_type)`

新映射：

```python
def workflow_for(task_type):
    if task_type == TaskType.MECHANICAL:
        return MECHANICAL_WORKFLOW
    if task_type == TaskType.STRUCTURAL:
        return STRUCTURAL_WORKFLOW
    return STANDARD_WORKFLOW
```

接口语义：

- `None` 仍返回 `STANDARD_WORKFLOW`，用于新建任务包时只创建 `task-info.yaml` 和 `requirements.md`。
- 字符串输入继续支持已有调用方式，但只接受当前 `TaskType` 的值。
- `structural` 必须有独立 workflow，不能再落到 standard。

误用风险：

- 若 `None` 默认返回 structural，新建任务包会提前创建设计文件。
- 若未知字符串默默返回 standard，错误配置可能被隐藏。实现阶段可继续保持当前行为或收紧为 standard fallback；本轮重点是有效 `TaskType.STRUCTURAL` 必须显式映射。

## 模块内部设计

状态机编排落在 `workflows.py`：

- `DESCRIPTIONS` 增加 `PLANNING` 和 `PLANNED` 描述，移除旧 verification design 描述。
- `STANDARD_NEXT_STEPS` 改为 requirements gate 后进入 `planning`。
- `MECHANICAL_NEXT_STEPS` 改为 requirements gate 后进入 `implementing`。
- 新增 `STRUCTURAL_NEXT_STEPS`，沿用 overview/detailed 后进入 `planning`。
- 三个 Workflow 的 `gate_next` 分别表达自动跳转，不在 transition 命令里写 if/else 特例。
- `ACTIVE_STATUSES` 和 `GATE_STATUSES` 由三条 workflow 合并计算。

文件和章节校验落在 `TaskPackageDocument` 与 `Workflow.section_requirements()`：

- `PLAN` 只在 `STANDARD_WORKFLOW` 和 `STRUCTURAL_WORKFLOW` 的 `PLANNED` 文件添加中出现。
- `MECHANICAL_WORKFLOW` 的 `file_additions` 不包含 `PLAN`、`OVERVIEW_DESIGN`、`DETAILED_DESIGN`。
- `STRUCTURAL_WORKFLOW` 的章节累计顺序是 requirements、overview、detailed、plan、evidence。
- `STANDARD_WORKFLOW` 的章节累计顺序是 requirements、plan、evidence。

模板创建落在 `core/task_packages.py`：

- `create_task_package()` 仍用 `workflow_for(None).scaffold_files(proposing)`，因此只创建 `task-info.yaml` 和 `requirements.md`。
- `ensure_task_package_stage_files()` 在进入 `planning` 后根据当前 workflow 创建 `plan.md`。
- 删除旧模板后，任何仍请求 `TaskPackageDocument.VERIFICATION_DESIGN` 的代码会在测试中暴露为 import/attribute error。

阶段指令消费关系：

- `planning/instructions.md` 消费 `requirements.md`；如果是 structural，还消费 `overview-design.md` 和 `detailed-design.md`。
- `implementing/instructions.md` 消费 `plan.md`，执行其中子任务和验证设计。
- `verifying/instructions.md` 消费 `plan.md`，执行最终验证清单或定性审核矩阵，把结果写入 `evidence.md`。

## 数据语义

状态转换：

```text
mechanical:
proposing -> requirements_designed -> implementing -> implemented -> verifying -> verified -> archived

standard:
proposing -> requirements_designed -> planning -> planned -> implementing -> implemented -> verifying -> verified -> archived

structural:
proposing -> requirements_designed -> overview_designing -> overview_designed -> detailed_designing -> detailed_designed -> planning -> planned -> implementing -> implemented -> verifying -> verified -> archived
```

文档产生规则：

| task_type | proposing | requirements_designed 后 | planned 后 | verified 后 |
|-----------|-----------|--------------------------|-------------|-------------|
| mechanical | `task-info.yaml`, `requirements.md` | 无新增，进入 `implementing` | 不适用 | `evidence.md` |
| standard | `task-info.yaml`, `requirements.md` | `plan.md` | `plan.md` 必须有计划章节 | `evidence.md` |
| structural | `task-info.yaml`, `requirements.md` | `overview-design.md`，随后 `detailed-design.md`，随后 `plan.md` | `plan.md` 必须有计划章节 | `evidence.md` |

一致性约束：

- `TaskStatus` 的状态值、`Workflow.status_sequence`、`Workflow.gate_next`、阶段 hook 路径和 `task-info.yaml` 模板注释必须使用同一套状态语言。
- `TaskPackageDocument.PLAN.value`、模板文件名、指令引用、implementing/verifying 消费路径必须使用同一文件名。
- `verification.method` 仍保留在 `task-info.yaml`，它表示主要验证方式，不再暗示有独立 verification design 阶段。

## 阶段门禁

进入实施前必须满足：

1. `TaskStatus`、`TaskPackageDocument` 和 `workflows.py` 的接口设计已闭合，旧 `verification_designing` / `verification_designed` / `verification-design.md` 不在新主路径中。
2. 三条 workflow 的状态序列和文档产生规则已在详细设计中明确。
3. `plan.md` 的章节语义能同时服务 `standard` 和 `structural`。
4. skill 指令改动范围已列清，尤其是 implementing/verifying 必须改为消费 `plan.md`。
5. 测试覆盖点已列清，能在实现阶段先写或先更新测试。
6. 当前活跃任务包硬切换策略已明确：不兼容旧状态，必要时手工迁移当前任务包。

## 决策闭合

- 接受：删除/替换旧 `verification_designing` / `verification_designed` 状态，而不是保留但不使用。理由是保留旧 enum 会让外部调用和测试继续把旧状态当合法协议，违背硬切换。
- 接受：用 `plan.md` 同时承载实施步骤和验证设计。理由是计划需要直接服务执行，验证设计如果独立存在，会再次把“怎么验”和“怎么做”拆散。
- 接受：新增 `STRUCTURAL_WORKFLOW`，不再让 structural 复用 standard。理由是新 standard 不经过两阶段设计，structural 必须保留完整设计路径。
- 拒绝：为旧活跃任务包提供自动兼容迁移。理由是用户明确要求现有活跃也不兼容；兼容分支会继续污染新协议。
- 延期：是否把旧归档文件批量改名为 `plan.md`。触发条件是未来需要对归档任务包重新执行当前 CLI 校验；本轮只保证新协议不依赖旧归档。

## 错误处理

主要失败路径：

- 旧状态进入当前 CLI：`parse_status()` 无法解析或 `validate_task_package()` 报 unknown status。处理方式是停止流程，由维护者迁移任务包状态；不在 workflow 中回退到旧状态。
- 模板缺失：进入 `planning` 时如果 `task-package.plan.md` 不存在，`ensure_task_package_stage_files()` 抛 `FileNotFoundError`。这是发布包缺模板，应修复模板或安装包，不静默跳过。
- 文档章节缺失：`validate_task_package()` 在 `planned` 或后续状态报告 `plan.md` 对应章节缺非占位内容。
- 指令引用旧文件：协议文档测试失败，指出仍有当前 skill 指令引用 `verification-design.md`。
- 三类分流错误：状态流转测试失败，指出实际 next stage 不符合 task_type。

静默出错风险：

- 最大风险是只改 CLI 状态机，但 implementing/verifying 仍读 `verification-design.md`。这会让流程表面进入 `planning`，实际执行仍靠旧文档。防护方式是协议文档测试扫描当前指令中的旧文件引用，并在实施测试中检查 `TaskPackageDocument.PLAN` 是计划阶段工作文件。

异常传播：

- 配置或模板错误继续通过现有异常和 CLI 非零退出暴露。
- 校验错误继续通过 `validate_task_package()` 返回字符串列表暴露。
- 状态未知错误通过 `validate_task_package()` 和 transition 命令暴露，不做兼容吞掉。

## 迁移说明

实施顺序：

1. 更新测试期望和最小模板夹具，引入 `PLAN`、`planning`、`planned` 和三条 workflow 的断言。
2. 更新 `TaskStatus` 与 `TaskPackageDocument`。
3. 更新 `workflows.py`，新增 `STRUCTURAL_WORKFLOW` 并改三条状态流。
4. 新增 `planning` 阶段指令和 `task-package.plan.md` 模板，删除旧 verification-designing 指令和模板。
5. 更新 proposing、implementing、verifying、RWP 说明和 task-info 模板中的旧引用。
6. 迁移当前任务包：本任务在完成 detailed 后，后续阶段应使用新 `planning` / `planned` 与 `plan.md`；如果 CLI 硬切换后当前 `task-info.yaml.status` 仍是旧状态，手工改到新状态序列中的对应阶段。
7. 运行聚焦测试和全量测试。

切换点：

- `TaskStatus` 和 `workflows.py` 合入后，新 CLI 即不再识别旧 `verification_designing` / `verification_designed` 为当前协议状态。
- `TaskPackageDocument.PLAN` 合入后，新计划阶段只创建和校验 `plan.md`。

回滚触发点：

- 新建任务包无法进入 proposing 或 requirements gate，说明基础状态机破坏，应回滚 `workflows.py` 和 `TaskStatus` 的改动重新设计。
- `standard` 仍进入 overview/detailed 或 `mechanical` 仍进入 planning，说明分流设计实现错误，应回滚 workflow 分流改动。
- implementing/verifying 无法找到计划来源，说明指令和文档模型未同步，应回滚或补齐 `plan.md` 消费路径。

兼容策略：

- 无运行时兼容策略。旧活跃任务包必须迁移或重建；历史归档只作为静态证据保留，不保证通过当前 CLI 校验。

## 推荐图示

实施前建议在 `plan.md` 中补一张三类 workflow 对照表，而不是在源码中加入图。源码侧保持枚举和 workflow 数据结构即可。

如需辅助理解，可在 README 或协议文档后续任务中补文档职责图：

```text
requirements.md
  ├─ mechanical -> implementing -> evidence.md
  ├─ standard -> plan.md -> implementing -> evidence.md
  └─ structural -> overview-design.md -> detailed-design.md -> plan.md -> implementing -> evidence.md
```

## 反思

本设计最大的实现风险不是状态机本身，而是旧词散落在模板、测试和阶段指令里。只改 Python 代码会得到一个表面新、执行仍旧的协议。

因此实现必须把“旧名清除”当成验证对象之一：当前协议入口、模板和 live skill 指令中不应继续把 `verification-design.md` 作为计划来源。历史归档可以保留旧事实，但不能反过来要求新 CLI 兼容旧协议。

另一个风险是 `mechanical` 跳过 `plan.md` 后没有显式验证设计。这个风险可接受，因为 `mechanical` 的前提就是执行路径和验证方式能从需求直接推出；若需要拆验证步骤，就不应分类为 `mechanical`，而应升为 `standard`。
