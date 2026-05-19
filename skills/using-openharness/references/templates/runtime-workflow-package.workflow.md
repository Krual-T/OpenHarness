---
name: <RWP_NAME>
description: <DESCRIPTION>
---

# Runtime Workflow Package

## Purpose
说明这个运行时工作流包（Runtime Workflow Package，RWP）验证什么真实运行时行为。

## When To Use
说明什么类型的任务应考虑使用这个工作流。

## Prerequisites
列出需要的环境变量、账号、服务、权限、测试数据和外部系统状态。

## Scripts
说明 `scripts/` 下每个脚本的作用。

## Runtime Observation
说明运行后应观察哪些日志、API 返回、消息状态、数据库状态、trace、截图或外部系统记录。

## Success Criteria
说明什么事实成立时判定通过。

## Failure Evidence
说明失败时必须保存哪些证据。

## Limitations
说明这个工作流不覆盖什么。

## Writeback Guidance
- `detailed-design.md`: 写入被选中的工作流、脚本、前置条件、预期观察和降级路径。
- `verification-design.md`: 写入实际执行命令、退出码、输出摘要、运行时观察和阻塞情况。
- `evidence.md`: 写入产物路径、日志路径、外部记录、人工步骤、残余风险和后续事项。
