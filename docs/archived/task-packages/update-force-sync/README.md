# OH-045 Update Force Sync Option

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 为 `openharness update` 增加显式 `--force-sync` 参数，使用户可以有意识地把 OpenHarness 源码 clone 强制同步到上游后再刷新已安装 CLI。

## Current Status
- 当前处于实现阶段：需求和设计已经收敛，正在用测试先锁定 CLI 参数、命令顺序和失败中断语义。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
