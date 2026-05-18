# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Result
- verify_by：`unit_test`
- result：passed
- summary：`entrypoints` 路径存在性校验已从生产代码移除，stale README entrypoint 不再触发 `missing referenced path`。

## Test Results
| Command | Exit Code | Result |
|---------|-----------|--------|
| `uv run pytest tests/openharness_cases/test_task_package_core.py -q` | 0 | `15 passed in 0.44s` |
| `rg -n "missing referenced path|_referenced_path_exists" openharness_cli` | 1 | 无匹配，符合预期 |
| `uv run pytest tests/openharness_cases -q` | 0 | `53 passed, 1 skipped in 0.74s` |

## Files
- `openharness_cli/validate.py`：删除 `entrypoints` 路径存在性校验和不再使用的 `_referenced_path_exists()`。
- `tests/openharness_cases/test_task_package_core.py`：更新校验测试，覆盖 stale README entrypoint 不再报错。
- `docs/task-packages/relax-entrypoint-validation/`：记录本轮需求、验证设计和证据。

## Acceptance Coverage
| Acceptance Criteria | Evidence |
|---------------------|----------|
| `validate_task_package()` 不再对 `entrypoints` 生成 `missing referenced path` | 生产代码扫描无匹配 |
| stale README entrypoint 有测试覆盖 | `test_validate_task_package_rejects_unknown_status_but_allows_stale_entrypoints` |
| 其他校验仍生效 | 同一测试仍断言 unknown status 错误存在；全量 case 测试通过 |

## Residual Risks
- `TaskInfo.entrypoints` 字段仍保留，这是本轮有意兼容策略。

## Follow-ups
- 无本轮必需 follow-up。
