# OH-017 Maintenance And Entropy Reduction

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 把 `OH-004` 中仅剩的维护流拆成独立 focused package，定义 OpenHarness 的例行维护边界、触发条件、写回位置与首个实施波次。

## Current Status
- `archived`。
- 已完成首个维护实施波次：刷新 4 条 stale memory object，补齐 3 条 fact 的 `owner`，补记 1 条关于串行保存的 project-memory 工作流事实，并把 `audit_memory.py --fail-on high` 收敛到无发现。
- 本包现在作为 OpenHarness 例行维护的历史基线，后续维护波次若需要新的命令、checklist 或协议扩展，应再拆新的 focused package。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
