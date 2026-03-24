# Detailed Design

## Runtime Verification Plan
- Verification Path:
- 本轮是 skill 与测试 productization，不涉及业务运行时验证。
- 需要执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 与 `uv run pytest`，确认任务包、技能文档、模板与仓库测试一起成立。
- Fallback Path:
- 如果 `check-tasks` 或 `uv run pytest` 被环境或无关失败阻塞，本轮只能停在 `verifying`，不能宣称协议已 productize 完成。
- Planned Evidence:
- 受影响 skill 文档与模板已更新
- 针对新协议的仓库测试已补充并通过
- `05-verification.md` 和 `06-evidence.md` 记录实施与验证结果

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/archived/task-packages/gstack-methodology/README.md`
  - 作为任务入口页，说明这不是工具安装任务，而是方法论设计任务。
- `docs/archived/task-packages/gstack-methodology/STATUS.yaml`
  - 记录当前处于 `detailed_ready`，表明设计已成形但尚未进入实现。
- `docs/archived/task-packages/gstack-methodology/01-requirements.md`
  - 明确目标、边界、非目标与约束。
- `docs/archived/task-packages/gstack-methodology/02-overview-design.md`
  - 说明“按阶段组织、按角色注入”的总体结构。
- `docs/archived/task-packages/gstack-methodology/03-detailed-design.md`
  - 明确阶段与角色的映射、职责边界和收敛协议。
- `docs/archived/task-packages/gstack-methodology/05-verification.md`
  - 记录本轮 skill productization 的验证路径与结果。
- `docs/archived/task-packages/gstack-methodology/06-evidence.md`
  - 记录残余风险与后续事项。
- `skills/using-openharness/SKILL.md`
  - 落地入口协议中的角色注入、阶段门禁与挑战闭环。
- `skills/brainstorming/SKILL.md`
  - 落地需求阶段的产品/CEO 视角与 requirements gate。
- `skills/exploring-solution-space/SKILL.md`
  - 落地 overview / detailed design 阶段的角色注入与 challenge closure。
- `skills/using-openharness/references/skill-hub.md`
  - 对齐 live skill taxonomy 与新的阶段化多视角模型。
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
  - 为 overview 模板增加 stage gate 槽位。
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
  - 为 detailed 模板增加 challenge closure 槽位。
- `skills/using-openharness/references/templates/task-package.05-verification.md`
  - 为 verification 模板增加 traceability 槽位。
- `skills/using-openharness/tests/test_openharness.py`
  - 用仓库测试钉住新协议文案与模板结构。

## Interfaces
本轮设计定义的是概念接口，而不是代码接口。

阶段接口：

- 每个阶段都应有一个主代理
- 每个阶段都应有一组默认注入角色
- 每个阶段都应产出一个主稿文档或主稿结论
- 每个阶段都应携带上一阶段的决策清单作为输入
- 每个阶段都应产出本阶段新增或修改的硬约束
- 每个阶段都应说明后续验证需要观察的证据类型

角色接口：

- 产品视角只挑战用户价值、使用场景、成功标准、优先级，不直接决定技术方案
- CEO 视角只挑战投入产出比、阶段时机、战略一致性与最坏可承受代价，不得扩展到愿景包装、组织叙事或泛化商业空谈
- 架构视角只挑战边界、复杂度、可演进性、主路径稳定性
- 测试视角除挑战验证矩阵、失败路径、回归面和证据充分性外，还应推动把不可测、不可观测、不可回滚的设计提前暴露
- review 视角负责在阶段结果成形后做独立审视，而不是参与所有早期发散
- 风险视角只处理高影响风险，并受时间盒与风险分级约束，不能无限扩张验证范围

收敛接口：

- 主代理负责发起挑战
- 辅助角色负责给出有限边界内的反馈
- 主代理必须逐条处置关键挑战，只允许三种状态：
  - 接受并落为约束
  - 拒绝并给出理由与替代
  - 延期并写清触发条件与最晚落点
- 未完成处置的关键挑战不得静默跨阶段
- 主代理负责裁决冲突并形成阶段结论，但必须遵守收敛优先级，而不是自由裁量

建议的阶段映射如下：

1. `brainstorming`
   - 主代理：需求收敛代理
   - 注入角色：产品视角、CEO 视角
2. `02-overview-design.md`
   - 主代理：设计主代理
   - 注入角色：架构视角、产品视角
3. `03-detailed-design.md`
   - 主代理：设计主代理
   - 注入角色：架构视角、测试视角
4. `05-verification.md`
   - 主代理：验证主代理
   - 注入角色：review 视角、风险视角

浏览器或视觉辅助不属于阶段接口，只属于可选展示接口。

## Stage Gates

建议的阶段门禁如下：

1. `brainstorming`
   - 必须产出：目标用户与核心场景、唯一成功指标、明确不做清单、成本上限、可测试验收标准、至少一个反例
2. `02-overview-design.md`
   - 必须产出：关键约束、接口边界、关键失败模式、降级或回滚方向
3. `03-detailed-design.md`
   - 必须产出：测试策略矩阵、可观测性要求、实现落点、迁移顺序、验证证据类型
4. `05-verification.md`
   - 必须产出：需求到验证的追踪表、剩余风险清单、风险接受理由

建议的反思检查项如下：

- 本阶段最脆弱的一个假设是什么
- 如果该假设为假，会通过什么信号最先暴露
- 本阶段是否已经定义足够早、足够便宜的验证方式来打破幻觉
- 本阶段是否存在一个未被承认的回退点

## Error Handling
需要重点防止四类误用：

- 误把角色当阶段
  - 结果是流程被多个角色切碎，失去主路径。
- 误把辅助工具当核心能力
  - 结果是浏览器、界面、前端交互被错误提升为默认前提。
- 误把多智能体当多人并行写稿
  - 结果是产生多个不收敛版本，而不是对同一主稿的挑战。
- 误把角色职责做成全能
  - 结果是产品、CEO、架构、测试视角互相越界，讨论噪声过高。

避免静默出错的方式是：

- 在每个阶段显式写明主代理是谁
- 在每个阶段显式写明注入角色是谁
- 为每个角色写明允许挑战的问题域
- 在阶段文档中记录主代理如何处理分歧
- 为关键挑战定义否决条件，说明什么情况下必须回退到上一阶段或终止
- 为风险视角设置时间盒和分级，避免验证无限膨胀
- 防止产品视角在总体设计阶段重新打开已经关闭的需求边界

## Decision Closure

当前任务包里的关键挑战处置如下：

- 接受：阶段必须先于实现补齐门禁、挑战闭环与收敛判据，不能只停留在方法论文档。
- 接受：具体入口技能名称统一为 `using-openharness`，避免 skill id 与协议概念混淆。
- 拒绝：把新的门禁锚点立即强制施加到所有历史归档任务包上。
  - 理由：这会把当前 productization 任务膨胀成一次历史迁移。
  - 替代：先在 live templates、live skills 与测试中落实；校验器保持对历史包兼容，后续如需机械强制再单独开包迁移。
- 延期：是否把门禁和挑战闭环变成 task-package validator 的硬性要求。
  - 触发条件：准备统一迁移现有 active / archived task package 时。
  - 最晚落点：未来若要宣称“门禁由仓库机械强制”，必须先完成迁移任务包。

## Migration Notes
建议分三步迁移，而不是一次性把所有技能重写。

1. 先把入口 skill、需求阶段 skill、探索阶段 skill、skill hub 与模板一起更新
   - 避免 live surface 局部采用新协议，其他地方仍停在旧语义。
2. 再用仓库测试把关键文案与结构钉住
   - 确保阶段门禁、角色注入、挑战闭环不会在后续维护中静默回退。
3. 最后通过任务包验证与仓库测试确认协议 productization 完成
   - 每一步都保留回退到“单主代理直推”的能力，避免流程过重。

若后续实现发现角色注入成本过高，可以回退到“仅保留阶段问题清单，不启用真实多智能体”这一中间态。

## Detailed Reflection
我重点反思了三个问题。

第一，是否需要把“产品视角”和“CEO 视角”做成独立常驻代理。当前结论是否定的。它们更适合作为定向挑战角色，而不是持续主持整个任务。

第二，是否要把浏览器能力写进详细设计。当前结论也是否定的。浏览器只应在出现视觉问题时作为可选配套，不应污染多视角协作协议的核心定义。

第三，是否只要规定“什么时候注入角色”就足够。当前结论也是否定的。若没有阶段门禁、角色输出接口和挑战闭环，这套设计会退化为评论流，而不是决策流。

因此详细设计的核心不是工具编排，而是：

- 阶段到角色的映射
- 角色到问题域的映射
- 阶段到硬性产出的映射
- 挑战到处置结果的映射
- 主代理的收敛责任
- 渐进式落地顺序
