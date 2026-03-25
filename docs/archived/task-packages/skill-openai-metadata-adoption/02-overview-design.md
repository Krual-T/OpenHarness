# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
覆盖范围是仓库 live repo skills 的技能目录表面，也就是 `skills/*/SKILL.md` 以及对应新增的 `skills/*/agents/openai.yaml`。

同时覆盖一层轻量防回归测试，优先落在现有 `skills/using-openharness/tests/openharness_cases/` 测试体系中，因为它已经承担 live protocol surface 的文档与结构回归。

不纳入范围的部分：
- `docs/archived/` 中的历史 task package；
- 用户主目录下的系统级技能与外部仓库技能；
- OpenAI metadata 之外的新 skill loader 或注册机制。

## Proposed Structure
推荐方案分三层：

1. 技能目录层
   - 为每个 live repo skill 增加 `agents/openai.yaml`。
   - `interface` 负责对外展示名、简短说明和默认提示。
   - `policy.allow_implicit_invocation` 负责表达该技能是否允许仅凭用户语义自动触发。
   - `dependencies.tools` 只在确有需要时声明，不为了形式统一而空写。

2. 策略分类层
   - 核心流程技能保持可隐式触发：`using-openharness`、`brainstorming`、`exploring-solution-space`、`systematic-debugging`、`test-driven-development`、`verification-before-completion`。
   - 明显需要明确上下文或显式授权的技能降为显式调用优先：`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`、`finishing-a-development-branch`。
   - 条件型辅助技能单独判断：`requesting-code-review`、`receiving-code-review`、`project-memory` 是否允许隐式触发，依据是“仓库是否希望 Codex 在常见输入下自动选择它们而不增加误触发成本”。当前推荐保留 `receiving-code-review` 和 `project-memory` 的隐式触发，`requesting-code-review` 设为显式调用优先。

3. 测试约束层
   - 在现有测试目录中增加 metadata 存在性与策略分类断言。
   - 测试只验证 repo 约定，不实现新的解析器；必要时直接读取 YAML 文件做结构检查。

关键约束是：metadata 只下沉“稳定、值得机器读取的约束”，而不是把整份 `SKILL.md` 摘要复制进 YAML。

## Key Flows
主流程如下：

1. 维护者在 `skills/<skill>/SKILL.md` 定义技能职责与正文边界。
2. 同目录下的 `skills/<skill>/agents/openai.yaml` 提前向 Codex 暴露该技能的展示元数据、隐式触发策略与工具依赖。
3. Codex 在技能发现阶段先读取 `name`、`description` 和 `agents/openai.yaml`，再决定是否需要加载完整 `SKILL.md`。
4. 防回归测试读取 repo skill 目录，验证关键技能的 metadata 文件存在且触发策略符合仓库约定。

状态流不是新增运行时状态，而是把“能否隐式触发”从正文约束前移成 metadata 约束，缩短技能发现的主路径。

## Stage Gates
进入 detailed 之前，overview 必须已经明确：

1. 哪些 skill 属于本轮 live surface，需要补 metadata。
2. 哪些 skill 继续允许隐式触发，哪些改成显式调用优先。
3. metadata 的字段边界只使用官方已公开支持的结构。
4. 防回归策略落在现有测试体系，而不是临时人工约定。
5. 如果某个技能的 implicit 策略存在争议，要么在 overview 中作出明确取舍，要么在 detailed 中以决策闭环方式记录延期条件。

关键失败模式与降级方向：
- 如果某技能是否允许隐式触发无法在本轮稳定定论，则默认保守收敛到显式调用优先，而不是继续放任模糊触发。
- 如果某技能当前没有明确工具依赖，就先不声明 `dependencies.tools`，避免为了“看起来完整”而写出虚假依赖。

## Trade-offs
推荐方案的收益：
- 直接复用 OpenAI 官方 metadata 入口，不引入自定义协议。
- 让“是否隐式触发”变成机器可读约束，减少技能描述轻微改动导致的触发漂移。
- 成本低，只需补 YAML 文件与少量测试。

代价：
- 需要为每个 skill 写一份短元数据，维护面会增加。
- 某些技能的隐式/显式边界需要做主观取舍，不能完全自动推导。

不选的方案：
- 只给少数技能补 metadata。问题是仓库表面会继续不一致，维护者仍无法形成统一心智模型。
- 通过扩写 `description` 来替代 `allow_implicit_invocation`。问题是这仍依赖自然语言边界，无法把“必须显式调用”的约束真正下沉到官方 metadata 层。
- 先写一个 metadata 生成脚本。当前技能数量有限，静态文件更直观，也更容易评审和回归测试。

回退面很小：若某个技能的触发策略判断失误，只需修改单个 `agents/openai.yaml` 和对应测试，不需要回退仓库协议。

## Overview Reflection
本轮 overview 反思重点挑战了两个方向：

1. 是否应该把所有 helper skill 都改成显式调用优先。
   - 结论：不能一刀切。像 `receiving-code-review` 和 `project-memory` 这类技能虽然是 helper，但其触发条件本身可以从用户输入或当前任务上下文稳定识别，保留隐式触发更符合仓库自主工作流。

2. 是否需要先新增一个脚本统一校验 metadata。
   - 结论：当前不需要。仓库已有轻量 pytest 文本与结构测试体系，直接复用更稳，避免为少量静态 YAML 过度工程化。

验证影响：
- overview 已经把最终验证路径约束到“读取 metadata 文件 + 运行现有 pytest + 运行 `check-tasks`”，后续 detailed 只需要把测试粒度、文件落点和策略表写具体。

Challenge Closure:
- 接受：对明显需要人工授权或明确场景的技能使用 `allow_implicit_invocation: false`。
- 拒绝：为了追求一致性而给所有技能声明空的 `dependencies.tools`。
- 延期：如实现阶段发现 `requesting-code-review` 或 `project-memory` 的策略分类与真实使用体验冲突，可在实现验证后单点调整，但不得影响本轮先建立 metadata 全覆盖。
