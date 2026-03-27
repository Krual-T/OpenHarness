# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先用 `uv run openharness check-tasks` 和 `uv run openharness bootstrap --json` 确认仓库协议与 active package 状态，再用归档 task package 的 `STATUS.yaml`、`04-verification.md`、`05-evidence.md` 提取内部案例，最后对照 `superpowers`、`OpenSpec`、`spec-kit` 以及 OpenAI / Anthropic 的正式资料，把“减少假完成”“`reflection` / `stage gate` 收益”“下一轮边界”收口成正式判断。
- Executed Path: 已执行 `uv run openharness check-tasks` 并得到 `Validated 39 task package(s)`；已执行 `uv run openharness bootstrap --json`，确认当前 active package 中 `OH-036`、`OH-037`、`OH-033` 都处于 `verifying`；已阅读并摘取以下归档 package 作为内部案例：
  - `workflow-transition-and-verification-artifacts`
  - `task-package-completion-semantics`
  - `workflow-stage-visibility-and-task-intake`
  - `workflow-redesign`
  - `python-verification-maturity`
  - `maintenance-and-entropy-reduction`
  - `skill-protocol-deduplication`
- 还已对照外部正式资料，确认：
  - `superpowers` 更偏执行期增能与工具装配，不提供 OpenHarness 这种仓库内状态与归档证据闭环。
  - `OpenSpec` 与 `spec-kit` 更偏 spec 驱动的任务拆解与实现手册，不直接承担持续的 archive / evidence contract。
  - OpenAI 与 Anthropic 的官方材料强调 eval、tool use、skills、可观测性与迭代修正，但没有支持“固定多阶段制度文本越多越好”这一前提。
