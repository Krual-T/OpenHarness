# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 OpenHarness 的 live 产品定位和技能协议收敛到“吸纳设计与协作能力”这条主线上，而不是让读者误以为它主要在卖某个浏览器辅助或固定运行环境。

## Problem Statement
仓库当前已经具备不少你想要的能力雏形，例如：

- `brainstorming` 负责需求脑暴与收敛。
- `exploring-solution-space` 负责探索、总体设计与反思。
- 设计阶段已经要求 reflection 和 bounded subagent discussion。
- `test-driven-development`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion` 已经覆盖测试与评审。

但 live surface 仍然有两个问题：

- 浏览器相关内容虽然本质上只是视觉问题下的可选辅助，却在 `brainstorming` 中足够显眼，容易让人误读成 OpenHarness 的重要卖点甚至前置依赖。
- README 和技能总览还没有把“真正核心吸纳的是设计方法、测试方法、多智能体讨论与反思，以及带着产品价值判断去思考”表达得足够集中。

这会带来实际偏差：做后端项目、前后端分离项目或纯服务型项目的人，容易先看到一个与自己不相干的视觉辅助，而不是先看到自己真正需要的设计与协作工作流。

## Definitions
- `live surface`
  - 本轮需要直接对齐的 live 文件集合：`README.md`、`skills/brainstorming/SKILL.md`、`skills/exploring-solution-space/SKILL.md`、`skills/using-openharness/references/skill-hub.md`，以及固定这些表述的 `skills/using-openharness/tests/test_openharness.py`。
- `capability model`
  - OpenHarness 对外强调的核心能力集合：需求脑暴、探索与总体设计、详细设计与反思、测试与评审、bounded multi-agent collaboration、验证闭环。
- `visual companion`
  - `brainstorming` 下仅在视觉问题里按需使用的浏览器辅助工具；它不是仓库安装前提，不是通用任务的默认主路径，也不是能力模型的第一入口。
- `product/value checks`
  - 非人格化的方法论检查项，用来提醒代理在需求与设计阶段显式检查用户问题、预期价值、业务影响、范围边界和过度设计风险；它们不是新 persona，也不是新的 entry skill。
- `review loops / multi-agent execution helper`
  - 指已有的 review、bounded discussion、subagent-driven execution 等机制；本轮只提升它们在 live surface 中的可见度，不新增新的工具链、脚本或命令。

## Artifacts In Scope
- `README.md`
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/tests/test_openharness.py`

## Artifacts Out Of Scope
- `INSTALL.codex.md`
- `skills/brainstorming/references/visual-companion.md`
- runtime helper skills、runtime surface map 和 runtime capability contract 细节
- 新增 product、CEO、reviewer 等独立 persona skill
- 新增浏览器安装、浏览器测试或前端 runtime baseline
- 新增任何新的 skill、脚本或命令来承载本轮 capability model 对齐

## Required Outcomes
1. README 要新增或重写一段明确的核心能力描述，至少同时覆盖：
   - 需求脑暴
   - 探索、总体设计、详细设计
   - reflection 与 bounded subagent discussion
   - 测试、review loops、verification
   - 这段描述应出现在 runtime capability contract 章节之前，让读者先建立“方法论优先”的产品心智。
   - README 不得把浏览器、visual companion 或任何浏览器安装步骤放在首屏定位段落里，也不得把它们写成默认前置步骤。
2. `brainstorming` 必须把 `visual companion` 明确为视觉问题下的按需工具，并满足以下验收条件：
   - 明确写出它不是默认要求或通用项目主路径。
   - 明确写出非视觉问题默认继续使用 terminal/text。
   - 保留 companion 能力本身，不删除原有按需使用规则。
3. `exploring-solution-space` 和 skill hub 必须把 `product/value checks` 写成具体检查项，而不是人格化角色，并满足以下验收条件：
   - 至少覆盖用户问题、预期价值、业务影响、范围边界四类检查。
   - 检查项要落在明确的技能阶段或反思步骤中，而不是停留在 README 口号。
   - 文案不得要求新增 product/CEO 独立技能或新的强制流程分支。
4. live surface 必须更清楚地描述多智能体协作能力，并至少在以下两个层面可见：
   - 设计阶段的 reflection、bounded subagent discussion/review
   - 实现或验证阶段的 review loops / multi-agent execution helper
5. 测试策略必须使用 `skills/using-openharness/tests/test_openharness.py` 中的关键段落断言来锁定能力边界，而不是整文件快照；断言至少需要覆盖：
   - README 是否先突出核心能力
   - `brainstorming` 是否把 visual companion 定义为 optional
   - `exploring-solution-space` 是否包含 `product/value checks`
   - skill hub 是否把多智能体协作与方法论能力描述为核心工作流的一部分
6. 本包作为一个 focused package 交付，但实施顺序必须清晰分成两个波次：
   - 第一波：文案与信息架构对齐
   - 第二波：测试断言加固

## Non-Goals
- 不移除浏览器视觉辅助本身；本轮只是校正其边界和定位。
- 不把产品视角、CEO 视角、评审视角拆成一组新的 mandatory skills。
- 不为所有项目引入统一的浏览器安装、运行时 helper 或前端测试基线。
- 不借这轮去重写整个 OpenHarness 入口协议或任务包协议。

## Constraints
- 必须保留 `using-openharness` 作为唯一仓库入口技能，不能重新发明第二套入口。
- 必须保留现有 task package、reflection、verification 和 archive 协议，不把这轮变成新的流程体系。
- 多智能体协作仍然要走 bounded context，不能把完整会话历史直接塞给 reviewer 或讨论者。
- README、skill hub 和技能文档的调整需要由关键段落断言固定下来，否则 live wording 很容易再次漂移。
- 测试断言应固定能力边界和术语意图，不应脆弱到依赖整段原文逐字不变。
