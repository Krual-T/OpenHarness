# 详细设计

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 哪些文件会新增或修改，为什么是这些地方？
> - 涉及哪些接口、契约和稳定边界？精度需要细到什么程度？
> - 模块内部职责如何拆分？谁负责状态变化、校验、编排和副作用？
> - 关键数据结构、字段语义或状态转换约束是什么？
> - 准备怎么验证这轮工作真的成立？如果主验证路径走不通，降级路径是什么？
> - testing-first / verification-first 的实施顺序是什么？
> - observability 要求是什么？要靠什么看见失败或退化？
> - 失败路径、误用风险和静默出错风险是什么？
> - 迁移顺序和回滚注意事项是什么？
> - 还有哪些挑战被接受、拒绝或延期？
> - 哪些交互关系最适合用 PlantUML 表达？
>
> **写法建议**：先把实现设计写到足以判断验证对象，再写验证路径（否则容易让测试或命令替代真实设计）。Files Added Or Changed 不只是改动清单，更是"为什么这些地方承载本轮实现"的解释。模块内部职责、数据语义和异常边界要写到 agent 能直接据此落实现。如果你写完后还不能直接开始实施，说明 detailed 还不够具体。

## 可观察性与验证准备
- **验证路径**：本任务使用 `verify_by: qualitative`，主验证路径是文档语义审核加现有 CLI / pytest 回归命令。验证设计阶段需要先写审核矩阵，再实施文档和 CLI heading 校验改动。
- **回退路径**：如果中文 heading 改动导致当前任务包无法 transition，不能宣称完成；应回到 implementing 修复 `TaskPackageDocument` 的 heading 定义、模板或当前任务包文档。如果失败来自状态流转、hook 或数据模型变更，应回退实现，因为这些不在本轮允许范围。
- **预期证据**：后续 `verification-design.md` 需要收集四类证据：定性审核矩阵、`openharness task-package transition` 或等价校验结果、相关 pytest 结果、变更文件清单和残余风险。

验证优先顺序是：先在 `verification-design.md` 定义定性审核维度和回归命令，再实施改动。pytest 只覆盖 CLI heading 校验行为，不替代对 skill 和模板职责边界的语义审核。

## 新增或修改文件
本轮实现落点限定在 workflow skill 与模板文档表面。

- `skills/using-openharness/SKILL.md`
  - 承载会话入口协议。
  - 按 overview 结论收窄为“每个会话开始时使用”的入口 skill。
  - 删除仓库级约定、受保护文件、输出约定和完整状态机解释。
  - 保留任务包边界、进入任务包命令、阶段完成到完成态的最小映射。

- `skills/using-openharness/states/*/SKILL.md`
  - 承载阶段思考方法与推进门禁。
  - 调整每个阶段的职责描述，使其继续引导 agent 完成当前阶段最重要的思考工作，而不是只列执行清单。
  - 删除或压缩与模板重复的章节写作细节。

- `skills/using-openharness/references/templates/*`
  - 承载文档结构、完成标准和质量标准。
  - 移除流程教学、状态机教学和跨阶段职责说明。
  - 任务包 Markdown 文档章节标题改为中文；不保留临时英文兼容锚点。

- `.tmp/skills-backup/finishing-a-development-branch/`
  - 承载 `skills/using-openharness/states/finishing-a-development-branch/` 的备份。
  - 该 skill 不再作为主工作流自动注入阶段的优化对象，但备份应保留以便回滚或人工查阅。

明确不修改：

- CLI 状态值、hook 触发、任务包数据模型
- archived 历史包批量内容
- 任务包文件名语义

允许修改：

- `openharness_cli/models/task_package_document.py`
- `openharness_cli/validate.py`
- 与 Markdown heading 校验相关的测试

## 接口
本轮要更新的接口是 CLI 对任务包文件和 heading 的校验契约。`openharness_cli/models/task_package_document.py` 定义每类任务包文档需要检查的 heading；`openharness_cli/validate.py` 按这些 heading 检查非占位内容。

实现后，任务包 Markdown 文档的必需章节 heading 应以中文为准。CLI 校验、模板和当前任务包文档必须同步切换，避免文档为了通过 transition 保留临时英文锚点。状态值、gate 流转、hook 触发、命令语义和任务包数据模型保持不变。

本轮暴露给 agent 的协作契约是：

- 入口 skill 只建立会话入口和任务包协议，不复制 `AGENTS.md` 的仓库级约定。
- 阶段 skill 负责阶段思考方法、推进步骤、阻塞条件和完成态 transition。
- 模板负责文档章节、完成标准和质量标准。
- 需求阶段必须确定 `task_type`、`design_review_mode`、`verify_by`；后续阶段只消费字段，发现错误时回退需求阶段。

## 模块内部设计
`skills/using-openharness/SKILL.md` 的内部结构收敛为四段：

