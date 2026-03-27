# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先验证 task package 协议没有因为本轮分析写回而损坏：
  - `uv run openharness check-tasks`
- 再确认活跃包状态和入口可见性符合当前设计阶段：
  - `uv run openharness bootstrap --json`
- 然后用仓库内证据完成案例抽取：
  - 逐个阅读选定归档 package 的 `STATUS.yaml`、`02-overview-design.md`、`03-detailed-design.md`、`04-verification.md`、`05-evidence.md`
- 最后把评估结论回写到本包的 `04-verification.md` 和 `05-evidence.md`，并在需要时补一轮仓库校验：
  - `uv run openharness check-tasks`
- Fallback Path:
- 如果外部项目资料获取受限，就把外部结论收缩到已确认的 README、官方文档和仓库元数据层，不用搜索结果硬补推论。
- 如果某个归档 package 证据不足以支持“真实收益”判断，就把它降级为补充案例，不用它承担主结论。
- 如果本轮只能完成分析和边界收敛，而还无法证明下一轮应如何拆包，也不能宣称本包完成，只能停留在 `detailed_ready` 或更低状态，等待补充证据。
- Planned Evidence:
- 一份按内部案例与外部对照分开的证据表，至少说明每条结论来自哪个归档包或哪个外部项目。
- 一份针对 OpenHarness 的判断矩阵，明确区分：
  - 必要闭环
  - 可接受成本
  - 明显负担或重复协议
- 一份下一轮重构边界说明，明确：
  - 哪些结构应被保留
  - 哪些结构应被削减
  - 哪些结构下一轮允许直接重组，不预设兼容性
- `04-verification.md` 需要收集的核心证据类型是：
  - 仓库校验命令结果
  - 活跃包状态结果
  - 归档案例摘录对应的结论摘要
  - 外部项目对照摘要

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `docs/task-packages/openharness-evaluation-and-refactor-boundaries/02-overview-design.md`
  - 已经承载总体边界、案例选择策略和对照层次，是后续 detailed 落点的前提。
- `docs/task-packages/openharness-evaluation-and-refactor-boundaries/03-detailed-design.md`
  - 本轮要把案例抽取顺序、对照方法、结论分类法和下一轮拆包规则写具体，避免后续再次从头定义方法。
- `docs/task-packages/openharness-evaluation-and-refactor-boundaries/04-verification.md`
  - 后续需要记录这轮分析实际采用了哪些证据路径、哪些结论证据充分、哪些仍然不足。
- `docs/task-packages/openharness-evaluation-and-refactor-boundaries/05-evidence.md`
  - 后续需要收集用到的归档包、外部来源、命令和残余风险。
- `docs/task-packages/openharness-evaluation-and-refactor-boundaries/STATUS.yaml`
  - 需要随着阶段推进更新状态与完成定义，确保后续重构任务可以从这里接手。

本轮不应修改协议实现文件、CLI、模板或测试，因为这会把“评估设计”和“重构实现”混成一轮。

## Interfaces
本轮依赖四类接口与稳定边界：

- 仓库协议接口：
  - `AGENTS.md`
  - `manifest.yaml`
  - skills 的阶段职责
  - task package 的固定文件结构
  - 这些接口告诉我们 OpenHarness 自己宣称的工作方式是什么。
- 机械约束接口：
  - `openharness_cli/commands.py`
  - `openharness_cli/validation.py`
  - `openharness_cli/lifecycle.py`
  - `tests/`
  - 这些接口告诉我们哪些协议已经被落成硬约束，哪些仍只是文档叙事。
- 内部案例接口：
  - 归档 task package 中的 `STATUS.yaml`、`04-verification.md`、`05-evidence.md`
  - 这些是判断“有没有减少假完成”“reflection 是否改变决策”的主要观察入口。
- 外部对照接口：
  - `superpowers` README / 仓库
  - `OpenSpec` README / 仓库
  - `spec-kit` README / 仓库
  - OpenAI / Anthropic 官方文档
  - 这些接口只负责提供对照层级，不负责替代 OpenHarness 自己的内部证据。

关键 `observability` 入口：

- `check-tasks` 是否持续通过，说明本轮文档写回没有破坏协议。
- `bootstrap --json` 的状态输出，说明当前包的阶段推进是否真实生效。
- 归档包中的 `Traceability`、`Risk Acceptance`、`Residual Risks`、artifact 路径和 done criteria，说明某些流程是否真的改变了结构或验证，而不只是留下更长文档。

## Stage Gates
- 必须明确内部案例筛选标准，而不是继续无差别阅读全部归档包。
- 必须明确外部对照是分层比较，不再混淆“技能系统”“规格工件系统”“仓库协议系统”。
- 必须明确下一轮重构边界的输出结构，至少要能分成保留、削减、重组三类。
- 必须明确后续 `04-verification.md` 需要怎么判断一条结论是否证据充分：
  - 有仓库内事实支撑
  - 有归档案例支撑
  - 有外部对照支撑
  - 或只能暂列推断
