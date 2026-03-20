# AGENTS.md

本文件现在作为 `openharness` 的 repository map：它负责告诉协作者“事实来源在哪里、默认工作流是什么、完成任务时需要回写什么”，而不再承担细粒度任务状态管理。

## 1. 仓库地图

### 事实来源优先级

1. `AGENTS.md`
    - 仓库地图、默认协作协议、结构约束、验证要求。
2. `skills/using-openharness/references/manifest.yaml`
    - harness 的机器可读入口；声明 active / archived design package 布局、状态流和 artifact 根目录。
3. `docs/designs/<task>/`
    - 设计任务的唯一事实来源；每个任务是一个独立 design package。
4. `docs/archived/designs/<task>/`
    - 已完成 design package 的归档区；保留历史事实与验证证据，但不再属于 active package 集合。
5. `docs/architecture.md`
    - 当前系统结构说明。
6. `.project-memory/`
    - 已验证的项目事实、决策和可复用 workflow。
7. `docs/archived/legacy/`
    - 历史材料归档区；仅作为 legacy evidence，不再作为当前任务事实源。

### 设计任务包协议

每个设计任务应放在 `docs/designs/<task>/`，并固定包含：

- `README.md`：任务入口页和阅读导航。
- `STATUS.yaml`：机器可读状态源。
- `01-requirements.md`：需求、目标、非目标、完成定义。
- `02-overview-design.md`：总体设计、边界、主数据流/状态流。
- `03-detailed-design.md`：详细设计，先写测试设计，再写实现落点、runtime 验证方式与实施顺序。
- `05-verification.md`：验证方案与结果。
- `06-evidence.md`：落地证据、命令、剩余 follow-up。

默认阅读顺序：

1. `AGENTS.md`
2. `skills/using-openharness/references/manifest.yaml`
3. `docs/designs/<task>/README.md`
4. `docs/designs/<task>/STATUS.yaml`
5. `docs/designs/<task>/01-requirements.md`
6. `docs/designs/<task>/02-overview-design.md`
7. `docs/designs/<task>/03-detailed-design.md`
8. `docs/designs/<task>/05-verification.md`
9. `docs/designs/<task>/06-evidence.md`

## Python / uv 约定

- 仓库内 Python 相关命令统一使用 `uv run ...`。
- 工作流脚本依赖应写入 `pyproject.toml`，不要依赖会话里的临时安装。
- 只有明确的一次性临时场景才使用 `uv run --with ...`。

## 6. 提交要求

- 每次完成一轮可独立成立的改动后，都应进行一次 `git commit`。
- 提交粒度尽量聚焦；一个提交只解决一个明确问题。
- 提交信息应准确描述“为什么改”以及“改了什么”。
- 如果改动尚未通过最基本的自检，不应急于提交。

如果用户当前任务与上述约定冲突，以用户明确要求为准。
