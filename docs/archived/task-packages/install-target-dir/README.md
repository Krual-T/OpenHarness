# install-dir-prompt Prompt for install target directory

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务包解决 Codex 安装说明把路径默认写死到 `~` 下的问题，改为要求 Agent 在安装前先询问目标目录，再把技能安装到 `<target dir>/.agents/skills/openharness` 这样的目标位置。

## Current Status
- 当前已完成文档修改与验证，任务包将归档到 `docs/archived/task-packages/install-target-dir/`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
