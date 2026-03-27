# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先补与入口边界相关的协议测试或文档断言，确认新的 intake routing 约束和首轮回复边界已经落到稳定表面。
  - 再运行现有入口协议与 CLI 工作流测试，确认这轮设计不会破坏 `bootstrap` 当前承担的阶段可见性与 task-package 协议。
  - 最后运行仓库级 task package 校验。
- Executed Path:
  - 本轮先新增协议测试，覆盖 `using-openharness` 对 `bootstrap` 前台/后台角色的边界、阶段播报的自然化要求，以及 `brainstorming` 对用户可见 handoff 的限制。
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -k 'routes_bootstrap_by_request_axis or natural_user_visible_stage_updates or focused_on_problem_not_log_labels' -q`，先确认新增约束在实现前失败，再在实现后通过。
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`，结果为 51 passed。
  - 已执行 `uv run openharness check-tasks`，确认归档后的 `OH-035` 与仓库其余 task package 一起通过协议校验。
  - 已执行 `uv run openharness bootstrap`，确认默认 active package 列表中已不再出现 `OH-035`。
- Path Notes:
  - 本轮没有修改 `bootstrap` 的核心 CLI 行为；最终实现收敛在 skill 协议与协议测试，这是当前最小且足够的落点。
  - `test_cli_workflows.py` 本轮未重跑，因为没有改动 CLI 输出结构；现有证据已经能证明本轮要求的协议边界和仓库 task package 协议成立。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
- `uv run openharness check-tasks`

## Expected Outcomes
- 入口协议文档能够明确区分不同任务类型下 `bootstrap` 的前台或后台角色。
- 首轮用户可见回复的阶段播报仍然存在，但不再鼓励把执行日志标签直接暴露给用户。
- `check-tasks` 通过，证明新增任务包与更新后的设计文档仍满足仓库协议。

## Traceability
- `01-requirements.md` 定义了三个核心问题：主轴判断、`bootstrap` 角色边界、首轮回复自然度。
- `02-overview-design.md` 把问题收敛成 intake routing、context gathering、user-visible reply 三层结构。
- `03-detailed-design.md` 将这些结论映射到 skill、CLI、测试和实施顺序。
- `skills/using-openharness/SKILL.md` 和 `skills/brainstorming/SKILL.md` 已实现协议约束。
- `tests/openharness_cases/test_protocol_docs.py` 用新增断言和全量通过结果覆盖这些约束是否真实落地。
- `uv run openharness check-tasks` 证明任务包写回和归档没有破坏仓库协议。

## Risk Acceptance
- 当前接受的残余风险是：本轮约束主要落在 skill 协议和协议测试，还没有引入更贴近真实对话样例的自动化验证。
- 接受理由是本轮目标本来就是先把边界写成正式仓库协议，而不是一次性把所有对话行为都做成样例测试系统。
- 如果后续仍持续出现“首轮回复像执行日志”的实际问题，应重新审查是否新增更强的样例测试或辅助表面。

## Latest Result
- 最近一次结果为通过：新增协议测试已通过，`test_protocol_docs.py` 全量通过，`uv run openharness check-tasks` 也通过；`OH-035` 已实现、验证并归档。
- Latest Artifact:
- protocol-doc assertions, task-package validation, and archived-package absence from default bootstrap on 2026-03-27
