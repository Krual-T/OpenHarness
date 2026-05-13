---
name: requesting-code-review
description: 完成任务、实现主要功能或在合并前使用，验证工作是否满足要求
---

# 请求代码审查

## 何时请求

- 主要功能或重构之后
- 合并到 main 之前
- 声称一个广泛变更"安全"之前
- 卡住时、风险重构前、修复微妙 bug 后（可选）

## 步骤

1. 获取 diff 范围：`BASE_SHA=$(git rev-parse HEAD~1)` `HEAD_SHA=$(git rev-parse HEAD)`
2. 使用 `references/code-reviewer.md` 模板构建审查上下文：改了什么、要达成什么、diff 范围、已知风险
3. 执行审查并根据反馈行动：
   - Critical 问题立即修复
   - Important 问题推进前修复
   - Minor 问题适时记录
   - 审查结论有误时用技术理由回应

## 要点

- 不要因为变更"看起来小"就跳过审查
- 不要带着未修复的 Important 问题继续推进
- 不要反驳有效的技术反馈
