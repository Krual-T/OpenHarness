# 详细设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 可观察性与验证准备

主验证路径：

- `uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_yaml_quoting.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py`
- `uv run pytest`
- `rg -n "verify_by|VerifyBy" openharness_cli skills/using-openharness/references/templates skills/using-openharness/states tests/openharness_cases`

降级路径：

- 如果定向测试失败，先修正模型、模板或阶段说明，再运行全量 `uv run pytest`。
- 如果 `rg` 仍在新协议入口中发现 `verify_by` 或 `VerifyBy`，不能宣称完成；只有任务包需求和总体设计中作为历史背景出现时可接受。
- 如果旧活跃任务包因不兼容字段阻塞，应按新结构更新该任务包的 `task-info.yaml`，不能恢复旧字段兼容。

预期证据：

- 新建任务包模板生成 `verification.method` 和 `verification.rwp`，不生成 `verification.verify_by`。
- 缺失 `verification.method` 时，需求门禁报告 `verification method is not determined`。
- `verification.method: rwp` 或其他未知值时，校验报告 `unknown verification.method`。
- 阶段指令渲染上下文包含 `verification_method`、`rwp_enabled`、`rwp_reason`，不再依赖 `verify_by`。
- `pyproject.toml` 主版本号从 `0.x.y` 提升到 `1.0.0`。

## 新增或修改文件

- `openharness_cli/models/verification_method.py`：新增 `VerificationMethod` 枚举，只包含 `unit_test` 和 `qualitative`。
- `openharness_cli/models/verification_info.py`：改造验证配置模型，解析 `method`、保存 `raw_method`、解析 `rwp.enabled` 和 `rwp.reason`。
- `openharness_cli/models/task_package.py`：暴露 `verification_method`、`raw_verification_method`、`rwp_enabled`、`rwp_reason` 属性，供上层消费。
- `openharness_cli/workflows.py`：需求门禁改为检查 `verification.method` 和 RWP 确认字段。
- `openharness_cli/validate.py`：校验 `verification.method` 枚举和 `verification.rwp.enabled` 布尔语义。
- `openharness_cli/display.py`：阶段模板渲染上下文改为新字段。
- `openharness_cli/commands/task_package.py`：transition 后使用更新后的 package 渲染阶段说明，避免 hook 读旧对象。
- `openharness_cli/__init__.py`、`openharness_cli/models/__init__.py`：导出 `VerificationMethod`，移除 `VerifyBy`。
- `skills/using-openharness/references/templates/*.md`、`task-package.task-info.yaml`：任务包模板和验证模板改为新结构。
- `skills/using-openharness/states/*/instructions.md`：阶段说明改为按 `verification_method` 与 `rwp_enabled` 分支。
- `tests/openharness_cases/*.py`：更新字段断言、门禁错误、协议文档断言和流程测试。
- `pyproject.toml`：按不兼容改造升级主版本号。

## 接口

稳定 YAML 契约：

```yaml
verification:
  method: <unit_test | qualitative>
  rwp:
    enabled: <true | false>
    reason: <启用或不启用的理由>
```

模型接口：

- `VerificationInfo.method: Optional[VerificationMethod]`：解析成功后的主要验证方法。
- `VerificationInfo.raw_method: str`：用户写入的原始 `method` 字符串。未知值不会丢失，供校验输出精确错误。
- `VerificationInfo.rwp: RwpVerificationInfo`：RWP 独立配置。
- `RwpVerificationInfo.enabled: Optional[bool]`：`None` 表示未确认；`True` 和 `False` 都是已确认。
- `RwpVerificationInfo.reason: str`：启用或不启用的理由。

任务包属性：

- `TaskPackage.verification_method` 返回解析成功的 `method` 值。
- `TaskPackage.raw_verification_method` 返回原始 `method` 值。
- `TaskPackage.rwp_enabled` 返回 `"true"`、`"false"` 或空字符串，便于 Jinja 分支。
- `TaskPackage.rwp_reason` 返回确认理由。

错误传播：

- 缺失 `method` 由 `workflows.py` 的需求门禁报告，阻止状态推进。
- 未知 `method` 由 `validate.py` 报告 `unknown verification.method`。
- `rwp.enabled` 不是布尔值由 `validate.py` 报告类型错误。
- `rwp.reason` 缺失由需求门禁报告，避免静默默认。

## 模块内部设计

