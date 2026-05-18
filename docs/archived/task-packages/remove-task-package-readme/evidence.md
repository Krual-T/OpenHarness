# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Result
- verify_by：`unit_test`
- result：passed
- summary：定向任务包协议测试通过，全量 OpenHarness case 测试通过，旧 README 协议引用扫描无匹配。

## Test Results
| Command | Exit Code | Result |
|---------|-----------|--------|
| `uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_yaml_quoting.py -q` | 0 | `26 passed in 0.49s` |
| `rg -n "TaskPackageDocument\\.README|task-package\\.README|Current Status|Read This First" openharness_cli skills/using-openharness tests -g '!**/__pycache__/**'` | 1 | 无匹配，符合预期 |
| `uv run pytest tests/openharness_cases -q` | 0 | `53 passed, 1 skipped in 0.81s` |

## Files
- `openharness_cli/models/task_package_document.py`：移除 `TaskPackageDocument.README`。
- `openharness_cli/models/workflow.py`：移除 README `## Overview` 的全局章节校验。
- `skills/using-openharness/references/templates/task-package.README.md`：删除任务包 README 模板。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：删除默认 `entrypoints`。
- `skills/using-openharness/references/cli-reference.md`：更新任务包不再维护 README 的约束说明。
- `tests/openharness_cases/test_task_package_core.py`：更新创建与校验相关测试。
- `tests/openharness_cases/test_cli_workflows.py`：更新归档与 overview 校验相关测试。
- `tests/openharness_cases/test_yaml_quoting.py`：删除 README 模板夹具依赖。
- `docs/task-packages/remove-task-package-readme/`：新增本任务包文档。

## Acceptance Coverage
| Acceptance Criteria | Evidence |
|---------------------|----------|
| CLI 文档模型不再把 `README.md` 作为 base file | 扫描无 `TaskPackageDocument.README`；定向 pytest 通过 |
| 新建和推进任务包不再创建 `README.md` | `test_create_task_package_from_templates` 断言新任务包没有 `README.md` |
| 模板目录不再包含 `task-package.README.md` | 文件已删除；扫描无 `task-package.README` |
| 校验不再要求 README `Overview` | overview 缺反思测试不再创建 README，仍只校验 overview 阶段章节 |
| `task-info.yaml` 模板不再默认写入 README 或未来阶段 `entrypoints` | 模板已删除默认 `entrypoints`；全量 OpenHarness case 测试通过 |
| 旧 `entrypoints` 字段兼容保留 | 归档测试仍验证已有 `requirements.md` entrypoint 被改写到 archived 路径 |

## Residual Risks
- 历史归档包仍可能包含 README，这是有意保留的历史证据，不属于新协议要求。
- `TaskInfo.entrypoints` 字段仍存在，未来如果要完全移除，需要单独任务包处理兼容性。

## Follow-ups
- 无本轮必需 follow-up。
