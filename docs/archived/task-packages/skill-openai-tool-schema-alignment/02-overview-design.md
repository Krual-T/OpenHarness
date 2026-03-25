# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖三类表面：

1. 仓库内 live repo skills 的 `skills/*/agents/openai.yaml`。
2. `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 中对 skill metadata 的协议回归测试。
3. 本任务包自身的需求、设计、验证与证据记录。

不纳入范围的部分：
- 各技能的 `SKILL.md` 正文内容；
- `docs/archived/` 中历史任务包的历史实现；
- OpenAI 官方工具依赖支持范围之外的任何自定义扩展。

## Proposed Structure
推荐方案分两层：

1. schema 对齐层
   - 删除仓库里所有 `dependencies.tools: ["shell"]` 风格声明。
   - 保留 `interface` 与 `policy.allow_implicit_invocation` 不变。
   - 如果未来仓库真要声明工具依赖，只允许使用官方当前公开支持的对象数组形状。

2. 测试防回归层
   - 删除对 `["shell"]` 的直接断言。
   - 新增通用约束：若某个 skill 声明 `dependencies.tools`，它必须是对象数组，且当前只能出现 `type: "mcp"`。
   - 对当前没有官方支持依赖需求的技能，允许完全省略 `dependencies` 字段。

关键约束是，不把“官方代码里结构上可能接受任意 `type` 字符串”误解成“官方文档已经支持任意工具类型”。仓库对外声明应以公开支持面为边界。

## Key Flows
主路径如下：

1. 先核对 OpenAI 官方公开示例与官方代码仓库中的技能依赖模型。
2. 判断仓库当前哪些 `openai.yaml` 触犯了“形状不对”或“支持范围错误”，还是二者兼有。
3. 把受影响技能的 `dependencies` 移除，避免继续发布非官方约定。
4. 用测试把正确边界固化为“对象数组 + 当前仅 `mcp`”。
5. 运行仓库协议检查与测试，回写验证证据。

## Stage Gates
进入 detailed 前，overview 必须已经明确：

1. 官方依据来自哪些页面或仓库文件。
2. 仓库当前问题是“形状错误”还是“支持范围错误”，还是二者兼有。
3. 推荐动作是改成结构化 `shell`，还是直接移除 `shell` 依赖。
4. 测试将如何避免将来再次固化本地私有约定。
5. 如果未来 OpenAI 公布 `shell` 依赖，当前方案如何单点扩展。

失败模式与降级方向：
- 如果官方依据只能证明“对象数组”，不能证明 `shell` 是否公开支持，则也不应继续保留 `shell`，因为仓库没有足够依据宣称它是官方 schema。
- 如果后续官方文档新增了 `shell` 支持，只需单点更新 YAML 和测试，无需重做整个 skill metadata 分层。

## Trade-offs
推荐方案的收益：
- 让仓库测试重新围绕官方公开契约，而不是围绕历史本地写法。
- 避免下游维护者把 `shell` 误认为 OpenAI 当前正式支持的 `dependencies.tools` 类型。
- 改动面小，只涉及静态 YAML、测试和任务包文档。

代价：
- 失去在 metadata 层显式表达“这些技能通常会用到 shell”的本地提示。
- 后续若官方正式支持 `shell`，需要再补一轮更新。

不选的方向：
- 把 `["shell"]` 改成 `[{type: "shell", value: "shell"}]`。不选，因为当前公开文档没有把 `shell` 列为受支持类型，这仍然是在发明本地 schema。
- 保留现状，仅放宽测试。也不选，因为仓库仍会继续携带误导性的非官方 metadata。

## Overview Reflection
本轮 overview 反思重点挑战了两个方向：

1. 是否应该仅修测试，不改 YAML。
   - 结论：不行。这样只能减少显式错误断言，但仍然保留了误导性的非官方声明。

2. 是否应该把 `shell` 先改成结构化对象写法保留。
   - 结论：不行。官方公开说明当前只支持 `mcp`，因此“结构化 `shell`”依然是仓库私有扩展，不适合继续放在官方 metadata 名义下。

验证影响：
- 反思后将验证重点从“某个技能是否声明 shell”改成“是否符合官方对象数组形状，以及是否只使用当前公开支持的 `mcp`”。

Challenge Closure:
- 接受：以公开文档支持面为边界，删除非官方 `shell` 依赖声明。
- 拒绝：用结构化 `shell` 继续保留仓库本地约定。
- 延期：若未来 OpenAI 公开支持新的工具依赖类型，再单独开任务包更新。
