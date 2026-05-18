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
- **Planned Path**：人工审核受影响 skill 和模板中的 transition 指令，对照 `openharness_cli/workflows.py` 的 gate 状态和 `transition_engine.py` 的不可跳级规则。
- **Path Notes**：本轮不新增针对性测试；完成后运行现有测试套件，确认未破坏协议文档和 CLI 行为。

## Required Commands
```bash
uv run pytest
```

## Expected Outcomes
- `verification-designing` skill 的完成命令是 `openharness task-package transition <task> verification_designed`。
- `implementing` skill 的完成命令是 `openharness task-package transition <task> implemented`。
- `task-package.task-info.yaml` 模板中的 mechanical 流程包含 `requirements_designed[G]`。
- `task-package.verification_design.md` 模板不再要求设计阶段填写 `Executed Path`。
- 现有测试通过。

## Traceability
- Required Outcome 1 通过审核 `skills/using-openharness/SKILL.md` 完成。
- Required Outcome 2 通过审核 `states/verification-designing/SKILL.md` 和 `states/implementing/SKILL.md` 完成。
- Required Outcome 3 通过审核 `references/templates/task-package.task-info.yaml` 和 `references/templates/task-package.verification_design.md` 完成。

## Risk Acceptance
接受风险：未新增针对性测试，未来若再次大改状态机，仍需要同步审核 skill 和模板。这个风险由用户明确接受，因为本轮目标是快速对齐已知漂移。

## Verification Execution Plan
- 实现完成后立即执行人工审核和 `uv run pytest`。
- 如果发现新的不一致，只修与当前 CLI 状态机直接冲突的文档，不扩大到流程重设计。
