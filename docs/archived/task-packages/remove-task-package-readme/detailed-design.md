# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
主验证路径是运行与任务包协议相关的单元测试：

- `uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_yaml_quoting.py -q`
- `uv run openharness check-tasks`

预期证据：

- 创建任务包测试确认新任务包不会生成 `README.md`。
- workflow/validate 测试确认缺少 README 不再触发校验错误，阶段文档章节仍被校验。
- 归档测试确认路径改写仍作用于已有 `entrypoints` 引用，但不会制造 README 期望。
- YAML quoting 测试确认删除 README 模板后，`task-info.yaml` 仍正确转义敏感自然语言字段。

如果 `check-tasks` 因现有非本轮任务包状态失败，fallback 是记录失败原因并用定向 pytest 覆盖本轮代码路径；但应优先修复本轮引入的任务包元信息问题。

## Files Added Or Changed
- `openharness_cli/models/task_package_document.py`：移除 `TaskPackageDocument.README`，这是协议层删除的核心落点。
- `openharness_cli/models/workflow.py`：删除对 README `## Overview` 的全局章节校验，避免校验器继续隐式要求 README。
- `skills/using-openharness/references/templates/task-package.README.md`：删除任务包 README 模板，使新建任务包不会查找或生成该文件。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：删除默认 `entrypoints`，避免模板引用 README 或尚未创建的未来阶段文件。
- `skills/using-openharness/references/cli-reference.md`：更新约束说明，明确任务包不再维护单独 README。
- `tests/openharness_cases/test_task_package_core.py`：更新最小模板、创建任务包、缺失路径校验相关测试。
- `tests/openharness_cases/test_cli_workflows.py`：更新归档路径改写和 overview 校验测试。
- `tests/openharness_cases/test_yaml_quoting.py`：删除测试夹具对 README 模板的依赖。
- `docs/task-packages/remove-task-package-readme/`：记录本轮需求、设计、验证计划和证据。

## Interfaces
`TaskPackageDocument` 仍是任务包文档协议枚举。移除 `README` 后，调用方通过枚举遍历得到的文档集合不再包含 `README.md`。这会影响：

- `TaskPackageDocument.base_files()`：只返回 `TASK_INFO`。
- `Workflow.required_files()`：从 `task-info.yaml` 开始累计阶段文件。
- `Workflow.scaffold_files()`：新建和推进状态时只创建 `task-info.yaml` 与当前阶段工作文件。
- `TaskPackage.documents`：协议视图不再列出 README。

`TaskInfo.entrypoints` 保持可选字段，不在本轮删除。接口语义是：如果旧包或手写包显式提供 `entrypoints`，CLI 仍解析、序列化、校验路径存在；新模板不主动写入。

## Module Internals
文档模型变更通过枚举收敛，不需要在创建逻辑中增加特殊分支。`create_task_package()` 和 `ensure_task_package_stage_files()` 继续调用 workflow 的 `scaffold_files()`，因此只要枚举和 workflow 正确，创建和补齐路径会自然停止生成 README。

`Workflow.section_requirements()` 原本手动把 README 的 `## Overview` 加入所有状态校验。删除该手动追加后，章节校验完全来自阶段文件的 `section_specs`。这保留了阶段文档质量门禁，同时移除了 README 的全局门禁。

模板删除后，`_create_task_package_document()` 不需要知道 README 被移除；它只处理 workflow 传入的文档。这样失败路径保持简单：如果未来某个 workflow 重新引用不存在模板，仍会抛出 `FileNotFoundError`。

## Data Semantics
状态和摘要语义集中到 `task-info.yaml`：

- `status` 是唯一状态源。
- `summary` 是任务包短摘要。
- 阶段 Markdown 是各阶段事实来源。
- `README.md` 不再是任务包协议数据的一部分。

`entrypoints` 从默认数据结构中移除，但作为兼容字段保留。归档时 `_rewrite_archived_package_paths()` 仍会递归改写存在于 `task-info.yaml` 中的路径，不需要知道路径是否指向 README。

## Decision Closure
- 接受：从 `TaskPackageDocument` 删除 README，而不是只删除模板。
- 接受：新模板不再写 `entrypoints`，避免默认引用未来阶段文件。
- 延期：完全删除 `TaskInfo.entrypoints` 字段。该字段可能被历史包或未来非 README 场景使用，本轮不扩大破坏面。
- 拒绝：批量删除 archived 包的历史 README。历史包保持原貌更能保留证据链。

## Error Handling
主要风险是遗漏某个旧 `TaskPackageDocument.README` 引用导致运行时 `AttributeError` 或测试失败。通过 `rg` 扫描和定向 pytest 覆盖创建、校验、归档路径。

另一个风险是删除 README 后 `check-tasks` 对当前活跃包的要求变化。预期这是目标行为；如果失败，应检查是否仍有模板或任务包元信息默认引用 README。

## Migration Notes
迁移顺序：

1. 先改 `TaskPackageDocument` 和 `Workflow.section_requirements()`。
2. 再删除 README 模板并清理 `task-info.yaml` 模板默认 `entrypoints`。
3. 更新 CLI 参考说明。
4. 更新测试夹具和断言。
5. 运行定向 pytest 与 `openharness check-tasks`。

回滚触发点：如果发现外部流程依赖每个任务包都有 README，需要恢复 `TaskPackageDocument.README`、README 模板、workflow 全局 README section 校验和相关测试断言。但目前本地 CLI 流程没有读取 README 作为状态或阶段事实来源。

## Detailed Reflection
再次挑战点是 `entrypoints` 是否应该一并删掉。结论仍是延期：默认模板不再写它即可消除 README 维护负担；完全移除字段会扩大到数据模型兼容性，不是本轮必要条件。

测试策略挑战点是是否只跑定向 pytest。结论是定向 pytest 必须跑，`openharness check-tasks` 也应跑，因为这是协议变更，任务包校验本身必须作为验证对象。
