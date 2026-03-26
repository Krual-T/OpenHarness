# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 将 OpenHarness 仓库自测迁移到顶层 `tests/`。
  - 删除 `skills/using-openharness/scripts/openharness.py`。
  - 通过 `docs/archived/legacy/` 快照与 archived package 校验回退保持旧包可验证。
  - 执行顶层测试与 `uv run openharness check-tasks`。
- Executed Path:
  - 已将 `skills/using-openharness/tests/` 下的测试迁移到顶层 `tests/`。
  - 已删除 `skills/using-openharness/scripts/openharness.py`。
  - 已在 `docs/archived/legacy/skills/using-openharness/` 下保存旧脚本与旧测试路径的历史快照。
  - 已在 `openharness_cli/validation.py` 中为 archived package 增加 legacy 路径回退校验。
  - 已执行 `uv run pytest tests/openharness_cases/test_entrypoint.py -q`
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
  - 已执行 `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
  - 已执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
  - 已执行 `uv run openharness check-tasks`
- Path Notes:
  - 这轮没有修改历史归档 task package 内容，而是通过 legacy 快照和 archived-only 校验回退保持旧证据可验证，符合“不改以前任务包”的目标。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_entrypoint.py`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py`
- `uv run pytest tests/openharness_cases/test_task_package_core.py`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py`
- `uv run openharness check-tasks`

## Expected Outcomes
- 顶层测试全部通过，说明迁移后的导入、CLI workflow 与协议文档仍然一致。
- `check-tasks` 通过，说明 archived package 的旧引用已经可以通过 legacy 快照继续验证。

## Traceability
- `01-requirements.md` 要求把测试迁到顶层、删除兼容脚本、并且不改旧任务包。
- `02-overview-design.md` 与 `03-detailed-design.md` 将方案收敛为“顶层测试 + 删除兼容层 + archived legacy 快照”。
- 顶层四组测试覆盖入口、协议文档、task package 校验和 CLI 工作流；`check-tasks` 证明仓库整体协议仍成立。

## Risk Acceptance
- 仍然接受的残余风险是：`docs/archived/legacy/` 中保留了一份历史镜像，会增加少量仓库体积。
- 这个代价可以接受，因为它只服务 archived 证据校验，不参与 runtime，也避免了机械性重写大量旧任务包。
- 如果后续希望进一步压缩 legacy 快照范围，可以单独开任务讨论更细的 archived path policy。

## Latest Result
- 最近一次验证通过：
  - `uv run pytest tests/openharness_cases/test_entrypoint.py -q` 输出 `3 passed`
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 输出 `45 passed`
  - `uv run pytest tests/openharness_cases/test_task_package_core.py -q` 输出 `22 passed`
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q` 输出 `15 passed`
  - `uv run openharness check-tasks` 输出已校验 33 个 task package
- Latest Artifact:
  - 无额外产物文件；证据以命令输出和本包文档为主。
