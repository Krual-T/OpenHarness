# Task Classification

本文件负责任务分类：确定 `task_type` 和 `design_review_mode`，并写入 `STATUS.yaml`。

## task_type

读取 `STATUS.yaml` 后，首先确认 `collaboration.task_type` 是否已填写。

| 值 | 含义 | 适用场景 |
|----|------|---------|
| `mechanical` | 机械任务 | 改动范围明确、无架构决策、不需要设计文档，直接改代码+验证 |
| `standard development` | 标准开发 | 需要完整的需求→设计→实现→验证流程 |
| `protocol/architecture` | 协议/架构 | 涉及跨模块契约、状态模型、迁移策略，需要更审慎的逐项设计确认 |

**如何确认**：
- 如果 `STATUS.yaml` 中 `task_type` 已存在，直接使用
- 如果缺失，根据任务性质提议一个分类，说明理由，等用户确认后再写入。不要自行决定
- 写入路径：`STATUS.yaml.collaboration.task_type`

## design_review_mode

仅在非 `mechanical` 任务时适用：

| 值 | 行为 |
|----|------|
| `stepwise` | 每个设计决策点向用户确认后才继续。`protocol/architecture` 默认此项 |
| `auto` | 记录决策点但不逐项打断用户。用户明确授权后才使用 |

**如何确认**：
- `mechanical` 任务不需要此字段
- `protocol/architecture` 默认 `stepwise`，除非用户说"不用逐项确认"
- `standard development` 主动提议 `stepwise`，但用户可以选 `auto`
- 写入路径：`STATUS.yaml.collaboration.design_review_mode`

## 分类时机

`brainstorming` 完成后、需求已收敛时，对 task_type 做最终确认。不要把分类决策拖到设计阶段。