- 已将正式评估结论写回 `OH-036`，并明确哪些结论已证实、哪些仍属推断。
- Path Notes:
- 当前路径已经足以支撑“正式评估结论”这一轮目标，因为内部案例、当前命令结果与外部对照都已落到文档证据中。
- 当前路径还不足以宣称整个评估 stream 已经 `archived`，因为下一轮重构仍在活跃进行中，且本包当前更适合作为 `OH-037` 的事实前提保留在 active task packages 中。
- 先前一度怀疑 `bootstrap --json` 与 `STATUS.yaml` 存在状态刷新不一致，但本次串行重跑没有复现；因此目前只能把它保留为历史可疑信号，而不能继续当作已复现缺陷写入结论。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run openharness check-tasks`
- `uv run openharness bootstrap`
- `uv run openharness bootstrap --json`

## Expected Outcomes
- 仓库 task package 协议继续有效。
- `OH-036` 的需求、overview、detailed 三层文档都具备正式内容，并已把评估问题收口成正式判断。
- 归档 package 能为“假完成”“stage gate 收益”“协议同步面负担”提供足够具体的内部案例，而不是只有抽象理念。
- 本轮能把下一轮重构边界收敛成“保留 / 削减 / 重组”三类，并明确 `OH-037` 现在只能承接这些结论，不能提前展开设计。

## Traceability
- `01-requirements.md` 中关于“是否减少假完成”的问题，主要由 `workflow-transition-and-verification-artifacts`、`task-package-completion-semantics`、`python-verification-maturity` 提供证据。
- `01-requirements.md` 中关于“`reflection` / `stage gate` 是否有真实收益”的问题，主要由 `workflow-redesign`、`workflow-stage-visibility-and-task-intake`、`skill-protocol-deduplication` 提供证据。
- `01-requirements.md` 中关于“协议同步面和维护负担”的问题，主要由 `maintenance-and-entropy-reduction`、`skill-protocol-deduplication` 提供证据。
- `02-overview-design.md` 已把这些证据面收敛为内部案例层、外部对照层和仓库事实层。
- `03-detailed-design.md` 已把下一轮边界明确为：
  - 保留 task package / 状态 / verification / archive 闭环
  - 削减重复协议与无收益的固定流程义务
  - 重组入口层、CLI 输出和 skill 承载分工
- 当前缺口是：这些结论还没有在一个新的后续重构 task package 中被正式接手，因此本包尚不应宣称完成闭环。

## Risk Acceptance
- 当前接受的风险一：内部案例主要来自归档包而非你个人口述案例。之所以可接受，是因为这些归档包已经是仓库内正式事实源，足以承担第一轮评估依据。
- 当前接受的风险二：外部对照资料深度不完全一致。之所以可接受，是因为本轮目标是结构对照与边界收敛，不是做完整市场调研。
- 当前接受的风险三：先前怀疑过 `bootstrap` 输出与 `STATUS.yaml` 可能出现阶段不一致，但当前串行验证没有复现。之所以仍保留这条风险，是因为此前记录已经出现过该怀疑，后续若再次出现应单独最小复现，而不是继续凭记忆扩大结论。

## Formal Evaluation Conclusions
- 关于“是否真的减少假完成”：
  - 结论：有，且这是 OpenHarness 当前最明确、证据最强的正收益。
  - 证据基础：
    - `workflow-transition-and-verification-artifacts` 把 `verify` 从临时 stdout 提升为带指纹的 artifact，并把 archive 绑定到最新成功验证。
    - `task-package-completion-semantics` 明确收紧了 `archived` 语义，直接针对“设计写完就像完成”的误判。
    - `python-verification-maturity` 明确要求如实记录验证强度，而不是把弱证据伪装成强证据。
  - 结论边界：
    - OpenHarness 减少的是“仓库内正式完成声明的假完成”，不是从根本上阻止人跳过流程或直接改文件。
- 关于“`reflection` / `stage gate` 是否有真实收益”：
  - 结论：`stage gate` 有局部真实收益，但固定 `reflection` 义务没有足够证据证明自己是核心价值来源。
  - 证据基础：
    - `workflow-stage-visibility-and-task-intake` 证明清楚阶段含义和下一步，能减少“设计未收口就进入执行”的混乱。
    - `skill-protocol-deduplication` 与 `maintenance-and-entropy-reduction` 反过来证明，制度文本和阶段说明如果分散复制，会快速变成维护负担。
    - 当前归档案例中，真正改变结构的多是语义收紧、边界重划和验证闭环增强，而不是“多写一轮 reflection 文本”本身。
  - 正式判断：
    - 应保留有明确判定作用的 stage gate。
    - 不应继续把所有固定 `reflection` 义务默认视为必须保留的协议核心。
- 关于“和外部项目对照后，OpenHarness 的定位是否成立”：
  - 结论：成立，但定位应收窄。
  - 正式判断：
    - 相比 `superpowers`、`OpenSpec`、`spec-kit`，OpenHarness 的独特点不是更会写 spec，也不是更会装配 agent，而是把任务文档、状态、验证、归档串成仓库内可追溯闭环。
    - 相比 OpenAI 和 Anthropic 的官方方法，OpenHarness 当前过重之处不在“重视评估”，而在“把入口制度文本和阶段说明铺得太广”。
    - 因此下一轮不是继续扩协议，而是保留证据闭环，削减重复表面。
- 关于“下一轮重构边界”：
  - 保留：
    - task package 作为唯一事实源
    - `STATUS.yaml` 的机器可读状态
    - `04-verification.md` / `05-evidence.md` 的验证与证据写回
    - archive protocol
  - 削减：
    - skills、guidance、README、task package 之间对同一协议的重复解释
    - 没有证据表明能稳定改变结果的固定 `reflection` 义务
    - 对轻任务过重的前台流程感
  - 重组：
    - 仓库入口层与 CLI 输出边界
    - stage visibility 与用户可见自然回复的关系
    - 文档 contract 与 skills 制度文本的承载分工
- 关于“OH-037 现在是否应继续设计”：
  - 结论：不应。
  - 触发条件：
    - 只有当本包结论被视为稳定事实源后，`OH-037` 才能进入 `02-overview-design.md`。
    - 在此之前，`OH-037` 只应保留需求层承接，不应提前锁定实现结构。

## Confidence Split
- 已有充分证据支撑的判断：
  - OpenHarness 的主要收益来自减少正式完成声明中的假完成。
  - archive / verification / evidence 是当前系统最该保留的核心闭环。
  - 协议重复解释已经构成真实维护负担。
- 证据中等、但已足够指导下一轮的判断：
  - stage gate 有价值，但主要价值来自“明确判定点”，不是来自更长的流程文案。
  - 入口层与阶段播报应被重组，而不是继续增补说明。
- 仍属于推断、后续可以再补证据的判断：
  - 固定 `reflection` 义务在更多真实会话里是否完全无收益。
  - 对不同规模任务是否需要轻重两套前台播报策略。
  - 不保留兼容性在实际重构成本上的净收益有多大。

## Latest Result
- 当前结果是：`OH-036` 已完成正式评估结论写回，内部案例与外部对照已收口为可执行边界，并已按协议保持在 `verifying`。
- 本次 fresh verification 中，`bootstrap --json` 与当前 `STATUS.yaml` 一致，active packages 都正确显示为 `verifying`。因此“入口层与状态源边界需要重组”仍是设计判断和历史经验判断，但这次没有新增复现证据。
- Latest Artifact:
- 无独立 artifact；当前证据主要是仓库文件、归档 package 内容、外部正式资料与命令输出。
