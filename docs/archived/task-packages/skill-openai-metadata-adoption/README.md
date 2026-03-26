# OH-023 Skill OpenAI Metadata Adoption

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务包聚焦为仓库内 vendored skills 补齐 `agents/openai.yaml` 元数据，统一声明面向 Codex 的界面文案、隐式触发策略与必要工具依赖。
- 设计结论是按技能职责分层：保留核心流程技能的隐式触发能力，把只适合在明确上下文下使用的执行型或收尾型技能改成显式调用优先，并用轻量测试防止后续回退到“只有说明文、没有元数据约束”的状态。

## Current Status
- 本任务已完成实现与验证，任务包将随本轮一起归档。
- 当前状态与 `STATUS.yaml` 一致，应为 `archived`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
