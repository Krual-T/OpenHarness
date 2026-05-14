---
name: dispatching-parallel-agents
description: 当存在 2 个以上互不依赖的独立任务时使用，通常由 subagent-driven-development 的并发判断触发
triggers_on: [implementing]
requires: [subagent-driven-development]
next_skills: []
---

# 并行调度子代理

## 何时使用

由 `subagent-driven-development` 的并发判断触发。当子任务满足以下条件时：
- 多个独立的子任务
- 每个子代理用有限上下文就能完成
- 子代理不会编辑同一文件
- 子代理之间没有读取-执行-写入的依赖链

不要用于探索性调试、紧耦合重构或阻塞下一步的任务。

## 步骤

1. 按独立问题域分组
2. 为每个域准备一个边界清晰的 prompt（包含：具体范围、明确目标、约束条件、期望输出）
3. **文件冲突预检**：列出每个子任务预计修改的文件，确认无重叠
4. 并行调度所有子代理
5. 所有子代理返回后：
   - 检查文件冲突（即使有预检，也要确认）
   - 逐一审查结果质量
   - 合并变更
6. 运行完整验证（测试 + 文档审核）
7. 抽查高风险区域

## 与 subagent-driven-development 的关系

`subagent-driven-development` 决定是否使用子代理、是否并发。
`dispatching-parallel-agents` 负责并发调度的执行细节。

如果任务包没有明确标注可并发，先调用 `subagent-driven-development` 判断，再决定是否进入并行调度。

## Prompt 结构

每个子代理的 prompt 需包含：具体范围、明确目标、约束条件、期望输出。不要给子代理"修复一切"这种模糊指令。

## 验证

子代理返回后：检查是否有文件冲突 → 运行完整验证 → 抽查高风险区域
