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
- **Planned Path**：先运行聚焦测试验证新增行为，再运行完整 OpenHarness 测试套件确认没有破坏现有协议。
- **Executed Path**：在 `verifying` 阶段写入实际命令、退出码和结果。
- **Path Notes**：本轮验证对象是文档协议一致性和 CLI 行为回归，`unit_test` 足以覆盖新增 CLI 行为；文档一致性通过测试断言和全文搜索辅助确认。

## Required Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py -q`
- `uv run pytest tests/openharness_cases -q`

## Expected Outcomes
- 聚焦测试通过，覆盖 `task-package view` 注入当前状态 skill 和 gate 失败时不修改 `task-info.yaml.status`。
- 完整 OpenHarness 测试通过。

## Traceability
- Required Outcome 1 由 `AGENTS.example.md` diff、全文搜索和完整测试的协议文档断言支撑。
- Required Outcome 2 由新增 `task-package view` CLI 测试支撑。
- Required Outcome 3 由新增 gate 失败不落盘测试支撑。

## Risk Acceptance
- archived 历史任务包中的旧术语保留，作为历史事实，不纳入本轮清理。
- verifying/implementing 的 evidence 语义仍有后续优化空间，但不影响本轮示例协议和 CLI 回归测试目标。

## Verification Execution Plan
- 实现完成后由 Codex 在当前仓库根目录执行 Required Commands。
- **Fallback**：如果聚焦测试失败，回到 `implementing` 修正测试或被测行为；如果完整测试因无关历史问题失败，在 `evidence.md` 记录阻塞并保留聚焦测试结果。
