# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先补 CLI 和协议文档测试，证明当前还没有 `project-memory` CLI surface。
- 再实现 parser、handler 和命令转发。
- 再更新活跃 `project-memory` skill 文档与必要协议断言。
- 最后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_task_package_core.py`。
- 再执行 `uv run openharness check-tasks`。
- Fallback Path:
- 如果全量测试因无关改动受阻，至少要拿到本轮新增或直接相关测试通过，以及 `openharness check-tasks` 通过；如果连这些都没有 fresh evidence，不能宣称完成。
- 如果包装层参数设计出现阻塞，允许先保持底层脚本不动，但不允许绕过测试直接修改文档宣称已收口。
- Planned Evidence:
- parser 暴露 `project-memory` 子命令树的测试结果。
- 子命令转发到正确脚本与 repo 参数的测试结果。
- 活跃 skill 文档改为正式 CLI 入口的 diff。
- `check-tasks` 通过记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/cli.py`：增加 `project-memory` 命令树与参数定义。
- `openharness_cli/commands.py`：增加 project-memory 命令转发逻辑，统一处理 `--repo` 与参数拼装。
- `openharness_cli/main.py` 与可能的 `__init__.py` 导出：暴露新 handler，保持测试导入路径稳定。
- `skills/project-memory/SKILL.md`：把推荐命令面切到正式 CLI。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖 parser 和命令转发行为。
- `tests/openharness_cases/test_protocol_docs.py` 或新的协议测试文件：约束活跃文档与 CLI surface 一致。

## Interfaces
对外接口：

- `openharness project-memory query <query> [options]`
- `openharness project-memory check-stale [options]`
- `openharness project-memory audit [options]`
- `openharness project-memory archive <object_id> [options]`
- `openharness project-memory save-fact <fact_id> [options]`
- `openharness project-memory save-workflow <workflow_id> [options]`
- `openharness project-memory save-decision <decision_id> [options]`

稳定边界：

- CLI 负责参数面和仓库根路径注入。
- 底层脚本负责业务校验、YAML/index 读写和文本输出。

`observability` 入口：

- CLI 测试可观察 parser choice 和 `_run_command` 收到的最终命令字符串。
- 集成验证可观察脚本真实输出和 `check-tasks` 结果。

## Module Internals
内部职责拆分：

- parser 层只负责命令树，不参与业务判定。
- command wrapper 层维护“子命令 -> 脚本文件名”的映射，并做参数转义、repo 路径注入和统一执行。
- project-memory 脚本层继续负责具体数据写入、索引重建、审计和查询副作用。

这样可以把新增复杂度控制在适配层，不侵入现有 memory 业务实现。

## Data Semantics
本轮几乎不改 `.project-memory/` 数据语义。需要保证的只是 CLI 参数语义与底层脚本现有参数语义一致，例如：

- `--repo` 在 CLI 层表示目标仓库根目录，转发后应落为脚本的 `--repo-root`。
- 位置参数如 `query`、`fact_id`、`workflow_id`、`decision_id`、`object_id` 必须原样保留。
- 其余可选参数应按原顺序透传，避免包装层悄悄改写语义。

## Stage Gates
- 必须先有失败测试，覆盖 CLI 子命令不存在或未正确转发的现状。
- 必须确定 `--repo -> --repo-root` 的透传策略。
- 必须确定不改 project-memory schema 和脚本内部逻辑，避免实现阶段失控。
- 必须提前列清最终验证命令和预期证据。

## Decision Closure
- 接受：包装层调用现有脚本是本轮主实现方式，因为它最符合“统一入口而不复制逻辑”的目标。
- 拒绝：新增一套与脚本并行的 Python API 再让 CLI 调它，因为这会先引入额外抽象成本。
- 延期：是否给 `project-memory` 再做更细的帮助文本或 JSON 统一输出格式，留到真实使用暴露问题后再评估。

## Error Handling
主要失败路径：

- 用户输入未知二级子命令：由 argparse 直接报错。
- 用户在错误目录调用且未传 `--repo`：底层脚本可能找不到 repo root，这属于显式失败。
- 包装层少传 `--repo-root` 或错误改写参数：这是一类静默出错风险，可能让命令在当前目录运行到错误仓库，所以测试必须覆盖最终命令字符串。

异常传播策略：

- 底层脚本非零退出时，CLI 直接返回失败，不在包装层吞掉错误。
- 不在包装层添加新的 fallback 语义，避免掩盖底层失败原因。

## Migration Notes
迁移顺序：

1. 先加测试。
2. 再加 CLI 子命令和 handler。
3. 再改活跃 skill 文档。
4. 最后跑验证并回写 task package。

兼容策略：

- 底层 `skills/project-memory/scripts/*.py` 继续保留，作为当前实现面和潜在回退路径。
- 活跃文档不再把脚本路径当推荐入口，但不需要在本轮删除这些脚本。

回滚触发点：

- 如果发现包装层导致参数语义不稳定或难以测试，可回滚 CLI 包装改动，同时保留原脚本逻辑不受影响。

## Detailed Reflection
反思后确认：

- 测试重点应放在 parser 暴露面和最终命令拼装，而不是重复测试每个 project-memory 脚本的内部逻辑。
- `--repo` 与 `--repo-root` 的映射是最值得出错的边界，必须在用例里显式锁住。
- 保留脚本作为实现面能让回滚成本足够低，符合本轮聚焦范围。
