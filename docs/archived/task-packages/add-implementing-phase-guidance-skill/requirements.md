# 需求

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **写前确认**：
> 1. 当前痛点、缺口或风险是什么？为什么现在做而不是以后？
> 2. 本轮必须交付哪些结果？各自的验收标准是什么？
> 3. 本轮明确不做什么？至少想出一个反例——看起来相关但不属于本轮。
> 4. 目标用户是谁？核心场景是什么？
> 5. 成本上限和不可违反的约束是什么？

## 目标

将 implementing 阶段技能从"仅 TDD 循环指导"升级为完整的实现阶段引导，参照 Karpathy 的 LLM 编程行为准则（Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution），补充入口分流、重入指南、人机协同停点、反合理化、与相邻文档边界等标准章节，使其与其他五个阶段技能结构一致。

**单一成功指标**：implementing 阶段技能包含与其他阶段技能对等的全部标准章节，且 Karpathy 四项准则已融入实现指导。

## 问题陈述

1. **结构不一致**：implementing 是六个阶段技能中唯一缺少入口分流、重入指南、反合理化、与相邻文档边界四个标准章节的技能。
2. **人机协同断点**：commit `7f584a6` 为 brainstorming 之后的四个阶段（exploring-solution-space、detailed-design、verification-designing、verifying）增加了强制性人机协同停点，但 implementing 被遗漏——agent 写完中间事实后可以直接 transition，用户没有审阅确认的机会。
3. **实现指导单一**：当前只覆盖 TDD 循环（RED → GREEN → REFACTOR），缺少"如何写代码"的行为准则——agent 容易过度抽象、做非必要的重构、在不确定时默不作声地选一个方案。
4. **缺少项目工具指引**：agent 不知道本项目的测试/检查/格式化命令（`uv run pytest`、`uv run ruff check`、`uv run pyright` 等）。

目标用户是执行 implementing 阶段的 agent；核心场景是 agent 从 `verification-designing` 进入 implementing 后，需要知道怎么写代码、怎么和用户协同、怎么处理失败回退。

## 必须交付的结果

1. **融入 Karpathy 四项准则到实现步骤** — 验收标准：implementing SKILL.md 的步骤章节中可见 Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution 四项准则的具体行为指令，且每项指令可直接指导 agent 的编码行为
2. **补充入口分流章节** — 验收标准：区分"首次进入 implementing（完整 TDD 流程）"与"从 verifying 回退（增量修复）"两种场景，各有对应的行为分支
3. **补充重入指南** — 验收标准：从 verifying 回退时，agent 知道如何声明本轮增量目标（"上次失败的是 X，本轮只验证 X 是否修复 + 已有通过的 Y 不退化"）
4. **补充 evidence.md 文档审阅停点** — 验收标准：写完 evidence.md 中间事实并通过阶段结束检查自检后，告知用户文档路径，获得用户审阅确认后才可 transition
5. **补充项目工具命令参考** — 验收标准：列出本项目用到的 `uv run pytest`、`uv run ruff check`、`uv run pyright` 等命令，agent 知道如何运行
6. **补充反合理化表格** — 验收标准：至少覆盖 4 个常见借口（如"先全部实现完再跑测试""这个抽象以后会用到的""evidence 最后补一下就行"等）及其反驳
7. **补充常见失败模式** — 验收标准：在当前 TDD 循环故障处理表之外，补充 implementing 阶段特有的编码行为失败模式（如过度抽象、跳过 RED 直接 GREEN、擅自重构无关代码等）
8. **补充与相邻文档边界章节** — 验收标准：明确 implementing 写什么（中间事实、变更文件、TDD 循环记录）vs verification-designing 写什么（验证策略）vs verifying 写什么（最终结论、残余风险）

## 非目标

- 不修改 CLI 状态机或 workflow 定义——纯 skill 指令层面改动
- 不修改 `verification-designing/SKILL.md` 或 `verifying/SKILL.md`
- 不引入逐项设计确认机制——那是设计阶段的职责，implementing 阶段不适用
- 不修改 `evidence.md` 模板文件——模板本身不需要改动

## 约束

- 改动范围仅限于 `skills/using-openharness/states/implementing/SKILL.md`
- 不改变现有 TDD 循环（RED → GREEN → REFACTOR）的核心逻辑，Karpathy 准则作为补充而非替代
- 与其他五个阶段技能保持结构一致（章节命名、停点格式、术语统一）
- 遵循仓库的 skill 写作约定（YAML frontmatter、中文正文、英文命令/状态值/文件名/路径）
