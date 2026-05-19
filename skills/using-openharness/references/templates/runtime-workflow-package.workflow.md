---
name: <RWP_NAME>
description: <DESCRIPTION>
---

# Runtime Workflow Package

## Purpose
说明这个 RWP 验证什么真实运行时行为。一两句话说清楚：验证什么系统/服务/流程的什么行为。
> 例：验证 Lark 消息发送后，消息在 5 秒内出现在目标群聊中。

## When To Use
说明什么类型的任务应考虑使用这个 workflow。
> 例：涉及 Lark 消息发送功能的任务、需要验证消息投递时效性的回归测试。

## Prerequisites
列出运行脚本需要的所有前置条件：
- 环境变量（如 `LARK_APP_ID`、`LARK_APP_SECRET`）
- 账号/权限（如需要某个群的发送权限）
- 服务状态（如目标 API 可访问）
- 测试数据（如预置的群聊 ID）

## Scripts
说明 `scripts/` 下每个脚本的作用和用法。
> 例：
> - `send_and_check.py` — 发送消息并轮询检查是否送达，参数 `--target <env>`
> - `cleanup.py` — 清理测试消息，参数 `--target <env>`

## Runtime Observation
说明运行后应观察什么来判定结果：
- 日志输出（哪些关键行）
- API 响应（状态码、body 中的关键字段）
- 数据库/外部系统状态变化
- trace、截图等外部证据

## Success Criteria
说明什么条件成立时判定通过。用可验证的事实表述。
> 例：脚本退出码为 0，且 stdout 中出现 `"delivered: true"`。

## Failure Evidence
说明失败时必须保存什么证据以便排查：
- 完整的 stdout/stderr
- API 响应 body
- 相关服务的日志片段
- 环境快照（时间、配置版本等）

产物写入 `.harness/rwp/logs/` 目录。

## Limitations
说明这个 workflow 不覆盖什么。
> 例：不覆盖消息内容渲染正确性、不覆盖高并发场景、仅验证单一消息类型。

## Writeback Guidance
- `detailed-design.md`: 写入被选中的 workflow、脚本、前置条件、预期观察和降级路径。
- `verification-design.md`: 写入实际执行命令、退出码、输出摘要、运行时观察和阻塞情况。
- `evidence.md`: 写入产物路径（`.harness/rwp/logs/` 下的文件）、外部记录、人工步骤、残余风险和后续事项。
