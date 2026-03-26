# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 将协议、模板、校验器、测试和现有 task package 全部切到连续编号 `01/02/03/04/05`。
  - 执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py`
  - 执行 `uv run pytest tests/openharness_cases/test_task_package_core.py`
  - 执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py`
  - 执行 `uv run openharness check-tasks`
  - 执行 `uv run pytest -q`
- Executed Path:
  - 已先把协议测试改成期待新编号，让旧实现产生失败信号。
  - 已批量重命名模板、active task package 和 archived task package 中的 verification / evidence 文件。
  - 已同步更新 manifest、协议文档、校验常量、参考文档、测试以及 task package 内部路径引用。
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
  - 已执行 `uv run pytest tests/openharness_cases/test_task_package_core.py -q`
  - 已执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
  - 已执行 `uv run openharness check-tasks`
  - 已执行 `uv run pytest -q`
- Path Notes:
  - 这轮没有保留双编号兼容，因此验证重点是确认整仓已经只承认新编号，并且所有历史包也已完成真实文件改名和路径回写。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_protocol_docs.py`
- `uv run pytest tests/openharness_cases/test_task_package_core.py`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py`
- `uv run openharness check-tasks`
- `uv run pytest -q`

## Expected Outcomes
- 协议测试、task package 核心测试和 CLI workflow 测试通过。
- `openharness check-tasks` 通过，说明 active 与 archived task package 都已切到新编号。
- 全量 `pytest` 通过，说明仓库其余测试也没有残留旧编号假设。

## Traceability
- `01-requirements.md` 要求整仓切到连续编号，不保留双编号。
- `02-overview-design.md` 与 `03-detailed-design.md` 规定了“协议源先切、再批量重命名、再整仓校验”的主路径。
- 相关测试验证模板、协议引用、task package 校验和 archive 流程都只承认新编号；`check-tasks` 证明真实仓库数据已落地。

## Risk Acceptance
- 仍然接受的风险是：部分 archived task package 的历史叙述文本会自然带有“这轮把 05/06 改成 04/05”之类的后来视角，不再完全保留旧编号上下文。
- 这个风险可以接受，因为这轮明确目标就是统一现行协议与仓库内真实文件名，而不是保留旧编号的历史表象。
- 如果后续有人希望进一步区分“历史编号证据”和“现行协议编号”，需要单独开任务定义更细的 archival narrative policy。

## Latest Result
- 最近一次验证通过：
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 输出 `45 passed`
  - `uv run pytest tests/openharness_cases/test_task_package_core.py -q` 输出 `22 passed`
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q` 输出 `15 passed`
  - `uv run openharness check-tasks` 输出已校验 34 个 task package
  - `uv run pytest -q` 输出 `170 passed`
- Latest Artifact:
  - 无额外产物文件；证据以命令输出和仓库 diff 为主。
