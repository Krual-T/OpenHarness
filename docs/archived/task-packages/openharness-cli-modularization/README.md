# OH-019 Openharness CLI Modularization

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮工作聚焦 `skills/using-openharness/scripts/openharness.py` 与 `skills/using-openharness/tests/test_openharness.py` 的集中化问题。
- 主结论是保留这两个文件作为稳定入口，把核心实现下沉到新增包里，并把测试按职责拆到多个模块，入口测试文件只承担兼容导入与聚合作用。

## Current Status
- 当前已经完成实现与主要验证，正在补齐最终验证证据并准备归档。
- 入口脚本与入口测试文件都已保留，核心实现和核心测试已经迁移到新增包与子模块。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
