# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - task package 协议校验：`uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - 文档与 skill surface 回归：`uv run pytest skills/using-openharness/tests/test_openharness.py`
- Fallback Path:
  - 如果 `check-tasks` 失败，本轮最多只能宣称“文档草案已更新”，不能宣称能力模型已经 productize。
  - 如果 pytest 因 wording 断言失败，必须继续收敛 live docs 和测试，不能只以人工解释替代。
  - 如果只完成文档修改而没有同步测试，本包不能进入 `archived`。
- Planned Evidence:
  - `OH-018` 自身的 requirements、overview、detailed、verification 和 evidence 文档。
  - README、`brainstorming`、`exploring-solution-space`、skill hub 的 live wording 变更。
  - `test_openharness.py` 中新增或更新的断言。

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `README.md`
  - 调整产品定位与工作流叙述，让方法论能力成为主叙事。
- `skills/brainstorming/SKILL.md`
  - 调整视觉辅助的定位，并补入产品价值与业务影响层面的脑暴检查项。
- `skills/exploring-solution-space/SKILL.md`
  - 补强总体设计、详细设计与反思时对用户价值、业务影响、测试边界和 review 视角的要求。
- `skills/using-openharness/references/skill-hub.md`
  - 把 skill surface 的核心能力表达为设计、测试、review 和多智能体协作，并明确 companion 是按需工具。
- `skills/using-openharness/tests/test_openharness.py`
  - 新增或调整断言，防止 live wording 退回工具导向。

## Interfaces
本轮不引入新的脚本接口或 CLI，只修改面向代理和维护者的文本协议：

- README 是对外产品接口，决定维护者第一次如何理解 OpenHarness。
- `brainstorming` 和 `exploring-solution-space` 是核心认知流程接口，决定代理如何组织脑暴、设计和反思。
- skill hub 是核心能力索引接口，决定仓库如何解释“哪些是核心能力，哪些是可选辅助”。
- `test_openharness.py` 是这些文本接口的回归保护层。

稳定边界：

- 不新增新的 entry skill。
- 不改变 task package 文件结构。
- 不改变 runtime capability contract 的定义，只调整产品叙事中对浏览器和视觉辅助的相对位置。

## Error Handling
主要风险不是代码报错，而是能力表述漂移：

- 如果 README 说“方法导向”，但 skill docs 仍然突出浏览器 companion，读者仍会得到错误心智模型。
- 如果只在 skill docs 中加入 product/CEO 视角，而 README 不提，外部读者仍然看不到这项核心价值。
- 如果把这些视角写成空泛口号，没有绑定到具体检查项，就会再次退化成“听起来对，但执行时没人用”。

所以处理原则是：

- 每个新增能力表述都要落到明确的 skill stage 或检查项。
- 每条关键 live wording 都尽量由测试锁定。
- 对浏览器 companion 只强调“何时用”，不扩写成新的默认流程。

## Migration Notes
实施顺序：

1. 先修改 README，确定外层产品叙事。
2. 再修改 `brainstorming`、`exploring-solution-space` 和 skill hub，让核心能力与 README 对齐。
3. 最后更新 pytest 断言，保证 live wording 与协议一致。

兼容策略：

- 现有使用 visual companion 的能力保持兼容，只是被更明确地标注为按需工具。
- 现有 reflection、subagent discussion、review loop 不改变机制，只提升其在产品叙事中的可见度。

回滚注意事项：

- 如果某条新文案让 skill 语义变得模糊，优先回退那条文案，而不是回退“方法论优先”的总体方向。
- 如果测试发现 wording 与既有断言大面积冲突，应先调整断言设计，确保它们固定的是能力边界，而不是某个偶然句式。

## Detailed Reflection
我先挑战了测试策略。文本协议类改动最容易出现“改的时候觉得清楚，几天后又漂回去”，所以必须由现有 pytest 文本断言保护，而不是只靠人工记忆。

我也挑战了接口边界。最初可以把“产品视角”写进 `brainstorming` 就结束，但那会遗漏总体设计和详细设计阶段的商业影响权衡，因此必须同时覆盖 `exploring-solution-space`。

我还检查了迁移假设是否过度。因为本轮没有新增脚本或运行时 helper，落地成本主要在文档和测试一致性，不会触发额外环境依赖。

最后我确认了验证路径的强弱。对这种任务来说，`check-tasks` 加目标 pytest 已经足够；再去追求浏览器运行时验证反而会偏离用户提出的问题。
