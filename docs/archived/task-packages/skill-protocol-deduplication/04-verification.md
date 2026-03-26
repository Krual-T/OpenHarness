# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先人工核对 `using-openharness` 与 child skills 的职责边界是否已经收敛，再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 确认 task package 协议仍然有效。
- Executed Path: 修改 `brainstorming`、`exploring-solution-space`、`subagent-driven-development`、`requesting-code-review`、`dispatching-parallel-agents` 等 child skills，使其不再重复维护仓库级状态制度、归档协议和固定代理工作流；随后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Path Notes: 这轮任务的验收重点是职责边界是否收敛到单一入口层，而不是功能逻辑是否新增。因此“关键 skill 文本人工核对 + harness 校验”已经足够证明 active task package 没有被破坏。残余风险主要是未来可能再次发生协议复制。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- `using-openharness` 继续保留仓库级单一权威协议。
- child skills 显著缩短，并把仓库级流程规则收回到入口层，只保留自身阶段动作。
- harness 校验通过。

## Traceability
- `01-requirements.md` 对“区分仓库级常驻协议与 child skill 专属动作”的要求，对应到本轮对 `brainstorming`、`exploring-solution-space`、`subagent-driven-development` 等文件的直接精简与职责重划。
- `02-overview-design.md` 中“一主多辅”的结构，对应到保留 `using-openharness` 为唯一入口并删除 child skills 中平行闭环描述。
- `03-detailed-design.md` 中关于人工职责核对与 harness 校验的验证策略，对应到本轮实际执行的修改和命令结果。

## Risk Acceptance
- 仍接受的风险是当前没有自动化度量来判断“重复协议是否再次膨胀”，所以后续仍需要靠代码审查和任务包更新保持边界清晰。
- 如果未来入口 skill 与 child skill 再次出现大段重复制度说明，应重新打开同类任务，或补一条轻量文本约束。

## Latest Result
- 最近一次验证已通过。`uv run python skills/using-openharness/scripts/openharness.py check-tasks` 返回 `Validated 22 task package(s)`，没有发现任务包结构错误。
- Latest Artifact: stdout from `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
