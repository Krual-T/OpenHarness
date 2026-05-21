# 需求

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 目标

将 Karpathy 编程准则 #1（先思考再写代码——暴露假设、不隐藏歧义）和 #4（目标驱动执行——可验证的成功标准、循环直到通过）落实到 brainstorming 之后的四个阶段（overview_designing、detailed_designing、verification_designing、verifying），使当前人机协同密度从"前端重、后端轻"变为各阶段均衡。

**单一成功指标**：overview_designing、detailed_designing、verification_designing、verifying 四个阶段每个都至少有一个强制性的人机交互停点（非 `mechanical` 工作流下），且所有 `Exit Check` 标题统一改为中文"阶段结束检查"。

## 问题陈述

OpenHarness 的协议定位是"人机协同"，但停点密度在 brainstorming 之后断崖式下降：

- brainstorming 阶段有 6 个强制用户确认停点（commit `722f9d2`）
- exploring-solution-space 和 detailed-design 的"逐项设计确认"仅标为"建议"
- verification-designing 无任何人机停点，验证策略完全由 AI 自主决定
- verifying 仅 `qualitative` 模式强制人审，`unit_test` 和 `rwp` 的验证结论和残余风险由 AI 自行判断
- 四个阶段 skill 文件的退出检查标题 `Exit Check` 使用英文，与 brainstorming 的"阶段结束检查"不一致

**矛盾**：AI 自主性最高的阶段（实现、验证）恰好是人类介入最少的阶段，而人在前端对需求和设计做了严格把关后，后续实现和验证完全放手给 AI，导致"开头严格、后面放羊"。

**目标用户**：使用 OpenHarness 协议进行 SDD 开发的 AI agent 和人类协作者。

**核心场景**：AI agent 在完成 brainstorming 后，进入 design → implement → verify 的过程中，人在关键决策点（设计方向、验证策略、风险接受）能够介入确认。

## 必须交付的结果

1. **exploring-solution-space 阶段 skill 增强**
   - 将 `## 逐项设计确认` 从建议改为强制：`design_review_mode: stepwise` 时，架构级设计决策至少有一个停点（写完边界、主路径、推荐结构后，先确认方向再填细节）
   - 在步骤 4 后增加准则 #1 动作：存在多个可行方向时，必须列出候选+取舍，不得默选
   - 准则 #4 落地：阶段结束检查的 6 个问题从自问自答改为要求引用文档具体章节作为证据
   - `Exit Check` 标题改为中文"阶段结束检查"
   - 验收标准：skill 文件中存在明确的"停点"标记，且阶段结束检查每项都要求引用文档章节号

2. **detailed-design 阶段 skill 增强**
   - 将 `## 逐项设计确认` 从建议改为强制：`design_review_mode: stepwise` 时，接口精度决策至少有一个停点
   - 在步骤 3"接口精度"后增加准则 #1 动作：存在多个合理选择时（参数传 ID 还是对象、错误处理方式等），列出选项+代价，不得默选
   - 准则 #4 落地：阶段结束检查的 7 个问题改为要求引用具体产物（文件路径、接口签名、数据结构定义）作为证据
   - `Exit Check` 标题改为中文"阶段结束检查"
   - 验收标准：skill 文件中存在明确的"停点"标记，且阶段结束检查每项都要求引用具体产物

3. **verification-designing 阶段 skill 增强**
   - 新增人机停点：写完 `verification-design.md` 后，向用户展示验证命令清单+覆盖矩阵+不覆盖的风险和接受理由，获得确认后才 transition
   - 准则 #1 落地：明确陈述"哪些风险本轮不覆盖"以及接受理由，由用户确认盲区
   - 准则 #4 落地：增加可选步骤——在设计阶段就跑一次验证命令确认它们能正确失败（验证 RED），提前暴露验证策略 bug
   - `Exit Check` 标题改为中文"阶段结束检查"
   - 验收标准：skill 文件中存在"验证策略确认停点"，明确要求展示命令清单和风险接受

4. **verifying 阶段 skill 增强**
   - 扩展人审范围：所有 `verify_by` 模式（不只是 `qualitative`）下，evidence.md 写入最终结论（通过/有条件通过/不通过 + 残余风险清单）后，必须向用户展示并获确认后才 transition
   - 准则 #4 落地：增加"循环验证"概念——回退后重新进入 verifying 时，明确本轮验证的目标增量
   - `Exit Check` 标题改为中文"阶段结束检查"
   - 验收标准：skill 文件中明确要求所有 verify_by 模式都需要用户对最终结论的确认

5. **术语统一**
   - 四个阶段 skill 文件（exploring-solution-space、detailed-design、verification-designing、verifying）的 `## Exit Check` → `## 阶段结束检查`
   - 验收标准：`grep -r "Exit Check"` 在上述四个文件中返回零结果

## 非目标

- 不修改 CLI 层（transition_engine.py、workflows.py、task_status.py）——所有停点均为 skill 指令层面的行为约束
- 不调整 mechanical 工作流——mechanical 任务跳过 overview/detailed，验证策略简单，不需要这些停点
- 不新增工作流分叉字段——复用现有 `design_review_mode: stepwise/auto`
- 不涉及 brainstorming 阶段——该阶段已在 commit `722f9d2` 完成增强
- 不涉及 implementing 阶段——该阶段由 TASK-021 独立处理
- 不引入 Karpathy 准则 #2（简洁优先）和 #3（精准修改）——TASK-020 只落地 #1 和 #4

## 约束

- 仅修改 `skills/using-openharness/states/` 目录下的 SKILL.md 文件，不动 CLI Python 代码
- 保持现有 skill 文件的结构（步骤 → 退出检查 → 要点 → 边界 → 失败模式 → 反合理化）不变
- 新增停点必须是单向的——停点提示用户确认，确认后继续推进，不引入新的状态/子状态
- 向后兼容：`design_review_mode: auto` 时，逐项设计确认应保持为可选（不阻塞 AI 自主推进）
- 成本上限：不新增外部依赖，不改动超过 4 个 SKILL.md 文件 + 1 个实现 skill 调用
