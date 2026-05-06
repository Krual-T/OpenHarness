# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 OpenHarness 对 `Runtime Workflow Package`（`RWP`）的协议、发现路径、agent 路由规则、CLI 最小外壳、runtime API 和 task package 写回要求。

覆盖面包括：

- 将旧的 runtime `helper` 表述替换或降级为 RWP 协议，避免继续使用过泛的“辅助技能”概念。
- 定义项目内 RWP 目录包的发现原则：RWP 统一放在 `.harness/rwp/workflows/<workflow-name>/workflow.md`，不使用 `SKILL.md`，不被 Codex 等 agent 自动加载，而由 OpenHarness CLI 渐进披露。
- 定义 `workflow.md` 的职责：提供类似 skill meta 的 `name` 和 `description`，并在正文说明这个 runtime workflow 的用途、环境、可用脚本、观察证据、成功标准、失败证据、限制和写回要求。
- 定义 `openharness rwp` 的最小 CLI 表面：列出摘要、读取详情、显式运行指定 workflow 的脚本。
- 定义 `openharness.rwp` runtime API：脚本可以直接 `from openharness.rwp import get_logger` 获取标准 logger。
- 改造现有 OpenHarness skill 与写作 guidance，让 agent 在入口、探索、详细设计和完成前验证阶段主动考虑 RWP。
- 明确 RWP 运行结果、日志或其他 runtime 观察证据如何进入 `04-verification.md` 和 `05-evidence.md`。

不覆盖：

- 不实现 openrelay 或 Lark/飞书的具体 runtime 验证流程。
- 不定义固定的 RWP 内部 action 名称，例如 `check-env`、`observe`、`login` 或 `cleanup`。
- 不把 RWP 设计成 OpenHarness 内置的跨语言插件运行时。
- 不提供 OpenHarness 通用登录、token、API client 或 sandbox 库。
- 不要求所有项目维护集中 YAML 注册表。

## Proposed Structure
推荐结构分为四层：

1. `RWP directory package`
   - 每个项目在 `.harness/rwp/workflows/` 下放多个 RWP。
   - 每个 RWP 目录至少有 `workflow.md` 和 `scripts/`。
   - `workflow.md` 开头使用轻量 meta 头，最小字段是 `name` 和 `description`。
   - 正文承载 agent-readable 的详细说明，而不是脚本入口注册表。
   - `libs/` 只承载项目自有复用代码。
   - `logs/` 只承载运行证据与观察结果。

2. `OpenHarness CLI discovery and runner shell`
   - `openharness rwp list` 只读取并输出 RWP 摘要，支持渐进式披露。
   - `openharness rwp show <name>` 输出指定 RWP 的完整 `workflow.md`。
   - `openharness rwp run <name> <script.py> [args...]` 运行该 workflow `scripts/` 下显式指定的脚本。
   - CLI 不理解 Lark、浏览器、数据库或任何 workflow 内部业务语义；它只负责发现、读取、调用、返回退出码，并为后续 verification artifact 记录提供稳定输出。

3. `OpenHarness runtime API and project env`
   - OpenHarness 提供 `from openharness.rwp import get_logger`。
   - `get_logger()` 可以不带参数，脚本无需自己管理日志目录。
   - `openharness rwp run` 会自动尝试加载 `.harness/.env` 和 `.harness/rwp/.env`。
   - 项目自定义的 auth/token/client 逻辑仍由项目自己的 `libs/` 提供。

4. `Agent routing rules in existing skills`
   - `using-openharness` 负责入口判断：当任务可能涉及真实 runtime 行为时，agent 应查询 RWP 摘要，而不是只看 task package 的普通验证命令。
   - `exploring-solution-space` 负责探索阶段：根据任务包、代码触达面和 RWP 描述判断候选，并在 `02-overview-design.md` 记录是否采用、拒绝或延期。
   - `03-detailed-design.md` guidance 负责把选中的 RWP 写进测试优先设计，包括环境、运行驱动、观察点、成功标准、失败证据和预期写回。
   - `verification-before-completion` 负责完成前核对：如果设计纳入 RWP，必须执行、记录阻塞原因，或明确说明为什么本轮不能执行。
   - `04-verification.md` / `05-evidence.md` guidance 负责 fresh evidence、日志观察、artifact、残余风险和未覆盖缺口。

5. `Task-package evidence loop`
   - `03-detailed-design.md` 写计划：为什么选这个 RWP，预期运行什么，预期观察什么。
   - `04-verification.md` 写实际执行：运行命令、退出码、关键日志或 observation、偏差和 blocker。
   - `05-evidence.md` 写证据索引：artifact 路径、命令、人工步骤、残余风险和后续改进点。

关键数据/状态模型是 RWP 的三种披露状态：

- `summary`: `list` 只暴露 `name` 和 `description`，供 agent 低成本判断相关性。
- `detail`: `show` 暴露完整 `workflow.md`，供 agent 决定是否纳入本任务。
- `execution`: `run` 执行 workflow 脚本，并让 task package 记录 runtime 证据。

## Key Flows
主路径：

1. agent 进入 OpenHarness 任务，读取 active task package。
2. 如果任务可能涉及真实 runtime 行为，主智能体直接派子智能体运行 `openharness rwp list` 获取摘要。
3. agent 根据 `name`、`description`、任务包和代码触达面判断候选 RWP；候选较多或判断成本高时，可以让子智能体只基于摘要和任务上下文做候选筛选。
4. agent 对候选执行 `openharness rwp show <name>`，只读取相关 RWP 的详细说明。
5. overview 阶段记录采用、拒绝或延期的 RWP 结论。
6. detailed 阶段把选中的 RWP 纳入 runtime verification plan。
7. verification 阶段通过 `openharness rwp run <name> <script.py> [args...]` 执行；如果无法执行，记录 blocker 和残余风险。
8. evidence 阶段把命令、日志观察、artifact、失败证据或缺口写回。

