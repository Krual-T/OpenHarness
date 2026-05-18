# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 OpenHarness 任务包协议中与 per-task `README.md` 相关的活跃表面：CLI 的任务包文档枚举、workflow required/scaffold/section 校验、任务包模板、CLI 速查文档，以及围绕创建、校验、归档路径改写的测试。

本轮不批量迁移 `docs/archived/task-packages/` 下的历史任务包。历史 `README.md` 是当时协议的一部分，可以作为归档证据保留；新的 CLI 和模板不再把它作为期望文件。仓库根目录 `README.md` 也不属于本轮范围，它是项目级说明，不是任务包内部文档。

## Proposed Structure
推荐方案是把 `README.md` 从任务包文档模型中移除，而不是只删除模板文件。

具体边界如下：

- `TaskPackageDocument` 不再包含 `README` 成员，因此 `Workflow.required_files()`、`Workflow.scaffold_files()` 和 `TaskPackage.documents` 的协议视图都不会再期望任务包 README。
- `Workflow.section_requirements()` 不再为所有状态追加 README 的 `## Overview` 校验；每个阶段只校验对应阶段文档的章节。
- `skills/using-openharness/references/templates/` 删除 `task-package.README.md`，`task-package.task-info.yaml` 不再默认写入 `entrypoints`。
- `entrypoints` 的读取、序列化和存在性校验暂时保留为兼容字段；如果旧包或特殊包显式填写，它仍然会被校验，但新模板不会再制造这个维护面。
- 测试从“README 会被创建并归档改写”改为“README 不会被创建；归档只改写仍然存在的引用路径”。

这个方案让事实来源收敛为两类：`task-info.yaml` 负责状态和摘要，阶段 Markdown 负责阶段事实。它不再要求 agent 额外同步一个总览 README。

## Key Flows
新建任务包时，CLI 根据 `workflow_for(None).scaffold_files(proposing)` 创建 `task-info.yaml` 和 `requirements.md`。由于 `README.md` 不再是 base file，模板解析不会查找 `task-package.README.md`，新任务包目录里也不会出现 README。

推进状态时，CLI 先更新 `task-info.yaml.status`，再调用 `ensure_task_package_stage_files()` 补齐当前阶段文件。该补齐逻辑仍然只依赖 workflow 的 scaffold 文件集合，因此不会重新生成 README。

校验时，`validate_task_package()` 仍检查当前 workflow 所需文件、必填状态键、枚举字段、可选 `entrypoints` 引用，以及阶段章节内容。README 的失败信号被移除：缺少 README 或 README 没有 `## Overview` 不再构成错误。

归档时，`archive_task_package()` 继续移动整个任务包目录，并改写 `task-info.yaml` 中已有路径。因为新模板不再写入 README 路径，所以新包不会产生 README 改写；旧包如果显式保留引用，仍由通用路径改写函数处理。

## Stage Gates
进入详细设计前必须满足以下条件：

- 能明确说明新任务包为什么不再需要 per-task `README.md`。
- CLI 文档模型、模板和测试的变化范围已经覆盖创建、推进、校验、归档四条路径。
- 已确认不批量迁移历史归档包，避免把协议变更扩大成历史重写。
- `entrypoints` 是否完全删除已有结论：本轮只从默认流程移除，不破坏旧字段兼容。
- 至少一个备选方案已经被拒绝并写明原因。

## Trade-offs
采用“从文档模型移除 README”的方案，收益是协议更简单，状态摘要不再重复，agent 不需要同步 `Current Status` 和 `Read This First`。代价是历史包和新包的结构会不同；读历史包时仍会看到旧 README，但这是归档事实，不影响新流程。

备选方案一是保留 README，但把模板改短，只留下任务摘要。这能减少当前占位问题，但仍然重复 `task-info.yaml.summary` 和阶段文档结论，也不能解决状态过期问题，因此拒绝。

备选方案二是删除 `entrypoints` 字段模型。这个方向更彻底，但会影响历史包和可能的外部消费者；本轮目标是去掉 README 文档，不是清理所有可选元信息字段，因此延期。

## Recommended Diagrams
本轮不需要 PlantUML 图。涉及的是单一文档类型从协议集合中移除，关系可以通过文件清单和测试覆盖表达，图示不会明显降低歧义。

## Overview Reflection
挑战一：只删模板是否足够？结论是拒绝。只删 `task-package.README.md` 会让 `TaskPackageDocument.README` 继续存在，CLI 在创建或校验时仍可能期望 README，协议没有真正收敛。

挑战二：是否应该重写所有 archived 包删除 README？结论是拒绝。归档包是历史证据，批量迁移会增加无关 churn，并可能破坏旧 evidence 对路径的引用。

挑战三：是否同步删除 `entrypoints` 字段？结论是延期。它目前不是 README 专属字段；默认模板可以先不写，解析和校验保留兼容更稳。