1. 协议定位
   - 说明 OpenHarness 是 SDD 驱动的任务包协作协议。
   - 说明 `using-openharness` 仅在每个会话开始时使用。
   - 不要求读取 `AGENTS.md`，因为框架负责加载。
   - 不写仓库级输出约定、受保护文件、Python / uv 或提交要求。

2. 任务包边界
   - 需要任务包：代码修改、设计决策、bug 修复、新增功能、改变仓库事实源的文档更新。
   - 不需要任务包：纯问答、解释现有代码、未进入执行的方案讨论。
   - 已经进入任务包的设计讨论，确认后的设计决策仍要写回任务包文档。

3. 进入任务包
   - 需要任务包时先运行 `openharness task-package list`。
   - 有匹配包时运行 `openharness task-package view <task>`。
   - 无匹配或空时运行 `openharness task-package new <name>`。
   - 随后执行 CLI 输出的当前阶段 skill。

4. 阶段完成
   - 每个活跃阶段完成后，用 `openharness task-package transition <task> <完成态>` 推进到对应完成态。
   - 保留最小映射：
     - `proposing` → `requirements_designed`
     - `overview_designing` → `overview_designed`
     - `detailed_designing` → `detailed_designed`
     - `verification_designing` → `verification_designed`
     - `implementing` → `implemented`
     - `verifying` → `verified`
   - 只说明 agent 负责把当前阶段 transition 到对应完成态；后续推进由 CLI 处理，不解释完整状态机和 gate 内部实现。

## 数据语义
本轮关键数据语义不是新增数据结构，而是 workflow 文档中的职责字段和状态字段如何被解释。

阶段 skill 的稳定语义：

- 阶段目的：当前阶段最重要的问题是什么。
- 阶段方法：agent 应该如何思考、发散、收敛、挑战、下沉或验证。
- 推进门禁：Exit Check、阻塞条件、对应完成态。
- 回退路径：发现需求、设计、验证策略、实现或环境问题时回到哪里。
- 模板引用：只指向对应模板路径，不复制模板章节的完整写法。

各阶段的目的语义：

- `brainstorming`：发散、挑战前提、收敛需求和边界。
- `exploring-solution-space`：探索可行方案、比较取舍、确定系统边界。
- `detailed-design`：把总体方案落到可实现、可观察、可回退的设计粒度。
- `verification-designing`：按 `verify_by` 设计判断方式和通过标准。
- `implementing`：按验证契约实现，记录中间事实。
- `verifying`：执行验证，比较预期和实际，给出最终证据结论。

阶段 skill 应删除或压缩的语义：

- 与模板重复的章节级写作指导。
- 仅重复“不要跳过此阶段”的冗长反合理化表格。
- 非当前阶段的长篇说明。
- 仓库级约定和入口协议说明。

`task_type`、`design_review_mode` 和 `verify_by` 的字段语义：

- 三者都必须在需求阶段确认并写入 `task-info.yaml`。
- 后续阶段只消费这些字段；发现错误时回退需求阶段修正。
- `design_review_mode: stepwise` 要继续保留逐项确认行为；`auto` 表示 agent 可以自主推进并写回设计决策。

模板的稳定语义：

- 模板是文档承载结构，不是阶段导师。
- 模板应说明文档用途、章节结构、每章完成标准、常见不合格表现和相邻文档边界。
- 模板不使用“最低要求”作为主导措辞，避免 agent 追求刚好过线。
- 模板优先使用“完成标准”“合格文档需要说明”“进入下一阶段前应当能够判断”等措辞。
- 模板不写完整状态流教学、CLI 命令教学、阶段推进说明或大段阶段方法论。

各模板的特殊语义：

- `task-package.task-info.yaml` 只保留 YAML 结构、字段示例和枚举提示；删除完整状态流注释；自然语言字段示例使用中文；不解释 workflow。
- `task-package.requirements.md` 保留对 `task_type`、`design_review_mode`、`verify_by` 三项分类的写入提醒，因为三者必须在需求阶段确定。
- `task-package.detailed-design.md` 避免把详细设计收窄为运行时验证计划。对应中文 heading 应转向“可观察性与验证准备”等语义，而不是保留 `## 可观察性与验证准备` 作为兼容锚点。
- `task-package.verification-design.md` 按 `verify_by` 分流 `unit_test`、`qualitative`、`rwp`，不默认 pytest。
- `task-package.evidence.md` 区分开发中事实和最终验证结果；最终通过/失败结论只能由 verifying 阶段填写。CLI 校验应同步使用中文 heading。

## 阶段门禁
进入实施前必须满足：

- 已确定所有实现落点：入口 skill、阶段 skill、模板、CLI heading 定义、相关测试、`.tmp` 备份目录。
- 已确定稳定边界：只改 Markdown heading 校验，不改状态流转、hook、命令语义、任务包数据模型或文件名。
- 已确定入口 skill 的四段结构和 transition 命令模板。
- 已确定阶段 skill 的改写规则：保方法、清门禁、减重复。
- 已确定模板改写规则：中文 heading、完成标准、不写“最低要求”、不承担阶段方法论。
- 已确定迁移顺序：先改 CLI heading 定义和测试，再改模板和当前任务包文档，再改入口 skill 和阶段 skill，最后移动收尾 skill 备份。
- 已确定验证证据：定性审核矩阵、CLI/pytest 回归、变更文件清单、残余风险。