- 解析层：`VerificationInfo.from_dict()` 只读取 `method` 和 `rwp`。旧 `verify_by` 留在 `_extra` 中，不转换成新字段。
- 序列化层：`VerificationInfo.to_dict()` 输出 `method` 和 `rwp`；如果 `raw_method` 是未知值，原样写回 `method`，避免失败路径改写用户输入。
- 门禁层：`_check_requirements_gate()` 只判断是否完成需求阶段确认，不负责枚举错误诊断。
- 校验层：`validate_task_package()` 负责报告未知枚举、RWP 类型错误等结构问题。
- 展示层：`display._render_template()` 只向阶段模板提供新字段，不再提供 `verify_by`。
- 文档层：阶段说明负责解释用户确认规则、RWP 启用规则和各阶段分支行为。

## 数据语义

- `verification.method`：主要验收方法。只能是 `unit_test` 或 `qualitative`。
- `verification.rwp.enabled`：是否启用运行时工作流证据。必须显式为布尔值，不能用字符串 `"true"` 或 `"false"`。
- `verification.rwp.reason`：需求阶段确认记录。即使 `enabled: false` 也必须填写。
- `verification.verify_by`：旧字段。不读取、不转换、不作为新任务包入口。若同时存在新旧字段，CLI 只消费新字段；旧字段作为额外未知数据保留。
- `method: rwp`：非法值。它不是缺失字段，而是未知方法，应通过校验暴露。

## 阶段门禁

- 实现落点已限定在 CLI 模型、门禁、校验、模板、阶段说明、测试和版本号。
- `VerificationInfo.raw_method` 必须存在，避免未知方法被吞掉。
- `rwp.enabled: false` 必须被视为已确认，不得因为布尔假值被门禁误判为缺失。
- 阶段模板上下文不得继续依赖 `verify_by`。
- 测试必须覆盖缺失字段、非法方法、模板生成和协议文档清理。

## 决策闭合

- 接受：保存 `raw_method`。理由是未知方法需要被精确报告，不能和缺失字段混为一类。
- 拒绝：继续导出 `VerifyBy` 作为别名。替代方案是新增并只导出 `VerificationMethod`。理由是本轮明确不兼容，保留旧名称会延续错误语义。
- 延期：批量迁移历史归档任务包。触发条件是未来需要对归档包运行新校验或重新激活旧任务包。

## 错误处理

主要失败路径：

- 缺少 `verification.method`：transition 到 `requirements_designed` 时阻塞，提示写入 `verification.method`。
- 缺少 `verification.rwp.enabled`：transition 阻塞，提示确认是否启用 RWP。
- 缺少 `verification.rwp.reason`：transition 阻塞，提示写入理由。
- `verification.method: rwp`：validate 阶段报未知方法，提示期望值只有 `qualitative` 和 `unit_test`。
- `verification.rwp.enabled: "false"`：validate 阶段报类型错误，提示必须是布尔值。

静默出错风险：

- 如果 `from_dict()` 遇到未知 `method` 后只把 `method` 置空，用户会看到“method 未设置”，但真正问题是写了非法值。通过 `raw_method` 保留原始值，并在 `validate.py` 中报告未知枚举来避免这个问题。

## 迁移说明

迁移顺序：

1. 模型层引入 `VerificationMethod`、`raw_method` 和 `RwpVerificationInfo`。
2. 门禁、校验和模板渲染改为消费新属性。
3. 任务包模板和阶段说明改为新字段。
4. 测试从旧字段断言迁移到新字段断言。
5. 将当前活跃任务包按新结构更新，避免新门禁阻塞自身。
6. 升级 `pyproject.toml` 主版本号。

兼容策略：不兼容。旧 `verification.verify_by` 不读取、不转换、不自动迁移。

切换点：模板、门禁、阶段说明和测试全部改为新字段后，`verify_by` 不再是新任务包协议入口。

回滚触发点：如果新字段导致 CLI 无法发现或推进任何活跃任务包，回滚到上一提交；不通过临时恢复双读来掩盖问题。

## 推荐图示

不需要图示。字段结构和消费链可以由 YAML 片段、文件清单和测试覆盖表达清楚。

## 反思

验证策略挑战：单靠协议文档断言是否足够？

结论：不够。字段模型会影响 CLI 行为，必须用单元测试覆盖任务包创建、门禁、校验和阶段输出；文档断言只负责确认新协议入口不再写错。

接口边界挑战：是否需要让 `rwp.enabled: false` 也强制写理由？

结论：需要。RWP 是用户确认开关，不启用也是决策。没有理由会让后续验证阶段无法判断这是主动排除还是遗漏。
