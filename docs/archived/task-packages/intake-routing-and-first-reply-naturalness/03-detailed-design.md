# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先补协议与行为相关的聚焦测试，覆盖至少三类判断：何时前台使用 `bootstrap`、何时只后台使用、何时首轮回复不应以执行日志为主。
  - 再执行与入口协议、CLI 输出和文档表面相关的现有测试，确保这轮边界调整没有破坏现有 task package 协议。
  - 至少执行：
    - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
    - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
    - `uv run openharness check-tasks`
- Fallback Path:
  - 如果新的行为测试本轮尚未落地，不能宣称这个任务已验证完成，只能停留在设计完成状态。
  - 如果 CLI 测试因文案细节波动失败，应先确认失败的是“字符串细节”还是“角色边界回归”；不能为了过测试而撤掉边界约束。
  - 如果 `check-tasks` 失败，必须先修复任务包协议问题，再讨论实现是否可继续推进。
- Planned Evidence:
  - 新增或更新的协议文档与测试断言。
  - 任务类型与 `bootstrap` 角色映射的设计证据。
  - 验证命令输出与 `check-tasks` 结果。
  - `04-verification.md` 中对入口行为覆盖面的归档说明。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/SKILL.md`
  - 需要补充 intake routing 边界，明确何时应把 active task context 拉到台前，何时只把 `bootstrap` 作为后台上下文。
- `skills/brainstorming/SKILL.md`
  - 需要校准“向用户说明当前阶段”的表达方式，避免把它实现成执行日志回放。
- `skills/exploring-solution-space/SKILL.md`
  - 需要保持与新的入口分层一致，避免在探索阶段再次把上下文工具误当成用户主轴。
- `openharness_cli/commands.py`
  - 可能需要补充对 `bootstrap` 角色的帮助文案或输出定位，但不应破坏现有列包和阶段可见性。
- `tests/openharness_cases/test_protocol_docs.py`
  - 需要覆盖 skill 协议层面对入口边界和首轮回复约束的表达，避免文档与行为再次漂移。
- `tests/openharness_cases/test_cli_workflows.py`
  - 如果 CLI 输出定位发生变化，需要同步覆盖文本与 JSON 表面，确认“可见性保留、前台化受限”同时成立。
- `docs/task-packages/intake-routing-and-first-reply-naturalness/*`
  - 记录需求、设计、验证和证据。

## Interfaces
入口协议接口：

- `using-openharness`
  - 输入是用户当前请求与仓库协议上下文。
  - 输出应先是任务主轴判断，再决定是否需要 active task context。
  - 稳定边界是：它仍然是唯一仓库入口 skill，但不能把所有请求都下沉成同一条 task-package 执行流。

上下文工具接口：

- `openharness bootstrap`
  - 继续输出 active task package、stage guidance 和 author entry 等事实。
  - 其稳定边界是“提供上下文事实”，而不是“默认成为所有首轮回复的主叙事”。
  - `observability` 入口是 CLI 文本输出、JSON 输出和相关测试断言。

用户可见回复接口：

- 首轮回复必须至少回答三件事：现在主要在判断什么、刚确认了哪个关键事实、下一步准备怎么推进。
- 首轮回复不应把命令标签、路径列表、原始 CLI 输出或 `Explored` / `Ran` 这类内部执行痕迹当作主要内容。
- `observability` 入口是协议文档中的明确规则，以及必要时新增的测试断言或样例约束。

## Stage Gates
- 必须明确测试先覆盖哪几类入口请求，以及这些场景各自期望的 `bootstrap` 角色。
- 必须明确至少一个可观察信号来识别“首轮回复又退化成执行日志回放”。
- 必须明确协议改动落点和 CLI 改动落点的分工，避免再次把问题全塞给单一表面。
- 必须明确迁移顺序：先定协议边界，再补测试，再决定是否需要 CLI 辅助调整。
- 必须明确后续 `04-verification.md` 需要收集的证据类型，而不只是运行命令结果。

## Decision Closure
- 接受：把“主轴判断先于 `bootstrap`”作为本轮核心约束，因为它直接决定入口是否会错位。
- 接受：保留阶段播报，但要求它服务于当前任务叙事，而不是回放命令顺序。
- 拒绝：通过禁用 `bootstrap` 一刀切解决自然度问题。理由是会损失 active task 推进场景的有效入口。
- 拒绝：只靠文案润色解决问题。理由是没有路由边界的文案很容易再次漂移。
- 延期：是否引入更正式的对话样例测试。触发条件是协议文本和现有测试仍无法稳定约束入口体验。

## Error Handling
- 主要失败路径一：请求明明是评估或局部讨论，却被误判成 active task 推进，导致前台出现无关的 `bootstrap` 输出。
- 主要失败路径二：为了追求自然，代理完全不再说明当前阶段、刚完成什么和下一步，导致 workflow 透明度下降。
- 误用风险：把 `bootstrap` 的“可以提供上下文”误读成“应该默认前置”。
- 静默出错风险：回复表面看起来更顺，但其实仍然在后台沿用错误的主轴判断，只是把日志包装得更像人话。
- 规避方式：测试和文档都要同时覆盖“路由是否正确”和“展示是否自然”，而不是只测其中一侧。

## Migration Notes
- 先更新 `OH-035` 的设计文档，固定问题边界和推荐结构。
- 再修改 skill 协议，明确 intake routing、`bootstrap` 角色和首轮回复边界。
- 然后补充或调整测试，确保协议约束有稳定落点。
- 最后再决定 CLI 是否需要同步补充帮助文案或输出说明；若不需要，不应为了“看起来完整”而硬改 CLI。
- 回滚触发点是：如果实现后发现 active task 推进场景的信息透明度明显下降，应优先回退过度收缩的展示约束，而不是回退整个主轴判断结构。

## Detailed Reflection
- 我先挑战了测试顺序。如果先改 skill 文案再想验证，很容易把边界写成正确口号却没有可观察信号；因此应先明确场景，再写断言。
- 我也挑战了接口分工。如果把主轴判断和上下文工具继续混在一起，后续任何自然度问题都还会反复出现，因此必须显式拆层。
- 我检查了迁移假设：这轮不一定需要大改 CLI，本质上先是协议与测试问题，CLI 只在确实需要强化角色定位时再跟进。
- 当前 detailed 已经足够约束后续实现；如果开始实施，已经知道先补哪类测试、再改哪些 skill、最后决定 CLI 是否需要最小跟进。
