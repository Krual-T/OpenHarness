# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先用 pytest 锁住 `project-memory` CLI 暴露面、命令转发和活跃协议文档约束，再执行 `openharness check-tasks` 确认 task package 协议仍然成立。
- Executed Path:
  - 已执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_task_package_core.py`，结果为 `97 passed`。
  - 已执行 `uv run openharness check-tasks`，结果为仓库内 `41` 个 task package 全部通过协议校验。
  - 额外执行了 `uv run openharness project-memory query "project-memory cli 收拢 openharness 子命令" --include-unusable` 和 `uv run openharness project-memory save-fact project_memory_official_cli_entrypoint ...`，确认新 CLI 包装层能真实驱动现有 project-memory 能力。
- Path Notes:
  - 本轮没有单独补端到端 shell 帮助截图，但已有 parser 测试、命令转发测试、真实 query/save 命令和仓库协议校验共同覆盖主风险，足以证明这轮“CLI 收口而非逻辑重写”的目标成立。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_task_package_core.py
- uv run openharness check-tasks

## Expected Outcomes
- `openharness` parser 暴露 `project-memory` 子命令树。
- 新增测试通过，说明 `project-memory` 命令会转发到正确脚本并携带 `--repo-root`。
- 活跃 `project-memory` skill 文档只推荐正式 CLI 入口，不再回退到脚本直调。
- 仓库 task package 协议校验继续通过。

## Traceability
- `01-requirements.md` 中“新增 project-memory 子命令树”的结果，由 CLI parser 测试和命令转发测试对应。
- “活跃 skill 文档改为正式 CLI 入口”的结果，由 `skills/project-memory/SKILL.md` 文本变更和协议文档测试对应。
- “不破坏现有 task package 主流程 CLI”的结果，由相关现有测试全量通过和 `openharness check-tasks` 对应。
- 额外新增 `.project-memory` fact，把这轮新的仓库级可复用知识沉淀到项目记忆。

## Risk Acceptance
- 当前接受的残余风险是：CLI 仍通过脚本桥接 project-memory，而不是直接调用统一库接口。之所以可接受，是因为本轮目标是统一入口而不是重写领域逻辑，桥接层回滚成本低且测试面清楚。
- 另一个接受项是：`--repo` 现在挂在 `project-memory` 命令组而不是每个叶子命令上。如果后续真实使用证明这影响可用性，再开单独任务评估是否支持更宽松的参数位置。

## Latest Result
- 最近一次验证结果为通过：pytest 相关套件 `97 passed`，`openharness check-tasks` 也通过，且新 CLI 已成功执行真实的 query/save 路径。
- Latest Artifact:
  - 最新 artifact 以 `STATUS.yaml` 中的 `verification.last_run_artifact` 为准，文件位于 `.harness/artifacts/OH-039/verification-runs/`。
