# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先实现单一中文作者入口页，并把它接入 `AGENTS.md`、`using-openharness` 和相关 stage skill。
  - 再根据入口页内容微调五类模板提示，确保模板提示与 guidance 边界一致。
  - 如决定扩展 CLI，则更新 `openharness bootstrap` 输出并补测试。
  - 实现后运行 `uv run openharness check-tasks`，确保 task package 协议仍然有效。
  - 如果改了 CLI 或协议表面测试，再运行针对性 pytest，验证入口文案与引用关系未破坏现有行为。
- Fallback Path:
  - 如果 CLI 输出改动成本明显高于预期，就先落地 `AGENTS.md`、入口 skill、skill-hub 和作者入口页，不把 bootstrap 作为阻塞项。
  - 如果模板增强被证明噪声过大，就回退为更少但更明确的最小提示，不扩写成长模板。
  - 如果发现某个 stage skill 已经承载了过多静态说明，就优先收缩 skill 内容并改为链接导流，而不是继续复制说明。
  - 如果没有把作者入口挂到用户真实会看到的位置，就不能宣称此任务完成，即便 reference 文件已经新增。
- Planned Evidence:
  - 中文作者入口页及其被引用的仓库表面。
  - 更新后的 `AGENTS.md`、关键 `SKILL.md`、模板文件和可能的 CLI 输出测试。
  - `check-tasks` 通过结果。
  - 若修改 CLI，则包含相应测试通过结果和 bootstrap 输出变化证据。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `AGENTS.md`
  - 需要把中文作者入口和默认阅读路径说得更直接，让首次进入仓库的人一眼看到。
- `skills/using-openharness/SKILL.md`
  - 需要把作者入口纳入仓库入口协议层，避免只有 skill 内部路由，没有面向作者的导流。
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
  - 需要在各阶段增加对作者入口或对应 guidance 的更直接引用，但仍保持动作导向。
- `skills/using-openharness/references/skill-hub.md`
  - 需要成为 skill 路由与作者入口之间的中间导航表面。
- `skills/using-openharness/references/`
  - 需要新增一份中文作者入口页，集中说明五类文档和阅读路径。
- `skills/using-openharness/references/templates/task-package.01-requirements.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.04-verification.md`
- `skills/using-openharness/references/templates/task-package.05-evidence.md`
  - 需要轻量增强最小提示，降低首次落笔难度。
- `openharness` CLI 或对应测试文件
  - 只有在决定让 bootstrap 输出暴露作者入口时才修改。

## Interfaces
本轮接口边界如下：

- 作者入口页与 guidance 的边界
  - 作者入口页只做导航、分流和最短解释。
  - 五份 guidance 继续作为正式写作 contract。
- skill 与作者入口页的边界
  - skill 负责在恰当阶段导流到作者入口或对应 guidance。
  - skill 不复制整套静态写作规则。
- 模板与 guidance 的边界
  - 模板只负责最短提示和最低防错。
  - guidance 继续负责完整解释、边界和常见误写。
- bootstrap 与仓库文档的边界
  - bootstrap 只做“你现在可看哪里”的提示，不嵌入大段静态说明。

可观测性入口包括：

- `AGENTS.md` 是否已暴露作者入口。
- `using-openharness` 和 stage skill 是否都能稳定导向正确 guidance。
- 模板是否仍然轻量但明显比当前更具体。
- bootstrap 文案与测试是否反映入口变化。

## Stage Gates
- 必须列出作者入口页、入口 skill、模板和可选 CLI 输出这四类落点。
- 必须明确哪些改动是必需项，哪些是可降级项。
- 必须明确实现后至少要跑 `uv run openharness check-tasks`。
- 如果计划修改 bootstrap，必须同时定义对应测试或验证观察点。
- 必须明确迁移顺序，避免先改模板、后补入口，导致用户仍然找不到 guidance。

## Decision Closure
- 接受：新增单一中文作者入口页，作为 guidance 的稳定导航层。
- 接受：`AGENTS.md`、入口 skill、关键 stage skill 和模板共同承担导流职责。
- 接受：bootstrap 是否修改作为条件项处理，不阻塞第一轮可用性修正。
- 拒绝：为每个 skill 单独提供完整中文副本。理由是维护成本高，而且不能直接解决发现路径问题。
- 拒绝：只增强模板。理由是它无法覆盖仓库入口阶段。
- 延期：是否为“入口发现成功率”增加更强自动测试。触发条件是第一轮实现后仍频繁出现“guidance 看不见”的反馈。

## Error Handling
- 如果作者入口页开始重复五份 guidance 的正文，会制造新的事实源分散。
  - 处理方式：入口页只写导航与最短解释，正文继续指向原 guidance。
- 如果 stage skill 导流路径不一致，用户会得到互相冲突的入口。
  - 处理方式：统一由 `using-openharness` 和 skill-hub 定义入口，再让 stage skill 引用它们。
- 如果模板增强过度，用户新建包时会被噪声淹没。
  - 处理方式：模板只增加最低必要提示，不加入长段背景说明。
- 如果只改 reference 不改入口表面，外部仍会认为项目是形式主义。
  - 处理方式：至少同步修改 `AGENTS.md` 或入口 skill，确保真实可见性变化发生在用户前置路径上。

## Migration Notes
建议实施顺序如下：

1. 先新增中文作者入口页，并确定它与五份 guidance 的链接关系。
2. 再更新 `AGENTS.md`、`using-openharness` 和 `skill-hub`，让入口真正可见。
3. 再更新三个关键 stage skill，使各阶段导流一致。
4. 再轻量增强五个模板提示。
5. 最后视成本决定是否更新 bootstrap 输出和对应测试。

兼容策略：

- 不修改 task package 文件名和状态流。
- 五份 guidance 继续保持原位置和原职责。
- archived task package 不需要即时迁移。

回滚注意事项：

- 如果 bootstrap 方案不可控，只回滚 CLI 相关改动，不回滚作者入口页和文档入口改动。
- 如果模板增强不合适，局部回退模板提示即可，不影响入口层与 guidance 层。

## Detailed Reflection
- 我重新检查了“是不是一定要先改 CLI 才算入口优化”。结论是否定的。CLI 很有价值，但不是第一轮可用性修复的唯一入口；真正关键的是用户第一次看到的仓库表面能否指向 guidance。
- 我也检查了“是否会因为新增入口页而让事实源再次分散”。这个风险只能靠严格边界控制解决，所以入口页必须避免重写 guidance 正文。
- 我反思了模板增强的风险。模板增强必须服务于快速落笔，而不是把模板本身变成阅读负担。
- 我检查了验证策略。第一轮重点是确认入口是否真实暴露、引用是否连通、协议是否未被破坏，因此 `check-tasks` 是最低验证；如果涉及 CLI，再补相应测试。
- 当前 detailed 已经足够支撑后续实现，因为实现落点、迁移顺序、失败路径和降级方向都已经明确。
