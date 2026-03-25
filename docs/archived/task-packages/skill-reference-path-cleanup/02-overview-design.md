# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
- 覆盖范围是 live skill surface 中真正参与当前仓库协议导航的文档，以及维护者会直接阅读的技能配套材料，重点是 `skills/using-openharness/references/`、`skills/systematic-debugging/` 和与其配套的协议文档测试。
- 关注的边界不是“全仓库所有历史文本是否统一”，而是“当前协作者沿着 live protocol docs 跳转时是否能落到真实文件”。
- 不纳入范围的是 archived task packages、模板中的占位符路径、以及与本轮路径有效性无关的 skill 结构优化。

## Proposed Structure
推荐方案分成三层：

1. live reference cleanup
   - 只修复 live docs 中会解析到不存在文件的真实路径。
   - 对于位于 `skills/using-openharness/references/` 内部的交叉引用，统一改成与当前文件同级可解析的稳定写法，例如直接写文件名而不是再套一层 `references/` 前缀。
2. retired skill path cleanup
   - 清理 `skills/systematic-debugging/` 下维护者可见材料中的旧路径 `skills/debugging/systematic-debugging`。
   - 统一替换为当前仓库真实 skill 路径，避免协作者误判真实入口。
3. lightweight regression guard
   - 在现有 `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 中增加针对关键 live docs 引用有效性的断言。
   - 同时补充对已确认旧 skill 路径的防回归断言。
   - 校验目标是“关键引用仍指向真实文件，关键技能材料不再宣传 retired path”，而不是试图把所有 Markdown 路径都做成通用解析器。

这样做的主路径足够短：
- 先修文档里已经确认失效的引用。
- 再修维护材料里已经确认失效的旧 skill 入口。
- 再把这些高风险交叉引用固化到现有文本测试里。
- 最后通过 `check-tasks` 与 `pytest` 证明任务包协议和 live docs 同时保持一致。

## Key Flows
主流程如下：

1. 从 `using-openharness`、`skill-hub`、runtime capability 相关参考文档出发，识别 live surface 中的真实导航路径。
2. 逐个检查这些文档内部对 sibling references 的写法，确认哪些路径在当前目录结构下会落空。
3. 把失效路径改成当前目录可解析的稳定写法，保持文档语义不变，只修导航有效性。
4. 清理 `systematic-debugging` 目录里已经确认的旧 skill 路径，统一对齐当前真实入口。
5. 在 `test_protocol_docs.py` 中增加针对这些关键引用与旧路径残留的断言，确保后续再写回错误 sibling path 或 retired path 时直接失败。
6. 执行 `check-tasks` 与目标 `pytest`，并把结果回写到任务包。

## Stage Gates
- 必须明确 live surface 与 archived evidence 的边界，确认不把历史归档文本误纳入本轮主修复范围。
- 必须确认至少一条真实失效路径，而不是只基于“可能有旧路径”做泛化清理。
- 必须确认至少一条真实 retired skill path 残留，并把它纳入本轮主修复面。
- 必须给出防回归方向：不是仅靠人工复查，而是把关键 live 引用收进现有文本测试。
- 必须说明失败模式与回退方向：若新增的自动校验过于泛化、误伤模板占位路径，应收窄到受影响的 live docs 白名单，而不是放弃防回归。

## Trade-offs
- 收益是把问题收敛到真实的 live 导航失效点和已确认的旧入口残留，修改面仍然有限，但能直接恢复当前协议文档与技能材料的可信度。
- 代价是本轮不会顺手消灭 archived package 中所有历史旧路径，也不会做全仓库通用 Markdown 链接校验器。
- 不选“全仓库批量搜索替换”的方案，因为会把模板占位符、归档证据和 live 协议面混在一起，既容易误改，也不利于验证。
- 不选“只改文档不加测试”的方案，因为 sibling path 和 retired path 两类错误都已经真实出现，继续依赖人工记忆成本太高。
- 不选“直接做通用链接检查器”的方案，因为当前真实问题集中且边界清晰，先用现有测试文件加白名单断言更低风险。

## Overview Reflection
- 我先挑战了“是否应该把 archived task packages 一起清理”。结论是不应该。本任务的成功标准是 live protocol surface 的可信度，而归档材料属于历史证据，批量修改会扩大范围并削弱历史可追溯性。
- 我再挑战了“是否应该顺手做一个通用 Markdown 路径解析器”。目前没有证据表明全仓库都需要这个层级的抽象；真实缺陷集中在少数 live docs，优先用受影响文档白名单测试更稳妥。
- 我也挑战了“是否只修 `using-openharness` 的 references，不把 `systematic-debugging` 旧路径纳入”。结论是否定的，因为这些材料会被维护者直接读取，继续保留旧入口会破坏任务目标里“真实入口唯一”的要求。
- 架构视角下接受的约束是：主路径必须短，修复只改变路径写法，不改变 runtime capability contract 的职责边界。
- 产品视角下接受的约束是：这一轮先解决“读文档时会被带到不存在文件”的直接痛点，不追求一次性把所有历史文本都清零。
- 验证影响已经显式纳入方案：如果没有自动断言，本轮只能算一次手工清扫，不能算稳定协议收敛。
