# 证据

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 变更文件

- `openharness_cli/models/verification_method.py` — 新增 `VerificationMethod`，只包含 `unit_test` 和 `qualitative`。
- `openharness_cli/models/verification_info.py` — 改造验证配置模型，解析 `method`、保存原始 `raw_method`、解析 RWP 开关和理由。
- `openharness_cli/models/task_package.py` — 暴露 `verification_method`、`raw_verification_method`、`rwp_enabled`、`rwp_reason`。
- `openharness_cli/workflows.py` — 需求门禁改为检查 `verification.method` 和 RWP 确认字段。
- `openharness_cli/validate.py` — 校验非法 `verification.method` 和非布尔 `verification.rwp.enabled`。
- `openharness_cli/display.py` — 阶段模板渲染上下文改为新验证字段。
- `openharness_cli/commands/task_package.py` — transition 后使用更新后的 package 渲染阶段说明。
- `openharness_cli/__init__.py`、`openharness_cli/models/__init__.py` — 导出 `VerificationMethod`，移除旧 `VerifyBy` 导出。
- `openharness_cli/models/verify_by.py` — 删除旧枚举文件。
- `skills/using-openharness/references/templates/task-package.task-info.yaml` — 新任务包模板改为 `verification.method` 和 `verification.rwp`。
- `skills/using-openharness/references/templates/task-package.verification-design.md` — 验证策略模板改为引用 `verification.method`。
- `skills/using-openharness/references/templates/task-package.evidence.md` — 证据模板改为按 `method` 和 RWP 开关填写。
- `skills/using-openharness/states/proposing/instructions.md` — 需求阶段改为确认 `verification.method` 和 RWP 开关。
- `skills/using-openharness/states/verification-designing/instructions.md` — 验证策略阶段改为消费 `verification_method` 和 `rwp_enabled`。
- `skills/using-openharness/states/implementing/instructions.md` — 实现阶段改为按 `verification.method` 执行主要循环，RWP 作为附加验证。
- `skills/using-openharness/states/verifying/instructions.md` — 验证执行阶段改为按 `verification.method` 和 RWP 开关检查 evidence。
- `tests/openharness_cases/test_task_package_core.py` — 更新门禁和模板断言，新增非法 method 和 RWP 类型校验测试。
- `tests/openharness_cases/test_yaml_quoting.py` — 更新 YAML 占位符断言。
- `tests/openharness_cases/test_cli_workflows.py` — 更新临时任务包测试数据为新验证字段。
- `pyproject.toml`、`uv.lock` — 按不兼容改造升级版本到 `1.0.0`。
- `docs/task-packages/verification-method-rwp-split/` — 新增并维护本任务包需求、设计、验证策略和实现证据。

## 测试结果

最终验证执行：

```bash
uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py
```

结果：48 passed, 0 failed。

```bash
uv run pytest
```

结果：58 passed, 0 failed。

```bash
rg -n "verify_by|VerifyBy" openharness_cli skills/using-openharness/references/templates skills/using-openharness/states tests/openharness_cases
```

结果：退出码 1，无匹配结果。

## 验收标准覆盖

| 标准 | 证据 |
|------|------|
| CLI 数据模型改为 `verification.method` 与 `verification.rwp` | `test_task_package_core.py` 聚焦测试通过 |
| 新任务包模板不再生成旧字段 | `test_create_task_package_from_templates`、`test_create_task_package_quotes_yaml_sensitive_status_fields` 通过 |
| 阶段指令不再使用旧入口 | `rg -n "verify_by|VerifyBy" ...` 无匹配 |
| 非法 `method: rwp` 被识别为未知方法 | `test_validate_task_package_reports_unknown_verification_method` 通过 |
| `rwp.enabled` 必须为布尔值 | `test_validate_task_package_rejects_string_rwp_enabled` 通过 |
| 主版本号升级 | `pyproject.toml` 和 `uv.lock` 为 `1.0.0` |

## 验证结果

- **method**: unit_test
- **rwp_enabled**: false
- **Result**: passed

所有 `verification-design.md` 中声明的必需命令均已执行，实际退出码和预期一致。

## 残余风险

- 历史归档任务包仍可能包含旧 `verification.verify_by` 字段。接受理由：归档区只作为历史证据保留，本轮明确不批量迁移归档任务包。
- 仍处于活跃状态的 TASK-023 使用旧验证字段，后续继续推进时需要按新结构更新。接受理由：本轮不处理 TASK-023 的验证交接内容，只改变协议模型。
- `rg` 扫描范围不包含任务包历史文档。接受理由：本任务需求和设计文档需要保留旧字段作为背景和反例；新协议入口已在 CLI、模板、阶段说明和测试范围内清理。

## 后续事项

- 后续继续处理 TASK-023 时，先把该任务包的 `task-info.yaml` 更新为 `verification.method` 和 `verification.rwp`。
