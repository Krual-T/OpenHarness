---
name: using-openharness
description: 在任何对话开始时使用——建立如何发现和使用仓库工作流技能，在做出任何回应之前
---

<SUBAGENT-STOP>
如果你作为子代理被调度执行特定任务，跳过本技能，除非任务明确涉及仓库 harness 协议。
</SUBAGENT-STOP>

# OpenHarness 工作流

## 定位

`using-openharness` 是仓库入口技能。它决定：
- 在做出任何回应前，是否有仓库或流程技能适用
- 任务真相在哪里（`docs/task-packages/<task>/`）
- 何时调用 `brainstorming`、`exploring-solution-space`
- 何时使用 Runtime Workflow Package (RWP) 或记录 RWP 缺失

## 技能调用顺序

1. 先 `using-openharness` —— 仓库工作流和任务包协议
2. 再流程技能 —— `brainstorming`、`exploring-solution-space`、`systematic-debugging`
3. 最后执行技能 —— `subagent-driven-development`

适用就用，不要绕过它即兴创建一个平行工作流。

## 入口协议

1. 先判断是否需要任务上下文，不要无脑跑 `openharness bootstrap`
2. 需要时才跑 `openharness bootstrap` 列出活跃任务包
3. 用户需要中文优先入口时，先打开 `references/author-entry.md`
4. 从项目根目录运行 `openharness`，在子目录时传 `--repo <project-root>`
5. 按顺序打开任务包：`README.md` → `STATUS.yaml` → `01-requirements.md` → `02-overview-design.md` → `03-detailed-design.md` → `04-verification.md` → `05-evidence.md`
6. 仅在任务包内部一致后才开始实现

## 任务分类与设计确认模式

`STATUS.yaml` 中可包含协作状态：
```yaml
collaboration:
  task_type: protocol/architecture    # mechanical / standard development / protocol/architecture
  design_review_mode: stepwise         # stepwise / auto
```

- `task_type` 仅在用户确认后写入。缺失时不视为已确认
- 进入 `02` 或 `03` 设计前，如 `task_type` 缺失，先提议分类等用户确认
- 非 `mechanical` 任务进入设计时，主动提议逐项设计确认
- `protocol/architecture` 任务默认逐项确认，除非用户明确授权 `auto`
- `mechanical` 任务不默认逐项确认，直接修改和验证

## 默认流程

1. `using-openharness` 入口
2. `brainstorming` → 收敛需求 → 写 `01-requirements.md`
3. `exploring-solution-space` → 探索 → 写 `02-overview-design.md` → 反思 → 写 `03-detailed-design.md` → 反思
4. 进入 `in_progress` 执行
5. 进入 `verifying` 验证
6. 更新验证和证据后 `archived`

## 更新方式

- 任务包 Markdown 正文中文优先，但节标题、命令、状态值、YAML 键、文件名、路径保持英文
- 各阶段使用对应的写作指引：`references/requirements-writing-guidance.md`（01）、`references/overview-design-writing-guidance.md`（02）、`references/detailed-design-writing-guidance.md`（03）、`references/verification-writing-guidance.md`（04）、`references/evidence-writing-guidance.md`（05）
- `README.md` 保持简短，是人的入口
- `STATUS.yaml` 保持机器可读，是 harness 状态源
- 不要在技能文字中重复长篇写作指引

## 归档

- 活跃工作：`docs/task-packages/<task>/`
- 已完成：移至 `docs/archived/task-packages/<task>/`
- 移动前更新 `04-verification.md`、`05-evidence.md`，设置 `STATUS.yaml.status` 为 `archived`
- 移动后更新仍然指向旧位置的任务包引用

## 验证

- 声称完成前运行 `openharness check-tasks`
- 创建任务包：`openharness new-task <name> --task-id <id> --title <title>`
- 更新工具：`openharness update`
- 运行验证：`openharness verify <task-name-or-id>`
- Python 仓库优先使用 `uv run ...` 命令
