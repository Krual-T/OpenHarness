# Verification Strategy

## Verification Path

- **Planned Path**：执行 `uv run pytest tests/openharness_cases -q`。
- **Fallback Path**：如果全量测试失败，按失败范围单独运行相关测试文件，并在修复后重新跑全量。
- **Path Notes**：本轮改动是 CLI 行为和协议模板，`tests/openharness_cases` 覆盖核心命令、模型、模板和协议文档。

## Required Commands

```bash
uv run pytest tests/openharness_cases -q
```

## Expected Outcomes

期望所有 OpenHarness 用例通过。关键场景包括：

- 新建任务包只创建当前阶段需要的文件。
- 状态推进会创建下一活跃阶段的工作文件。
- 归档成功后源目录不存在。
- 归档目标已存在时源包保持原状态。
- 模板和状态指令都使用无前缀语义文件名。

## Traceability

- Requirements 1-2 由归档成功测试和归档目标冲突测试覆盖。
- Requirements 3-5 由新建包测试、模板测试和协议文档测试覆盖。
- Requirements 6 由全量 `tests/openharness_cases` 结果覆盖。

## Risk Acceptance

接受历史归档包仍保留旧文件名的风险，因为历史包是事实记录，本轮明确不迁移历史归档。后续如果需要统一历史格式，应另开任务包。

## Verification Execution Plan

实现完成后立即执行全量 pytest，并把结果写入 `evidence.md`。
