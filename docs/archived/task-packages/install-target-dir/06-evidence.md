# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- Agent 的最终执行仍依赖其遵循文档，不是由脚本强制。

## Manual Steps
- 人工确认让 Codex 抓取 `INSTALL.codex.md` 时，会先询问目标目录。

## Files
- `README.md`
- `INSTALL.codex.md`
- `docs/archived/task-packages/install-target-dir/README.md`
- `docs/archived/task-packages/install-target-dir/STATUS.yaml`
- `docs/archived/task-packages/install-target-dir/01-requirements.md`
- `docs/archived/task-packages/install-target-dir/02-overview-design.md`
- `docs/archived/task-packages/install-target-dir/03-detailed-design.md`
- `docs/archived/task-packages/install-target-dir/05-verification.md`
- `docs/archived/task-packages/install-target-dir/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py new-task install-target-dir install-dir-prompt "Prompt for install target directory"`
- `rg -n "~/.codex/openharness|~/.agents/skills/openharness|ask the user|<target dir>" README.md INSTALL.codex.md docs/archived/task-packages/install-target-dir -S`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Artifact Paths
- `docs/archived/task-packages/install-target-dir/05-verification.md`
- `docs/task-packages/skill-openai-tool-schema-alignment/STATUS.yaml`

## Follow-ups
- 如果后续需要进一步降低执行偏差，可以另开任务包引入真正的安装脚本。
