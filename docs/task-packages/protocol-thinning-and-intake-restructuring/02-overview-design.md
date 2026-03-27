# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
这轮 overview 覆盖四类仓库表面：

- 仓库级协议表面：
  - `AGENTS.md`
  - `skills/using-openharness/references/manifest.yaml`
  - `README.md`
- 入口与流程表面：
  - `skills/using-openharness/SKILL.md`
  - `skills/brainstorming/SKILL.md`
  - `skills/exploring-solution-space/SKILL.md`
  - `skills/verification-before-completion/SKILL.md`
- CLI 与状态表面：
  - `openharness bootstrap`
  - `openharness transition`
  - `openharness verify`
  - `openharness check-tasks`
- 约束与回归表面：
  - 当前 `tests/` 中对 entry skill、stage visibility、reflection、author entry、protocol docs 的断言

这轮不覆盖的内容：

- 不重做 task package 的固定文件结构。
- 不引入新的 stage、helper 类型或第二套入口系统。
- 不在这轮直接改实现；本轮只决定下一轮重构的主结构和落点。
- 不为了兼容旧表面而默认保留 README、skill 文本、CLI 输出里所有现有说明。

## Proposed Structure
推荐结构是“三层权威、两类入口、一个状态源”。

三层权威：

- 第一层：`AGENTS.md`
  - 只保留仓库地图、事实来源优先级，以及少量仓库级约定。
  - 不再承载默认工作流、阶段方法、写作方法论、task package 结构协议或验证流程编排。
- 第二层：`manifest.yaml` + `STATUS.yaml`
  - `manifest.yaml` 负责机器可读的固定协议。
  - 每个 task package 的 `STATUS.yaml` 是任务状态唯一状态源。
  - CLI 只能读取和变更这个状态源，不能再形成和它并行的“入口自有状态解释”。
- 第三层：task package 正文
  - 任务事实、验证计划、证据和风险回写只留在 task package。
  - skill 和 README 只负责把人导向这里，不重复解释完整任务制度。

两类入口：

- 人类入口：
  - `README.md` 只讲“OpenHarness 是什么、为什么存在、怎样安装、怎样开始用”。
  - 不再承担完整流程教学，也不重复 stage、reflection、archive 等制度细节。
- 代理入口：
  - `using-openharness` 仍是唯一入口 skill。
  - 但它只保留路由职责、阶段切换规则和必要的约束，不再做长篇制度手册。
  - child skills 只保留自己阶段需要执行的动作，不重复仓库级协议。

一个状态源：

- 用户可见阶段信息继续存在，但它应是 `STATUS.yaml` 的派生展示，而不是额外的半独立叙事层。
- `bootstrap` 负责提供任务上下文和阶段信息，但不再默认承担过重的“首轮流程教学”。
- 用户聊天回复里的“当前在做什么、下一步做什么”应更多由 agent 自然表达承担，而不是把 CLI 输出直接推到前台。

关键约束：

- 不削弱 verification / evidence / archive 闭环。
- 不保留平行入口。
- 不允许 skill、README、CLI、task package 同时维护同一套长制度说明。

## Key Flows
主路径分成五步：

1. 进入仓库时先分辨“当前需要的是仓库地图、任务上下文，还是直接继续某个任务”。
   - 如果确实依赖 active package 状态，再前台使用 `bootstrap`。
   - 如果当前问题只是解释仓库规则或继续当前已知任务，`bootstrap` 可以退到后台。
2. 用户或代理先从 `AGENTS.md` 和 `using-openharness` 获得最短入口。
   - 这里应只回答：事实源在哪里、现在属于哪个阶段、接下来该去哪里。
3. 一旦进入具体任务，事实转移到 task package。
   - 需求、总体设计、详细设计、验证、证据全部由 task package 承载。
4. CLI 从 `STATUS.yaml` 派生出状态说明。
   - `transition` 负责合法推进。
   - `bootstrap` 负责展示当前状态和下一步。
   - `verify` 负责写入可追溯的验证结果。
