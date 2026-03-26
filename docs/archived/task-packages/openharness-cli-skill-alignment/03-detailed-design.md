# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 更新活跃协议文档中的命令入口与根目录说明。
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Fallback Path:
  - 如果测试或协议校验失败，需要继续修正文档与任务包，不能在没有 fresh evidence 的情况下宣称这一轮已完成。
- Planned Evidence:
  - 活跃协议文档改为优先使用 `openharness <cmd>` 的 diff。
  - `check-tasks` 通过记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `AGENTS.md`、`AGENTS.examaple.md`、`INSTALL.codex.md`、`skills/using-openharness/SKILL.md`：统一活跃协议文档中的标准命令入口。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`：补充协议文档断言，防止脚本路径重新回流到主文档。

## Interfaces
- CLI 对外命令名不变，`--repo` 参数不变。
- 文档层对 `--repo` 的解释要与当前实现一致：它接收一个仓库路径，默认值是当前目录。

## Stage Gates
- 必须同步改活跃协议文档，避免说明继续落后于实现。
- 必须确认任务包中的范围描述已经收缩到文档层，不再宣称会改 CLI 根目录行为。

## Decision Closure
- 接受：只在 skills 和协议文档中统一入口，不扩张到 CLI 行为改造。
- 拒绝：批量改写所有历史归档证据中的旧命令，因为这会破坏历史真实性，且工作量与收益不成比例。
- 延期：如果后续仍希望改成“从子目录也能自动找到根目录”，再单独开 task package 做 CLI 行为改造。

## Error Handling
- 如果维护者照旧脚本路径命令操作，协议文档不再为这种入口背书。
- 如果维护者不在项目根目录，文档应明确提示使用 `--repo`，避免形成错误预期。

## Migration Notes
- 新文档采用单一标准入口 `openharness <cmd>`。
- 兼容入口 `skills/using-openharness/scripts/openharness.py` 继续保留，但不作为协议文档推荐路径。
- 若需要回滚，只需撤回文档切换，不影响 CLI 与 task package 数据结构。

## Detailed Reflection
- 这轮最容易失控的点是把“入口统一”和“CLI 行为改造”混成一个任务，所以最终只保留前者。
- 验证上以协议文档断言和 `check-tasks` 为主，不为了这轮目标额外扩大测试面。
