# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
本轮目标是把 OpenHarness 现有含混的 runtime `helper` 想法收敛成清晰的 `Runtime Workflow Package`（暂称 `RWP`）协议：项目可以通过一个不会被 Codex 等 agent 自动加载的目录注册 runtime 级验证工作流，OpenHarness CLI 负责渐进式披露名称、描述和详细内容，并提供统一运行外壳；agent 在合适任务中应主动发现、选择、纳入验证计划，并把执行结果、日志观察、证据缺口写回 task package。

单一成功指标：本轮完成后，OpenHarness 文档和协议能让一个项目作者清楚知道如何新增一个 RWP，也能让 agent 清楚知道何时查询 RWP、何时读取详情、何时纳入 `03-detailed-design.md` / `04-verification.md` / `05-evidence.md`，且不会把具体 runtime workflow 的内部步骤提前固定为通用命令。

## Problem Statement
目标用户是两类人：

- OpenHarness 维护者，需要把 runtime 级验证纳入固定 workflow，而不是只留下“项目自己处理”的口头约定。
- 下游项目作者和执行任务的 agent，需要在任务涉及真实运行、外部系统、账号凭证、日志、回调、消息、浏览器或其他 runtime 行为时，能发现项目已有的验证工作流并把它纳入测试证据。

当前矛盾是：OpenHarness 已经有 task package、验证写回和 runtime capability contract 的雏形，但 `helper` 这个概念太泛，无法清楚表达“项目如何新增一个 runtime test workflow，让 agent 主动发现并纳入测试体系”。如果继续只靠 README、聊天记录或临时命令，agent 很容易只跑 `pytest` 就声称完成，或者把一次性脚本误当成项目级可复用能力。

现在需要做，是因为真实项目中的 runtime 验证经常包含登录、token 获取、第三方 API、消息投递、日志观察、回调确认和失败证据收集。这些内容既不能被 OpenHarness 通用框架硬编码，也不能完全留给人工记忆。OpenHarness 需要定义一个项目可插拔、agent 可渐进披露读取、结果可写回 task package 的协议层。

## Required Outcomes
- 明确弃用或降级 `helper` 作为核心概念，提出更清晰的 RWP 概念边界。
  - Acceptance Criteria: 文档能说明 RWP 与普通 skill、普通脚本、临时命令、旧 `helper` 的区别。
- 明确 RWP 的注册形态是目录包，而不是集中 YAML 注册表，也不是 `SKILL.md` 自动加载入口。
  - Acceptance Criteria: 文档能说明 RWP 目录下 `workflow.md` 使用类似 skill 的 YAML meta 头提供 `name` 和 `description`，但不使用 `SKILL.md` 文件名，避免被 agent 自动加载。
- 明确 OpenHarness CLI 对 RWP 的最小职责。
  - Acceptance Criteria: 文档能说明 CLI 至少应支持列出 RWP 摘要、读取某个 RWP 详情、运行某个 RWP 的统一外壳；CLI 不应预定义具体 workflow 内部的环境检查、观察、登录、清理等子命令。
- 明确 agent 主动纳入 RWP 的 skill 规则应落在哪些现有 OpenHarness skill 或 guidance 中。
  - Acceptance Criteria: 文档能指出入口路由、探索阶段、详细设计、完成前验证、验证与证据模板各自需要承担的规则，而不是新增一个平行入口 skill。
- 明确 RWP 合格标准。
  - Acceptance Criteria: 文档能要求 RWP 说明环境准备、运行驱动、runtime 观察、日志或其他 evidence 来源、成功标准、失败证据、限制和 task package 写回要求，但不要求这些能力映射为固定命令名。
- 明确 `lark-cli` 或飞书/Lark 相关工作流只作为首个参考样例。
  - Acceptance Criteria: 文档能说明这个样例用于验证协议是否能承接真实外部系统交互，而不是把 `lark-cli` 抽象成通用 runtime 测试模型。

## Non-Goals
- 不在本包里实现 openrelay 的具体飞书测试场景。
- 不把 runtime 验证简化成某个固定命令或固定步骤列表。
- 不要求所有项目都使用同一种工具、语言、外部系统或脚本目录内部结构。
- 不让 RWP 使用 `SKILL.md` 作为入口，也不依赖 Codex 自动加载机制。
- 不在 `workflow.md` 中声明固定脚本入口表；具体 workflow 的内部 action、参数和脚本组织由该 RWP 自己决定。
- 不在本轮定义 OpenHarness 通用的登录、token 获取或 API client 库；项目可以在 RWP 目录内放自己的复用库，但这不是 OpenHarness 核心协议的第一优先事项。

Counterexample: 一个项目只新增 `scripts/smoke.py` 并在 README 里写“可以手动运行这个脚本”，但没有 RWP 描述、没有 agent 可发现的名称与描述、没有说明 runtime 观察和 evidence 写回要求。这看起来也能做 runtime 验证，但不属于本任务要沉淀的可插拔 RWP 协议。

## Constraints
- 必须保持 `using-openharness` 是唯一仓库入口 skill；RWP 不能变成第二套入口系统。
- 必须沿用 task package 的 `03-detailed-design.md`、`04-verification.md`、`05-evidence.md` 写回闭环。
- RWP 发现必须支持渐进式披露：agent 先看到名称和描述，判断相关性后再读取详情，避免一次性加载所有 runtime 工作流内容。
- OpenHarness CLI 可以负责发现、展示、运行外壳和记录结果，但不应理解每个 runtime workflow 的业务语义。
- 本轮 `cost cap` 是设计并实现最小可验证协议表面；如果需要构建复杂插件运行时、跨语言 sandbox、统一认证库或完整 Lark 场景自动化，应拆成后续 task package。
