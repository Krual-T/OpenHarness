# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 实现完成后运行 `uv run openharness check-tasks`。
  - 如果修改了 bootstrap 或相关测试表面，再运行对应 pytest 用例。
  - 人工检查仓库入口、作者入口页、关键 stage skill 和模板是否形成一致导流。
- Executed Path:
  - 当前仅执行了 `uv run openharness new-task ...` 创建任务包，并完成设计文档编写。
  - 已执行 `uv run openharness check-tasks`，确认新增 task package 在当前设计状态下通过协议校验。
  - 尚未进入实现，因此还没有新鲜的实现级验证结果。
- Path Notes:
  - 本轮目标是把任务边界、总体方案和详细落点收敛到可执行，因此当前验证足以支撑“任务包设计完成且协议有效”，但不足以支撑 `in_progress`、`verifying` 或 `archived`。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run openharness check-tasks`

## Expected Outcomes
- task package 协议保持通过。
- 中文作者入口与 guidance 导流在用户真实入口表面上可见。
- 模板提示更具体，但没有显著膨胀。

## Traceability
- `01-requirements.md` 要求解决中文入口不可见与 guidance 难发现的问题。
- `02-overview-design.md` 通过“单一中文作者入口 + 多表面导流 + 模板轻增强”定义总体方案。
- `03-detailed-design.md` 已经把实现落点、降级路径和验证方式写清。
- 当前缺口是实现证据尚未产生，因此只能证明设计已经完成，不能证明优化效果已经落地。

## Risk Acceptance
- 当前接受“尚未实现”的风险，因为本轮目标是先把任务推进到可执行设计。
- 如果后续实现后用户仍然反馈 guidance 难发现，说明入口层设计不够，需要重新审查作者入口、导流位置和模板增强幅度。

## Latest Result
- 最近一次结果是：`uv run openharness check-tasks` 通过，说明 `OH-034` 当前作为设计完成的任务包是协议有效的；实现级验证尚未开始。
- Latest Artifact:
  - 无
