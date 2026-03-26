# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 用 `uv run python skills/project-memory/scripts/check_stale.py` 识别 stale memory object，再用 `save_fact.py` / `save_decision.py` 逐条刷新并补齐元数据。
  - 用 `uv run python skills/project-memory/scripts/audit_memory.py --fail-on high` 确认高优先级 memory finding 已经清零。
  - 用 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`、`bootstrap` 与 `uv run pytest` 验证维护波次没有破坏 task package、active 列表与仓库回归。
  - 用 `uv run python skills/using-openharness/scripts/openharness.py verify maintenance-and-entropy-reduction` 记录结构化 artifact，再归档 package。
- Executed Path:
  - 已串行执行 `save_fact.py` / `save_decision.py`，刷新 `runtime_capability_contract_protocol`、`project_runtime_surface_map_protocol`、`project_runtime_helper_addition_protocol`、`task_package_language_policy_phase_one`，并新增 `project_memory_saves_must_run_serially`。
  - 已执行 `uv run python skills/project-memory/scripts/check_stale.py`，确认相关对象已回到 `reviewed` / `verified` 且无 stale reason。
  - 已执行 `uv run python skills/project-memory/scripts/audit_memory.py --fail-on high`，结果为 `No audit findings.`。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`、`bootstrap`、`uv run pytest` 与 `verify maintenance-and-entropy-reduction`，随后归档 `OH-017`。
- Path Notes:
  - `verify maintenance-and-entropy-reduction` 捕获的是归档前的 active 状态，因此其中的 `bootstrap` 仍会看到 `OH-004` 与 `OH-017`；最终仓库级 `bootstrap` 结果在 `OH-004` 的关闭验证里再次确认。
  - 这轮维护不新增 CLI，只把现有审计路径真正跑通；是否需要维护命令或 checklist 仍留给未来新的 focused package 判断。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/project-memory/scripts/check_stale.py`
- `uv run python skills/project-memory/scripts/audit_memory.py --fail-on high`
- `uv run pytest`

## Expected Outcomes
- stale memory object 与高优先级 audit finding 被清零。
- `check-tasks` 继续验证全部 task package。
- `verify maintenance-and-entropy-reduction` 产出结构化 artifact，且 package 可以归档。
- 仓库测试继续通过。

## Latest Result
- Passed on 2026-03-23 for the first maintenance implementation wave:
  - `uv run python skills/project-memory/scripts/check_stale.py`
  - `uv run python skills/project-memory/scripts/audit_memory.py --fail-on high`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py verify maintenance-and-entropy-reduction`
  - 结果：stale memory object 已刷新完毕，`audit_memory.py --fail-on high` 返回 `No audit findings.`，`check-tasks` 验证了 `17 task package(s)`，全量测试保持 `53 passed`，并成功生成结构化 artifact 后归档 `OH-017`。
- Latest Artifact:
  - 见 `STATUS.yaml.verification.last_run_artifact`
