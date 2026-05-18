# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 按 `task-info.yaml.verification.verify_by` 类型选择对应章节填写。不要求全部填写——只写实际执行的。

## Verification Result
- **verify_by**: qualitative
- **Result**: passed

## Test Results

```bash
uv run pytest
```

结果：51 passed, 1 skipped。

变更文件：
- `skills/using-openharness/SKILL.md`：补充 CLI 注入边界和活跃状态到 gate 状态的 transition 表。
- `skills/using-openharness/states/verification-designing/SKILL.md`：完成命令改为 `verification_designed`。
- `skills/using-openharness/states/implementing/SKILL.md`：完成命令改为 `implemented`。
- `skills/using-openharness/states/detailed-design/SKILL.md`：实际执行结果只进入 `evidence.md`。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：mechanical 状态流补回 `requirements_designed[G]`。
- `skills/using-openharness/references/templates/task-package.verification_design.md`：验证策略模板改为计划和回退路径，不再要求 `Executed Path`。
- `skills/using-openharness/references/templates/task-package.README.md`：README 模板章节改为校验器要求的 `## Overview`。
- `tests/openharness_cases/test_protocol_docs.py`：既有协议测试断言从 `Executed Path` 同步为 `Fallback Path`。

## Semantic Review

审核对象：
- `skills/using-openharness/SKILL.md`：入口说明已明确 `new`、`view`、`transition` 会注入当前活跃状态 skill，并要求活跃阶段完成后 transition 到对应 gate。
- `skills/using-openharness/states/verification-designing/SKILL.md`：完成命令已改为 `verification_designed`，与 `workflows.py` 中 gate 推进到 `implementing` 一致。
- `skills/using-openharness/states/implementing/SKILL.md`：完成命令已改为 `implemented`，与 `workflows.py` 中 gate 推进到 `verifying` 一致。
- `skills/using-openharness/states/detailed-design/SKILL.md`：已明确 `verification_design.md` 写计划，实际执行结果进入 `evidence.md`。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：mechanical 流程已补回 `requirements_designed[G]`。
- `skills/using-openharness/references/templates/task-package.verification_design.md`：验证策略模板已从 `Executed Path` 改为 `Fallback Path`，不再要求设计阶段记录实际执行。
- `skills/using-openharness/references/templates/task-package.README.md`：模板标题已改为 `## Overview`，匹配 `TaskPackageDocument.README` 的校验要求。

发现：
- 已关闭：状态 skill 曾提示跳过 gate，现已改为指向 gate 状态。
- 已关闭：mechanical 流程注释曾漏掉 `requirements_designed[G]`，现已对齐。
- 已关闭：验证设计模板曾混入执行结果语义，现已回到计划语义。
- 已关闭：README 模板标题曾与校验器不一致，现已对齐。

结论：通过。

## Runtime Observation

不适用。

## Residual Risks
本轮未新增针对性测试。该风险由用户明确接受；如果后续再次调整状态机，需要同步人工审核 skill 和模板中的流程指令。

## Follow-ups
无。
