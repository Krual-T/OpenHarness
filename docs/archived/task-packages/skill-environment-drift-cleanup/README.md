# OH-020 Skill Environment Drift Cleanup

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这项任务聚焦清理 skills 中已经偏离当前仓库运行环境的指令。
- 重点包括旧入口文件约定、不可用工具名、错误的 Python 工作流示例，以及默认假设存在但当前环境并不保证的 reviewer 或任务编排能力。

## Current Status
- 当前仅完成问题立项，尚未进入需求收敛和方案设计。
- 后续需要先确认哪些 skill 受影响、哪些表述只是示例、哪些已经会误导实际执行，再推进到 `requirements_ready`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
