# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
收敛 skill 体系里重复出现的仓库级协议、阶段门槛和流程说明，让仓库入口层负责常驻规则，具体 skill 只保留与自身职责直接相关的指导。

## Problem Statement
当前 `using-openharness`、`brainstorming`、`exploring-solution-space`、`subagent-driven-development` 等 skill 都承担了大量流程制度说明，包含 stage gate、reflection、review loop、写回规则、子智能体升级条件等。这些内容部分重叠、部分略有变体，导致两个问题：

1. 单个 skill 文档过长，触发一次就会吞掉大量上下文。
2. 仓库协议一旦调整，需要同步修改多处文本，否则很容易出现局部过时或相互冲突。

如果不处理这个问题，skills 会越来越像一组彼此重叠的“总章程”，而不是职责清晰、按需加载的能力模块。

## Required Outcomes
1. 识别哪些规则属于仓库入口层常驻协议，哪些属于具体 skill 的专属动作。
2. 为核心 skill 建立职责边界，避免重复描述同一套阶段制度和写回协议。
3. 设计可执行的收敛方案，例如主协议集中、child skill 精简、通过引用而不是重复粘贴来共享规则。
4. 修改完成后，child skills 的体积与职责都应明显更聚焦，不再承担大段重复的仓库级制度说明。

## Non-Goals
- 不在这项任务里清理旧环境术语和不可用工具名，那属于独立任务。
- 不改变 task package 的核心协议语义和状态流定义。
- 不为了缩短文档而删除真正必要的执行约束。

## Constraints
- 必须保持 `using-openharness` 作为唯一仓库入口 skill 的定位不变。
- 不能通过删除规则来制造“更短”，而是要通过职责分层和引用关系来减少重复。
- 收敛后的结构仍需支持 AGENTS.md 中规定的阅读顺序、task package 写回要求和验证协议。
- 反例：如果只是把重复段落搬到别的 skill 里，或者留下多个内容不一致的“主说明”，都不算成功。
