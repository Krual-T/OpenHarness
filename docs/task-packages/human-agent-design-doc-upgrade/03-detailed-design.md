# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py`
  - 先补协议测试，使其对新的 overview/detailed contract 先失败，再修改 guidance/template 使测试转绿。
- Fallback Path:
  - 如果快照测试比预期更脆弱，允许最小范围更新相关字符串断言，但不能绕过“新 contract 必须进入 guidance/template”的验证目标。
  - 如果只能修改 guidance 而模板快照难以同步通过，则本轮不能宣称完成，因为 `openharness new-task` 仍会脚手架出旧 contract。
- Planned Evidence:
  - `04-verification.md` 记录测试命令、执行结果和仍未覆盖的验证盲区。
  - `05-evidence.md` 记录修改文件、设计文档、命令与剩余风险。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/references/overview-design-writing-guidance.md`
  - 这里承载 `02` 的正式写作 contract，需要加入更适合人机协作的设计信息与图示建议。
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
  - 这里承载 `03` 的正式写作 contract，需要补足可直接支撑编码的内部设计信息。
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
  - 这里决定 `openharness new-task` 的默认起笔体验，需要同步新的总体设计提示。
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
  - 这里决定详细设计脚手架是否能提醒作者写模块内部分工、接口精度与异常处理。
- `tests/openharness_cases/test_protocol_docs.py`
  - 这里承载 guidance/template contract 的最低验证。
- `tests/openharness_cases/test_cli_workflows.py`
  - 这里覆盖 `new-task` 脚手架输出，确保模板更新真实生效。

## Interfaces
这轮改动暴露的是“设计文档写作 contract”接口，而不是运行时 API。

稳定边界：

- `overview-design-writing-guidance.md` 仍然只服务 `02-overview-design.md`，不接管 `03` 的落地细节。
- `detailed-design-writing-guidance.md` 仍然只服务 `03-detailed-design.md`，不重新选择总体方向。
- 模板只给最短提示，完整解释继续留在 guidance。

关键契约：

- `02` 必须能让读者回答模块、接口、关键数据/状态模型、架构级约束和主流程问题。
- `03` 必须能让读者回答文件落点、模块内部职责、接口精度、数据语义、异常边界、实现顺序和验证路径问题。
- `PlantUML` 图示是推荐协作介质，不是替代文字约束的事实源。

关键 `observability` 入口：

- 协议测试中的 guidance 文本断言
- `new-task` 生成模板的文本快照
- `OH-038` 自身的 task package 文档，用于检查设计约束是否前后一致

## Stage Gates
- 必须先有失败的测试来证明新的 contract 还没落地。
- 必须明确 overview 与 detailed 分别新增哪些必答问题和模板提示。
- 必须明确 `PlantUML` 在 overview/detailed 各自推荐的图类型，且不能把图当成唯一事实源。
- 必须明确哪些旧内容继续保留，避免误伤现有阶段边界。
- 必须明确预期证据是“guidance 文本变化 + 模板变化 + 测试通过”，而不是只改其中一层。

## Decision Closure
- 接受：overview 需要补入模块划分、接口责任、关键数据/状态模型和架构级约束，因为这些是 agent 形成整体实现模型的前提。
- 接受：detailed 需要补入模块内部职责、接口精度、数据语义、异常与边界条件，因为这些是 agent 能否稳定编码的关键。
- 接受：`PlantUML` 应作为正式推荐图示方法进入 guidance/template，因为它是文本化、可版本管理、对人机共享上下文都友好的图示方式。
- 拒绝：把图示做成强制渲染或强制数量要求；这会让本轮扩张到工具链与校验器问题。
- 延期：是否未来要增加针对 diagram 存在性的自动校验，等先积累实际使用样本后再决定。

## Error Handling
主要失败路径：

- guidance 更新了，但模板没更新，导致老 contract 仍从 `new-task` 流入新 package。
- overview 补了太多实施细节，和 detailed 重新重叠。
- detailed 只增加章节名，没有增加可执行粒度，结果仍然不能指导 agent 编码。

误用风险：

- 把 `PlantUML` 图当作唯一设计说明，文字里不再写边界、约束和例外。
- 把传统软件工程目录机械映射进 `02`/`03`，导致模板过长、阶段边界消失。

静默出错风险：

- 如果测试只断言文件存在、不检查新关键术语，仓库会表面通过，但实际写作 contract 没有增强。

避免方式：

- 在协议测试里直接断言新 contract 关键词。
- 在 guidance 中明确 overview/detailed 各自的边界。
- 在模板中提醒“图不能替代文字约束”。

## Migration Notes
迁移顺序：

1. 先更新 `OH-038` 的需求与设计文档，固定本轮事实。
2. 再写协议测试，让旧 guidance/template 下测试先失败。
3. 然后修改 guidance 和模板。
4. 最后跑验证并回写 `04/05`。

兼容策略：

- 不修改 task package 文件名、状态流和 CLI 输入输出模型。
- 已归档 package 不做批量迁移；新 contract 主要影响未来新建包和未来编辑的活跃包。

切换点：

- 当 guidance 与模板同时更新且测试通过时，新的写作 contract 才算生效。

回滚触发点：

- 如果测试证明模板文案膨胀过度或破坏阶段边界，应回退到“guidance 保留完整 contract、模板只保留问题提示”的更轻方案。

## Detailed Reflection
- 我检查了是否只改 guidance 就够。结论是不够，因为 `new-task` 模板会继续把旧设计 contract 带给新作者。
- 我检查了是否需要新建额外 reference 专门讲 diagram。结论是暂时不需要；把 diagram 规则落在 overview/detailed guidance 内，更贴合作者实际写作路径。
- 我检查了测试是否应该做更强的语义判定。结论是本轮不做；最低有效做法是扩展文本 contract 断言和模板快照，先让协议演进可验证。
- 我接受一个现实约束：本轮仍然是“改写作 contract”，不是“把所有设计知识自动结构化”。因此 detailed 必须补得更可执行，但不能假装替代实施中的进一步思考。
