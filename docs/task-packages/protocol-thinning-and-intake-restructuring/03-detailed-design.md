# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先补测试和协议断言，再改实现，顺序如下：
    - 先新增或修改 `tests/openharness_cases/test_cli_workflows.py`
      - 锁住 `transition` 后 `bootstrap` / `bootstrap --json` 必须读取到同一份最新状态。
      - 锁住 `bootstrap` 的文本和 JSON 输出只展示必要阶段信息，不继续膨胀成流程手册。
    - 再新增或修改 `tests/openharness_cases/test_protocol_docs.py`
      - 锁住 `AGENTS.md`、README、`using-openharness`、child skills 的职责边界。
      - 锁住“entry skill 负责路由，child skills 不重复仓库级制度”这一收口结果。
    - 然后改 CLI 与生命周期实现：
      - `openharness_cli/commands.py`
      - `openharness_cli/lifecycle.py`
      - 必要时包括 `openharness_cli/repository.py`
    - 最后收文档面：
      - `AGENTS.md`
      - `README.md`
      - `skills/using-openharness/SKILL.md`
      - 相关 child skills 与 reference 文档
  - 实施完成后执行：
    - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
    - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
    - `uv run openharness check-tasks`
- Fallback Path:
  - 如果一次性同时收入口文案和 CLI 输出导致测试改动面过大，先完成“状态唯一来源收口”与“CLI 展示减重”，把 README 和 child skills 的进一步删减留到同一包的第二波实现。
  - 如果状态一致性问题暂时无法稳定复现或定位，就先把验证目标降级为：
    - 增加最小可复现测试
    - 缩小 `bootstrap` 的职责
    - 但不能宣称“状态源和展示层已经彻底一致”。
  - 如果 protocol docs 的旧断言阻塞本轮减重，应先修改测试使它们检查“职责边界清楚”，而不是继续逼迫文案重复。
