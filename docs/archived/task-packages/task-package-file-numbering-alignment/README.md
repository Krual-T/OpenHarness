# OH-032 Align Task Package File Numbering

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮任务把 task package 文件编号从历史上的不连续序列收敛成连续的 `01/02/03/04/05`。具体来说，原先的 verification 与 evidence 文件顺位整体前移一位，并同步更新模板、协议、校验器、测试以及现有 task package 的真实文件名与引用。

## Current Status
- 当前处于实现准备阶段。范围已经明确，不保留双编号，也不做兼容层；会整仓切换到连续编号。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
