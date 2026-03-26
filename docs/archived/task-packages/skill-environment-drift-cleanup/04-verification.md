# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先人工核对受影响 skill 是否已经移除旧入口约定、不可用工具名和错误的 Python 工作流默认假设，再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 确认任务包协议未被破坏。
- Executed Path: 先用 `rg` 检查 `CLAUDE.md`、`TodoWrite`、`Task(...)`、旧 reviewer 能力名和旧 harness CLI 路径在 active skills 中的残留，再修改 `using-openharness`、`using-git-worktrees`、`subagent-driven-development`、`requesting-code-review`、`receiving-code-review`、`dispatching-parallel-agents` 及相关引用模板，最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Path Notes: 这轮问题本质是协议文本与仓库事实的偏移，不是运行时代码缺陷，因此“关键文本人工核对 + harness 结构校验”已经覆盖主风险。当前没有新增自动 lint 来扫描所有旧术语，因此残余风险会在 `05-evidence.md` 中单列。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- active skills 不再把旧入口文件、不可用工具或错误的 Python 安装流程写成当前仓库默认约束。
- harness 校验通过，说明任务包结构和归档前提没有被修改破坏。

## Traceability
- `01-requirements.md` 中关于旧入口约定、工具能力假设和命令约定冲突的要求，对应到本轮对多个 skill 与引用模板的直接修改。
- `02-overview-design.md` 中“删除 / 替换 / 降级”的处理规则，对应到删除 `TodoWrite`、`Task(...)`、固定 reviewer 类型，以及把 harness CLI 路径改成当前仓库真实 `uv run python ...` 命令。
- `03-detailed-design.md` 中的验证路径，对应到本轮执行的残留词汇扫描和 `check-tasks` 命令。

## Risk Acceptance
- 仍接受的风险是仓库中的历史归档材料或非活跃参考说明可能保留旧环境词汇，因为它们不再承担 active 执行入口角色。
- 如果后续再次发现 active skill 或 active task package 引入旧环境词汇，应重新打开类似清理任务，或补一个自动化扫描约束。

## Latest Result
- 最近一次验证已通过。`uv run python skills/using-openharness/scripts/openharness.py check-tasks` 返回 `Validated 22 task package(s)`，没有发现任务包结构错误。
- Latest Artifact: stdout from `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
