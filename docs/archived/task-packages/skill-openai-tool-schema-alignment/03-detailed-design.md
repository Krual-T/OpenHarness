# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先运行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k "openai_metadata"`，确认 metadata 相关用例通过。
  - 再运行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，确认完整 harness 测试入口未被破坏。
  - 最后运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认任务包协议仍然一致。
- Fallback Path:
  - 如果 `-k` 过滤不足以覆盖新断言，则直接依赖完整 `uv run pytest skills/using-openharness/tests/test_openharness.py`。
  - 如果 pytest 通过但 `check-tasks` 失败，不能宣称完成，因为这说明任务包写回不完整。
  - 如果外部官方核查证据没有落到任务包，也不能宣称“已与官方对齐”。
- Planned Evidence:
  - 八个 skill 的 `openai.yaml` 不再含有 `shell` 依赖声明。
  - 测试中不再断言 `["shell"]`，而是检查官方对象数组形状和当前支持范围。
  - `pytest` 与 `check-tasks` 通过结果。
  - 指向 OpenAI 官方仓库示例与参考文档的外部依据。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/finishing-a-development-branch/agents/openai.yaml`
- `skills/project-memory/agents/openai.yaml`
- `skills/requesting-code-review/agents/openai.yaml`
- `skills/systematic-debugging/agents/openai.yaml`
- `skills/test-driven-development/agents/openai.yaml`
- `skills/using-git-worktrees/agents/openai.yaml`
- `skills/using-openharness/agents/openai.yaml`
- `skills/verification-before-completion/agents/openai.yaml`
  - 删除非官方 `shell` 工具依赖声明。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 把仓库测试从字符串数组断言收敛到官方 schema 约束。
- `docs/archived/task-packages/skill-openai-tool-schema-alignment/*`
  - 写回本轮需求、设计、官方核查结论、验证和证据。

## Interfaces
本轮涉及两类稳定接口：

1. OpenAI skill metadata 接口
   - `agents/openai.yaml`
   - 当前稳定边界为 `interface`、`policy.allow_implicit_invocation`，以及在需要时使用官方公开支持的 `dependencies.tools` 对象数组。

2. 仓库协议测试接口
   - `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
   - 负责保护 live repo skill metadata 的形状与策略边界。

## Stage Gates
进入 `in_progress` 前，detailed 必须已经明确：

1. 受影响技能列表已经收敛。
2. 对 `shell` 的处理已经定为删除，而不是改写成本地对象。
3. 测试覆盖了“错误旧形状”和“当前官方支持范围”。
4. 验证命令与外部依据记录方式已经写清楚。

## Decision Closure
接受：
- 直接删除八个技能中的 `shell` 依赖声明。
- 允许 skill metadata 完全省略 `dependencies`，因为当前仓库并没有官方支持的 MCP 依赖需求。
- 用一条通用测试覆盖官方对象数组形状。

拒绝：
- 继续在测试里断言 `["shell"]`。
- 把 `shell` 改写成 `type: "shell"` 再继续保留。

延期：
- 是否把“技能通常会用到 shell”的信息搬到别的仓库私有文档层。触发条件是未来确认这类提示确实有维护价值，但又不适合放在官方 metadata 中。

## Error Handling
主要风险与防护如下：

1. 风险：未来有人重新按旧样例写回 `tools: - shell`。
   - 防护：测试要求 `dependencies.tools` 必须是对象数组，字符串条目会直接失败。

2. 风险：未来有人把任意自定义类型塞进 `dependencies.tools`。
   - 防护：测试当前只接受 `type: "mcp"`。

3. 风险：误删真实需要的官方依赖。
   - 防护：本轮删除前已核对当前仓库没有任何 MCP 依赖需求，后续若新增可单点恢复。

## Migration Notes
落地顺序：

1. 先移除 YAML 中的 `shell` 依赖。
2. 再更新测试，防止旧形状回流。
3. 最后执行验证并回写任务包。

兼容策略：
- `SKILL.md` 正文不变。
- `dependencies` 作为可选字段被移除，不影响 skill 的核心发现与策略路由。

回滚注意事项：
- 如果未来官方文档正式支持 `shell`，应基于新的官方示例单点恢复，不应回滚到字符串数组写法。

## Detailed Reflection
本轮 detailed 反思确认了三点：

1. 测试策略足够轻，不需要新 CLI 或新校验器。
2. 接口边界应以公开文档为准，而不是以官方代码中更宽的内部类型为准。
3. 删除 `dependencies` 不会破坏当前仓库技能工作流，因为这些字段此前只被当作静态元数据和错误断言使用。
