# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
这轮设计覆盖的是 OpenHarness 对中文作者的入口可见性和 guidance 导流结构，而不是重写整套协议。

纳入范围的表面包括：

- `AGENTS.md` 中对默认入口和作者阅读顺序的表达方式。
- `skills/using-openharness/` 与相关 stage skill 中对 guidance 入口的导流方式。
- `skills/using-openharness/references/` 下可能新增的中文作者入口页或导览页。
- `references/templates/` 中五类 task package 模板的短提示。
- `openharness bootstrap` 的输出文案，如果需要用它暴露作者入口。

不纳入范围的部分包括：

- 修改 task package 固定文件列表、状态流或归档协议。
- 为每个 skill 提供整篇中文翻译版。
- 引入新的评分器来判断文档质量。
- 替换掉 `OH-033` 已经建立的五份 guidance 结构。

## Proposed Structure
推荐采用“单一中文作者入口 + 多表面导流 + 模板轻增强”的结构。

1. 新增一个明确的中文作者入口页
   - 位置应放在 `skills/using-openharness/references/` 下，作为稳定事实源。
   - 它负责回答三个问题：我现在先看什么、五类文档分别看哪份 guidance、如果我只想快速开始应怎么走。
   - 它不重写五份 guidance 的正文，只做导航、分流和最短解释。
2. `using-openharness` 与关键 stage skill 负责导流
   - `using-openharness` 负责把“中文作者入口存在”提升到入口协议层。
   - `brainstorming`、`exploring-solution-space`、`verification-before-completion` 只在各自阶段提醒用户进入对应 guidance，不复制整套写作方法论。
3. 模板负责最低增强
   - 保持模板轻量，但把现在偏抽象的提示略微收紧，例如增加“至少回答什么问题”或“不要写成什么”。
   - 模板仍不是正式手册，只是降低第一次落笔难度。
4. bootstrap 负责暴露当前可走入口
   - 如果用户从 CLI 进入仓库，bootstrap 应给出作者入口或 guidance 导航提示，而不是只列出 active task packages。

主边界如下：

- 作者入口页是导航层，不是新的方法论文档层。
- 五份 guidance 仍然是正式写作 contract。
- 模板仍然是脚手架，不承载大段说明。
- CLI 输出只做导向，不承担静态说明正文。

## Key Flows
主流程建议改成下面这样：

1. 用户进入仓库，先从 `AGENTS.md` 或 bootstrap 看到“中文作者入口”。
2. 作者入口页说明 task package 的五类文档分别由哪份 guidance 约束，并给出“如果你现在处于需求/总体设计/详细设计/验证收尾，先看哪份”。
3. 用户在进入某个 stage skill 时，会再次被导向当前阶段对应的 guidance，而不是要求自己回忆文件名。
4. 用户打开模板时，模板自身提供更具体的最小提示，帮助快速落笔。
5. 如果用户需要深入理解，再进入对应 guidance 正文，而不是一开始就被多个英文 skill 包围。

失败信号包括：

- 用户仍然需要先搜索仓库，才能知道 guidance 在哪里。
- 中文作者入口和 stage skill 的导流指向不一致。
- 模板增强过度，导致脚手架本身噪声过大。
- bootstrap 只列任务状态，却没有帮助用户定位写作入口。

## Stage Gates
- 必须明确作者入口放在哪个稳定表面，而不是只说“增加说明”。
- 必须明确导航层、guidance 层、模板层和 CLI 暴露层的职责边界。
- 必须至少给出一个未采用替代方案，并说明不选原因。
- 必须识别关键失败模式，包括入口不可见、事实源分散和模板膨胀。
- 必须给出降级方向：如果 bootstrap 改动过重，至少应先在 `AGENTS.md`、skill-hub 和入口 skill 中建立稳定入口。

## Trade-offs
我比较了三种主要方案：

- 方案一：把所有入口说明都塞进 `AGENTS.md`
  - 收益是仓库顶层可见性最高。
  - 代价是 `AGENTS.md` 会继续膨胀，而且它不适合承载具体的五类文档导航。
- 方案二：只增强模板
  - 收益是用户新建 task package 时立刻能看到更多提示。
  - 代价是模板只能帮助“开始写”，不能解决“我现在该看哪份 guidance”这个更早的入口问题。
- 方案三：新增单一中文作者入口页，并由 `AGENTS.md`、bootstrap、关键 skill 和模板共同导流
  - 这是推荐方案。
  - 收益是既不新增第二套方法论文档，又能把现有 guidance 真实暴露给用户。
  - 代价是需要协调多个表面的文案同步，但职责边界清楚。

回退方向：

- 如果 bootstrap 改动成本过高，可以先在 `AGENTS.md` 和 `using-openharness` 中建立稳定入口，再决定是否把同样入口加入 CLI 输出。
- 如果模板增强后仍然显得噪声太大，应回退到更少但更硬的提示，而不是重新塞成长篇说明。

## Overview Reflection
- 我先挑战了“是不是只要把 skill 翻译成中文就够了”。结论是否定的。真正的问题不是语言表面本身，而是用户看见的第一入口没有把 guidance 暴露出来；只翻译 skill 仍然不能保证发现路径清楚。
- 我也挑战了“是不是只需要模板多写几句”。结论也是否定的。模板只能解决落笔阶段的问题，不能取代仓库入口导航。
- 我检查了“新增中文作者入口会不会制造新的事实源”。风险存在，所以入口页必须只做导航，不重写五份 guidance 的正文。
- 我还挑战了“bootstrap 是否真的需要改”。结论是视成本而定。如果 CLI 改动轻，就应加入；如果改动重，也不能阻塞 `AGENTS.md` 和入口 skill 先行建立可见性。
- 当前不需要子智能体讨论，因为这轮主要是仓库信息架构和入口体验设计，不涉及高不确定性的外部技术选型。
