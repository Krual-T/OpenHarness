# AGENTS.md

本文件现在作为 `openharness` 的 repository map：它负责告诉协作者“事实来源在哪里、默认工作流是什么、完成任务时需要回写什么”，而不再承担细粒度任务状态管理。

## 1. 仓库地图

### 事实来源优先级

1. `AGENTS.md`
    - 仓库地图、默认协作协议、结构约束、验证要求。
2. `skills/using-openharness/references/manifest.yaml`
    - harness 的机器可读入口；声明 active / archived task package 布局、状态流和 artifact 根目录。
3. `docs/task-packages/<task>/`
    - 任务包（task package）的唯一事实来源；每个任务是一个独立 task package。
4. `docs/archived/task-packages/<task>/`
    - 已完成 task package 的归档区；保留历史事实与验证证据，但不再属于 active package 集合。
5. `.project-memory/`
    - 已验证的项目事实、决策和可复用 workflow。
6. `docs/archived/legacy/`
    - 历史材料归档区；仅作为 legacy evidence，不再作为当前任务事实源。

## 2. Python / uv 约定

- 仓库内 Python 相关命令统一使用 `uv run ...`。
- 工作流脚本依赖应写入 `pyproject.toml`，不要依赖会话里的临时安装。
- 只有明确的一次性临时场景才使用 `uv run --with ...`。

## 3. 提交要求

- 每次完成一轮可独立成立的改动后，都应进行一次 `git commit`。
- 提交粒度尽量聚焦；一个提交只解决一个明确问题。
- 提交信息应准确描述“为什么改”以及“改了什么”。
- 如果改动尚未通过最基本的自检，不应急于提交。

## 4. 信息输出要求（必须遵循）

- 回复用户 or 任何向用户展示、输出信息时都禁止使用中文英文穿插的简述型、口号型表达，而是采用通俗易懂的中文进行表述（包括函数的参数释义），如有必要，例如专有英文名词需要使用括号补充在中文后面，或者通用的英文产品、英文人名、知名度高的英文也可以直接使用

如果用户当前任务与上述约定冲突，以用户明确要求为准。
