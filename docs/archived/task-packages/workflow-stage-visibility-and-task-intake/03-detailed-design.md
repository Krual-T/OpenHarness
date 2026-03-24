# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先运行针对新行为的聚焦测试，确认新增测试先红后绿：
    - `uv run pytest skills/using-openharness/tests/test_openharness.py -k "allocate_next_task_id or scaffolds_task_package_before_exploration_when_missing or requires_explicit_stage_checkpoints or bootstrap_reports_stage_guidance_in_text_output or bootstrap_json_includes_stage_guidance"`
  - 再运行完整 CLI / 协议测试：
    - `uv run pytest skills/using-openharness/tests/test_openharness.py`
  - 最后运行仓库任务包校验：
    - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Fallback Path:
  - 如果完整测试因无关历史问题失败，至少要保留聚焦测试和 `check-tasks` 结果，并在 `05-verification.md` 里明确写出阻塞点，不能宣称本包已完成验证。
  - 如果 CLI 输出断言因为文案微调失败，应优先统一代码与测试口径，而不是删掉阶段播报。
- Planned Evidence:
  - 聚焦测试从失败转为通过的结果。
  - 完整 `test_openharness.py` 的通过结果。
  - `check-tasks` 对 active / archived package 的校验结果。
  - `06-evidence.md` 中记录新增或修改的脚本、技能文档和 README。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/scripts/openharness.py`
  - 增加自动编号与阶段提示逻辑，并把这些信息接到 `bootstrap` / `new-task` 上。
- `skills/using-openharness/tests/test_openharness.py`
  - 先写失败测试，再覆盖自动编号、阶段输出和技能协议文案。
- `skills/using-openharness/SKILL.md`
  - 写明进入新 stage 时的用户播报要求。
- `skills/brainstorming/SKILL.md`
  - 写明没有 package 时的自动建包时机。
- `README.md`
  - 把新的入口体验补进公开说明，避免 live docs 与实现脱节。
- `docs/archived/task-packages/workflow-stage-visibility-and-task-intake/*`
  - 记录这轮需求、设计、验证和证据。

## Interfaces
CLI 接口：

- `bootstrap`
  - 继续保留现有列包行为。
  - 额外输出 `current stage`、`next stage`、`next step`。
  - JSON 模式新增同名字段，避免下游再次推断。
- `new-task`
  - 保留老的 `task_name task_id title` 用法。
  - 新增自动编号路径，使 agent 可以只提供任务名与标题并请求自动编号。

协议接口：

- `brainstorming`
  - 当 requirements 已足够成形且准备进入 exploration 时，如果没有现成 package，应先 scaffold package。
- `using-openharness`
  - 每次进入新 workflow stage，都要向用户播报当前阶段、刚完成的东西和下一步动作。

## Stage Gates
- 必须有失败测试证明新增能力此前不存在。
- 必须有稳定的自动编号策略，且不会破坏已有命令调用。
- 必须同时覆盖文本输出与 JSON 输出，避免“人看得到、工具读不到”。
- 必须把建包时机写进技能协议，而不是只写在 task package 里。
- 必须保留 `check-tasks` 和现有状态流，不引入新的迁移脚本。

## Decision Closure
- 接受：把阶段提示放进 `bootstrap` 主输出，因为它是仓库入口，用户最自然会先看到这里。
- 接受：自动编号采用“扫描现有 task id 后递增”的方式，因为它最简单且足够稳定。
- 拒绝：一进入 brainstorming 就自动建包。理由是会把很多尚未成形的话题固化成噪音 package。
- 拒绝：只靠 README 解释新流程。理由是 README 不能约束 agent 的实际 handoff 行为。
- 延期：是否在进入 `in_progress` 前增加强制人工确认。触发条件是后续继续观察到“设计未审核即实现”的体验问题仍然明显。

## Error Handling
- 如果仓库中没有任何可解析的带前缀编号，自动编号要退回稳定默认前缀，而不是崩溃。
- 如果用户同时提供手工 `task_id` 与自动编号开关，优先按显式输入处理或直接报错，避免静默覆盖。
- 如果 `bootstrap` 没有找到 package，应继续保持可用输出，不因为缺少阶段信息而报错。
- 如果技能文案和测试不一致，应以当前协议目标为准修正文案，而不是删除断言逃避行为约束。

## Migration Notes
- 先加测试，再补 CLI 行为，再补技能文案，最后更新公开说明与任务包证据。
- 老的 `new-task task_name task_id title` 调用保持不变，因此现有历史 evidence 不需要回写。
- 若需要回滚，可单独回退阶段播报文本或自动编号逻辑，不影响现有 task package 结构。

## Detailed Reflection
我先挑战测试策略：如果只测字符串存在，很容易放过错误的状态映射；因此至少要覆盖文本输出和 JSON 输出两个出口。

我也挑战了接口边界：自动建包真正落点在 skill，而编号能力落点在 CLI。两者必须同时改，否则要么 agent 不会在正确时机建包，要么想建时还会被 `task_id` 卡住。

我检查了迁移假设：只要保留旧的 `new-task` 用法，历史包和旧 evidence 都不需要迁移，这是这轮改动能保持小范围的关键。

没有使用有边界的子智能体讨论，因为这轮变化主要是仓库内协议与入口脚本协同，分歧点已经在前一轮分析中收敛。
