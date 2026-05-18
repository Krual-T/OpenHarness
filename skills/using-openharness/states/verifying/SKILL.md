---
name: verifying
description: 当任务状态是 verifying（执行验证、收集证据）时由 CLI 自动注入
---

# 执行验证

## 何时使用

实现已完成，需要执行验证并收集证据。

## 步骤

1. **执行验证命令**：运行 `verification-design.md` 中声明的全部验证命令
2. **判断结果**：逐条对比期望退出码 vs 实际退出码和输出
3. **处理失败**：见下方"验证失败处理"
4. **补充 evidence.md**：
   - 补充实际执行的命令和结果
   - 补充验收标准覆盖表
   - 标记残余风险和延后事项
5. **自检 Exit Check**

完成后：`openharness task-package transition <task> verified`

（`verified` 是 gate 状态，CLI 检查 evidence.md 存在且非空后自动归档）

## 验证失败处理

不是所有失败都意味着"回去改代码"。按失败原因分流：

| 失败类型 | 判定 | 动作 |
|---------|------|------|
| 命令执行报错（找不到文件、权限拒绝、环境变量缺失） | 验证环境问题，非代码问题 | 修复环境后重新执行 |
| 退出码与期望不符（期望 0，实际 1） | 代码未通过验证 | 回到 `implementing` 修复代码 |
| 输出内容与预期不符，但退出码为 0 | 验证命令不够精确——期望输出写得太宽 | 回到 `verification-design.md` 收紧期望输出 |
| rwp 脚本超时或挂起 | 工作流脚本有资源泄漏或死循环 | 回到 `implementing`，同时检查工作流脚本自身的 bug |
| qualitative 审核结论模糊（"差不多""基本可以"） | 审核判定准则不够具体 | 回到 `verification-design.md` 补充判定准则 |

**关键约束**：不要看到失败就自动跳回 implementing。先判断失败属于代码问题、环境问题还是验证策略问题——三者回退路径不同。

## evidence.md 完整性检查

在 transition 到 verified 之前，evidence.md 必须包含以下内容（按 verify_by）：

**unit_test**：
- [ ] 每条验证命令的实际执行结果（命令、退出码、输出摘要）
- [ ] 变更文件清单（一个文件一行，附带改动说明）
- [ ] 验收标准覆盖表（每条标准 → 对应测试函数名 → 结果）
- [ ] 残余风险（本轮未覆盖的边界 + 接受理由）

**qualitative**：
- [ ] 审核对象列表（文件路径 + 审核维度）
- [ ] 每项发现（问题描述 + 严重程度 + 是否闭合）
- [ ] 最终结论（通过 / 有条件通过 / 不通过）
- [ ] 未闭合问题的 follow-up 计划

**rwp**：
- [ ] 工作流名称和调用命令
- [ ] stdout 中的结构化输出（不要截断或改写）
- [ ] stderr 是否有异常日志
- [ ] 产物路径（输出文件、日志、截图等）
- [ ] 盲区说明（工作流无法覆盖的场景 + 为什么可接受）

如果 checklist 有缺项，先补充再 transition。

## Exit Check

1. 所有验证命令是否已执行？
2. evidence.md 是否包含了实际运行的命令和结果？
3. 验收标准是否全部有对应的证据覆盖？
4. 是否有验证失败的条目？如果有，是否已分流到正确的回退路径？

全部能回答 → `openharness task-package transition <task> verified`

## 要点

- verifying 阶段不是"跑一遍测试就过"——必须逐条对比期望退出码和实际输出
- evidence.md 的 checklist 是硬门禁：缺一项就不能 transition
- 验证失败时先诊断再跳转，不要默认回到 implementing

## 常见失败模式

- 跳过验证命令直接写 evidence.md——evidence 必须基于实际执行结果
- verification-design.md 中声明了 N 条命令，但 verifying 只跑了 N-1 条——遗漏的命令不声不响
- rwp 工作流执行后只看了 stdout，忽略了 stderr 中的异常日志
- qualitative 审核写成"代码看起来不错"——没有任何判定准则可对照
- 验证失败后直接改代码而不先判断失败根因，导致反复 RED-GREEN 空转
