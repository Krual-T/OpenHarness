# OH-018 Workflow Stage Visibility And Task Intake

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 收敛两类使用摩擦：一是让人和 agent 都能快速看清当前处于哪个 workflow stage、下一步要做什么；二是把“自动创建 task package”的时机固定在 brainstorming 结束、即将进入下一阶段之前，而不是要求用户提前手工准备完整标识。

## Current Status
- 当前处于实现与验证阶段。
- 本包会同时更新 task package 文档、`using-openharness` / `brainstorming` 协议说明、`openharness.py` CLI 行为以及对应测试。
- 完成后应能让维护者从入口输出看见阶段与下一步，并让 agent 在没有现成 package 时，先完成 brainstorming，再自动创建 package 进入 exploration。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
