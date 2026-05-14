# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
这轮设计覆盖的是 OpenHarness 如何定义“更适合人和 agent 协作开发”的总体设计与详细设计写作 contract，而不是修改 task package 的固定生命周期。

纳入范围：

- `skills/using-openharness/references/overview-design-writing-guidance.md`
- `skills/using-openharness/references/detailed-design-writing-guidance.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- 与上述 contract 对齐的协议测试

不纳入范围：

- 新增 task package 文件或改变 `02`/`03` 的基本阶段职责
- 强制引入图渲染工具链、图片产物目录或图语法校验
- 一次性重写所有历史 package
- 把总体设计写成教科书式“大而全”总设，导致与 `03` 的边界消失

## Proposed Structure
推荐采用“两份 guidance + 两份模板同步增强”的结构，而不是只改其中一层。

1. `02-overview-design.md` 强化为“架构协作说明”
   - 保留现有 `System Boundary`、`Trade-offs`、`Overview Reflection` 等阶段价值。
   - 增补对模块划分、依赖方向、边界级接口关系、关键数据/状态模型、架构级安全/一致性约束的要求。
   - 增加 `PlantUML` 图示建议，优先支持上下文图、模块图、主流程图。
2. `03-detailed-design.md` 强化为“实施协作说明”
   - 保留现有 `testing-first`、验证路径、文件落点、迁移顺序、回滚说明。
   - 增补模块内部职责、接口精度、数据语义、异常处理、边界条件和可直接编码的实现顺序要求。
   - 增加 `PlantUML` 图示建议，优先支持时序图、状态图、数据关系图。
3. 模板只保留短提示，不复制完整 guidance
   - guidance 负责定义写作 contract。
   - template 负责让作者起笔时不会漏掉关键设计维度。
4. 测试只验证 contract 的最小存在性
   - 通过测试确保 guidance/template 至少包含新要求。
   - 不把“设计好坏”升级成难以维护的语义评分器。

关键约束是：overview 只写架构级边界和结构，不下沉到函数级实现；detailed 承接 overview，但不重新争论总体方向。

## Key Flows
主流程如下：

1. 作者在 `01-requirements.md` 收敛“为什么需要增强设计文档”。
2. 在 overview guidance 中先建立整体设计模型：
   - 改动覆盖哪些仓库表面
   - 模块如何划分与依赖
   - 关键接口和数据/状态边界在哪里
   - 为什么这个结构更适合人和 agent 协作
3. 在 detailed guidance 中把整体模型下沉为可执行实现设计：
   - 实现落点在哪些文件
   - 接口和数据语义要细到什么程度
   - 测试优先和验证路径如何安排
   - 失败如何观测、迁移和回滚
4. 模板同步给出最短提醒，让新建 package 的作者在脚手架层面就能看到这些约束。
5. 协议测试校验 guidance 与模板仍满足最小 contract。

关键失败信号：

- 如果 overview 仍然只有边界/主流程，没有模块、接口和数据模型，说明人机协作约束仍然不够。
- 如果 detailed 仍然主要描述验证路径和文件落点，没有接口精度、异常边界和实现顺序，说明它仍不足以支撑 agent 执行。
- 如果模板过长到接近教程，说明职责回退到了错误层。

## Stage Gates
- 必须明确 overview 与 detailed 的新分工：`02` 负责架构协作，`03` 负责实施协作。
- 必须明确至少一组“人和 agent 共同需要”的设计信息，并决定它们分别属于 `02` 还是 `03`。
- 必须明确图示在 overview 与 detailed 中的推荐落点，并声明图不能替代文字约束。
- 必须定义失败模式：如果作者仍需主要依赖 archived packages 猜模块边界或接口粒度，改造就不算成功。
- 必须给出降级方向：如果模板承载不了这么多信息，就把细节留在 guidance，模板只保留问题提示，而不是回退到完全不写。

## Trade-offs
我考虑了三种主要方向：

- 方案一：只增强 `03-detailed-design.md`
  - 收益是更贴近编码落地。
  - 代价是总体边界和模块关系仍然模糊，人和 agent 会在不同前提下细化实现，最终拼接风险高。
- 方案二：只增强 `02-overview-design.md`
  - 收益是架构表达更完整。
  - 代价是落到实施时仍缺乏精确接口、数据语义和异常路径，agent 仍要自行补假设。
- 方案三：同步增强 `02` 与 `03`，并配套 `PlantUML` 图示建议
  - 这是推荐方案。
  - 收益是从“整体模型”到“实施模型”的信息链路连续，既保留当前协议的阶段治理优势，又补足传统软件工程里对开发协作更重要的结构化设计信息。
  - 代价是 guidance 和模板会比现在更重，需要用测试约束和章节边界避免文档膨胀。

回退面：

- 如果某些传统软件工程设计项对本仓库过重，可以用“关键数据/状态模型”“架构级安全约束”这种轻量表达替代固定 ER 图或完整数据字典。
- 如果 `PlantUML` 建议被证明过强，可降级为“推荐图示类型”，而不是强制每个 package 都画图。

## Overview Reflection
- 我先挑战了“是不是只要把 `03` 写细一点就够了”。结论是拒绝。因为没有更强的 overview 边界和结构信息，detailed 细化仍会建立在不稳定前提上。
- 我也挑战了“是不是应该完全回到传统软件工程教材目录”。结论是拒绝。OpenHarness 仍需要保持 task-package 分阶段协议，不能把 `02`/`03` 写成脱离当前仓库工作流的总设说明书。
- 我接受了“应该把模块、接口、数据、异常、安全等设计信息重新拉回文档 contract”，但要求这些信息按 overview/detailed 分层表达，而不是堆成一个大全章节表。
- 我延期了“是否要新增自动校验 `PlantUML` 图语法或数量”的问题。本轮先把图示作为正式推荐写法纳入 guidance/template，等真实使用一轮后再决定是否需要更强约束。
