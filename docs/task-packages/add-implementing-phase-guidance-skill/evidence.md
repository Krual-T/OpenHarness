# 证据

## 变更文件

- `skills/using-openharness/states/implementing/SKILL.md` — 端到端重写：以 Karpathy 四项准则为主干章节（Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution），按 verify_by 三分支，补齐入口分流、证据审阅停点、工具命令参考、重入指南、相邻文档边界、常见失败模式、反合理化等标准章节。verifying 阶段反馈后修正三处：rwp 增加 unit_test 前置步骤并收窄边界到退出码+stderr、完成后 rwp 描述同步、阶段结束检查 rwp 增加单元测试项
- `skills/using-openharness/states/verification-designing/SKILL.md` — 要点新增一条：三阶段闭环呼应（设计验证 → 执行验证 → 判定验证）
- `skills/using-openharness/states/verifying/SKILL.md` — 开头新增职责声明：implementing 已记录中间结果，verifying 职责是判定正确性

## 语义审核

implementing 阶段完整性确认：对照 `verification-design.md` 中的 16 条审核矩阵，确认所有审核对象已写完、内容非空。

审核对象覆盖：
- #1-5: 入口分流 + 四项 Karpathy 准则可操作性和分支正确性 — 已写完
- #6-8: evidence.md 中间事实、审阅停点、阶段结束检查 — 已写完
- #9-10: 工具命令、重入指南 — 已写完
- #11-12: 要点 verify_by 标注、相邻文档边界 — 已写完
- #13-14: 常见失败模式 9 条、反合理化 6 条 — 已写完
- #15-16: 结构一致性、语言规则 — 已写完

中间发现：所有章节按 detailed-design 的设计内容写入，14 个章节齐全，内容非空。正确性判定留给 verifying 阶段。
