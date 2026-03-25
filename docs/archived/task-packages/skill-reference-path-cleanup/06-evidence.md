# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前测试白名单只覆盖 `using-openharness` runtime capability 文档链路与 `systematic-debugging` 已确认的维护材料；其他 live docs 若存在新的路径漂移，仍需要后续任务包继续收敛。
- 本轮没有引入全仓库通用 Markdown 链接解析器，因此跨目录、更宽范围的链接一致性仍依赖后续专题治理。

## Manual Steps
- 无。当前 task package 已完成实现、验证并可归档。

## Files
- docs/archived/task-packages/skill-reference-path-cleanup/README.md
- docs/archived/task-packages/skill-reference-path-cleanup/STATUS.yaml
- docs/archived/task-packages/skill-reference-path-cleanup/01-requirements.md
- docs/archived/task-packages/skill-reference-path-cleanup/02-overview-design.md
- docs/archived/task-packages/skill-reference-path-cleanup/03-detailed-design.md
- docs/archived/task-packages/skill-reference-path-cleanup/05-verification.md
- docs/archived/task-packages/skill-reference-path-cleanup/06-evidence.md
- skills/systematic-debugging/CREATION-LOG.md
- skills/systematic-debugging/test-academic.md
- skills/systematic-debugging/test-pressure-1.md
- skills/systematic-debugging/test-pressure-2.md
- skills/systematic-debugging/test-pressure-3.md
- skills/using-openharness/references/runtime-capability-contract.md
- skills/using-openharness/references/project-runtime-surface-map.md
- skills/using-openharness/references/skill-hub.md
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py

## Commands
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- rg -n "references/(project-runtime-surface-map|adding-project-runtime-helper|runtime-capability-contract)\\.md|skills/debugging/systematic-debugging" skills/using-openharness/references skills/systematic-debugging
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- uv run python skills/using-openharness/scripts/openharness.py check-tasks

## Artifact Paths
- docs/archived/task-packages/skill-reference-path-cleanup/01-requirements.md
- docs/archived/task-packages/skill-reference-path-cleanup/02-overview-design.md
- docs/archived/task-packages/skill-reference-path-cleanup/03-detailed-design.md
- docs/archived/task-packages/skill-reference-path-cleanup/05-verification.md
- docs/archived/task-packages/skill-reference-path-cleanup/06-evidence.md

## Follow-ups
- 如果后续发现 live docs 范围外还有成批路径漂移，再拆出新的全仓库链接治理 task package。
