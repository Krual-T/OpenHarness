# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
从 OpenHarness 的任务包协议中移除 per-task `README.md`，让 CLI、模板、校验和测试都不再期望每个任务包维护单独 README。

单一成功指标：新建、推进、校验和归档任务包时，OpenHarness 不再要求或生成任务包内的 `README.md`；任务摘要和状态只来自 `task-info.yaml`，阶段事实只来自对应阶段文档。

## Problem Statement
当前任务包 README 没有承担不可替代的流程职责。CLI 的状态推进依赖 `task-info.yaml.status`，阶段指导依赖 hook 注入的 state skill，具体事实写在 `requirements.md`、`overview-design.md`、`detailed-design.md`、`verification-design.md` 和 `evidence.md`。

README 反而造成重复和漂移：`Current Status` 重复 `task-info.yaml.status`，`Read This First` 容易列出尚未创建或已删除的阶段文档，`Overview` 又重复 `task-info.yaml.summary` 和需求结论。继续保留它会增加 agent 和维护者的同步成本。

目标用户是使用 OpenHarness 创建、推进和验证任务包的 agent 与维护者。核心场景是新建任务包后，agent 只需要读取 `task-info.yaml` 和当前阶段文档即可判断下一步，不再维护额外 README。

现在要做，是因为该问题涉及模板和 CLI 协议面；只在某个活跃包里删除 README 不能改变未来任务包的行为。

## Required Outcomes
1. 从 CLI 文档模型移除任务包 README。
   - acceptance criteria：`TaskPackageDocument` 不再包含 `README`；workflow 的 required/scaffold 文件集合不再包含 `README.md`；章节校验不再默认要求 README 的 `## Overview`。
2. 更新任务包模板。
   - acceptance criteria：删除 `skills/using-openharness/references/templates/task-package.README.md`；`task-package.task-info.yaml` 不再默认写入指向 README 或未来阶段文档的 `entrypoints`。
3. 保留必要兼容性。
   - acceptance criteria：不批量迁移 archived 历史任务包；如果旧包已有 `entrypoints` 字段，CLI 仍可解析和序列化，通用路径改写逻辑不被破坏。
4. 更新文档和测试。
   - acceptance criteria：CLI 参考说明 `task-info.yaml` 是唯一状态源且任务包不再维护 README；创建、归档、语义校验、YAML quoting 相关测试改为覆盖新行为。

## Non-Goals
- 不删除仓库根目录 `README.md`，它是项目级说明，不是任务包内部文档。
- 不批量重写 `docs/archived/task-packages/` 下历史包里的 README。
- 不在本轮完全移除 `entrypoints` 字段；它不是 README 专属字段，默认模板先不再生成即可。
- 不改变 CLI 状态机、状态值、gate 流转或 hook 注入机制。

Counterexample：清理 archived 历史包中的旧 README 看起来相关，但属于历史迁移和证据重写，不属于本轮。

## Constraints
- 必须保持 `task-info.yaml` 是唯一状态源。
- 必须保持现有任务包发现逻辑仍以 `task-info.yaml` 为入口。
- 新协议不得要求 agent 在阶段文档之外同步二次摘要。
- cost cap：只改任务包 README 相关的 CLI、模板、参考说明、测试和本任务包文档，不扩张到整体工作流文档重写。
