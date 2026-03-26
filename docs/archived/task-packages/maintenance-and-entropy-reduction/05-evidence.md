# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前高优先级 memory finding 已清零，但后续维护波次仍可能再次产生 stale object、owner 缺失或路径漂移，需要按本包定义的顺序重新审计。
- live skill surface 仍主要依赖现有文本测试与人工判断；如果后续发现重复人工步骤，应再拆新的 focused package 产品化维护入口。
- `.project-memory/` 的保存脚本共享 `aliases.yaml`，未来批量刷新对象时仍必须串行执行保存命令，否则会重新引入并发写风险。

## Manual Steps
- 无。

## Files
- docs/archived/task-packages/maintenance-and-entropy-reduction/README.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/STATUS.yaml
- docs/archived/task-packages/maintenance-and-entropy-reduction/01-requirements.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/02-overview-design.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/03-detailed-design.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/04-verification.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/05-evidence.md
- docs/archived/task-packages/harness-completion-roadmap/README.md
- docs/archived/task-packages/harness-completion-roadmap/02-overview-design.md
- docs/archived/task-packages/harness-completion-roadmap/03-detailed-design.md
- docs/archived/task-packages/harness-completion-roadmap/04-verification.md
- docs/archived/task-packages/harness-completion-roadmap/05-evidence.md
- .project-memory/aliases.yaml
- .project-memory/decisions/task_package_language_policy_phase_one.yaml
- .project-memory/facts/project_memory_saves_must_run_serially.yaml
- .project-memory/facts/project_runtime_helper_addition_protocol.yaml
- .project-memory/facts/project_runtime_surface_map_protocol.yaml
- .project-memory/facts/runtime_capability_contract_protocol.yaml
- skills/project-memory/SKILL.md
- skills/project-memory/scripts/check_stale.py
- skills/project-memory/scripts/audit_memory.py
- skills/project-memory/scripts/save_decision.py
- skills/project-memory/scripts/save_fact.py
- skills/project-memory/scripts/save_workflow.py
- skills/project-memory/scripts/project_memory_lib.py
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
- uv run python skills/project-memory/scripts/save_fact.py runtime_capability_contract_protocol --owner codex --verified-commit "$(git rev-parse HEAD)"
- uv run python skills/project-memory/scripts/save_fact.py project_runtime_surface_map_protocol --owner codex --verified-commit "$(git rev-parse HEAD)"
- uv run python skills/project-memory/scripts/save_fact.py project_runtime_helper_addition_protocol --owner codex --verified-commit "$(git rev-parse HEAD)"
- uv run python skills/project-memory/scripts/save_decision.py task_package_language_policy_phase_one --owner codex --verified-commit "$(git rev-parse HEAD)"
- uv run python skills/project-memory/scripts/save_fact.py project_memory_saves_must_run_serially --title "project-memory 保存命令必须串行执行" --summary "批量刷新 project-memory 对象时，save_* 脚本不能并行运行。" --statement "skills/project-memory/scripts/save_fact.py、save_decision.py 和 save_workflow.py 都会通过 project_memory_lib.save_memory_object 重写 .project-memory/aliases.yaml 并重建索引；同一轮批量刷新多个 memory object 时必须串行执行这些保存脚本，不能并行运行，否则会发生竞争写入并破坏 aliases.yaml。" --alias "project-memory 保存命令能并行吗" --alias "aliases.yaml 为什么会损坏" --alias "project-memory save_fact 要串行吗" --tag project-memory --tag workflow --tag maintenance --applies-to skills/project-memory/scripts/save_fact.py --applies-to skills/project-memory/scripts/save_decision.py --applies-to skills/project-memory/scripts/save_workflow.py --applies-to skills/project-memory/scripts/project_memory_lib.py --evidence skills/project-memory/scripts/project_memory_lib.py --owner codex --verified-commit "$(git rev-parse HEAD)"
- uv run python skills/project-memory/scripts/check_stale.py
- uv run python skills/project-memory/scripts/audit_memory.py --fail-on high
- uv run python skills/using-openharness/scripts/openharness.py new-task maintenance-and-entropy-reduction OH-017 "Maintenance And Entropy Reduction" --owner codex --summary "Define a recurring maintenance workflow that audits task-package drift, project-memory freshness, and skill-surface wording drift so OpenHarness stays legible as it grows."
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- uv run pytest
- uv run python skills/using-openharness/scripts/openharness.py transition maintenance-and-entropy-reduction in_progress
- uv run python skills/using-openharness/scripts/openharness.py transition maintenance-and-entropy-reduction verifying
- uv run python skills/using-openharness/scripts/openharness.py verify maintenance-and-entropy-reduction
- uv run python skills/using-openharness/scripts/openharness.py transition maintenance-and-entropy-reduction archived

## Artifact Paths
- 见 `STATUS.yaml.verification.last_run_artifact`

## Follow-ups
- 如果未来维护波次再次暴露出重复人工步骤，再单独产品化维护命令或 checklist，不要把新协议扩展硬塞回这个已归档包。
- 如果后续出现新的 skill drift guardrail 需求，应从维护流重新拆新的 focused package，而不是恢复 `OH-017` 为 active。
