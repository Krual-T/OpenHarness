# Verification Strategy

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **本文件在 `verification_designing` 阶段编写（TDD 红阶段，先于实现）**。
> 定义验证策略——计划怎么验证、用什么命令、期望什么结果。
> 实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。
>
> **使用前先确认你能回答这些问题**：
> - 每项 Required Outcome 是否有对应的验证方法？
> - 验证命令是否具体到可以直接复制粘贴执行？
> - 是否有边界或错误场景的验证？
> - 哪些风险本轮不覆盖，接受理由是什么？
> - 计划路径和回退路径分别是什么？

## Verification Path
- **Planned Path**：增加 CLI 回归测试，构造 verifying 状态任务包和非空 evidence，执行 `transition <task> verified`，断言输出归档成功且任务包移动到 archived root。
- **Fallback Path**：如果 CLI runner 构造复杂，直接测试 `execute_transition()` 的归档结果对象，再保留现有 CLI 测试覆盖显示层。
- **Path Notes**：主路径能覆盖用户看到的错误输出，因此足够支撑本轮修复。

## Required Commands
```bash
uv run pytest
```

## Expected Outcomes
- 新增或调整的测试失败于旧实现，修复后通过。
- 全量测试通过。

## Traceability
- Required Outcome 1 由自动归档 CLI 测试覆盖。
- Required Outcome 2 由直接归档 CLI 测试或现有路径覆盖。
- Required Outcome 3 由原有 `already in` 分支保留和现有测试行为覆盖。

## Risk Acceptance
接受风险：本轮只修归档结果显示，不重构所有 transition 结果语义。若后续新增更多终态副作用，再考虑把结果类型进一步细分。

## Verification Execution Plan
- 实现完成后运行 `uv run pytest`，把结果写入 `evidence.md`。
