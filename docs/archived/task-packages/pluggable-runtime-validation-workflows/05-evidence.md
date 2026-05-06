# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 本轮验证的是 OpenHarness RWP 协议、CLI 外壳、runtime API 和文档路由，不包含真实 Lark/飞书 runtime workflow。
- `openharness rwp run` 第一版只支持 `.py` 脚本；其他语言 runner 被明确延后。
- `get_logger()` 只提供标准 logger，不定义日志落盘策略；具体 workflow 需要自行决定日志 handler 和 artifact 结构。

## Manual Steps
- 无已执行的人工 runtime 步骤。

## Files
- `openharness_cli/cli.py`: 新增 `rwp list/show/run` 子命令结构。
- `openharness_cli/commands.py`: 新增 RWP 命令实现、`.env` 加载和脚本执行外壳。
- `openharness_cli/repository.py`: 新增 RWP 发现、metadata 解析、workflow/script 解析。
- `openharness_cli/models.py`: 新增 `RuntimeWorkflowPackage` 数据模型。
- `openharness/rwp.py`: 新增 `get_logger()` runtime API。
- `pyproject.toml`: 把 `openharness` Python package 纳入 setuptools package 列表。
- `README.md`: 把 runtime 验证说明从 helper/surface 迁移到 RWP。
- `skills/using-openharness/SKILL.md`: 把 runtime routing 改为 RWP 发现、子智能体选择和 task package 写回。
- `skills/using-openharness/references/runtime-capability-contract.md`: 重写为 RWP 协议层。
- `skills/using-openharness/references/runtime-workflow-packages.md`: 新增项目接入 RWP 的协议说明。
- `skills/using-openharness/references/templates/runtime-workflow-package.workflow.md`: 新增 RWP `workflow.md` 模板。
- `tests/openharness_cases/test_rwp_workflows.py`: 新增 RWP CLI/API 行为测试。
- `tests/openharness_cases/test_protocol_docs.py`: 更新 parser 和协议文档断言。

## Commands
- `uv run pytest tests/openharness_cases/test_protocol_docs.py::test_openharness_single_cli_supports_all_subcommands tests/openharness_cases/test_protocol_docs.py::test_task_package_commands_use_current_handlers_only tests/openharness_cases/test_rwp_workflows.py`
  - 初次执行作为 TDD red，失败于缺少 `rwp` 命令、`cmd_rwp` 和 `openharness.rwp` package。
- `uv run pytest tests/openharness_cases/test_protocol_docs.py::test_openharness_single_cli_supports_all_subcommands tests/openharness_cases/test_protocol_docs.py::test_task_package_commands_use_current_handlers_only tests/openharness_cases/test_rwp_workflows.py`
  - 实现后执行，7 passed。
- `uv run pytest tests/openharness_cases/test_protocol_docs.py::test_openharness_skill_routes_runtime_work_through_capability_contract tests/openharness_cases/test_protocol_docs.py::test_skill_hub_describes_runtime_capability_layer tests/openharness_cases/test_protocol_docs.py::test_runtime_reference_docs_use_existing_sibling_paths tests/openharness_cases/test_protocol_docs.py::test_readme_describes_runtime_capability_contract tests/openharness_cases/test_protocol_docs.py::test_runtime_capability_reference_defines_declaration_shape_and_writeback tests/openharness_cases/test_protocol_docs.py::test_runtime_workflow_package_reference_defines_minimum_contents_and_selection_flow tests/openharness_cases/test_protocol_docs.py::test_runtime_workflow_package_template_provides_adoption_shape tests/openharness_cases/test_protocol_docs.py::test_runtime_workflow_package_reference_defines_env_and_logger_boundaries`
  - 初次执行作为文档 red，8 failed；文档迁移后执行，8 passed。
- `uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_rwp_workflows.py`
  - 执行结果为 102 passed。
- `uv run pytest`
  - 执行结果为 201 passed。
- `uv run openharness verify pluggable-runtime-validation-workflows`
  - final verification command；执行 `uv run pytest` 与 `uv run openharness check-tasks`，两条 required commands 均为 exit code 0。

## Artifact Paths
- `.harness/artifacts/OH-040/verification-runs/20260506T054719836818Z.json`
  - 由 `uv run openharness verify pluggable-runtime-validation-workflows` 生成，记录最终 required commands snapshot 与 exit codes。

## Follow-ups
- 下游项目可以新增真实 `.harness/rwp/workflows/<workflow-name>/workflow.md`，用具体 Lark/飞书或其他 runtime 场景验证 RWP 接入体验。
- 如果后续需要非 Python runner，应单独开包设计跨语言执行协议。
- 如果多个 workflow 需要统一日志格式，可以在具体项目或后续 OpenHarness 任务中扩展 `openharness.rwp` runtime API。
