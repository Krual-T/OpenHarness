# 总体设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 系统边界

### 覆盖

- `skills/using-openharness/states/implementing/SKILL.md` — 端到端重写，以 Karpathy 四项准则为主干章节
- Goal-Driven Execution 按 `verify_by` 三分支：`unit_test` 走 TDD 循环、`qualitative` 对照审核矩阵逐项写、`rwp` 运行工作流观察输出
- 新增章节：入口分流、evidence.md 文档审阅停点、项目工具命令参考、重入指南、反合理化、常见失败模式、与相邻文档边界

### 不覆盖

- 其他五个阶段技能（brainstorming、exploring-solution-space、detailed-design、verification-designing、verifying）— 不做任何修改
- CLI 状态机（`openharness_cli/workflows.py`、`openharness_cli/models/task_status.py`）— 不涉及
- `evidence.md` 模板文件（`skills/using-openharness/references/templates/task-package.evidence.md`）— 模板本身不改
- `verifying/SKILL.md` 中关于 evidence.md 最终结论的指令 — 不做调整
- 任何 Python 源码、测试文件、workflow 定义

## 推荐结构

### 文件落点

单文件改动：`skills/using-openharness/states/implementing/SKILL.md`

### 章节结构

```
1. 入口分流 — 首次进入 vs 从 verifying 回退
2. Think Before Coding — 写代码前先理解
3. Simplicity First — 最小代码解决问题
4. Surgical Changes — 只碰必须改的
5. Goal-Driven Execution — 按 verify_by 三分支执行循环
6. 完成后 — evidence.md 中间事实记录
7. evidence.md 文档审阅停点 — 人机协同确认
8. 阶段结束检查 — 退出条件
9. 项目工具命令参考 — uv run pytest / ruff / pyright
10. 重入指南 — 从 verifying 回退的增量流程
11. 要点 — 核心约束和豁免
12. 与相邻文档的边界 — 写什么 vs 不写什么
13. 常见失败模式 — 编码行为 + TDD 故障
14. 反合理化 — 常见借口和反驳
```

### 各章节职责

| 章节 | 职责 | 对标 |
|------|------|------|
| 入口分流 | 判断场景，分流到完整流程或增量修复 | brainstorming 的入口分流 |
| Think Before Coding | 陈述假设、暴露歧义、不确定时主动问 | Karpathy #1 |
| Simplicity First | 最少代码、不做请求之外的抽象 | Karpathy #2 |
| Surgical Changes | 只碰必须改的、匹配现有风格、清理自己的遗留 | Karpathy #3 |
| Goal-Driven Execution | 按 verify_by 分流：unit_test 走 TDD（RED→GREEN→REFACTOR）、qualitative 对照审核矩阵逐项写、rwp 运行工作流 | Karpathy #4 + 现有 TDD |
| 完成后 | 写 evidence.md 中间事实（文件名、命令、退出码、输出摘要） | 现有完成后逻辑 |
| 文档审阅停点 | 告知路径→用户审阅→确认后 transition | 其他阶段的文档审阅停点 |
| 阶段结束检查 | 可判定退出条件列表，按 verify_by 区分检查项 | 其他阶段的 Exit Check |
| 项目工具命令参考 | `uv run pytest`、`uv run ruff check`、`uv run pyright` | 新增，当前缺失 |
| 重入指南 | 从 verifying 回退时的增量目标声明 | 其他阶段的重入指南 |
| 要点 | 核心约束摘要，verify_by 相关约束分列 | 其他阶段的要点 |
| 与相邻文档边界 | implementing vs verification-designing vs verifying | 其他阶段的边界章节 |
| 常见失败模式 | 编码行为失败（过度抽象、擅自重构无关代码）+ 按 verify_by 的验证循环故障（照搬 TDD 到定性任务等） | 其他阶段的常见失败模式 |
| 反合理化 | 借口 + 不成立理由 | 其他阶段的反合理化 |

## 关键流程

### 主路径

