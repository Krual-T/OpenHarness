# OH-038 Human-Agent Design Doc Upgrade

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Summary
- 这轮 task package 解决的是 OpenHarness 当前 `02-overview-design.md` 与 `03-detailed-design.md` 更偏流程收敛和验证推进、但对人和 agent 协作开发不够“可执行”的问题。
- 本轮目标是把总体设计与详细设计的写作 contract 强化为更适合实现协作的结构化设计说明，并引入 `PlantUML` 图示建议作为正式辅助约束。

## Current Status
- 当前已完成需求、总体设计和详细设计收敛，包状态进入 `detailed_ready`。
- 实现尚未开始；后续将先补测试，再修改 guidance/template，并用现有协议测试验证脚手架与文档 contract 一致。

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `04-verification.md`
- `05-evidence.md`
