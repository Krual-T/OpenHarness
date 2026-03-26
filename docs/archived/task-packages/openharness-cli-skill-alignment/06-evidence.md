# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前 CLI 仍然把 `--repo` 默认值解释为当前目录，不会自动向上找到项目根目录。
- 本轮没有改动任何运行时代码，因此如果后续想优化子目录执行体验，需要单独开任务处理。

## Manual Steps
- 无。

## Files
- AGENTS.md
- AGENTS.examaple.md
- INSTALL.codex.md
- skills/using-openharness/SKILL.md
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- docs/archived/task-packages/openharness-cli-skill-alignment/README.md
- docs/archived/task-packages/openharness-cli-skill-alignment/STATUS.yaml
- docs/archived/task-packages/openharness-cli-skill-alignment/01-requirements.md
- docs/archived/task-packages/openharness-cli-skill-alignment/02-overview-design.md
- docs/archived/task-packages/openharness-cli-skill-alignment/03-detailed-design.md
- docs/archived/task-packages/openharness-cli-skill-alignment/05-verification.md
- docs/archived/task-packages/openharness-cli-skill-alignment/06-evidence.md

## Commands
- openharness new-task openharness-root-discovery --auto-id --title "OpenHarness Root Discovery And Skill CLI Alignment" --owner codex --summary "Unify active workflow docs around the openharness CLI and make the CLI resolve repository roots from subdirectories."
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -q
- uv run python skills/using-openharness/scripts/openharness.py check-tasks

## Artifact Paths
- No generated artifact files.

## Follow-ups
- 如果后续要把“默认在项目根目录执行”的文档约束升级为真正的 CLI 能力，需要单独开 task package，设计 `--repo` 与自动根目录发现的交互语义。
