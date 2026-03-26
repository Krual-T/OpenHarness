# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 人工核对 `using-openharness` 与 child skills 的职责边界是否已经收敛，再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- Fallback Path:
- 如果 harness 校验失败，先修正任务包文档或引用路径后重跑；如果只是文本看起来更短，但没有证明职责边界更清楚，就不能宣称完成。
- Planned Evidence:
- 证据包括修改后的核心 skill 文本、任务包中的设计与验证写回，以及一次 fresh harness 校验结果。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/SKILL.md`：保留仓库级单一权威协议，不把关键规则拆散。
- `skills/brainstorming/SKILL.md`、`skills/exploring-solution-space/SKILL.md`：去掉重复的仓库级制度，只保留阶段专属动作与输出要求。
- `skills/subagent-driven-development/SKILL.md` 以及少量 helper skill：删除自带的平行闭环，改为引用仓库入口层和当前会话能力。
- 本 task package 下的 `04-verification.md`、`05-evidence.md`、`STATUS.yaml`：记录验证结果并在完成后归档。

## Interfaces
- 稳定接口是 `using-openharness` 提供的仓库级协议：任务包结构、阶段流、写回位置和归档要求。
- child skills 的接口是“输入什么阶段上下文、产出什么阶段结果”，而不是自带完整仓库章程。
- 任何 child skill 如果需要再次声明仓库级协议，必须只作为引用提示，不能演化成第二份权威文本。

## Stage Gates
- 必须列明每个要改的 child skill 是删除哪些重复规则、保留哪些阶段专属动作。
- 必须写明验证依赖“人工职责核对 + harness 校验”两类证据。
- 必须定义预期证据类型：关键文件 diff、执行命令、结果摘要、残余风险。

## Decision Closure
- 接受：仓库级规则继续集中在 `using-openharness`，因为当前仓库已经把它定义成唯一入口 skill。
- 拒绝：新增一个独立 protocol 文件层来承接共享制度，因为这会新增维护点并稀释现有入口层定位。
- 接受：child skills 保留本阶段必要 gate，但删除整段重复的仓库级状态制度，避免以后继续分叉。

## Error Handling
- 最大风险是“去重”变成“删空”，导致 child skill 失去执行指引。处理方式是先保留阶段动作、输出物和局部检查点，再删仓库级重复说明。
- 另一个风险是入口层和 child skill 之间出现新的交叉引用循环。处理方式是只让 child skill 指向入口层，不反向复制 child skill 规则。
- harness 校验不能自动识别职责边界是否合理，因此需要人工审查关键 skill 是否仍能单独指导其阶段动作。

## Migration Notes
- 先收敛入口层与核心 child skills 的职责边界，再清理执行型 helper skill 中的平行流程描述。
- 兼容策略是保持现有 skill 名称和触发关系不变，只调整正文职责。
- 如果某个 child skill 精简后出现执行信息缺口，回滚时优先补阶段专属说明，不回退到重复整套仓库协议。

## Detailed Reflection
- 反思后确认 OH-021 最关键的不是“字数少了多少”，而是事实来源是否只剩一个权威入口。因此设计里把文本长度当作结果，不当作目标。
- 另一个结论是 OH-020 与 OH-021 会同时触碰 `subagent-driven-development` 等文件，所以实施时必须以“先纠错、再去重”的顺序改写，避免把错误内容先抽象固化。
