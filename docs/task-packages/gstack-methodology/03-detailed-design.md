# Detailed Design

## Runtime Verification Plan
- Verification Path:
- 本轮属于文档设计，不涉及运行时代码验证。
- 需要执行的验证是任务包完整性检查，以及确认状态与文档叙述一致。
- Fallback Path:
- 如果 `check-tasks` 受环境问题阻塞，本轮只能宣称“文档已起草”，不能宣称任务包已经通过仓库协议验证。
- Planned Evidence:
- 任务包目录完整
- `STATUS.yaml` 与文档内容一致
- `05-verification.md` 和 `06-evidence.md` 记录本轮命令与结果

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/task-packages/gstack-methodology/README.md`
  - 作为任务入口页，说明这不是工具安装任务，而是方法论设计任务。
- `docs/task-packages/gstack-methodology/STATUS.yaml`
  - 记录当前处于 `detailed_ready`，表明设计已成形但尚未进入实现。
- `docs/task-packages/gstack-methodology/01-requirements.md`
  - 明确目标、边界、非目标与约束。
- `docs/task-packages/gstack-methodology/02-overview-design.md`
  - 说明“按阶段组织、按角色注入”的总体结构。
- `docs/task-packages/gstack-methodology/03-detailed-design.md`
  - 明确阶段与角色的映射、职责边界和收敛协议。
- `docs/task-packages/gstack-methodology/05-verification.md`
  - 记录本轮只进行文档级验证。
- `docs/task-packages/gstack-methodology/06-evidence.md`
  - 记录残余风险与后续事项。

## Interfaces
本轮设计定义的是概念接口，而不是代码接口。

阶段接口：

- 每个阶段都应有一个主代理
- 每个阶段都应有一组默认注入角色
- 每个阶段都应产出一个主稿文档或主稿结论

角色接口：

- 产品视角只挑战用户价值、使用场景、成功标准、优先级，不直接决定技术方案
- CEO 视角只挑战投入产出比、阶段时机、战略一致性，不直接替代需求分析
- 架构视角只挑战边界、复杂度、可演进性、主路径稳定性
- 测试视角只挑战验证矩阵、失败路径、回归面和证据充分性
- review 视角负责在阶段结果成形后做独立审视，而不是参与所有早期发散

收敛接口：

- 主代理负责发起挑战
- 辅助角色负责给出有限边界内的反馈
- 主代理负责裁决冲突并形成阶段结论

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

## Migration Notes
建议分三步迁移，而不是一次性把所有技能重写。

1. 先完成方法论文档定稿
   - 目标是让阶段骨架和角色注入规则足够清楚。
2. 再选择一个最适合验证的阶段先落地
   - 例如先增强 `brainstorming` 的产品/CEO 视角注入。
3. 最后再把反思、review、测试视角逐步接入其他阶段
   - 每一步都应保留回退到“单主代理直推”的能力，避免流程过重。

若后续实现发现角色注入成本过高，可以回退到“仅保留阶段问题清单，不启用真实多智能体”这一中间态。

## Detailed Reflection
我重点反思了两个问题。

第一，是否需要把“产品视角”和“CEO 视角”做成独立常驻代理。当前结论是否定的。它们更适合作为定向挑战角色，而不是持续主持整个任务。

第二，是否要把浏览器能力写进详细设计。当前结论也是否定的。浏览器只应在出现视觉问题时作为可选配套，不应污染多视角协作协议的核心定义。

因此详细设计的核心不是工具编排，而是：

- 阶段到角色的映射
- 角色到问题域的映射
- 主代理的收敛责任
- 渐进式落地顺序
