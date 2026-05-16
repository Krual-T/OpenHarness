---
name: reviewing-task-package
description: 当任务状态是 verifying 且任务包文档需要质量审核时使用
---

# 任务包文档审核

## 何时使用

以下任一情况：
- 程序化验证通过（`openharness check-tasks`），但文档读起来像占位符
- 需要判断内容是否有信息量，而非仅检查章节是否存在
- 任务包进入 `verifying` 或 `archived` 前，需要独立的文档质量审查
- 用户质疑文档是否真正反映了设计思考过程

## 审核流程

1. **读取写作指南**：用 CLI 发现指南，再读取内容作为审核标准
   - `openharness writing-guide` 列出所有可用指南
   - `openharness writing-guide read requirements` 读取需求文档写作指南
   - `openharness writing-guide read overview` 读取概览设计写作指南
   - `openharness writing-guide read detailed` 读取详细设计写作指南
   - `openharness writing-guide read verification` 读取验证文档写作指南
   - `openharness writing-guide read evidence` 读取证据文档写作指南
2. **读取任务包文档**：对照 guidance 中的 Exit Check 和 Common Failure Modes 逐条审查
3. **输出质量评估**：
   - 通过的项：简述为什么通过
   - 不通过的项：指出具体位置、问题和修改建议
   - 需要澄清的项：说明缺失什么信息
4. **决定是否阻塞**：审核不通过时，不进入下一阶段

## 审核原则

- **语义优于形式**：章节存在不等于内容有价值
- **具体优于抽象**："提升质量"是抽象的，"增加 X 测试覆盖率到 Y%"是具体的
- **可追溯优于完备**：证据链比篇幅更重要
- **挑战优于附和**：审核的目的是发现问题，不是盖章通过

## 常见审核发现

| 形式正确但内容空洞的信号 | 期望的替代 |
|--------------------------|-----------|
| Goal 只写"提升系统稳定性" | 写清"将错误恢复时间从 X 缩短到 Y" |
| Trade-offs 只写"选了 A 因为更好" | 说明"选 A 放弃了 B 的 Z 能力，代价是 W" |
| Reflection 只写"经过反思确认方案可行" | 说明"挑战了 X 假设，发现 Y 约束后接受" |
| Verification 只写"运行测试" | 写清"运行 X 命令，预期 Y 输出，实际 Z" |

## 与程序化验证的关系

`openharness check-tasks` 检查形式合规性。
`reviewing-task-package` 检查语义质量。
两者互补，不是替代关系。

## 按任务类型调整审核范围

- **mechanical**：只审核 `01-requirements.md`、`04-verification.md`、`05-evidence.md`
- **standard / protocol/architecture**：审核全部 01-05

## 要点

- 审核不通过时，文档需要修改后重新审核
- 不要为了让审核通过而堆砌文字
- 审核报告本身应写回 `04-verification.md` 或 `05-evidence.md` 作为质量证据