- 必须明确这轮不进入实现，因此任何“直接改协议验证想法”的冲动都应被拦回下一轮。

## Decision Closure
- 接受：把归档 task package 当作第一轮真实使用案例。理由是它们已经包含需求、设计、验证和证据写回，比临时回忆更稳定。
- 接受：把外部项目分层比较。理由是 `superpowers`、`OpenSpec`、`spec-kit` 解决的并不是完全同一层问题，强行同层比较会失真。
- 接受：把下一轮重构目标收敛成“减轻协议同步面，同时保留验证闭环”。理由是归档案例已经显示 OpenHarness 的核心价值主要来自 task package、状态语义、验证写回和归档证据，而高风险负担主要来自 skill / guidance / README / tests 的重复维护与入口负担。
- 拒绝：继续扩张外部调研范围。理由是这会增加资料面，但不一定更接近下一轮重构边界。
- 拒绝：在本轮默认保留兼容性。理由是本轮任务的价值之一，就是为下一轮争取真实重组空间。
- 延期：下一轮是否应拆成多个重构子包。触发条件是本轮结论显示“保留 / 削减 / 重组”三类内容跨度过大，单个后续包无法承载。

## Error Handling
- 主要失败路径一：把 README 自述当成项目真实能力，而忽略 CLI、校验器和测试实际约束到哪里。规避方式是所有核心判断都至少回到一个代码或测试表面。
- 主要失败路径二：把归档包写得完整误判成“该流程真实有效”。规避方式是优先检查它是否留下了结构变化、artifact、traceability 或后续 follow-up，而不是只看章节是否齐全。
- 主要失败路径三：把不同外部项目的不同层级能力误当成同类产品比较。规避方式是始终先判断比较层次，再下相似或差异结论。
- 误用风险：为了给下一轮让路，过早把所有现有结构都判成负担。规避方式是保留“必要闭环”这一类，不把减负等同于全盘否定。
- 静默出错风险：最终得出“有优点也有问题”的模糊结论，看起来平衡，实际上无法指导下一轮重构。规避方式是强制产出下一轮边界清单，而不是只做评论。

## Migration Notes
- 迁移顺序不是代码迁移，而是结论迁移：
  - 先完成内部案例抽取
  - 再完成外部正式对照
  - 然后形成 OpenHarness 的结构分类
  - 最后从分类结果中拆出下一轮重构边界
- 当前已经收敛出的下一轮重构边界候选如下：
  - 保留：
    - task package 作为唯一事实源
    - `STATUS.yaml` 的机器可读状态
    - verification / evidence writeback
    - archive protocol
  - 削减：
    - skills、guidance、README、task package 之间对同一协议的重复解释
    - 没有证据显示能改变决策的固定 `reflection` 义务
    - 对轻任务过重的前台流程感
  - 重组：
    - 仓库入口层与 CLI 输出的边界
    - stage visibility 与用户可见自然回复的关系
    - 任务文档 contract 与 skills 文字制度的承载分工
- 如果后续继续验证支持这个方向，下一轮更像“协议减重与入口重组”包，而不是“继续往现有结构上补更多 guidance”包。
- 本轮没有兼容策略要求；相反，必须刻意避免在设计阶段把兼容性固化成默认边界。
- 切换点是：一旦下一轮重构边界已经足够具体，就不应继续在本包里扩写更多评价文字，而应单独开新的重构 task package。
- 回滚触发点是：如果后续发现某条“应直接重组”的结论缺少足够证据，应回退到 overview / detailed 重新补证据，而不是把不充分判断硬推给下一轮实现。

## Detailed Reflection
我先挑战了“这轮没有代码实现，是否还需要 detailed 级别的方法设计”。结论是需要。因为这轮真正的实现对象不是功能代码，而是下一轮重构边界；如果没有详细的取证和收敛方法，后续仍会重新讨论。

我也挑战了“是否应该先写下一轮重构方案，再倒推证据”。结论是否定。这样很容易把现有偏好包装成评估结果，因此仍应坚持先取证、再分类、最后拆边界。

我再检查了接口边界：本轮最重要的稳定边界不是某个 CLI 命令，而是“哪些表面算正式证据”。当前结论是：仓库代码与测试、归档 task package、外部正式文档三者足够构成这一轮的证据面。

我接受的假设是：第一轮真实案例可以由归档包承担。若后续发现这些归档包不足以判断实际使用成本，再补人工案例。

我延期的判断是：下一轮重构是否先动 skills、还是先动 task package / CLI 关系。这要等本轮最终分类完成后再决定。
