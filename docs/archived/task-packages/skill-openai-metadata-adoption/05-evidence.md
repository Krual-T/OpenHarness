# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- `receiving-code-review` 与 `project-memory` 的 implicit 策略后续可能因真实使用体验继续细调。
- 本轮没有新增更重的 metadata 校验器，后续若技能数继续增长，可能需要把目录枚举测试提取成复用辅助函数。

## Manual Steps
- 无。

## Files
- docs/archived/task-packages/skill-openai-metadata-adoption/README.md
- docs/archived/task-packages/skill-openai-metadata-adoption/STATUS.yaml
- docs/archived/task-packages/skill-openai-metadata-adoption/01-requirements.md
- docs/archived/task-packages/skill-openai-metadata-adoption/02-overview-design.md
- docs/archived/task-packages/skill-openai-metadata-adoption/03-detailed-design.md
- docs/archived/task-packages/skill-openai-metadata-adoption/04-verification.md
- docs/archived/task-packages/skill-openai-metadata-adoption/05-evidence.md
- skills/brainstorming/agents/openai.yaml
- skills/dispatching-parallel-agents/agents/openai.yaml
- skills/exploring-solution-space/agents/openai.yaml
- skills/finishing-a-development-branch/agents/openai.yaml
- skills/project-memory/agents/openai.yaml
- skills/receiving-code-review/agents/openai.yaml
- skills/requesting-code-review/agents/openai.yaml
- skills/subagent-driven-development/agents/openai.yaml
- skills/systematic-debugging/agents/openai.yaml
- skills/test-driven-development/agents/openai.yaml
- skills/using-git-worktrees/agents/openai.yaml
- skills/using-openharness/agents/openai.yaml
- skills/verification-before-completion/agents/openai.yaml
- skills/brainstorming/SKILL.md
- skills/exploring-solution-space/SKILL.md
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py

## Commands
- sed -n '1,220p' AGENTS.md
- sed -n '1,220p' skills/using-openharness/SKILL.md
- sed -n '1,220p' skills/brainstorming/SKILL.md
- sed -n '1,220p' skills/exploring-solution-space/SKILL.md
- sed -n '1,240p' skills/using-openharness/references/manifest.yaml
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- find docs/task-packages -maxdepth 1 -mindepth 1 -type d | sort
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/README.md
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/STATUS.yaml
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/01-requirements.md
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/02-overview-design.md
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/03-detailed-design.md
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/04-verification.md
- sed -n '1,260p' docs/task-packages/skill-openai-metadata-adoption/05-evidence.md
- find skills -maxdepth 2 \( -name SKILL.md -o -name openai.yaml \) | sort
- uv run python skills/project-memory/scripts/query_memory.py "openai yaml 技能元数据"
- uv run python skills/project-memory/scripts/query_memory.py "skill metadata openai.yaml"
- sed -n '1,200p' skills/project-memory/agents/openai.yaml
- sed -n '1,260p' README.md
- uv run pytest skills/using-openharness/tests/test_openharness.py -k 'skill_openai_metadata or openai_metadata or implicit_invocation or project_memory_metadata or live_repo_skills_all_ship_openai_metadata'
- uv run pytest skills/using-openharness/tests/test_openharness.py -k "skill_openai_metadata or openai_yaml or implicit_invocation"
- uv run pytest skills/using-openharness/tests/test_openharness.py
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- mv docs/task-packages/skill-openai-metadata-adoption docs/archived/task-packages/skill-openai-metadata-adoption
- uv run python skills/using-openharness/scripts/openharness.py bootstrap

## Artifact Paths
- docs/archived/task-packages/skill-openai-metadata-adoption/01-requirements.md
- docs/archived/task-packages/skill-openai-metadata-adoption/02-overview-design.md
- docs/archived/task-packages/skill-openai-metadata-adoption/03-detailed-design.md

## Follow-ups
- 如果后续继续扩大 skill 集合，补一个专用辅助函数或小型校验器，避免测试中的技能清单散落增长。
- 如果真实使用中发现某些 helper skill 仍被误触发，再基于验证证据微调 `allow_implicit_invocation` 分类。
