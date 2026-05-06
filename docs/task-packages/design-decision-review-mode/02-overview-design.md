# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮把逐项设计确认作为 OpenHarness 现有设计阶段协议的一部分，而不是新增独立 skill 或新 task package 文件结构。

覆盖面包括：

- `using-openharness` 的入口级路由规则。
- `brainstorming` 的任务分类与需求后交接规则。
- `exploring-solution-space` 的 overview/detailed 设计阶段执行规则。
- `overview-design-writing-guidance.md` 与 `detailed-design-writing-guidance.md` 的写回要求。
- 对应协议测试。

不覆盖：

- 不新增独立 skill。
- 不新增 task package 文档文件。
- 不实现 UI、表单、wizard 或 CLI。
- 不改变 verification 阶段的 fresh evidence 要求。

## Proposed Structure
逐项设计确认落在现有 OpenHarness 层次中：

1. `using-openharness`
   - 只放入口级规则：非机械开发任务进入设计阶段时，agent 应主动提出逐项设计确认。
2. `brainstorming`
   - 在需求收敛后识别任务分类：`mechanical`、`standard development`、`protocol/architecture`。
   - agent 提出推荐分类，但任务分类必须经过人类确认后才作为后续设计阶段的触发强度依据。
3. `exploring-solution-space`
   - 真正执行逐项确认，把 design decision points 拆开推进。
4. `overview-design-writing-guidance.md`
   - 要求 `02` 记录影响系统边界、主结构、流程的已确认设计点。
5. `detailed-design-writing-guidance.md`
   - 要求 `03` 记录实现级接口、文件、测试、迁移顺序的已确认设计点。

这个结构的关键边界是：逐项设计确认是设计阶段的协作方式，不是第二套工作流入口。

## Key Flows
主流程：

1. 任务需求收敛后，agent 判断并提出任务分类建议。
2. 人类确认任务分类，或调整为另一类。
3. 如果分类是 `mechanical`，agent 不主动提出逐项确认，直接说明“这是机械改动，我会直接修改并验证”。
4. 如果分类是 `standard development`，agent 在进入 `02` 或 `03` 前主动提出逐项设计确认；用户可以要求更粗粒度或授权自主推进。
5. 如果分类是 `protocol/architecture`，agent 在进入 `02` 或 `03` 前主动提出并默认逐项推进；除非用户明确授权跳过，否则每个关键 design decision point 都要确认。
6. 已确认的 overview 级设计点写入 `02-overview-design.md`；已确认的 detailed 级设计点写入 `03-detailed-design.md`。
7. 如果后续 detailed 设计点改变前序 overview 边界，先同步 `02`，再继续 `03`。

失败信号：

- agent 未经人类确认就把任务分类作为后续触发依据。
- 非 mechanical 任务直接一次性写完整设计，未主动提出逐项确认。
- 已确认设计点只留在聊天里，没有写回 task package。
- detailed 设计改变 overview 边界，但没有先更新 `02`。

逐项确认的单点格式：

```text
设计点 N/M：<短标题>

推荐方案：
<一句或几句说明推荐做法>

理由：
<为什么这样做，主要取舍是什么>

影响范围：
<会写入 02 还是 03，会影响哪些 skill/guidance/code>

请确认：
<一个明确 yes/no 或修改型确认问题>
```

`N/M` 表示当前设计点进度。`M` 可以是当前已识别的设计点总数；如果探索中发现新设计点，agent 应更新后续进度并说明新增原因。

每次只处理一个设计点。用户确认后，agent 立即写回对应 task package 文档。用户修改前序设计点时，agent 先更新已有文档，再继续新设计点。用户说“继续”可以视为确认当前设计点，但不等于授权后续所有设计点自动通过。

用户响应解释规则：

- `确认` / `ok` / `可以` / `继续` / `下一个`
  - 只表示当前设计点通过。
  - agent 写回当前设计点后，再提出下一个设计点。
  - 不表示后续设计点自动通过。
- `自主推进` / `你决定` / `不用每点确认`
  - 表示降低后续确认粒度。
  - agent 仍需把关键 decision points 写回 task package。
  - 对 `protocol/architecture`，agent 应先复述“我会跳过逐点确认，但仍会记录关键取舍”，再继续。
- 用户修改当前设计点
  - agent 先复述最终版设计点。
  - 写回 task package。
  - 再进入下一个点。
- 用户推翻前序设计点
  - agent 先更新已写入的 `02` 或 `03`。
  - 如果影响总体边界，先同步 `02`，再继续 `03`。
  - agent 需要说明哪些后续设计点受影响。

进入设计阶段前的推荐话术：

```text
这个任务已确认属于 <classification>。接下来会进入 <overview/detailed> 设计阶段。

我建议按逐项设计确认推进：我会每次提出一个设计点，包含推荐方案、理由、影响范围和确认问题；你确认后我写回 task package，再进入下一个点。

当前预计有 N 个设计点。先从 1/N 开始。
```

## Stage Gates
overview 进入 detailed 前必须满足：

- 已确认逐项设计确认落在现有 `using-openharness` / `brainstorming` / `exploring-solution-space` / writing guidance 层级中，不新增独立 skill 或 task package 文件结构。
- 已确认任务分类包含 `mechanical`、`standard development`、`protocol/architecture`，且分类必须经过人类确认。
- 已确认非 mechanical 任务进入 `02` 或 `03` 前，agent 应主动提出逐项设计确认。
- 已确认单个设计点必须带 `N/M` 进度、推荐方案、理由、影响范围和确认问题。
- 已确认用户说“继续/下一个”只确认当前设计点，不授权后续设计点自动通过。
- 已确认逐项确认结束不等于设计阶段完成，仍必须满足 `02` 或 `03` 自身 stage gate。

## Trade-offs
备选方案一：所有任务都强制逐项确认。

这个方案最一致，但会让拼写、格式、路径引用等机械改动变慢。当前选择是对 `mechanical` 保持轻量，对非 mechanical 默认主动提出逐项确认。

备选方案二：只有用户明确要求时才启用逐项确认。

这个方案不会打扰用户，但会把协作质量继续依赖用户临场提醒。当前选择是 agent 主动提出，用户可以调整粒度或授权自主推进。

备选方案三：新增独立 skill。

这个方案边界清楚，但会制造第二套设计入口。当前选择是把它作为现有设计阶段协议，由 `using-openharness` 路由、`exploring-solution-space` 执行、writing guidance 写回。

## Recommended Diagrams
本轮不强制补图。逐项确认主流程可以用文字表达清楚；如果后续实现中出现阶段路由歧义，再补一张 `PlantUML` activity diagram 表达分类确认、逐项确认和文档写回流。

## Overview Reflection
挑战一：是否应该默认所有开发任务都逐项确认？

结论：拒绝。机械任务保持直接执行更合理；但非 mechanical 任务默认主动提出逐项确认。

挑战二：任务分类是否可以由 agent 自行决定？

结论：拒绝。agent 可以提出推荐分类，但必须经过人类确认，避免后续触发强度建立在错误分类上。

挑战三：用户说“继续”是否能视为授权后续全部设计点？

结论：拒绝。`继续` 只确认当前设计点，后续设计点仍需按当前粒度推进。

挑战四：N/M 设计点完成是否等于 stage gate 完成？

结论：拒绝。N/M 只是协作进度，设计阶段完成仍由 `02` 或 `03` 的 writing guidance gate 决定。如果发现 gate 缺口，agent 应新增设计点并更新进度。
