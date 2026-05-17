---
name: verifying
description: 当任务状态是 verifying（执行验证、收集证据）时由 CLI 自动注入
---

# 执行验证

## 何时使用

实现已完成，需要执行验证并收集证据。

## 步骤

1. **执行验证命令**：运行 `verification_design.md` 中声明的全部验证命令
2. **检查结果**：确认退出码、输出是否符合预期
3. **补充 evidence.md**：如果 implementing 阶段已写 evidence.md，检查是否需要补充
   - 补充实际执行的命令和结果
   - 补充验收标准覆盖表
   - 标记残余风险和延后事项
4. **自检**：evidence.md 是否包含所有必要信息

完成后：`openharness transition <task> verified`

（`verified` 是 gate 状态，CLI 检查 evidence.md 存在且非空后自动归档）

## Exit Check

1. 所有验证命令是否已执行？
2. evidence.md 是否包含了实际运行的命令和结果？
3. 验收标准是否全部有对应的证据覆盖？

全部能回答 → `openharness transition <task> verified`
