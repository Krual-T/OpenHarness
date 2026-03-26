# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 锁实现当前依赖 `fcntl.flock`，后续若仓库需要跨到不同文件锁语义的平台，可能还要补适配。
- 本轮还没有真实多进程赛跑级别的自动化测试，后续若继续增强 intake 并发能力，可再补一条端到端并发用例。

## Manual Steps
- 无。

## Files
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/README.md
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/STATUS.yaml
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/01-requirements.md
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/02-overview-design.md
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/03-detailed-design.md
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/04-verification.md
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/05-evidence.md
- skills/using-openharness/scripts/openharness_cli/commands.py
- skills/using-openharness/scripts/openharness_cli/repository.py
- skills/using-openharness/tests/openharness_cases/test_task_package_core.py

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `rg -n "new-task|auto-id|next task|task id|duplicate task id|concurrency" .`
- `git log --oneline --decorate -n 20`
- `sed -n '1,260p' skills/using-openharness/scripts/openharness_cli/commands.py`
- `sed -n '1,320p' skills/using-openharness/scripts/openharness_cli/repository.py`
- `sed -n '1,220p' skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py -k "duplicate_task_id or duplicate_allocated_id"`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Artifact Paths
- 无单独 artifact 文件。

## Follow-ups
- 如果后续观察到跨平台锁语义差异，再开新 task package 补锁适配策略。
- 如果后续需要更强的并发验证证据，再补真实多进程并行 `new-task --auto-id` 测试。
