# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 目前还没有实现入口优化，因此用户体验问题仍然存在。
- bootstrap 是否需要改动仍保留为条件项，尚未证明纯文档入口是否足够。

## Manual Steps
- 后续实现后，需要人工从“首次进入仓库的中文用户”视角检查入口是否真的可见。

## Files
- docs/task-packages/chinese-guidance-entry-and-discoverability/README.md
- docs/task-packages/chinese-guidance-entry-and-discoverability/STATUS.yaml
- docs/task-packages/chinese-guidance-entry-and-discoverability/01-requirements.md
- docs/task-packages/chinese-guidance-entry-and-discoverability/02-overview-design.md
- docs/task-packages/chinese-guidance-entry-and-discoverability/03-detailed-design.md
- docs/task-packages/chinese-guidance-entry-and-discoverability/04-verification.md
- docs/task-packages/chinese-guidance-entry-and-discoverability/05-evidence.md

## Commands
- uv run openharness bootstrap
- uv run openharness new-task chinese-guidance-entry-and-discoverability --auto-id --title "Chinese Guidance Entry And Discoverability" --owner codex --summary "Improve Chinese-first discoverability of task-package guidance and reduce protocol-only friction for new maintainers."
- uv run openharness check-tasks

## Artifact Paths
- docs/task-packages/chinese-guidance-entry-and-discoverability/

## Follow-ups
- 按 `03-detailed-design.md` 实现中文作者入口和相关导流改动。
- 决定是否把 bootstrap 输出也纳入第一轮实现。
- 实现后补充 `04-verification.md` 与 `05-evidence.md` 的执行证据。
