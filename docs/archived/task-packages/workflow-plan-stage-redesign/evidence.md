# 证据

## 验证结果

- **method**: unit_test
- **rwp_enabled**: false
- **Result**: passed

## 变更文件

- `openharness_cli/models/task_status.py` — 新增 `planning` / `planned` 状态，移除新协议对旧 verification design 状态的依赖。
- `openharness_cli/models/task_package_document.py` — 新增 `TaskPackageDocument.PLAN`，用 `plan.md` 承载计划阶段文档要求。
- `openharness_cli/workflows.py` — 重划 `mechanical`、`standard`、`structural` 三条工作流，新增 `STRUCTURAL_WORKFLOW`。
- `openharness_cli/__init__.py` — 导出 `STRUCTURAL_WORKFLOW`。
- `openharness_cli/core/rwp.py` — 将运行时工作流写回说明改为 `plan.md`。
- `skills/using-openharness/states/planning/instructions.md` — 新增计划阶段指令。
- `skills/using-openharness/states/verification-designing/instructions.md` — 删除旧验证设计阶段指令。
- `skills/using-openharness/states/implementing/instructions.md` — 改为从 `planned` 进入并消费 `plan.md`。
- `skills/using-openharness/states/verifying/instructions.md` — 改为从 `plan.md` 读取验证命令和审核矩阵。
- `skills/using-openharness/states/proposing/instructions.md` — 更新三类任务启用条件。
- `skills/using-openharness/states/detailed-design/instructions.md` — 将后续证据来源改为 `plan.md`。
- `skills/using-openharness/SKILL.md` — 将阶段完成表更新为 `planning` -> `planned`。
- `skills/using-openharness/references/templates/task-package.plan.md` — 新增计划模板。
- `skills/using-openharness/references/templates/task-package.verification-design.md` — 删除旧验证设计模板。
- `skills/using-openharness/references/templates/task-package.task-info.yaml` — 更新三类 workflow 注释。
- `skills/using-openharness/references/` 下 RWP 相关文档 — 将计划和写回文件改为 `plan.md`。
- `tests/openharness_cases/test_cli_workflows.py` — 增加三类 workflow 分流测试并更新旧文档断言。
- `tests/openharness_cases/test_task_package_core.py` — 更新模板夹具、状态目录断言和创建任务包断言。
- `tests/openharness_cases/test_protocol_docs.py` — 更新计划模板与 RWP 文档锚点断言。
- `tests/openharness_cases/test_yaml_quoting.py` — 更新模板夹具。
- `docs/task-packages/document-verification-and-qualitative-handoff/` — 将活跃任务包迁移到 `plan.md` 和新 `verification.method` 字段。
- `docs/task-packages/workflow-plan-stage-redesign/` — 写入需求、总体设计、详细设计、计划和本证据。

## 测试结果

```text
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_yaml_quoting.py -v
结果：51 passed, 0 failed
```

```text
uv run pytest tests/ -v
结果：61 passed, 0 failed
```

```text
rg -n "verification-design|verification_design|verification_designed|verification_designing|VERIFICATION_DESIGN" openharness_cli skills tests docs/task-packages -S
结果：命中只出现在 TASK-025 的 requirements / overview / detailed / plan 中，用于描述旧协议问题和替换对象；live 源码、live skill、测试断言和其他活跃任务包未命中。
```

```text
uv run openharness task-package list
结果：TASK-023 和 TASK-025 均可正常列出；TASK-025 当前为 implementing，TASK-023 当前为 implementing。
```

## 验收标准覆盖

| 标准 | 证据 |
|------|------|
| `mechanical` 不启用 plan 和两阶段设计 | `test_requirements_gate_routes_mechanical_directly_to_implementing` 通过 |
| `standard` 启用 `planning` / `plan.md`，不进入 overview/detailed | `test_requirements_gate_routes_standard_to_planning` 通过 |
| `structural` 保留 overview/detailed 后进入 planning | `test_requirements_gate_routes_structural_to_overview_before_planning` 通过 |
| 新任务包模板和文档模型使用 `plan.md` | `test_create_task_package_from_templates`、`test_design_package_templates_include_verification_path_sections` 通过 |
| live skill 指令消费 `plan.md` | 协议文档测试通过；旧协议名 `rg` 检查未在 live skill 命中 |
| 活跃任务包不依赖旧 `verification-design.md` | TASK-023 已迁移为 `plan.md`，`openharness task-package list` 可正常执行 |

## 运行时观察

未启用 RWP。

## 残余风险

- 历史归档任务包仍保留旧文件名和旧阶段名。接受理由：本轮明确不做历史兼容和归档迁移，归档只作为历史证据保留。
- 本轮未提供自动迁移命令。接受理由：用户明确要求现有活跃也不兼容旧协议，本轮已手工迁移当前活跃任务包；自动迁移可以作为未来独立任务。

## 后续事项

无。
