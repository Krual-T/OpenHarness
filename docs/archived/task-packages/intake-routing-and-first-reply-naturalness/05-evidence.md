# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前仍缺少“真实对话样例级”的自动化验证，因此只能证明仓库协议已经明确，不足以穷尽所有首轮回复风格漂移。
- 混合型请求的边界已经在协议中说明，但具体示例库仍可继续补强。

## Manual Steps
- 无。

## Files
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/README.md
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/STATUS.yaml
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/01-requirements.md
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/02-overview-design.md
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/03-detailed-design.md
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/04-verification.md
- docs/archived/task-packages/intake-routing-and-first-reply-naturalness/05-evidence.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/01-requirements.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/02-overview-design.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/01-requirements.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/02-overview-design.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/03-detailed-design.md
- skills/using-openharness/SKILL.md
- skills/brainstorming/SKILL.md
- tests/openharness_cases/test_protocol_docs.py

## Commands
- `openharness bootstrap`
- `rg -n "bootstrap|入口回复|自然|stage|next step|初始回复|routing|路由|skill.*used|announce the skill" docs/task-packages docs/archived/task-packages tests skills -S`
- `openharness new-task intake-routing-and-first-reply-naturalness --title "Intake Routing And First Reply Naturalness" --summary "Clarify when bootstrap should lead, when it should stay background-only, and how first user-visible replies should expose workflow context without reading like execution logs."`
- `openharness new-task intake-routing-and-first-reply-naturalness --auto-id --title "Intake Routing And First Reply Naturalness" --summary "Clarify when bootstrap should lead, when it should stay background-only, and how first user-visible replies should expose workflow context without reading like execution logs."`
- `uv run openharness check-tasks`
- `uv run openharness bootstrap`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -k 'routes_bootstrap_by_request_axis or natural_user_visible_stage_updates or focused_on_problem_not_log_labels' -q`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- `final verification command`: `uv run openharness check-tasks`

## Artifact Paths
- 无

## Follow-ups
- 若后续仍发现真实首轮回复频繁退化成执行日志回放，可单独开包补“对话样例级验证”。
- 若未来要让 CLI 更直接暴露“前台/后台使用边界”，再单独评估是否值得补充 `bootstrap` 帮助文案或其他辅助表面。
