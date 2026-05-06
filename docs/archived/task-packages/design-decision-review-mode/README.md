# OH-042 Design Decision Review Mode

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务把“逐项设计确认”产品化为 OpenHarness 设计阶段的默认协作范式。
- 非机械开发任务进入 `02-overview-design.md` 或 `03-detailed-design.md` 时，agent 应主动提出按设计点逐项确认，而不是等用户明确要求。
- 已确认的设计点必须写回 task package，并在后续设计点改变前序边界时先同步对应设计文档。

## Current Status
- Status: `proposed`
- 当前处于需求收敛阶段：任务已创建，正在把默认触发、任务分类、确认粒度和写回规则写成可执行要求。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
