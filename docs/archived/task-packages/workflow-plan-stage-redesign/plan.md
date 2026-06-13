# 计划

## 实施步骤

- [x] 更新核心状态和文档模型
  - 修改对象：`openharness_cli/models/task_status.py`、`openharness_cli/models/task_package_document.py`
  - 完成条件：新增 `planning` / `planned`；计划文档为 `plan.md`；旧 `verification_designing` / `verification_designed` 和 `TaskPackageDocument.VERIFICATION_DESIGN` 不再作为新协议接口存在。
  - 验证方式：聚焦测试导入和 CLI 流转测试通过；`rg` 检查 live 源码无旧接口引用。

- [x] 重划三条工作流
  - 修改对象：`openharness_cli/workflows.py`、`openharness_cli/__init__.py`
  - 完成条件：`mechanical` 从需求直接到实现；`standard` 从需求到计划再实现；`structural` 经过总体设计、详细设计、计划再实现；`workflow_for()` 显式映射 `structural`。
  - 验证方式：`tests/openharness_cases/test_cli_workflows.py` 中三条 requirements gate 分流测试通过。

- [x] 更新 skill 指令和模板
  - 修改对象：`skills/using-openharness/states/planning/instructions.md`、`skills/using-openharness/states/implementing/instructions.md`、`skills/using-openharness/states/verifying/instructions.md`、`skills/using-openharness/references/templates/task-package.plan.md`、`skills/using-openharness/references/templates/task-package.task-info.yaml`
  - 完成条件：新协议入口使用 `planning` / `planned` 和 `plan.md`；implementing 和 verifying 消费 `plan.md`；旧 verification-designing 阶段目录和模板被删除。
  - 验证方式：协议文档测试通过；`rg` 检查 live skill 无旧阶段和旧文件引用。

- [x] 更新 RWP 相关说明
  - 修改对象：`openharness_cli/core/rwp.py`、`skills/using-openharness/references/` 下 RWP 参考文档和模板。
  - 完成条件：运行时工作流写回说明指向 `plan.md`，不再指向 `verification-design.md`。
  - 验证方式：`tests/openharness_cases/test_protocol_docs.py` 中 RWP 参考测试通过。

- [x] 更新测试夹具与断言
  - 修改对象：`tests/openharness_cases/test_cli_workflows.py`、`tests/openharness_cases/test_task_package_core.py`、`tests/openharness_cases/test_protocol_docs.py`、`tests/openharness_cases/test_yaml_quoting.py`
  - 完成条件：测试夹具使用 `task-package.plan.md`；活跃 state skill 目录断言使用 `planning`；创建任务包不会提前创建 `plan.md`；进入 `planning` 时创建 `plan.md`。
  - 验证方式：聚焦测试命令通过。

- [x] 迁移当前活跃任务包到新协议
  - 修改对象：`docs/task-packages/document-verification-and-qualitative-handoff/`、`docs/task-packages/workflow-plan-stage-redesign/`
  - 完成条件：现有活跃任务包不再依赖旧 `verification-design.md` 文件名；本任务进入 `planning` 并写出 `plan.md`。
  - 验证方式：`uv run openharness task-package list` 和 `uv run openharness task-package view` 能正常显示当前阶段。

- [ ] 完成验证和收尾
  - 修改对象：测试运行结果、`docs/task-packages/workflow-plan-stage-redesign/evidence.md`、`pyproject.toml`
  - 完成条件：聚焦测试和全量测试通过；证据写入 `evidence.md`；版本号按提交要求递增。
  - 验证方式：运行本文件 `## 验证设计` 中声明的命令。

## 验证设计

- **主要验证方式**：`unit_test`
- **必需命令**：
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_yaml_quoting.py -v`
  - `uv run pytest tests/ -v`
- **预期结果**：
  - 聚焦测试全部通过，覆盖三类 workflow 分流、任务包创建、模板锚点、协议文档引用。
  - 全量测试全部通过，证明新状态和新文档模型没有破坏其他 CLI 行为。
  - `rg -n "verification-design|verification_design|verification_designed|verification_designing|VERIFICATION_DESIGN" openharness_cli skills tests docs/task-packages -S` 的命中只允许出现在本任务包需求/设计文档中作为旧协议问题描述，不允许出现在 live 源码、live skill 或测试断言中。
- **边界或错误场景**：
  - `mechanical` 在 requirements gate 后不得创建 `plan.md`。
  - `standard` 在 requirements gate 后必须进入 `planning`，不得进入 overview/detailed。
  - `structural` 在 requirements gate 后必须先进入 `overview_designing`，不得直接进入 `planning`。
  - 当前活跃任务包必须能被 `openharness task-package list` 和 `view` 正常读取。

## 完成判定

- **进入实现的条件**：需求、总体设计、详细设计和本计划已写入任务包；核心阶段语言已经确认使用 `planning` / `planned` 和 `plan.md`。
- **实现完成的条件**：核心代码、skill 指令、模板、测试和活跃任务包迁移完成；聚焦测试通过；`evidence.md` 记录中间事实。
- **验证完成的条件**：全量测试通过；旧协议名检查符合预期；`evidence.md` 写明验证结果、变更文件和残余风险。

## 风险接受

- 历史归档任务包不批量迁移，仍可能包含旧 `verification-design.md` 和旧状态名。接受理由：它们是静态历史证据，不作为当前 CLI 新协议的运行路径。
- 本轮不实现自动迁移命令。接受理由：用户明确要求不做旧协议兼容，活跃任务包在本轮已手工迁移；自动迁移可在未来有需要时单独设计。
