# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 这轮保护的是当前 live wording 与能力边界；如果未来新增新的 entry docs、skill hub 入口或 visual helper 表面，仍然可能出现新的叙事漂移，需要新的 focused package 继续收敛。
- 这轮没有把“产品/价值检查”产品化为独立结构化模板，只把它们落到了技能检查项里；若未来需要更强的可审计结构，再拆新包更合适。

## Manual Steps
- 无。

## Files
- README.md
- skills/brainstorming/SKILL.md
- skills/exploring-solution-space/SKILL.md
- skills/using-openharness/references/skill-hub.md
- skills/using-openharness/tests/test_openharness.py
- docs/archived/task-packages/capability-model-alignment/README.md
- docs/archived/task-packages/capability-model-alignment/STATUS.yaml
- docs/archived/task-packages/capability-model-alignment/01-requirements.md
- docs/archived/task-packages/capability-model-alignment/02-overview-design.md
- docs/archived/task-packages/capability-model-alignment/03-detailed-design.md
- docs/archived/task-packages/capability-model-alignment/05-verification.md
- docs/archived/task-packages/capability-model-alignment/06-evidence.md

## Commands
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- uv run python skills/using-openharness/scripts/openharness.py new-task capability-model-alignment OH-018 "Capability Model Alignment"
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- uv run pytest skills/using-openharness/tests/test_openharness.py
- uv run python skills/using-openharness/scripts/openharness.py verify capability-model-alignment
- mv /home/Shaokun.Tang/Projects/openharness/docs/task-packages/capability-model-alignment /home/Shaokun.Tang/Projects/openharness/docs/archived/task-packages/capability-model-alignment
- uv run python skills/using-openharness/scripts/openharness.py bootstrap

## Artifact Paths
- .harness/artifacts/OH-018/verification-runs/20260324T032344281959Z.json

## Follow-ups
- 如果未来希望把 product/value checks 进一步结构化，例如沉淀成 task package 模板、检查清单或独立校验器，应新开 focused package，不要在本包上继续堆叠。
- 如果 visual companion 后续扩展出新的安装说明、运行时依赖或额外入口，也应单开 focused package，避免再次稀释 OpenHarness 的主能力叙事。
