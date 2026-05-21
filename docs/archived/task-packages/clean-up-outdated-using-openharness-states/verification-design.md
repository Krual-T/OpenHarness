# 验证策略

## 验证路径

- **计划路径**：删除目标文件后，运行 `uv run pytest` 全量测试，确认无失败。
- **回退路径**：若 pytest 失败（非预期失败），用 `git restore` 回滚删除操作，逐项排查失败原因后重新执行。

## 必需命令

| 命令 | 期望退出码 | 说明 |
|------|-----------|------|
| `uv run pytest tests/openharness_cases/test_protocol_docs.py` | 0 | 目标测试文件，必须适配删除 |
| `uv run pytest` | 0 | 全量回归，确认无其他破坏 |

## 预期结果

- `test_live_repo_skills_all_ship_openai_metadata` 不再检查 state skills 下的 `agents/openai.yaml`（移除了对应断言或整个测试）
- 全量 `uv run pytest` 通过，无 FAILED

## 可追溯性

| 需求 | 验证 |
|------|------|
| 删除 brainstorming/scripts/ | `uv run pytest` 通过 |
| 删除 brainstorming/references/ 下 2 个文件 | `uv run pytest` 通过 |
| 删除 6 个 agents/openai.yaml | `test_protocol_docs.py` 适配后通过 |
| pytest 全部通过 | `uv run pytest` 退出码 0 |

## 风险接受

- 不验证已归档任务包中指向被删文件的路径——已归档文档是历史记录，保留原有引用不影响功能
- 不验证其他外部仓库是否引用了 `agents/openai.yaml`——这些文件仅被本项目测试消费

## 验证执行计划

- 执行时机：文件删除和测试修改完成后立即执行
- 执行人：agent
- 执行环境：本地 `uv run pytest`
- 失败处理：回到 implementing 修改代码，直到 pytest 通过