- Planned Evidence:
  - 一组通过的 CLI 测试，证明 `transition`、`bootstrap`、`bootstrap --json` 在状态展示上对同一任务给出一致结果。
  - 一组通过的 protocol docs 测试，证明 README、entry skill、child skills 的职责边界已经收口。
  - 一次 `uv run openharness check-tasks` 通过结果，证明 task package 协议仍成立。
  - `04-verification.md` 后续应记录：
    - 状态一致性测试结果
    - 文案职责边界测试结果
    - `check-tasks` 结果
    - 若有残余不一致，必须明确写出范围而不是模糊带过。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/commands.py`
  - 这里承载 `bootstrap` 的文本和 JSON 输出，是入口展示减重的直接落点。
- `openharness_cli/lifecycle.py`
  - 这里承载阶段描述和下一步文案，也是状态展示逻辑的中心位置；如果要避免展示层和状态源继续漂移，这里必须收口。
- `openharness_cli/repository.py`
  - 如果状态不一致问题最终确认和任务发现、状态读取或对象刷新有关，这里会成为修复落点。
- `AGENTS.md`
  - 需要继续缩短到“仓库地图 + 少量仓库级约定”，不再承载默认工作流、方法论或 task package 结构协议。
- `README.md`
  - 需要收回过重的流程教学，只保留产品定位、安装、起步和最短使用理解。
- `skills/using-openharness/SKILL.md`
  - 这是代理入口，必须保留路由和阶段切换规则，但要删除对仓库级制度的重复长篇解释。
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
  - 这些 child skills 应只保留阶段动作和最小 handoff 约束，不再复述入口层协议。
- `skills/using-openharness/references/skill-hub.md`
  - 如果仓库级职责边界变化影响 skill hub 的说明，这里需要同步收口。
- `tests/openharness_cases/test_cli_workflows.py`
  - 用来锁住 CLI 行为和状态展示一致性。
- `tests/openharness_cases/test_protocol_docs.py`
  - 用来锁住文档和 skill 的职责边界，防止减重后再次回弹。

## Interfaces
这轮依赖并会重组四类接口：

- 状态接口：
  - `STATUS.yaml.status` 是唯一状态源。
  - `transition` 是唯一合法推进入口。
  - `bootstrap` 和 `bootstrap --json` 只能派生展示，不能形成第二套状态解释。
- 入口接口：
  - `AGENTS.md` 面向仓库协作者。
  - `README.md` 面向首次了解项目的人。
  - `using-openharness` 面向代理入口路由。
  - 这三者不能再同时承担“完整制度说明”。
- 流程接口：
  - child skills 只描述本阶段动作、输入输出和 handoff，不定义仓库级真相。
  - task package 继续承载任务事实、验证和证据。
- 测试接口：
  - `test_cli_workflows.py` 观察命令行为是否一致。
  - `test_protocol_docs.py` 观察文案边界是否重新膨胀。

关键可观察入口：

- `bootstrap --json` 的 `status`、`current_stage`、`next_stage`、`next_step`
  - 用来判断展示层是否仍忠实反映状态源。
- `STATUS.yaml`
  - 用来判断真实状态是否已写入。
- protocol docs 测试中的关键断言
  - 用来判断哪些规则还在 README、entry skill、child skill 之间重复出现。
- `check-tasks`
  - 用来判断这轮减重是否破坏了 task package 协议。

## Stage Gates
- 必须先定义测试顺序，再开始改实现。
- 必须明确状态唯一来源、展示派生层、任务事实层三者的边界。
- 必须明确本轮至少有一条状态一致性观察路径：
  - 看 `STATUS.yaml`
  - 看 `bootstrap --json`
  - 看相关测试
- 必须明确改动顺序：
  - 先测状态和展示
  - 再收 CLI
  - 再收 entry skill
  - 最后收 README 和 child skills
- 必须明确证据类型：
  - CLI 测试通过
  - protocol docs 测试通过
  - `check-tasks` 通过
  - 若保留任何兼容面，要在验证里写明保留理由

## Decision Closure
- 接受：先做“状态源和展示边界收口”，再做“文案减重”。理由是状态一致性是更硬的工程问题，先解决它能减少后续文案重组时的歧义。
- 接受：继续保留 `bootstrap` 的阶段展示，但把它收成薄展示层。理由是阶段可见性有真实收益，不应因减重而一起被删掉。
- 拒绝：把 README 继续当成完整流程手册。理由是这会和 `AGENTS.md`、entry skill、task package 长期重复。
- 拒绝：通过新增一层配置或新命令来解决当前问题。理由是本轮目标是减面，不是再加一层表面。
- 延期：是否需要把 `author-entry` 和 guidance discoverability 一并进一步压缩。触发条件是本轮实现后仍发现入口路径过长，且问题已不再来自状态和职责边界。

## Error Handling
- 主要失败路径一：只删文案，不收真实权威边界，结果是重复说明换了位置但没有减少。规避方式是先锁测试，再明确每个表面“负责什么 / 不负责什么”。
- 主要失败路径二：只改 `bootstrap` 输出，不核对 `STATUS.yaml` 与生命周期逻辑，结果继续出现展示和状态不一致。规避方式是把状态一致性测试放在第一波。
- 主要失败路径三：为了减重，把验证和证据语义一起削弱。规避方式是任何文案收缩都不能触碰 task package、verification、archive 的闭环。
- 误用风险：把 child skill 精简成过短提示，导致阶段动作不够清楚。规避方式是只删除仓库级制度，不删除阶段动作和 handoff 规则。
- 静默出错风险：CLI 看起来更短了，但实际仍从旧文案或旧状态推导下一步，测试没有覆盖出来。规避方式是同时检查文本输出、JSON 输出和状态文件，而不是只看其中一个表面。

## Migration Notes
迁移顺序分三波：

1. 第一波：状态与展示收口
   - 先补状态一致性测试。
   - 再调整 `commands.py` / `lifecycle.py`，让 `bootstrap` 成为更薄的展示层。
   - 切换点：`bootstrap` 文本和 JSON 都直接围绕 `STATUS.yaml` 的最新状态派生。
2. 第二波：入口层收口
   - 缩短 `using-openharness`，让它只保留路由、阶段切换和必要约束。
   - 同步更新 `AGENTS.md`，防止两边继续并行教学。
3. 第三波：README 与 child skills 收口
   - README 退回产品说明和起步入口。
   - child skills 退回各自阶段动作。

兼容策略：

- 本轮不默认保留旧文案形态。
- 唯一应优先保留的是：
  - task package 协议
  - 状态流
  - verification / evidence / archive 语义

回滚触发点：

- 如果第一波之后状态一致性测试仍无法通过，就不要进入大规模文案删减。
- 如果 protocol docs 测试显示减重会破坏 child skill 的基本可用性，就先停止 README 与 child skill 的进一步收缩，保留已经完成的状态收口。

## Detailed Reflection
我先挑战了“是否应该先收 README 和 skill 文案，因为这部分最直观”。结论是否定。因为如果状态源和展示边界没先收口，文案删完之后仍会留下最关键的歧义，也更难解释为什么要这么删。

我再挑战了“是否应该把状态不一致问题单独拆包，不放进这轮”。结论是否定。因为 `OH-037` 的主题就是入口重组和协议减面，而状态展示与真实状态打架正是入口层最直接的问题，不应继续外包给后续。

我接受的假设是：这轮不需要发明新入口或新命令，只要把现有权威层和展示层职责收清，就足以把主路径缩短。

我延期的判断是：是否要在本轮顺手继续压缩 `skill-hub` 与 guidance discoverability。这件事有价值，但它依赖前两波实现后再看入口长度是否仍然过重，因此暂不提前锁死。