## 决策闭合
- 接受：CLI heading 校验与模板中文 heading 同步修改。理由是用户明确不保留英文兼容 heading；如果 CLI 仍要求英文，模板会继续被迫保留过渡锚点。
- 接受：模板用“完成标准”替代“最低要求”。理由是“最低要求”会诱导 agent 追求刚好过线，不符合本轮提升文档质量的目标。
- 拒绝：把阶段 skill 改成纯执行清单。理由是阶段 skill 的核心价值是引导阶段思考方法。
- 拒绝：本轮顺手调整 CLI 状态机或 hook 行为。理由是当前问题是文档职责和 heading 校验冲突，不是状态机缺陷。
- 延期：批量重写 archived 历史包中文 heading。触发条件是未来需要让 archived 包也通过新的严格校验；本轮只处理当前 workflow 表面和当前任务包。


## 错误处理
主要失败路径和处理：

- 中文 heading 与 CLI 校验不一致：表现为 `openharness task-package transition` 或 `check-tasks` 报缺少必需章节。处理是同步修正 `TaskPackageDocument`、模板和当前任务包文档，不通过增加英文兼容 heading 规避。
- 模板被写成阶段导师：表现为模板里出现完整流程教学、CLI 命令教学或大段阶段思考方法。处理是把方法论移回阶段 skill，只保留文档用途、章节结构、完成标准和不合格表现。
- 阶段 skill 被压缩过度：表现为只剩步骤列表，缺少阶段目的、思考方法、阻塞和回退。处理是恢复阶段方法段落，但不复制模板章节写法。
- 误改状态机或 hook：表现为状态流、CLI 命令语义或 hook 输出变化。处理是回退这类实现，只保留 heading 校验相关 CLI 修改。
- `.tmp` 备份丢失：表现为 `finishing-a-development-branch` 原内容无法追溯。处理是从 git 或工作树恢复备份目录，不继续归档或删除。

## 迁移说明
实施顺序：

1. 更新 CLI heading 定义和相关测试。
   - 修改 `openharness_cli/models/task_package_document.py` 中各文档的必需 heading 为中文。
   - 检查 `openharness_cli/validate.py` 是否需要支持新的 heading 语义；如果只是读取定义，不做额外改动。
   - 更新 `tests/openharness_cases` 中依赖英文 heading 的测试数据和断言。

2. 更新当前任务包文档和模板。
   - 将模板 heading 改为中文。
   - 将当前任务包文档同步到中文 heading，移除临时英文兼容锚点。
   - 把“最低要求”类措辞改成“完成标准”类措辞。

3. 更新入口 skill。
   - 收窄为四段结构。
   - 保留 `openharness task-package transition <task> <完成态>` 命令模板。

4. 更新阶段 skill。
   - 逐个阶段按“阶段目的、阶段方法、推进门禁、回退路径、模板引用”检查。
   - 删除与模板重复的章节写作指导。

5. 移动收尾 skill。
   - 将 `skills/using-openharness/states/finishing-a-development-branch/` 移到 `.tmp/skills-backup/finishing-a-development-branch/`。

切换点：CLI heading 定义、模板和当前任务包文档三者都切到中文 heading 后，才能运行 transition 或 check-tasks 作为有效验证。

回滚触发点：

- 如果 CLI heading 改动引发大范围非目标测试失败，先回滚 heading 定义和测试，重新评估是否需要拆出独立 CLI 兼容任务。
- 如果模板改动造成 agent 失去阶段方法引导，回滚模板中的方法论删除并重新分配到阶段 skill。
- 如果移动收尾 skill 导致主流程引用断裂，恢复原路径并在验证设计中记录该引用来源。

## 推荐图示
不需要新增 PlantUML 图。本轮关系是文档职责和校验契约，文字列表比图更直接。若后续实现发现 CLI heading 校验迁移路径复杂，再补一张“文档类型到中文 heading”的表格即可，不需要流程图。

## 详细设计反思
反思结论：

- 测试策略不能只靠 pytest，因为大部分目标是文档职责边界；必须以定性审核矩阵为主，pytest 只验证 CLI heading 校验没有坏。
- 接口边界已经扩大到 CLI heading 校验，但不能继续扩张到状态机、hook 或数据模型，否则会变成另一个任务包。
- 迁移假设中最容易出错的是“先改模板再改 CLI”。正确顺序是先让 CLI 认识中文 heading，再切模板和当前任务包文档。
- 预期证据必须同时证明“能通过工具校验”和“文档语义没有互相抢职责”。只跑命令不足以证明本任务完成。
