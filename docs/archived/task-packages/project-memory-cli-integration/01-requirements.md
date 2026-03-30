# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 `project-memory` 的正式使用入口收敛到 `openharness` CLI，使维护者可以用稳定、可文档化、可测试的子命令完成查询、审计、陈旧性检查、归档和保存操作，而不必继续记忆零散的 `skills/project-memory/scripts/*.py` 路径。

单一成功指标：仓库内活跃协议表面把 `openharness project-memory ...` 作为标准入口，并且自动化测试能证明这些子命令真实存在且会正确转发到现有 project-memory 能力。

## Problem Statement
目标用户是维护 OpenHarness 协议、task package 和 `.project-memory/` 的仓库维护者。核心场景是在仓库根目录或显式传 `--repo` 的情况下，执行 memory query、save、audit、archive 和 stale check。

当前矛盾是：`project-memory` 已经被纳入 live skill surface 和 skill metadata，但官方 CLI 仍只覆盖 task package 主流程；维护者要么直接调用 skill 脚本，要么在协议里口头记住这是一类“未来再收口”的能力。这样会带来三个问题：

- 官方入口和实际入口分叉，技能文档难以给出唯一推荐路径。
- CLI 无法对 `project-memory` 提供统一帮助、参数收口和测试约束。
- 后续继续扩展 memory 工作流时，仍会沿着零散脚本路径累积文档债务。

现在做这件事的原因也已经明确：仓库前面一轮全局 CLI 工作已经把它列成后续 follow-up，如果继续拖延，skill surface 与 CLI surface 的不一致会继续扩大。

## Required Outcomes
1. `openharness` 新增 `project-memory` 子命令树，至少覆盖 `query`、`check-stale`、`audit`、`archive`、`save-fact`、`save-workflow`、`save-decision`。
   acceptance criteria:
   `openharness` parser 能识别这些子命令，并把参数正确转发到现有 project-memory 能力。
2. 活跃 `project-memory` skill 文档改为以 `openharness project-memory ...` 作为标准命令示例。
   acceptance criteria:
   `skills/project-memory/SKILL.md` 不再把 `scripts/...` 当作主入口。
3. 活跃协议测试覆盖新的 CLI surface 和文档约束。
   acceptance criteria:
   相关 pytest 用例能证明新子命令已暴露，且活跃文档不会回退到旧入口表述。
4. 这轮改动不破坏现有 task package 主流程 CLI。
   acceptance criteria:
   现有 `bootstrap`、`check-tasks`、`new-task`、`transition`、`verify`、`update` 仍保持可用。

## Non-Goals
- 不把所有 skills 的脚本入口一口气全部并入 `openharness`；本轮只收口 `project-memory`。
- 不重写 project-memory 的底层 YAML/index 读写逻辑；优先复用现有实现能力。
- 不改变 `.project-memory/` 的对象 schema、打分规则或 freshness guardrail。
- 不清理历史归档文档中的所有旧命令示例；只更新活跃协议表面。
- counterexample: “顺手把 `systematic-debugging`、`requesting-code-review` 等 skill 的脚本也并进 CLI” 看起来方向相近，但这是另一个 task package，不属于本轮。

## Constraints
- 必须遵守现有仓库协议：活跃文档使用中文叙述，命令、状态值、YAML 键名、文件名和路径保持英文。
- Python 命令统一走 `uv run ...`；不能依赖临时安装。
- 需要兼容 `openharness` 已安装为全局 CLI 的场景，因此子命令不能假设调用者正在 skill 目录里。
- 要尽量复用现有 project-memory 脚本或库，不新增第二套并行实现。
- `cost cap` 是一次聚焦改动：只做到 `project-memory` CLI 收口、活跃文档对齐和必要测试，不扩大成大规模 CLI 重构。
- 一旦需要改变 project-memory 数据模型、引入新的存储后端或修改其他 skill 的官方入口，这就不再是同一个 task package。
