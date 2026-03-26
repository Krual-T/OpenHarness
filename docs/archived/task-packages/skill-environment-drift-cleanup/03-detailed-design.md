# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先人工检查受影响 skill 的关键段落是否已经移除旧环境残留，再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Fallback Path:
- 如果 harness 校验失败，先修任务包或引用路径，再重新执行；如果只能做到文本修改但没有 fresh verification evidence，就不能宣称完成或归档。
- Planned Evidence:
- 证据包括修改后的 skill 文件内容、harness 校验命令结果，以及任务包中的验证与证据写回。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-git-worktrees/SKILL.md`：清理旧入口、旧安装流程和与当前仓库不一致的默认假设。
- `skills/subagent-driven-development/SKILL.md`：移除不存在的任务面板与固定 reviewer 能力假设，改成与当前会话能力一致的表述。
- `skills/requesting-code-review/SKILL.md`、`skills/receiving-code-review/SKILL.md`、`skills/dispatching-parallel-agents/SKILL.md`：修正旧能力名和误导性示例。
- 必要时修改少量引用模板或说明文档，避免错误术语继续传播。
- 本 task package 下的 `04-verification.md`、`05-evidence.md`、`STATUS.yaml`：记录执行证据并在完成后归档。

## Interfaces
- 稳定边界是 `AGENTS.md`、`skills/using-openharness/SKILL.md` 和当前会话真实可用的工具能力。
- child skills 不得再把不存在的工具、子智能体类型或外部仓库约定当成接口前提。
- 如果示例需要展示命令，必须与仓库统一的 `uv run ...` 约定兼容，或明确声明只是通用示意而非默认执行路径。

## Stage Gates
- 必须列清受影响文件与每类修改目的，避免实施时范围漂移。
- 必须明确验证策略依赖“人工核对关键文本 + harness 校验”两层证据，而不是只看 diff。
- 必须写明预期证据类型：修改文件列表、执行命令、校验结果、残余风险。

## Decision Closure
- 接受：把不存在的能力假设直接删除，而不是保留成“以后可能用到”的占位说明，因为当前仓库没有证据支持它们。
- 接受：把错误的 Python 工作流统一替换为 `uv run` 约定，因为这是 `AGENTS.md` 已明确的仓库规则。
- 延期：更大范围的 skill 结构瘦身交给 OH-021 处理，本任务不把所有重复协议都当作环境漂移来改。

## Error Handling
- 主要误用风险是把“通用 AI 工作方式”误写成“本仓库强约束”。处理方式是逐条对照 `AGENTS.md` 和当前工具能力，只保留能被证明的内容。
- 另一个风险是删除过度，误删仍然有价值的执行提示。处理方式是优先删除错误前提，保留与当前能力兼容的抽象指导。
- harness 校验只能保证任务包协议完整，不能自动证明所有技能文本都合理，因此需要补充人工核对关键高风险段落。

## Migration Notes
- 迁移顺序先处理最容易误导执行的 skill，再处理辅助 skill 和引用示例，最后统一回写任务包。
- 兼容策略是不新增新的仓库入口层，仍以现有 `using-openharness` 为事实中心。
- 如果某次修改引入新的歧义，优先回到更短、更直接的当前仓库事实表述，不保留双轨说明。

## Detailed Reflection
- 反思后确认本任务不需要新增自动测试，因为问题本质是文本协议漂移，不是逻辑执行分支缺陷；现有 harness 校验足够覆盖任务包结构层面的回归。
- 需要克制的一点是不要把 OH-021 的结构优化目标全部提前做完，否则验证边界会被冲淡。实施时仍以“当前 skill 是否还会误导执行”为第一判断标准。
