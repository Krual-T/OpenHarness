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

## TDD 循环故障处理

每一轮 RED → GREEN → REFACTOR 都可能失败，但失败原因不同，回退路径也不同：

| 失败现象 | 诊断 | 回退动作 |
|---------|------|---------|
| RED 阶段命令本身无法运行（文件不存在、import 错误） | 验证基础设施未就绪，不是被测代码的问题 | 回到 `verification_design.md` 修正命令路径或依赖 |
| RED 阶段失败原因与预期不符（测试报错而不是 assertion failure） | 测试代码有 bug | 修复测试，仍在 RED 阶段 |
| GREEN 阶段多个循环后仍无法让测试通过 | 设计有缺陷，或需求不可实现 | 回到 `02-overview-design.md` 或 `01-requirements.md` |
| REFACTOR 后原先通过的测试变红 | 重构引入了回归 | 回滚最近一次重构，小步重做 |
| 所有验证通过，但发现遗漏场景 | 验证策略覆盖不足 | 回到 `verification_design.md` 补充验证命令 |

每完成一轮 TDD 循环，**立即**在 `evidence.md` 中追加该轮的测试命令和结果——不要等全部完成再补写。防止遗漏。

## evidence.md 写法约束

在 implementing 阶段写 evidence.md 时：
- **只写事实**：命令、退出码、输出摘要、变更文件。不写"实现得很优雅"
- **每轮一条**：RED 看到什么、GREEN 改了什么、REFACTOR 做了什么
- **变更文件用列表**：一个文件一行，附带一句话改动说明
- 如果 verify_by == unit_test：必须包含验收标准覆盖表（标准 → 测试函数）
- 如果 verify_by == qualitative：implementing 阶段只写草稿——最终结论留给 verifying 阶段
- 如果 verify_by == rwp：记录工作流名和观察到的输出路径，不在这里做最终结论

## 要点

- 先让测试失败，再写实现——不要跳过 RED
- evidence.md 只写事实，不写评价
- 如果验证失败且不是代码问题，回到 `verification_design.md` 修正验证策略
- 并行调度是横切策略，可在本阶段自行选择使用
- 不要等全部实现完成再补 evidence.md——每轮循环写完立即追加
