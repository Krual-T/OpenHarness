# Requirements

## Goal

修正任务包 CLI 的归档和文档脚手架行为，使活跃目录只保留真正活跃的任务包，新包只创建当前阶段需要的文档，并由 workflow 状态决定文档创建顺序。

## Problem Statement

- Current behavior: 自动归档后，`docs/task-packages/` 下出现了没有内容的任务包空目录；新建任务包会一次性创建全部设计文档；状态 skill 中不应该硬编码带阶段序号的验证文档名。
- Why it is insufficient: 空目录会误导活跃任务包列表和人工检查；提前创建全部文档会让阶段边界变模糊；在 skill 中硬编码序号会让文档顺序和 workflow 动态状态脱节。

## Target Users

直接用户是使用 `openharness task-package new`、`transition`、`list` 管理任务包的人和 agent。

## Required Outcomes

1. 归档必须按整个任务包目录移动，移动成功后源目录不存在；如果只剩空源目录，CLI 应清理掉。
2. 归档目标已存在或移动不完整时，CLI 必须报错，不能把源包静默留成坏状态。
3. 新建任务包只创建 `README.md`、`task-info.yaml` 和当前 `proposing` 阶段要写的 `requirements.md`。
4. 后续阶段文档由 CLI 在进入对应活跃阶段时创建：overview、detailed、verification design、evidence 按顺序出现。
5. 新任务包文档使用无前缀语义文件名；文档创建顺序由 workflow 的当前状态决定。
6. 单元测试覆盖新建、推进阶段创建文档、归档清理空源目录和目标冲突。

## Non-Goals

- Not doing: 不在 skill 中硬编码文档序号；不迁移历史归档包。

## Constraints

- Protocol boundary: 任务包状态仍由 `task-info.yaml` 管理，状态流转语义不变。
- Compatibility: 新 CLI 只面向无前缀语义文件名；本轮只迁移当前活跃任务包和模板。
- Cost cap: 不重写 workflow 引擎，只补齐归档原子性和阶段文档创建行为。

## Acceptance Criteria

- [x] task_type 和 verify_by 已写入 `task-info.yaml`。
- [x] 需求包含明确的反例：不在 skill 中硬编码文档序号。
- [ ] `uv run pytest tests/openharness_cases` 通过。