5. 用户可见自然回复只复述当前最相关的阶段结论。
   - 不把完整制度说明再次搬出来。

关键失败信号：

- README、skill、CLI 帮助文本和 task package 同时解释同一制度，说明重复面没有收干净。
- `bootstrap` 展示的状态与 `STATUS.yaml` 不一致，说明入口层和真实状态源仍然没有收口。
- child skills 仍大量重复 entry skill 的规则，说明入口重组失败。
- 入口变短之后，如果验证、证据或归档语义被一起弱化，说明削减过头了。

## Stage Gates
- 必须明确每个表面的职责边界：
  - `AGENTS.md` 负责什么，不负责什么。
  - `README.md` 负责什么，不负责什么。
  - `using-openharness` 负责什么，不负责什么。
  - child skills 负责什么，不负责什么。
  - CLI 输出负责什么，不负责什么。
- 必须明确状态唯一来源是 `STATUS.yaml`，其他地方只能派生展示，不能平行解释。
- 必须明确下一轮要优先收哪些重复面，而不是继续笼统说“减重”。
- 必须明确失败时的收缩方向：
  - 如果一次性同时重组 README、skills、CLI 风险过高，可以先保证“权威层收口”和“状态源收口”，把更细的文案清理留到后续波次。
- 必须明确 overview 结束后，下一阶段写的是“如何落到具体文件和测试”，而不是重新讨论要不要保留兼容性。

## Trade-offs
收益：

- 协议主路径会明显变短，新进入者不必在 README、entry skill、child skills、CLI 输出之间来回对照。
- 状态展示和真实状态源收口后，像这轮复现出来的“状态文件和入口输出不一致”问题会更容易定位。
- 保留 task package 闭环，意味着减重不会退化成“说得更轻松，但完成声明重新变虚”。

代价：

- README 会失去一部分“把所有东西一次说全”的感觉，首次阅读的人可能需要更快跳去 `AGENTS.md` 或 task package。
- `using-openharness` 和若干 child skills 需要被显著缩短，这会带来一轮测试和文案同步成本。
- 如果入口播报收得太猛，短期内可能让部分用户觉得阶段信息变少，需要用更自然的回复补回来。

不选的方案一：维持现在的多表面说明，只做小幅删词。

- 不选原因：
  - 这样最安全，但解决不了重复维护和状态边界混乱的问题。
  - `OH-036` 已经证明问题不在个别措辞，而在结构层重复承载。

不选的方案二：把所有制度都进一步集中到 CLI 输出里。

- 不选原因：
  - 这样会让 `bootstrap` 继续承担过重入口职责。
  - CLI 是展示层，不应变成比 task package 和 entry skill 更重的事实入口。

不选的方案三：彻底去掉阶段播报，只保留 task package 文档。

- 不选原因：
  - 这样虽然最轻，但会丢掉阶段可见性带来的真实收益。
  - 当前问题是“播报过重且边界不清”，不是“所有阶段可见性都没价值”。

## Overview Reflection
我先挑战了“是否应该把所有权威都收进 `AGENTS.md`，让 skill 和 CLI 都尽量变薄”。这个方向看起来最干净，但我拒绝了。原因是 `AGENTS.md` 适合做仓库地图，不适合承担动态状态和任务级事实；如果把一切都堆回这里，只会形成新的大入口。

我再挑战了“是否应该把 `bootstrap` 降到纯任务列表，不再展示阶段信息”。这个方向能最快减少前台流程感，但我没有接受。因为 `OH-036` 已经证明阶段可见性本身是有收益的，真正该削的是过量播报和重复解释，而不是完全撤掉状态提示。这个挑战被拒绝。

我接受的约束是：OpenHarness 下一轮必须把“谁是权威、谁只是导向、谁只是展示”讲清楚。没有这个收口，任何减文案动作都会变成局部修剪，过一段时间还会重新膨胀。

我延期的判断是：下一轮是否应该把 README 和 skill 文本的清理拆成两个实现波次。这个要等 detailed 阶段看具体文件落点和测试影响再定；如果一次性改动面过大，就分两波，但总体边界不变。