```
入口分流
  ├─ 首次进入 → Think Before Coding → Simplicity First
  │                → Surgical Changes → Goal-Driven Execution
  │                │   ├─ unit_test: TDD（RED → GREEN → REFACTOR）
  │                │   ├─ qualitative: 对照审核矩阵逐项写 → 自检 → 修正
  │                │   └─ rwp: 修改 → 运行工作流 → 观察输出 → 修正
  │                → 完成后（写 evidence.md 中间事实）
  │                → 文档审阅停点（用户确认）
  │                → 阶段结束检查 → transition implemented
  └─ 从 verifying 回退 → 声明增量目标
                           → Goal-Driven Execution（仅验证失败项 + 已有项不退化）
                           → 完成后（追加 evidence.md）
                           → 文档审阅停点 → 阶段结束检查 → transition implemented
```

### 失败信号

- Think Before Coding 阶段：发现假设不成立或需求有歧义 → 阻塞，向用户提问。不排除回退到 requirements.md
- Goal-Driven Execution 阶段（unit_test）：RED 失败 + 非被测代码问题 → 回退到 verification-designing。GREEN 多次循环不通过 → 回退到 detailed-designing 或 requirements.md
- Goal-Driven Execution 阶段（qualitative/rwp）：对照审核矩阵/工作流输出多次修正仍不满足 → 检查判定标准是否合理，必要时回退到 verification-designing
- 文档审阅停点：用户否定 → 回到对应步骤修正

## 阶段门禁

进入 detailed_designing 前必须确定：

1. 14 个章节的结构和职责分配已定稿，与用户确认
2. 四项 Karpathy 准则的内容边界已明确 — 每项准则写什么行为指令、不写什么
3. evidence.md 中间事实的记录格式已明确 — 命令、退出码、输出摘要、变更文件列表
4. 项目工具命令清单已确认 — `uv run pytest`、`uv run ruff check`、`uv run pyright` 等
5. 与其他阶段技能的边界声明已对齐 — 不会出现 implementing 和 verifying 对同一件事给出矛盾指令

## 取舍

### 推荐方案收益

- 四项准则作为顶层骨架，agent 进入 implementing 后按"先理解→写最简→只改该改的→循环验证"的顺序推进
- 与其他五个阶段技能章节结构一致，agent 跨阶段切换时认知负担低
- 单文件改动，无跨文件依赖

### 代价

- 放弃现有 SKILL.md 的全部内容，但不损失逻辑（TDD 循环、evidence.md 写法约束均保留融入）
- 文件长度预计从 70 行增加到约 150-200 行，但与其他阶段技能体量对齐（brainstorming 129 行、detailed-design 114 行）

### 备选方案及不选理由

**方案 B：保持现有结构，在"要点"章节追加 Karpathy 准则摘要**

- 不选理由：准则变成要点中的几条抽象建议，无法形成可操作的步骤级指令。agent 读完后仍然不知道"怎么做"。

**方案 C：Karpathy 准则写入独立 `references/karpathy-guidelines.md`，implementing SKILL.md 只引用**

- 不选理由：引导碎片化。implementing 阶段 agent 需要在一个地方看到全部行为指令，跨文件引用增加遗漏概率。Karpathy 准则原始文件有 MIT 许可，翻译融入不涉及合规问题。

## 推荐图示

本轮改动不涉及多模块交互或复杂数据流，无需图示。14 章节的线性结构已充分表达设计意图。

## 总体设计反思

| 挑战 | 结论 | 理由 |
|------|------|------|
| Karpathy 四项准则是否全部适用于 implementing 阶段？ | 全部接受 | Think Before Coding 解决"没理解就写"，Simplicity First 解决"过度抽象"，Surgical Changes 解决"顺手重构"，Goal-Driven Execution 解决"目标与验证脱节"——四项各自对应一个 implementing 阶段的真实失败模式 |
| TDD 循环（RED→GREEN→REFACTOR）是否适用于所有 verify_by？ | 不适用，按 verify_by 分流 | `unit_test` 走完整 TDD；`qualitative` 无测试可跑，循环变为"对照审核矩阵逐项写→自检→修正"；`rwp` 循环变为"修改→运行工作流→观察输出→修正"。要点中"先让测试失败"仅对 unit_test 生效 |
| 项目工具命令是否应该放在 implementing 技能中？ | 接受 | 当前 agent 不知道用什么命令跑测试，这是明确的缺口。放在 implementing 中是因为测试/检查/格式化都在本阶段高频使用 |
