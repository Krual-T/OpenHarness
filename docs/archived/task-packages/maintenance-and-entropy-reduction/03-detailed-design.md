# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 设计与 package 健康度路径：`uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - 活跃 package 可见性路径：`uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - memory freshness 路径：`uv run python skills/project-memory/scripts/check_stale.py`
  - memory audit 收敛路径：`uv run python skills/project-memory/scripts/audit_memory.py --fail-on high`
  - 仓库回归路径：`uv run pytest`
- Fallback Path:
  - 如果 `audit_memory.py --fail-on high` 仍然失败，本包最多只能宣称“设计已准备好”或“部分清理已完成”，不能宣称维护流已完成。
  - 如果 `check-tasks` 或 `pytest` 失败，应先修复仓库回归，再继续维护实施；不能把失败解释成“只是维护噪声”。
  - 如果只能运行不带 `--fail-on high` 的审计命令，本轮结果只能作为 baseline evidence，不能视为维护 closure。
- Planned Evidence:
  - `OH-017` 自身的设计文档、验证记录与证据记录。
  - `.project-memory/` 对象刷新或归档后的 YAML 变更。
  - 必要时新增或调整的 skill/docs/tests 变更。
  - `OH-004` 的路线图回写，说明维护流由 `OH-017` 接管。

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- 新增 `docs/archived/task-packages/maintenance-and-entropy-reduction/*`，作为维护流的 focused package 事实源。
- 更新 `docs/archived/task-packages/harness-completion-roadmap/README.md`，让父包直接指向新的活跃子包。
- 更新 `docs/archived/task-packages/harness-completion-roadmap/02-overview-design.md` 与 `03-detailed-design.md`，把维护流的 ownership 从“父包内的剩余流”收敛为“由 `OH-017` 接管的活跃子包”。
- 更新 `docs/archived/task-packages/harness-completion-roadmap/05-verification.md` 与 `06-evidence.md`，记录这次拆包和校验证据。

## Interfaces
本包不引入新的仓库入口，而是复用现有接口：

- `openharness.py check-tasks` 与 `bootstrap` 是 task package 维护面的固定接口。
- `check_stale.py` 与 `audit_memory.py` 是 `.project-memory/` 维护面的固定接口。
- `README.md`、`skill-hub.md` 与 `pytest` 文本测试共同构成 live skill surface 的维护接口。

写回边界如下：

- 审计结论与执行证据写回 `OH-017/05-verification.md`、`OH-017/06-evidence.md`。
- 会改变剩余路线图边界的结论写回 `OH-004`。
- 会改变可复用仓库事实的结论写回 `.project-memory/`。
- 会改变 live wording 或 drift guardrail 的结论写回 skill/docs/tests。

## Error Handling
维护流的关键不是“没有 findings”，而是“findings 被显式分类并写回”。因此：

- 审计命令输出 findings 本身不等于流程失败；真正的失败是 findings 没有被分类、没有写回，或被用聊天口头结论掩盖。
- stale memory object 不能只靠更新时间戳“消音”；必须重新核对证据是否仍然成立，再决定刷新、归档或替换。
- 如果 task package 健康度与 skill drift 同时出问题，应先修复会影响仓库可信度的基础错误，例如 `check-tasks` 失败或测试回归。
- 如果某个 finding 明显超出本包边界，例如需要定义新的共享 CLI、模板或协议，则应停止在 `OH-017` 内硬扩展，改为拆新的 focused package。

## Migration Notes
落地顺序建议如下：

1. 本轮先把 `OH-017` 设计写全，并把 `OH-004` 改成新的父级事实源。
2. 下一轮优先处理当前已经暴露出来的 `.project-memory/` stale objects 与缺失 `owner` 元数据，因为它们边界最清晰、验证路径也最成熟。
3. 如果 memory freshness 波次完成后仍然存在重复的人工审计步骤，再评估是否要单独开一个 package 产品化维护命令或维护 checklist。

回滚原则：

- 如果维护实施波次中发现设计边界不够稳定，可以把状态停在 `detailed_ready` 或退回补文档，但不要用半成品实现冒充完成。
- `OH-004` 应始终保留为 umbrella roadmap，不因单次维护波次回退而重新吸收详细设计。

## Detailed Reflection
- 我先挑战了测试策略。维护流最容易滑向“全是人工判断”，所以必须优先绑定已有命令与文本测试，而不是只写概念说明。
- 我再挑战了接口边界。当前设计避免引入新的 entry skill 或总命令，保持维护流只是消费现有 `openharness`、`project-memory` 与 `pytest` 接口。
- 我检查了迁移假设是否过于乐观。之所以把第一波实现锁定为 memory freshness，是因为仓库已经有真实 stale findings，而不是空想中的“未来可能需要维护”。
- 我也检查了验证路径是否过强或过弱。把 `audit_memory.py --fail-on high` 作为完成门槛是合理的，但本轮只做设计，因此需要在 `05-verification.md` 里明确区分 baseline audit 与最终 closure。
