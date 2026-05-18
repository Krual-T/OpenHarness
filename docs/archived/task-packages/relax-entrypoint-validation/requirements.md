# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
修复任务包移除 `README.md` 后的残留校验问题：`task-info.yaml.entrypoints` 是兼容性元信息，不应在 active package 的 `transition` 校验中继续被当成必须存在的路径清单。

单一成功指标：带有过期 `README.md` entrypoint 的任务包不再因为 `missing referenced path` 阻塞 CLI 校验或 transition。

## Problem Statement
上一轮已经从任务包协议中移除了 per-task `README.md`，但 `validate_task_package()` 仍会读取 `task-info.yaml.entrypoints`，并要求其中每个路径存在。旧任务包或迁移中的任务包可能仍保留 `README.md` entrypoint；这些路径不再属于新协议，却会在 `transition` 后触发 `missing referenced path`。

目标用户是执行 `openharness task-package transition` 的 agent 和维护者。核心场景是任务包进入下一阶段时，CLI 应校验当前状态必需的协议文档和章节，而不是因为可选历史入口字段阻塞。

现在要修，是因为这个问题直接影响 CLI 状态推进，且用户已经观察到 transition 仍在要求 README。

## Required Outcomes
1. 放宽 `entrypoints` 路径存在性校验。
   - acceptance criteria：`validate_task_package()` 不再对 `entrypoints` 中的路径生成 `missing referenced path` 错误。
2. 保留 `entrypoints` 字段的解析和序列化兼容。
   - acceptance criteria：不删除 `TaskInfo.entrypoints`，已有字段仍可读写。
3. 补测试覆盖 stale README entrypoint。
   - acceptance criteria：测试中包含 `docs/task-packages/<task>/README.md` 和其他不存在 entrypoint，校验结果不包含 `missing referenced path`。

## Non-Goals
- 不完全移除 `entrypoints` 字段。
- 不恢复任务包 README 协议。
- 不批量修改历史包里的 `entrypoints`。

Counterexample：给所有旧任务包自动删除 `entrypoints` 看似能解决问题，但那是历史数据迁移，不属于本轮 CLI 校验修复。

## Constraints
- `task-info.yaml` 仍是唯一状态源。
- 必须继续校验当前 workflow required files 和阶段章节内容。
- cost cap：只修改 `validate_task_package()` 和相关测试、任务包文档。
