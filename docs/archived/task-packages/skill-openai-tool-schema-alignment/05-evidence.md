# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 如果未来 OpenAI 文档新增 `shell` 或其他工具依赖类型，本仓库当前测试需要同步更新。
- 本轮外部证据主要来自 OpenAI 官方仓库公开文件，而不是单独的文档站页面；如果文档站后续补充更明确说明，应再回填。

## Manual Steps
- 无。

## Files
- `skills/finishing-a-development-branch/agents/openai.yaml`
- `skills/project-memory/agents/openai.yaml`
- `skills/requesting-code-review/agents/openai.yaml`
- `skills/systematic-debugging/agents/openai.yaml`
- `skills/test-driven-development/agents/openai.yaml`
- `skills/using-git-worktrees/agents/openai.yaml`
- `skills/using-openharness/agents/openai.yaml`
- `skills/verification-before-completion/agents/openai.yaml`
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/README.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/STATUS.yaml`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/01-requirements.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/02-overview-design.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/03-detailed-design.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/04-verification.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/05-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py new-task name OH-025 "skill-openai-tool-schema-alignment"`
- `bash -ilc 'type proxy; proxy bash -lc "echo proxy-ok"'`
- `bash -ilc 'proxy curl -L https://api.github.com/repos/openai/codex/git/trees/main?recursive=1 | rg -n "openai.yaml|SKILL.md|allow_implicit_invocation|dependencies" -n'`
- `bash -ilc 'proxy curl -L https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/openai-docs/agents/openai.yaml'`
- `bash -ilc 'proxy curl -L https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/mcp/skill_dependencies.rs | sed -n "1,260p"'`
- `bash -ilc 'proxy curl -L https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/mcp/skill_dependencies_tests.rs | sed -n "1,260p"'`
- `bash -ilc 'proxy curl -L https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md | sed -n "1,260p"'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "openai_metadata"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Artifact Paths
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/04-verification.md`
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/05-evidence.md`
- `https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md`
- `https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/openai-docs/agents/openai.yaml`
- `https://raw.githubusercontent.com/openai/codex/main/codex-rs/app-server-protocol/schema/typescript/v2/SkillToolDependency.ts`

## Follow-ups
- 如果 OpenAI 官方文档将来公开支持 `shell` 或其他工具依赖类型，应新增任务包重新评估本仓库是否需要声明这些依赖。
- 可以考虑把“这些技能通常依赖终端操作”迁移到仓库私有说明层，而不是官方 metadata 层。