失败信号：

- RWP 目录不存在或没有任何摘要：agent 应记录“项目未声明 RWP”，不能假装已有 runtime coverage。
- `workflow.md` 缺少 `name` 或 `description`：该 RWP 不应出现在 summary 中，CLI 应报告协议错误。
- 描述不清导致 agent 无法判断适用性：overview 应记录拒绝或延期理由，而不是强行纳入。
- `run` 入口失败或返回非零退出码：verification 应记录失败结果、stdout/stderr、日志观察和未覆盖缺口。
- RWP 文档只说“运行脚本”但没有说明观察和判定：不能算合格 RWP，应作为协议缺口处理。

降级方向：

- 如果项目尚未接入 RWP，本轮任务仍可回退到现有 `verification.required_commands` / `required_scenarios`，但必须在 task package 里明确 runtime coverage 缺口。
- 如果 RWP 能被发现但不能运行，仍可把 `show` 的详细内容作为计划依据，并在 `04-verification.md` 记录阻塞原因。
- 如果 CLI runner 约定尚未完全实现，第一版可先提供 list/show 和协议文档，run 作为详细设计中的最小可测增量。

## Stage Gates
进入详细设计前必须满足：

- RWP 的目录包边界已经确定：不使用 `SKILL.md`，不使用集中 YAML 注册表。
- CLI 的最小责任已经确定：`list`、`show`、`run` 外壳，不预定义 workflow 内部 action。
- agent 主动纳入 RWP 的规则已经分配到现有 skills 和 guidance，而不是新增平行入口。
- RWP 合格标准已经覆盖环境准备、运行驱动、runtime 观察、日志或 evidence 来源、成功标准、失败证据、限制和写回要求。
- 失败与降级路径已经可记录到 task package，不会把无法执行的 runtime workflow 伪装成已验证。
- 测试边界已经明确：CLI parser/command tests、协议文档 tests、task-package guidance tests 都需要更新。

## Trade-offs
备选方案一：集中 YAML 注册表。

这个方案机器解析简单，但会把 runtime workflow 降级成配置项，并迫使项目把脚本入口、适用条件和业务语义提前结构化。它不适合本任务，因为用户明确希望使用文件夹包和类似 skill 的渐进披露，而不是 YAML 注册。

备选方案二：继续沿用 `helper skill` 概念。

这个方案改动较小，但 `helper` 语义太宽，容易被理解为普通辅助文档或 agent skill，也容易被 Codex 自动加载机制污染上下文。RWP 的核心价值是“由 OpenHarness CLI 控制披露粒度并纳入 verification loop”，因此应替换旧术语。

备选方案三：OpenHarness 预定义 `check-env`、`observe` 等标准命令。

这个方案看似规范，但会把具体 workflow 内部步骤过早固定成通用接口。不同项目的 runtime 验证可能需要登录、消息投递、日志观察、浏览器截图、数据库检查或人工确认，OpenHarness 不应替它们命名内部 action。本轮只定义 `run` 外壳和合格标准。

推荐方案的代价是：第一版 RWP 的机器可解析程度有限，很多判断仍依赖 agent 阅读 `description` 和 `workflow.md`。这个代价可以接受，因为它换来了较低上下文成本和更少错误抽象。

## Recommended Diagrams
建议在详细设计或实现 PR 中补一张 `PlantUML` sequence diagram，表达 agent、OpenHarness CLI、RWP directory、task package 之间的主流程：

- agent 获取 RWP summary。
- agent 读取候选 RWP detail。
- agent 将 RWP 纳入 `03-detailed-design.md`。
- verification 阶段调用 `rwp run`。
- 结果写回 `04-verification.md` 和 `05-evidence.md`。

本轮 overview 暂不强制落图；文字边界已经能支撑详细设计。

## Overview Reflection
挑战一：是否应该让 OpenHarness CLI 自动选择任务相关 RWP？

结论：拒绝。CLI 自动选择会把 agent 判断、任务上下文和代码触达面耦合进工具层。OpenHarness CLI 应只负责发现、展示、运行外壳；选择由 agent workflow skill 规则完成。候选较多时，可以让子智能体基于摘要做筛选，但这仍是 agent 协作策略，不是 CLI 职责。

挑战二：是否需要在 `workflow.md` 中声明脚本入口表？

结论：拒绝作为本轮要求。`workflow.md` 的职责是解释 runtime workflow，而不是成为脚本注册表。具体 RWP 的内部 action 和脚本组织由该 RWP 自己决定；OpenHarness 只提供 `rwp run <name> ...` 的统一外壳。

挑战三：RWP 是否会重复现有 task package verification commands？

结论：接受部分重叠，但边界不同。`verification.required_commands` 是 task package 针对本任务声明的验证路径；RWP 是项目级可复用 runtime 验证能力。任务可以把 `openharness rwp run ...` 写入 required commands，也可以在 detailed/verification 文档中记录更复杂的执行与观察路径。

挑战四：是否应保留 runtime surface map？

结论：延期到详细设计决定迁移方式。现有文档已经有 runtime surface/helper 术语，RWP 可以替代它，也可以短期保留 surface map 作为索引。详细设计需要决定是直接改写这些 references，还是新增 RWP reference 后逐步迁移旧 surface/helper 文档。
