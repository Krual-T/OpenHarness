# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先修改受影响的 live docs，使 sibling references 指向当前目录下真实存在的文件。
- 再修改 `skills/systematic-debugging/` 下已确认的旧 skill 路径，使其对齐当前真实入口。
- 然后执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，确认新增的路径有效性断言通过。
- 再执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认任务包协议和状态写回仍然有效。
- Fallback Path:
- 如果 `pytest` 断言设计过宽，误把模板占位路径或示意路径当成缺陷，应先把测试收窄到 `using-openharness` live docs 白名单，再重新运行。
- 如果 `check-tasks` 失败，先修复任务包文档或状态字段，再重跑；在两条命令都没有 fresh 结果前，不能宣称实现完成。
- Planned Evidence:
- 证据包括修正后的 live docs 与技能材料内容、`test_protocol_docs.py` 中新增的断言、`pytest` 执行结果，以及 `check-tasks` 结果。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/references/runtime-capability-contract.md`
  - 修复对 sibling reference docs 的错误相对路径写法。
- `skills/using-openharness/references/project-runtime-surface-map.md`
  - 修复对 helper-addition 文档的错误相对路径写法。
- `skills/using-openharness/references/skill-hub.md`
  - 修复 runtime capability 相关文档的错误相对路径写法。
- `skills/systematic-debugging/test-academic.md`
- `skills/systematic-debugging/test-pressure-1.md`
- `skills/systematic-debugging/test-pressure-2.md`
- `skills/systematic-debugging/test-pressure-3.md`
- `skills/systematic-debugging/CREATION-LOG.md`
  - 清理已确认的旧 skill 路径 `skills/debugging/systematic-debugging`，统一到当前真实入口。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 增加 live docs 引用有效性和 retired skill path 残留的文本断言，防止同类回归。
- `docs/archived/task-packages/skill-reference-path-cleanup/README.md`
- `docs/archived/task-packages/skill-reference-path-cleanup/STATUS.yaml`
- `docs/archived/task-packages/skill-reference-path-cleanup/04-verification.md`
- `docs/archived/task-packages/skill-reference-path-cleanup/05-evidence.md`
  - 回写本轮设计、实现、验证证据。

## Interfaces
稳定边界如下：

- `AGENTS.md` 与 `skills/using-openharness/SKILL.md`
  - 定义 live protocol surface 的仓库级事实来源，本轮不改它们的协议语义。
- `skills/using-openharness/references/*.md`
  - 这些文档之间的交叉引用属于面向维护者的导航接口，必须能落到真实文件。
- `skills/systematic-debugging/*.md`
  - 这些配套材料属于维护者可见的技能表面，不应继续宣传已退休的 skill 入口。
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 这是当前仓库已有的文本协议测试入口，适合作为本轮防回归接口。

实现时不引入新的公共脚本接口，也不改变 runtime capability contract 的字段语义，只修路径解析有效性、旧入口一致性与相应断言。

## Stage Gates
- 必须明确测试策略：文档修复后，至少有一条自动断言能够证明关键 live 引用指向真实文件，并能阻止已确认旧入口再次出现。
- 必须明确可观测性要求：失败时能直接指出是哪份 live doc 的哪条引用又变成无效路径。
- 必须明确迁移顺序：先修 live docs，再补测试，最后跑 `pytest` 和 `check-tasks`。
- 必须明确预期证据类型：修改后的文档片段、测试断言、命令执行结果、任务包写回。

## Decision Closure
- 接受：本轮把真实问题收敛到 `using-openharness` runtime capability 文档链路，而不是扩大成全仓库链接治理，因为本地探索只在这里发现了明确失效路径。
- 接受：把 `systematic-debugging` 下已确认的旧入口残留并入本轮范围，因为它们会直接误导维护者识别真实 skill 入口，属于同一类路径收口问题。
- 接受：防回归优先复用 `test_protocol_docs.py` 增量加断言，而不是新建通用脚本，因为当前测试基座已经覆盖 live protocol docs。
- 拒绝：仅做手工文档修复不加自动校验。理由是这类 sibling path 错误已经证明会回流，只有手工检查不足以形成稳定闭环。
- 延期：若后续发现 archived materials 也需要批量路径迁移，需新开 task package；触发条件是 archived content 被重新提升为 live onboarding surface，或发现它们正在影响当前执行路径。

## Error Handling
主要风险有三类：

1. 误把占位符路径当成 bug
   - 处理方式是把自动断言限制在已确认存在真实文件的 live docs 与白名单引用上，不扫描 `<task>`、`*`、示意路径。
2. 修复文档时改动了语义而不只是路径
   - 处理方式是本轮只调整 sibling reference 的写法，不改 runtime capability contract 的业务含义。
3. 测试只断言文本包含某个文件名，没真正验证目标存在
   - 处理方式是断言需要直接解析到仓库内真实文件并检查 `exists()`，避免出现“字符串看起来合理但路径仍然失效”的静默错误。
4. 清理旧入口时误改成另一个非标准别名
   - 处理方式是统一对齐到当前仓库实际存在的 skill 目录 `skills/systematic-debugging/`，不引入新的兼容别名。

## Migration Notes
- 实施顺序固定为：
  1. 修复 `references/` 目录下三份 live docs 的 sibling path。
  2. 清理 `systematic-debugging` 下已确认的旧入口路径。
  3. 在 `test_protocol_docs.py` 中补路径存在性与旧入口残留断言。
  4. 跑 `pytest` 与 `check-tasks`。
  5. 更新 `04-verification.md`、`05-evidence.md` 与 `STATUS.yaml`。
- 兼容策略是保持文档文件名不变，只改引用写法，因此不会影响外部入口或脚本命令。
- 如果新增断言暴露出更多 live doc 失效路径，可在同一实施波次内继续纳入；若超出 `using-openharness` runtime capability 文档边界，则应停下重新评估是否拆包。

## Detailed Reflection
- 从测试视角反思后，当前方案足够具体：失败会精确落在某份 live doc 的某条引用，而不是只告诉我们“文档有问题”。
- 从架构视角反思后，本轮没有必要引入新的共享脚本。因为问题规模小、位置集中，用现有协议测试承载更符合“主路径短、结构稳定”的仓库风格。
- 从迁移视角反思后，最需要克制的是不要把 archived evidence 一起改掉。那样会把“修 live surface 和维护材料”演变成“重写历史”，超出本轮边界。
- 从验证视角反思后，`pytest + check-tasks` 已经足以覆盖本轮风险；只有当后续再出现跨目录更大范围的链接漂移时，才值得再考虑抽象出统一链接校验器。
