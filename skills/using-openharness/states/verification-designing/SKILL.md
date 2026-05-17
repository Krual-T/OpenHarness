---
name: verification-designing
description: 当任务状态是 verification_designing（设计验证策略，TDD 红阶段）时由 CLI 自动注入
---

# 验证策略设计

## 何时使用

需求已收敛（`01-requirements.md` 完成），需要先设计验证策略再动手实现。这是 TDD 的红阶段——先写"怎么验证"，再写"怎么实现"。

## 步骤

1. **读需求文档**：打开 `01-requirements.md`，确认 Required Outcomes 和 acceptance criteria
2. **确定验证方式**：根据 `STATUS.yaml.verification.verify_by` 选择
   - `unit_test` → 列出测试文件和测试命令
   - `qualitative` → 明确审核对象、审核标准和判定准则
   - `rwp` → 选择或编写运行时工作流脚本
3. **写 `verification_design.md`**：参考模板 `skills/using-openharness/references/templates/task-package.verification_design.md`
   - **Verification Path**：计划路径（怎么验证）和预期执行路径
   - **Required Commands**：逐条列出验证命令（命令、期望退出码、期望输出）
   - **Expected Outcomes**：每项验收标准的预期结果
   - **Traceability**：需求 → 验证的对应关系
   - **Risk Acceptance**：哪些风险本轮不覆盖，以及为什么可以接受
4. **自检 Exit Check**

## Exit Check

1. 每项 Required Outcome 是否都有对应的验证方法？
2. 验证命令是否具体到可以直接复制粘贴执行？
3. 是否有至少一个边界或错误场景的验证？
4. 是否明确了本轮不覆盖的风险和接受理由？

全部能回答 → `openharness transition <task> implementing`

## 要点

- 验证策略是"契约先行"：实现代码时必须让这些验证通过
- 不要在这里写实现方案——那是 `02-overview-design.md` 和 `03-detailed-design.md` 的职责
- 如果发现验证策略本身有歧义，回到 `01-requirements.md` 澄清需求
- 模板位于 `skills/using-openharness/references/templates/task-package.verification_design.md`
