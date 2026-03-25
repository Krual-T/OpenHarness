# OH-021 Skill Protocol Deduplication

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这项任务聚焦 skill 体系中重复的仓库级协议、阶段制度和流程要求。
- 主目标是把常驻规则收敛到合适的仓库入口层，让 child skills 更短、更聚焦，降低上下文膨胀和维护分叉。

## Current Status
- 当前仅完成问题立项，尚未进入需求收敛和方案设计。
- 后续需要先界定哪些规则应留在仓库入口层，哪些规则应从 child skills 中抽离或改成引用关系。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
