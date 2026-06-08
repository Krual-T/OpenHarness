# 验证策略

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 本文件在实现前编写。定义验证策略——计划怎么验证、用什么命令、期望什么结果。实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。

## 验证路径

- **计划路径**：以 `verification.method: unit_test` 为主要验证方法。先运行聚焦测试覆盖模型、门禁、模板、阶段说明和 CLI 流程，再运行全量测试，最后用 `rg` 检查新协议入口不再使用 `verify_by` 或 `VerifyBy`。
- **回退路径**：如果聚焦测试失败，回到 `implementing` 修正对应代码或文档；如果 `rg` 仍发现新协议入口引用旧字段，回到 `implementing` 清理模板或阶段说明；如果测试设计本身无法区分历史背景和新入口，回到 `verification_designing` 收紧命令范围。
- **路径说明**：本任务不启用 RWP，已确认 `verification.rwp.enabled: false`。验证对象是 CLI 字段模型、模板和协议文本，不需要运行时工作流证据。

## 必需命令

1. 聚焦测试：

   ```bash
   uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py
   ```

   - 期望退出码：0。
   - 期望输出：所有选中测试通过，无失败、无错误。

2. 全量测试：

   ```bash
   uv run pytest
   ```

   - 期望退出码：0。
   - 期望输出：全仓库测试通过，无失败、无错误。

3. 旧协议入口扫描：

   ```bash
   rg -n "verify_by|VerifyBy" openharness_cli skills/using-openharness/references/templates skills/using-openharness/states tests/openharness_cases
   ```

   - 期望退出码：1。
   - 期望输出：无匹配结果。

## 预期结果

必须观察到以下结果：

- 新建任务包模板包含 `verification.method`、`verification.rwp.enabled`、`verification.rwp.reason`，不包含 `verification.verify_by`。
- `VerificationMethod` 只包含 `unit_test` 和 `qualitative`。
- 缺失 `verification.method` 时，需求门禁报告 `verification method is not determined`。
- 缺失 `verification.rwp.enabled` 时，需求门禁报告 `RWP setting is not confirmed`。
- 缺失 `verification.rwp.reason` 时，需求门禁报告 `RWP reason is not documented`。
- `verification.method: rwp` 时，校验报告 `unknown verification.method`，而不是把它当成缺失字段。
- `verification.rwp.enabled: "false"` 时，校验报告 `verification.rwp.enabled` 必须是布尔值。
- 阶段指令和模板使用 `verification_method`、`rwp_enabled`、`rwp_reason`，不依赖 `verify_by`。
- `pyproject.toml` 版本号为 `1.0.0`。

## 审核交接包

本任务 `verification.method: unit_test`，不执行定性审核交接包。协议文本变化由聚焦测试中的文档断言和旧入口扫描覆盖。

- **审核对象**：无。
- **任务背景**：无。
- **审核目标**：无。
- **非审核范围**：不评价自然语言表达风格，只验证协议入口、字段名和命令行为。
- **输出格式**：无。

### 审核矩阵

| 审核对象 | 审核维度 | 通过标准 | 证据要求 |
|----------|----------|----------|----------|
| 不适用 | 不适用 | 本任务不走 `qualitative` 审核 | 聚焦测试和扫描命令通过 |

## 可追溯性

| 需求 / 交付物 | 验证证据 |
|---------------|----------|
| CLI 数据模型改为 `verification.method` 与 `verification.rwp` | 聚焦测试覆盖模型解析、序列化、非法 method、RWP 布尔校验 |
| 新任务包模板不再生成 `verify_by` | 聚焦测试和旧入口扫描 |
| 阶段指令改为确认 `method` 和 RWP 开关 | 协议文档测试和旧入口扫描 |
| RWP 是可选运行时证据开关 | 协议文档测试覆盖模板和阶段说明，新 `rwp.enabled/reason` 字段断言 |
| 不兼容读取旧 `verify_by` | 模型测试覆盖旧字段不转成 `method`；旧入口扫描确认 CLI 和新模板无旧入口 |
| 主版本号升级 | 全量测试或聚焦断言检查 `pyproject.toml` 为 `1.0.0` |

## 风险接受

- 历史归档任务包仍可能包含 `verification.verify_by`。接受理由：归档区是历史证据，不作为当前任务事实源；本轮非目标是不批量迁移归档。
- TASK-023 仍可能需要后续人工按新字段更新后才能继续推进。接受理由：本轮不处理 TASK-023 的验证交接内容，只改变协议模型；如果它后续被继续推进，应按新结构更新自身 `task-info.yaml`。
- `rg` 扫描只覆盖 CLI、模板、阶段说明和测试，不扫描任务包历史文档。接受理由：需求和设计文档需要保留 `verify_by` 作为历史背景和反例。

## 验证执行计划

实现完成后立即执行全部必需命令。执行环境为仓库根目录 `/home/Shaokun.Tang/Projects/openharness`，Python 命令必须使用 `uv run ...`。

- 验证失败时：回到 `implementing` 修改代码，或回到 `verification_designing` 修正策略。
- 如果失败原因是验证命令过宽或过窄，回到 `verification_designing` 修改本文件。
- 如果失败原因是代码、模板或阶段说明仍使用旧协议入口，回到 `implementing` 修改实现。
