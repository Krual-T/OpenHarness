# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- child skills 仍保留少量边界提醒语句，但本轮复查后判断它们当前主要服务于 stage-local 约束，不再是最重的重复协议面。
- 文本输出已经减重，但 JSON 输出暂时仍偏完整；如果未来需要进一步减面，要先证明不会伤到机器消费接口。
- 本轮把先前的状态不一致更倾向解释为并行执行竞态，但还没有单独做最小复现证明。
- `AGENTS.md` 已经收窄，但事实来源优先级仍留在仓库地图内；如果后续还要继续压缩，需要先证明这部分也适合迁出。

## Manual Steps
- 无。

## Files
- AGENTS.md
- README.md
- openharness_cli/commands.py
- skills/using-openharness/SKILL.md
- skills/using-openharness/references/skill-hub.md
- tests/openharness_cases/test_cli_workflows.py
- tests/openharness_cases/test_protocol_docs.py
- docs/archived/task-packages/protocol-thinning-and-intake-restructuring/README.md
- docs/archived/task-packages/protocol-thinning-and-intake-restructuring/STATUS.yaml
- docs/archived/task-packages/protocol-thinning-and-intake-restructuring/04-verification.md
- docs/archived/task-packages/protocol-thinning-and-intake-restructuring/05-evidence.md

## Commands
- `uv run openharness transition protocol-thinning-and-intake-restructuring in_progress`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`  # failing-first after tightening boundary assertions
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- `uv run pytest -q`
- `uv run openharness check-tasks`
- `uv run openharness bootstrap --json`
- `uv run openharness transition protocol-thinning-and-intake-restructuring verifying`
- `final verification command: uv run openharness check-tasks`

## Artifact Paths
- 无独立 artifact；当前证据来自测试输出、`bootstrap --json` 输出和 task package 文档写回。

## Follow-ups
- 如果后续仍觉得入口过重，再决定是否继续压缩 child skills 中少量边界提醒语句；当前不再默认把它当成必须继续清理的主问题。
- 继续防止仓库级制度说明回弹到 `AGENTS.md`、`README.md`、`using-openharness` 和 `skill-hub` 的多个表面。
- 评估是否需要单独把 `bootstrap` 的 JSON 输出也分成“稳定机器字段”和“可选人类提示”两层。
- 如果后续在串行执行下再次出现状态显示与 `STATUS.yaml` 不一致，应单独开包做最小复现和修复，不要再把它和入口减重混在一起。
- 当前串行 fresh verification 没有再次出现状态显示异常，因此这条 follow-up 继续保留为条件触发，而不是已确认 bug。
