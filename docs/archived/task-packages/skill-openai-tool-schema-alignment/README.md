# OH-025 skill-openai-tool-schema-alignment

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 本任务包聚焦校准仓库内 `agents/openai.yaml` 的 `dependencies.tools` 写法，使其与 OpenAI 当前公开示例和官方代码中的结构化 schema 保持一致。
- 本轮结论是移除仓库内八个技能里未被官方公开支持的 `shell` 依赖声明，并把测试从错误的字符串数组断言改成“仅接受官方对象数组形状，且当前仅允许 `mcp`”。

## Current Status
- 当前已完成需求收敛、外部官方核查、实现与验证，本任务包将在本轮归档。
- 当前状态应与 `STATUS.yaml` 一致，为 `archived`。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
