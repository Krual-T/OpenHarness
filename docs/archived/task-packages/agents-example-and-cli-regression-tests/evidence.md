# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 按 `task-info.yaml.verification.verify_by` 类型选择对应章节填写。不要求全部填写——只写实际执行的。

## Verification Result
- **verify_by**: unit_test
- **Result**: passed

## Test Results

命令：
```bash
uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py -q
```
结果：23 passed，退出码 0。

命令：
```bash
rg -n "STATUS\.yaml|openharness bootstrap|manifest\.yaml|systematic-debugging" AGENTS.example.md
```
结果：无匹配，退出码 1（符合预期，表示未发现旧协议关键词）。

命令：
```bash
uv run pytest tests/openharness_cases -q
```
结果：51 passed, 1 skipped，退出码 0。

变更文件：
- `AGENTS.example.md` — 将示例协议从旧 `STATUS.yaml` / `bootstrap` / `manifest.yaml` 表述更新为当前 `task-info.yaml`、`task-package list`、`task-package view` 和 transition 归档流程。
- `tests/openharness_cases/test_cli_workflows.py` — 新增 `task-package view` 注入当前阶段 skill 的 CLI 回归测试。
- `tests/openharness_cases/test_task_package_core.py` — 新增 gate 前置条件失败时不写入中间状态的回归测试。

验收标准覆盖：
| 标准 | 证据 |
|------|------|
| `AGENTS.example.md` 不再引用废弃协议 | `rg` 旧关键词无匹配 |
| `task-package view` 输出任务详情并注入状态 skill | `test_task_package_view_injects_current_stage_skill` |
| gate 失败不落盘 | `test_gate_precondition_failure_does_not_persist_intermediate_status` |

## Semantic Review

`verify_by: qualitative` 时填写：

- 审核对象（文件、文档、设计）
- 发现（问题、改进点）
- 结论
- 问题是否已闭合

## Runtime Observation

`verify_by: rwp` 时填写：

- 工作流名称
- 观察结果
- 产物路径
- 盲区说明

## Residual Risks
- 本轮没有清理 archived 历史任务包中的旧协议引用；这些文件保留为历史事实。
- transition 后 validation 失败仍可能留下已写入状态，本轮没有扩大修复，因为用户指定的是 gate 失败不落盘测试。

## Follow-ups
无。
