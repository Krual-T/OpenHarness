---
name: implementing
description: 当任务状态是 implementing（实现使验证通过，TDD 绿+重构阶段）时由 CLI 自动注入
---

# 实现

## 何时使用

验证策略已设计完成（`verification_design.md` 就绪），开始写代码使验证通过。

## 步骤

### TDD 循环：RED → GREEN → REFACTOR

1. **RED**：运行 `verification_design.md` 中声明的验证命令，亲眼看到失败
2. **GREEN**：最小实现使测试通过
3. **REFACTOR**：消除重复、提取函数、改善结构，保持测试全绿

重复直到所有验证通过。

### 完成后

1. 运行全部验证命令，确认全部通过
2. 写 `evidence.md`：
   - **Verification Result**：verify_by 类型 + passed/failed
   - **Test Results**（unit_test）：测试命令 + 结果 + 变更文件 + 验收标准覆盖表
   - **Semantic Review**（qualitative）：审核对象 + 发现 + 结论 + 闭合状态
   - **Runtime Observation**（rwp）：工作流名 + 观察结果 + 产物路径 + 盲区
   - **Residual Risks**：本轮未覆盖的风险
   - **Follow-ups**：延后事项
3. `openharness task-package transition <task> verifying`

## Exit Check

1. 所有 `verification_design.md` 中声明的验证命令是否全部通过？
2. `evidence.md` 是否存在且内容非空？
3. 变更文件是否已全部列出？

全部能回答 → `openharness task-package transition <task> verifying`

## 要点

- 先让测试失败，再写实现——不要跳过 RED
- evidence.md 只写事实，不写评价
- 如果验证失败且不是代码问题，回到 `verification_design.md` 修正验证策略
- 并行调度是横切策略，可在本阶段自行选择使用
