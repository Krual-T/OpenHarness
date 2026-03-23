# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 用 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 验证新 package 与父包回写后仍符合 harness 协议。
  - 用 `uv run python skills/using-openharness/scripts/openharness.py bootstrap` 确认活跃 package 列表已经从“只有 `OH-004`”变成“`OH-004` + `OH-017`”。
  - 用 `uv run python skills/project-memory/scripts/check_stale.py` 和 `uv run python skills/project-memory/scripts/audit_memory.py` 建立当前 maintenance baseline。
  - 用 `uv run pytest` 确认新增 package 与父包回写没有引入仓库级回归。
- Executed Path:
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py bootstrap`，在拆包前确认只有 `OH-004` 处于 active。
  - 已执行 `uv run python skills/project-memory/scripts/check_stale.py`，确认当前存在多个 stale memory object。
  - 已执行 `uv run python skills/project-memory/scripts/audit_memory.py`，确认当前 stale findings 之外还存在缺失 `owner` 的低优先级元数据问题。
  - 本轮文档写完后继续执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`、`uv run python skills/using-openharness/scripts/openharness.py bootstrap` 与 `uv run pytest`。
- Path Notes:
  - 这次执行的是 design round，不是 maintenance implementation round，所以 memory audit 先以 baseline 建模为主，而不是要求当场达到零高优先级 findings。
  - `audit_memory.py --fail-on high` 已经被写入完成门槛，但当前 round 还不应把未修复的高优先级 findings 伪装成“已关闭”。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/project-memory/scripts/check_stale.py`
- `uv run python skills/project-memory/scripts/audit_memory.py --fail-on high`
- `uv run pytest`

## Expected Outcomes
- `check-tasks` 可以验证包含 `OH-017` 在内的全部 task packages。
- `bootstrap` 应显示 `OH-004` 与 `OH-017` 这两个 active package。
- memory audit 输出应足够具体，能直接作为下一轮实施波次的输入。
- 仓库测试应继续通过。

## Latest Result
- Passed on 2026-03-23 for the design handoff round:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - Baseline evidence from `uv run python skills/project-memory/scripts/check_stale.py` and `uv run python skills/project-memory/scripts/audit_memory.py` shows that multiple stale memory objects and missing `owner` metadata still exist, which is why this package remains at `detailed_ready` rather than moving into maintenance completion claims.
- Latest Artifact: 无；当前还处于 `detailed_ready`，未运行 `openharness.py verify` 生成结构化 artifact。
