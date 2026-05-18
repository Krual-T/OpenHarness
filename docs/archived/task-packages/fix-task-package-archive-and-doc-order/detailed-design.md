# Detailed Design

## Runtime Verification Plan

- **Verification Path**：执行 `uv run pytest tests/openharness_cases -q`。
- **Fallback Path**：如果全量用例失败，先运行相关单测文件定位：`test_task_package_core.py`、`test_cli_workflows.py`、`test_yaml_quoting.py`、`test_protocol_docs.py`。
- **Planned Evidence**：在 `evidence.md` 写入全量 pytest 结果、关键覆盖点和残余风险。

## Files Added Or Changed

- `openharness_cli/models/task_package_document.py`：改为无前缀语义文件名。
- `openharness_cli/models/workflow.py`、`openharness_cli/workflows.py`：新增阶段工作文件定义，支持按状态创建文档。
- `openharness_cli/core/task_packages.py`：新建包只创建当前阶段文件；状态推进时补齐缺失阶段文件；归档后检查源目录残留。
- `openharness_cli/transition_engine.py`：`verified` gate 直接归档，归档目标冲突时保持源状态。
- `skills/using-openharness/references/templates/` 和 state skill：同步新文件名。
- `tests/openharness_cases/`：覆盖新建、阶段补文件、归档成功和归档目标冲突。
- 当前活跃任务包：迁移为无前缀语义文件名并清理空任务包目录。

## Interfaces

稳定接口仍是 `openharness task-package new` 和 `openharness task-package transition`。新增内部接口 `ensure_task_package_stage_files(package)`，只负责在模板存在且目标文件缺失时创建当前阶段应有文件，不覆盖已有人工内容。

## Module Internals

`Workflow` 负责声明状态和文档关系；`core/task_packages.py` 负责模板落盘；`transition_engine.py` 负责状态持久化和归档时机。归档路径中，目标存在检查必须发生在写 `verified` 状态之前，避免失败后任务包从活跃视图消失。

## Data Semantics

`file_additions` 表示某 gate 完成后验证所需的已完成文件；`working_files` 表示某活跃阶段开始时需要预创建、供作者填写的文件。`scaffold_files(status)` 是两者的并集，并保持 `TaskPackageDocument` 枚举顺序。

## Stage Gates

实施前确认：

- 模板文件名与 `TaskPackageDocument` 一致。
- 新建包只产生 base 文件和 `requirements.md`。
- `overview_designing`、`detailed_designing`、`verification_designing`、`verifying` 分别补齐对应阶段文件。
- 归档目标冲突不改变源包状态。

## Decision Closure

接受：`verified` gate 直接归档，而不是先写 `verified` 再递归到 `archived`。理由是归档失败时不能留下半完成状态。

拒绝：在 skill 中写死数字前缀。理由是数字前缀会把顺序固化在文本里，和 workflow 动态状态脱节。

## Error Handling

静默风险是归档移动失败但源包状态已变为非活跃。处理方式是在归档目标存在时提前报错，并且只有 `archive_task_package()` 成功后才返回 archived 结果。移动后如果源路径仍存在，空目录会被清理；非空源目录会报错。

## Migration Notes

实施顺序：先改文档枚举和模板，再改 scaffold 行为，再补 transition 归档路径，最后迁移当前活跃包文件名并清理空目录。回滚触发点是新建包或归档流程测试失败。

## Recommended Diagrams

不需要图示；本轮的关键关系可由 `Workflow.file_additions` 与 `Workflow.working_files` 的定义直接表达。

## Detailed Reflection

测试策略必须覆盖失败路径，不只覆盖成功归档。归档目标冲突测试证明状态不会被提前写坏；新建包测试证明不会一次性创建所有未来文档。
