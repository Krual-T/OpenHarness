# OH-030 OpenHarness Skill CLI Alignment

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮任务只解决协议入口统一问题：把当前生效的仓库协议文档统一到 `openharness <cmd>` 入口，并在 skills 中明确“默认在项目根目录运行；如果不在根目录，就显式传 `--repo <项目根目录>`”。

## Current Status
- 当前任务聚焦于活跃文档和 skills 的统一，不改 CLI 行为本身。状态以 `STATUS.yaml` 为准。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
