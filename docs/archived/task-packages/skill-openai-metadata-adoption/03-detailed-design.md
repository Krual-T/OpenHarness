# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先运行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k "skill_openai_metadata or openai_yaml or implicit_invocation"`，锁定本轮新增 metadata 与策略分类断言。
  - 再运行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，确认新增断言没有破坏现有 harness 文档与协议测试。
  - 最后运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认任务包结构和状态写回仍满足仓库协议。
- Fallback Path:
  - 如果聚焦 pytest 因测试命名尚未稳定而无法筛选，就直接运行完整 `uv run pytest skills/using-openharness/tests/test_openharness.py`。
  - 如果完整 pytest 通过但 `check-tasks` 失败，不能宣称完成，因为这说明 task package 或仓库协议表面仍不一致。
  - 如果 metadata 文件都写完但没有自动化测试覆盖，最多只能宣称“文档与结构已更新”，不能宣称任务完成。
- Planned Evidence:
  - 每个 live repo skill 目录下新增的 `agents/openai.yaml`。
  - 测试文件中的 metadata 存在性与策略分类断言。
  - `pytest` 与 `check-tasks` 的通过结果。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/brainstorming/agents/openai.yaml`
- `skills/dispatching-parallel-agents/agents/openai.yaml`
- `skills/exploring-solution-space/agents/openai.yaml`
- `skills/finishing-a-development-branch/agents/openai.yaml`
- `skills/receiving-code-review/agents/openai.yaml`
- `skills/requesting-code-review/agents/openai.yaml`
- `skills/subagent-driven-development/agents/openai.yaml`
- `skills/systematic-debugging/agents/openai.yaml`
- `skills/test-driven-development/agents/openai.yaml`
- `skills/using-git-worktrees/agents/openai.yaml`
- `skills/using-openharness/agents/openai.yaml`
- `skills/verification-before-completion/agents/openai.yaml`
- `skills/project-memory/agents/openai.yaml`
  - 需要统一字段形状，并补充缺失的 `policy` 与必要依赖；已有文件要按统一约定收敛。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 增加 repo skills metadata 覆盖与策略分类断言。
- `skills/using-openharness/tests/test_openharness.py`
  - 继续作为总入口聚合上述用例，无需新建并行测试入口。
- `docs/task-packages/skill-openai-metadata-adoption/*`
  - 写回本轮需求、设计、验证计划与证据占位。

## Interfaces
稳定接口只有两类：

1. OpenAI skill metadata 接口
   - `skills/<skill>/agents/openai.yaml`
   - 允许字段：`interface`、`policy.allow_implicit_invocation`、`dependencies.tools`
   - 这里的 YAML 是 Codex 技能发现阶段的前置接口，不替代 `SKILL.md` 正文。

2. 仓库测试接口
   - 现有 `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
   - 通过读取技能目录和 YAML 内容来验证仓库 live surface，没有引入新的命令行子命令或公共 Python API。

技能策略表按下列边界实现：

- 允许隐式触发：
  - `using-openharness`
  - `brainstorming`
  - `exploring-solution-space`
  - `systematic-debugging`
  - `test-driven-development`
  - `verification-before-completion`
  - `receiving-code-review`
  - `project-memory`

- 显式调用优先：
  - `dispatching-parallel-agents`
  - `subagent-driven-development`
  - `using-git-worktrees`
  - `requesting-code-review`
  - `finishing-a-development-branch`

如果实现阶段发现某个技能需要例外，必须同时改 metadata、测试和任务包设计说明，不能只改单处。

## Stage Gates
进入 `in_progress` 前，detailed 必须已经明确：

1. 每个目标技能是否新增 `agents/openai.yaml`，以及策略表已经定稿。
2. 测试新增落点已经确定在现有 protocol docs 测试中。
3. 现有 `project-memory/agents/openai.yaml` 的收敛方式已经说明，而不是留一个特殊例外。
4. 验证命令、失败回退路径和完成判定都已写清楚。
5. 预期证据类型已经覆盖文件新增、测试结果和任务包校验结果。

## Decision Closure
接受：
- 用静态 `agents/openai.yaml` 逐个落地 metadata，而不是生成脚本。
- 用 `allow_implicit_invocation: false` 把明确需要人工授权或显式语境的技能边界固定下来。
- 在现有 protocol docs 测试中增加 metadata 回归，而不是新开一套独立测试框架。

拒绝：
- 只为一两个技能补 metadata。理由是这会继续保留不一致表面，无法形成仓库级约束。
- 用更长的 `description` 替代 invocation policy。理由是文本只能提示，不能形成官方 metadata 层面的硬约束。

延期：
- 是否为部分技能补充图标、品牌色等纯 UI 字段。触发条件是未来需要面向 Codex app 做可视化展示优化时再讨论；本轮先保证策略与描述完整。

## Error Handling
主要风险与防护如下：

1. 风险：某个技能被误标为显式调用优先，导致自动工作流不再选中它。
   - 防护：只对那些正文中已经明确要求显式上下文、用户授权或隔离环境的技能收紧策略；其余保守保持 implicit。

2. 风险：metadata 与 `SKILL.md` 正文语义冲突。
   - 防护：测试至少检查关键技能的策略分类；实现时同时比对技能头部 `description` 与 YAML 的短描述、默认提示。

3. 风险：某些技能目录漏加 `agents/` 子目录。
   - 防护：用枚举 live repo skill 列表的测试一次性检查覆盖率，而不是靠人工浏览目录。

4. 风险：把不存在的工具依赖写入 `dependencies.tools`。
   - 防护：只在已有真实依赖且仓库中能说明用途时声明；否则留空不写。

## Migration Notes
落地顺序：

1. 先为所有目标技能创建 `agents/openai.yaml`，其中只写最小必要字段。
2. 再统一调整 `project-memory` 现有 metadata，使字段形状与其他技能一致。
3. 然后补测试，固定文件存在性与策略分类。
4. 最后跑验证命令并写回 `05-verification.md`、`06-evidence.md`。

兼容策略：
- `SKILL.md` 保持不动或只做最小冲突修正，因此旧的技能正文入口不会失效。
- metadata 是前置增强层，不会替代既有技能内容。

回滚注意事项：
- 若某技能策略判断错误，优先单独回滚该技能的 `policy.allow_implicit_invocation` 与对应测试，不需要整体撤回 metadata 覆盖。

## Detailed Reflection
本轮 detailed 反思主要验证了四点：

1. 测试是否足够轻。
   - 结论：足够。只需读取 YAML 与目录，不需要额外 CLI 功能。

2. 接口边界是否过宽。
   - 结论：不宽。本轮只使用官方公开字段，没有试图把仓库私有概念塞进 metadata。

3. 迁移是否会打断当前技能使用。
   - 结论：不会。新增 `agents/openai.yaml` 是增量表面，旧技能正文仍完整存在。

4. 是否还有高影响未决问题。
   - 结论：没有阻止实现的高影响未决问题。唯一需要在实现时继续留意的是 `requesting-code-review` 与 `project-memory` 的 implicit 边界体验，但这已经被限制为单点可回退决策，不会影响本轮主路径。
