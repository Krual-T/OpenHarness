# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
本轮目标是把“逐项设计确认”沉淀为 OpenHarness 设计阶段的默认协作范式：当非机械开发任务进入 `02-overview-design.md` 或 `03-detailed-design.md` 时，agent 应主动提出按设计点逐项确认，每次给出一个设计点、推荐方案、理由和确认问题；用户确认后再写回 task package 并推进下一个设计点。

单一成功指标：本轮完成后，OpenHarness 的入口 skill、设计阶段 skill 和对应 writing guidance 能明确要求 agent 在非机械开发任务的设计阶段主动提出逐项设计确认，并能把已确认的 decision points 写回 `02` 或 `03`，而不是依赖用户先说“每个设计点都需要我确认”。

## Problem Statement
目标用户是使用 OpenHarness 协作开发的维护者和 agent。

核心场景是：一个任务进入设计阶段，里面存在多个需要人机共同确认的取舍。过去 agent 往往一次性写完整 `02` 或 `03`，用户只能在成品文档上整体 review。这样容易发生两个问题：

- 用户不同意某个早期设计点时，后续文档已经建立在错误前提上，返工成本高。
- 设计决策留在聊天里，没有作为逐项确认的 decision points 写回 task package，后续实现时容易丢失上下文。

OH-040 的 RWP 设计过程中出现了更好的互动方式：agent 每次提出一个设计点，用户确认或修改后再推进下一个点。这个方式让目录结构、CLI 语义、脚本执行规则、日志边界和 runtime API 等关键决定逐步收敛，也避免了把用户并未确认的实现细节提前固化。

现在要做，是因为这不是 RWP 独有经验，而是 OpenHarness 设计阶段可以复用的协作协议。它应该由 agent 主动提出，不应要求用户明确说“每个设计点都需要我确认”。

## Required Outcomes
1. 定义任务分类规则。
   - Acceptance Criteria: 文档能区分 `mechanical`、`standard development`、`protocol/architecture` 三类，并说明每类是否默认启用逐项设计确认。
2. 定义默认触发规则。
   - Acceptance Criteria: 文档明确非机械开发任务进入 `02` 或 `03` 时，agent 应主动提出逐项设计确认；用户不需要先明确要求。
3. 定义逐项设计确认的交互协议。
   - Acceptance Criteria: 文档能说明每次只提出一个设计点，包含推荐方案、理由、确认问题；用户确认后再写回 task package。
4. 定义写回和回退规则。
   - Acceptance Criteria: 文档能说明 overview 级设计点写入 `02`，detailed 级设计点写入 `03`；如果后续点改变前序总体边界，先同步 `02` 再继续 `03`。
5. 更新相关 OpenHarness skills 和 writing guidance。
   - Acceptance Criteria: `using-openharness`、`brainstorming`、`exploring-solution-space`、`overview-design-writing-guidance.md`、`detailed-design-writing-guidance.md` 至少能表达该模式的触发和写回边界。
6. 添加协议测试。
   - Acceptance Criteria: 测试能锁住逐项设计确认模式在相关文档中的存在、默认触发、任务分类和写回规则。

## Non-Goals
- 不实现 UI、表单或交互式 wizard。
- 不要求所有机械改动都进入逐项设计确认。
- 不改变 task package 的文件结构。
- 不要求用户必须接受逐项确认；用户可以要求 agent 自主推进或调整确认粒度。
- 不把逐项确认用于 verification 阶段替代 fresh evidence。

Counterexample: 一个任务只是修正拼写、格式、明显路径引用或无行为变化的小测试断言。它属于 `mechanical`，可以直接修改并验证，不应该强制逐项设计确认。

## Constraints
- `using-openharness` 仍是唯一仓库入口 skill；逐项设计确认不能成为第二套入口系统。
- 设计点确认必须写回 task package，不能只停留在聊天记录。
- 本轮只产品化协作协议和 guidance，不引入新的 task package 文件。
- `cost cap` 是更新现有 skills、guidance 和协议测试；如果后续要构建交互式工具或专门 CLI，应另开任务包。
