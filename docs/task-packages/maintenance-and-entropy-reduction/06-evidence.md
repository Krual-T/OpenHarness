# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前只完成了维护流设计，没有完成第一波清理实现，因此 `.project-memory/` 的 stale findings 仍然存在。
- live skill surface 的维护仍主要依赖现有文本测试与人工判断，本轮还没有决定是否需要新的 checklist 或 CLI。
- `OH-017` 目前把多个维护面放在一个包里；如果后续某一面膨胀成新的协议改动，还需要继续拆包。

## Manual Steps
- 无。

## Files
- docs/task-packages/maintenance-and-entropy-reduction/README.md
- docs/task-packages/maintenance-and-entropy-reduction/STATUS.yaml
- docs/task-packages/maintenance-and-entropy-reduction/01-requirements.md
- docs/task-packages/maintenance-and-entropy-reduction/02-overview-design.md
- docs/task-packages/maintenance-and-entropy-reduction/03-detailed-design.md
- docs/task-packages/maintenance-and-entropy-reduction/05-verification.md
- docs/task-packages/maintenance-and-entropy-reduction/06-evidence.md
- docs/task-packages/harness-completion-roadmap/README.md
- docs/task-packages/harness-completion-roadmap/02-overview-design.md
- docs/task-packages/harness-completion-roadmap/03-detailed-design.md
- docs/task-packages/harness-completion-roadmap/05-verification.md
- docs/task-packages/harness-completion-roadmap/06-evidence.md
- skills/project-memory/SKILL.md
- skills/project-memory/scripts/check_stale.py
- skills/project-memory/scripts/audit_memory.py
- skills/using-openharness/references/skill-hub.md
- skills/using-openharness/scripts/openharness.py
- skills/using-openharness/tests/test_openharness.py
- README.md

## Commands
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- uv run python skills/project-memory/scripts/query_memory.py "maintenance workflow"
- uv run python skills/project-memory/scripts/query_memory.py "stale memory audit"
- uv run python skills/project-memory/scripts/query_memory.py "skill taxonomy drift"
- uv run python skills/project-memory/scripts/check_stale.py
- uv run python skills/project-memory/scripts/audit_memory.py
- uv run python skills/using-openharness/scripts/openharness.py new-task maintenance-and-entropy-reduction OH-017 "Maintenance And Entropy Reduction" --owner codex --summary "Define a recurring maintenance workflow that audits task-package drift, project-memory freshness, and skill-surface wording drift so OpenHarness stays legible as it grows."
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- uv run pytest

## Artifact Paths
- 无。

## Follow-ups
- 下一轮优先处理 `.project-memory/` 的 stale object 与缺失 `owner` 元数据，把它作为 `OH-017` 的首个实施波次。
- 如果 memory freshness 波次跑通后仍然存在重复人工步骤，再决定是否要单独产品化维护命令或维护 checklist。
- 如果后续发现 skill drift 需要新的通用 guardrail，应从 `OH-017` 再拆 focused child package，而不是在本包里无限扩张。
