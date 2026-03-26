# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前没有自动化规则去阻止未来再次引入旧环境术语，这一轮主要依靠职责收敛和人工校对。
- 历史归档文档仍可能保留旧术语，但它们不属于 active skill 执行入口。

## Manual Steps
- 无。

## Files
- docs/archived/task-packages/skill-environment-drift-cleanup/01-requirements.md
- docs/archived/task-packages/skill-environment-drift-cleanup/02-overview-design.md
- docs/archived/task-packages/skill-environment-drift-cleanup/03-detailed-design.md
- docs/archived/task-packages/skill-environment-drift-cleanup/04-verification.md
- docs/archived/task-packages/skill-environment-drift-cleanup/05-evidence.md
- docs/archived/task-packages/skill-environment-drift-cleanup/STATUS.yaml
- skills/using-openharness/SKILL.md
- skills/using-git-worktrees/SKILL.md
- skills/subagent-driven-development/SKILL.md
- skills/requesting-code-review/SKILL.md
- skills/receiving-code-review/SKILL.md
- skills/dispatching-parallel-agents/SKILL.md
- skills/brainstorming/references/spec-document-reviewer-prompt.md
- skills/subagent-driven-development/references/spec-reviewer-prompt.md
- skills/subagent-driven-development/references/code-quality-reviewer-prompt.md
- skills/subagent-driven-development/references/implementer-prompt.md
- skills/systematic-debugging/CREATION-LOG.md

## Commands
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- rg --files docs/task-packages
- git status --short
- git log --oneline -n 12
- rg -n "CLAUDE\.md|TodoWrite|Task\(|reviewer|subagent type|uv run --with|python -m venv|pip install|Task\b|Todo\b" skills AGENTS.md .agents -g 'SKILL.md' -g '*.md' -g '*.yaml'
- rg -n "CLAUDE\.md|TodoWrite|Task\(|code-reviewer subagent|Task tool|scripts/openharness.py|pip install|poetry install|general-purpose|code-reviewer type" skills -g 'SKILL.md' -g '*.md'
- uv run python skills/using-openharness/scripts/openharness.py check-tasks

## Artifact Paths
- stdout from `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Follow-ups
- 如果未来这类漂移再次出现，优先考虑补一条自动扫描 active skills 的轻量校验，而不是继续依赖人工抽查。
