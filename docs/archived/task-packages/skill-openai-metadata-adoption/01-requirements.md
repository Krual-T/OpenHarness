# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把仓库内 vendored skills 从“只有 `SKILL.md` 描述、几乎没有官方 metadata”提升到“具备可被 Codex 直接消费的 `agents/openai.yaml` 元数据”，让技能发现、隐式触发边界和工具依赖声明都尽量前置到官方支持层。

目标用户是后续在本仓库或下游仓库中复用这些 skills 的维护者与 Codex 本体；核心场景是 Codex 在读取 skills 元数据时，能够在不先加载全文的情况下知道技能名称、用途、是否允许隐式触发以及是否依赖额外工具。

## Problem Statement
当前 live repo skills 基本只有 `SKILL.md` 头部的 `name` 和 `description`，几乎没有 `agents/openai.yaml`。这带来三个直接问题：

1. 官方支持的元数据层基本空缺，Codex 只能依赖 `description` 做粗粒度隐式匹配，无法在 metadata 层先收紧触发边界。
2. 哪些技能适合自动触发、哪些技能应当显式调用，当前只散落在正文规则里，缺少机器可读约束，容易随着 skill 文案演化而漂移。
3. 像 `project-memory` 这样已经开始使用 metadata 的技能，与其他 skills 的表面不一致，维护者无法快速判断仓库对 OpenAI skill metadata 的采用标准。

现在做这件事，是为了把本仓库的 skill surface 从“说明文驱动”推进到“协议与 metadata 共同约束”，减少误触发和隐式行为扩大化。

## Required Outcomes
1. 明确 live repo skill 的覆盖范围，至少包括 `skills/` 根目录下当前对仓库协议或执行流程生效的每一个技能目录。
2. 为这些技能补齐 `agents/openai.yaml`，并且字段只使用官方文档已支持的形状：`interface`、`policy.allow_implicit_invocation`、`dependencies.tools`。
3. 给每个技能明确一条触发策略结论：保留隐式触发，或降为显式调用优先；结论必须能从技能职责和仓库协议中自洽推出。
4. 为需要工具依赖的技能补充 `dependencies.tools`，避免依赖要求只存在于长篇正文说明中。
5. 新增或扩展轻量测试，至少覆盖：
   - 关键 skills 的 `agents/openai.yaml` 存在；
   - 关键技能的 `allow_implicit_invocation` 分类符合设计；
   - metadata 与 `SKILL.md` 的职责描述不明显冲突。
6. 最终实现应能通过任务包声明的校验命令。

单一成功指标是：仓库内 live repo skills 的 metadata 覆盖率达到 100%，并且显式调用优先的技能不再仅靠正文约束来避免误触发。

Acceptance Criteria:
1. `find skills -path '*/agents/openai.yaml'` 的结果与设计声明的 live repo skill 集合一致。
2. 至少一条自动化测试会在某个技能缺失 metadata 或策略回退时失败。
3. 维护者只看 metadata，就能区分“可以被 Codex 隐式触发的核心流程技能”和“必须在明确语境下调用的辅助技能”。

Counterexample:
- 如果只是给 README 或 `SKILL.md` 增加说明，但仓库中大部分技能仍没有 `agents/openai.yaml`，或者没有用 `allow_implicit_invocation` 固定显式调用边界，则本任务不算完成。

## Non-Goals
- 不重命名、重写或拆分现有 skill 本体内容；本轮重点是补 metadata，而不是改技能协议。
- 不把仓库整体从 `skills/` 目录迁移到新的技能布局；当前只补齐每个技能目录内部的 `agents/openai.yaml`。
- 不引入重型 metadata 生成器、注册中心或额外打包流程；优先使用静态 YAML 文件和轻量测试。
- 不在本轮顺手扩展与 OpenAI metadata 无关的 skill 文案优化，除非为了消除 metadata 与正文的直接冲突。

## Constraints
- 必须以 OpenAI 官方 Codex skills 文档为 metadata 字段边界，避免设计依赖未公开支持的私有字段。
- 必须保留 `using-openharness` 作为仓库入口技能，不得因为补 metadata 而引入新的并行入口层。
- 隐式触发策略必须与仓库现有 skill routing 规则兼容，不能把需要仓库自主路由的核心流程技能误降成只能手工点名。
- 成本上限是一次聚焦改动：允许新增 `agents/openai.yaml` 和少量测试，不应扩展成大规模脚手架工程。
- 任务完成前仍需遵守仓库校验协议，至少运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 和本任务声明的验证命令。
