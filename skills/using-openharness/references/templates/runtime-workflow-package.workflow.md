---
name: <RWP_NAME>
description: <DESCRIPTION>
---

# Runtime Workflow Package

## Purpose
说明这个 Runtime Workflow Package 验证什么真实 runtime 行为。

## When To Use
用自然语言说明什么类型任务应该考虑这个 workflow。

## Prerequisites
列出需要的环境变量、账号、服务、权限、测试数据和外部系统状态。

## Scripts
说明 `scripts/` 下的脚本各自做什么。这里是说明，不是脚本注册表。

## Runtime Observation
说明运行后应该观察哪些日志、API 返回、消息状态、数据库状态、trace、截图或外部系统记录。

## Success Criteria
说明什么事实成立时可以判定通过。

## Failure Evidence
说明失败时必须保存哪些证据。

## Limitations
说明这个 workflow 不覆盖什么。

## Writeback Guidance
- `detailed-design.md`: 写入被选中的 workflow、脚本、前置条件、预期观察和 fallback。
- `verification-design.md`: 写入实际执行命令、退出码、stdout/stderr 摘要、runtime 观察和阻塞。
- `evidence.md`: 写入 artifact 路径、日志路径、外部记录、人工步骤、残余风险和 follow-up。
