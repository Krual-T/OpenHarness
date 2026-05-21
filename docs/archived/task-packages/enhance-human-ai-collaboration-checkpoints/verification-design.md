# 验证策略

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 验证路径

- **计划路径**：qualitative 双轨审核——先由子 Agent 逐项审核四个 skill 文件的改动是否满足审核矩阵，再由人类审阅者对子 Agent 结论逐项确认。
- **回退路径**：如果子 Agent 审核发现某项不通过，回到 `implementing` 修正对应文件的改动，修正后重新验证。如果审核矩阵某项判定准则本身有歧义导致双方结论分歧，回到 `verification_designing` 收紧准则。
- **路径说明**：grep 命令覆盖了停点存在性、术语统一等可自动检查的维度；审核矩阵覆盖了语义正确性（停点措辞是否清晰、res_review_mode 分支控制是否正确），两者互补。路径足够。

## 审核矩阵

### 审核对象

四个文件：

1. `skills/using-openharness/states/exploring-solution-space/SKILL.md`
2. `skills/using-openharness/states/detailed-design/SKILL.md`
3. `skills/using-openharness/states/verification-designing/SKILL.md`
4. `skills/using-openharness/states/verifying/SKILL.md`

### 审核维度和判定准则

| 维度 | 判定准则 | 判定方式 |
|------|---------|---------|
| D1. 停点存在性 | 文件 1、2 的 `## 逐项设计确认` 章节第一句包含 `必须逐项确认设计`（非 `建议`） | grep + 语义确认 |
| D2. 分支控制 | 文件 1、2 的停点强制表述受 `design_review_mode` 分支控制：`stepwise` 时为 `必须`，`auto` 时为 `保持为可选` | 语义确认 |
| D3. 多方案显式展示 | 文件 1 的步骤 4 之后有 "列出候选+各自取舍，不得默不作声地选一个" 或等效表述 | grep |
| D4. 接口多选一显式展示 | 文件 2 的步骤 3 接口精度之后有 "列出选项+各自代价，不得默不作声地选一个" 或等效表述 | grep |
| D5. 验证策略确认停点 | 文件 3 存在 `## 验证策略确认停点` 章节，内容包含验证命令清单 + 覆盖矩阵 + 不覆盖风险和接受理由的展示要求 | grep + 语义确认 |
| D6. 验证结论确认停点 | 文件 4 存在 `## 验证结论确认停点` 章节，内容包含最终结论展示和用户确认要求 | grep + 语义确认 |
| D7. 循环验证 | 文件 4 的验证结论确认停点章节包含 "明确本轮验证的增量目标" 或等效表述 | grep |
| D8. 可选提前验证 | 文件 3 的验证策略确认停点章节包含 `[可选]` 标记的提前跑验证命令的建议 | grep |
| D9. 术语统一 | 四个文件中 `Exit Check` 标题均不存在；`## 阶段结束检查` 标题均存在 | grep |
| D10. 阶段结束检查证据引用 | 文件 1 的阶段结束检查要求引用 `overview-design.md` 章节号；文件 2 的阶段结束检查要求引用文件路径、接口签名、数据结构 | 语义确认 |
| D11. 不引入外部标签 | 四个文件中不出现 "准则 #1""准则 #4""Karpathy" 字样 | grep |

### 逐文件审核覆盖

| 审核维度 | 文件1 | 文件2 | 文件3 | 文件4 |
|---------|-------|-------|-------|-------|
| D1. 停点存在性 | ✓ | ✓ | — | — |
| D2. 分支控制 | ✓ | ✓ | — | — |
| D3. 多方案显式展示 | ✓ | — | — | — |
| D4. 接口多选一显式展示 | — | ✓ | — | — |
| D5. 验证策略确认停点 | — | — | ✓ | — |
| D6. 验证结论确认停点 | — | — | — | ✓ |
| D7. 循环验证 | — | — | — | ✓ |
| D8. 可选提前验证 | — | — | ✓ | — |
| D9. 术语统一 | ✓ | ✓ | ✓ | ✓ |
| D10. 证据引用 | ✓ | ✓ | — | — |
| D11. 不引入外部标签 | ✓ | ✓ | ✓ | ✓ |

## 必需命令

定性审核的判定命令（grep 用于客观维度，语义确认用于主观维度）：

```bash
# D1 + D2: 停点存在性和分支控制（文件 1）
grep -n "必须逐项确认设计" skills/using-openharness/states/exploring-solution-space/SKILL.md
grep -n "design_review_mode: auto" skills/using-openharness/states/exploring-solution-space/SKILL.md

# D1 + D2: 停点存在性和分支控制（文件 2）
grep -n "必须逐项确认设计" skills/using-openharness/states/detailed-design/SKILL.md
grep -n "design_review_mode: auto" skills/using-openharness/states/detailed-design/SKILL.md

# D3: 多方案显式展示（文件 1）
grep -n "不得默不作声地选一个" skills/using-openharness/states/exploring-solution-space/SKILL.md

# D4: 接口多选一显式展示（文件 2）
grep -n "不得默不作声地选一个" skills/using-openharness/states/detailed-design/SKILL.md

# D5: 验证策略确认停点（文件 3）
grep -n "验证策略确认停点" skills/using-openharness/states/verification-designing/SKILL.md

# D6 + D7: 验证结论确认停点 + 循环验证（文件 4）
grep -n "验证结论确认停点" skills/using-openharness/states/verifying/SKILL.md
grep -n "增量目标" skills/using-openharness/states/verifying/SKILL.md

# D8: 可选提前验证（文件 3）
grep -n "可选" skills/using-openharness/states/verification-designing/SKILL.md

# D9: 术语统一（四个文件）
grep -rn "Exit Check" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# 期望：零结果
grep -rn "阶段结束检查" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# 期望：每文件至少一次匹配

# D11: 不引入外部标签（四个文件）
grep -rn "准则.*#1\|准则.*#4\|Karpathy" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# 期望：零结果
```

D10（证据引用）为语义确认维度，由子 Agent 和人类审阅者阅读对应章节原文后判断。

## 预期结果

| 维度 | 预期结果 |
|------|---------|
| D1 | 文件 1、2 的逐项设计确认章节首句含 `必须`，而非 `建议` |
| D2 | `design_review_mode: auto` 附近有 `可选` 或等效表述 |
| D3 | 文件 1 步骤 4 后有 `不得默不作声地选一个` |
| D4 | 文件 2 步骤 3 后有 `不得默不作声地选一个` |
| D5 | 文件 3 中有 `## 验证策略确认停点`，含命令清单+覆盖矩阵+风险接受 |
| D6 | 文件 4 中有 `## 验证结论确认停点`，含最终结论展示和用户确认要求 |
| D7 | 文件 4 中有 `增量目标` |
| D8 | 文件 3 中有 `[可选]` 标记 |
| D9 | `Exit Check` 零匹配；`## 阶段结束检查` 四文件均有匹配 |
| D10 | 文件 1 的阶段结束检查提到 `章节号`；文件 2 的阶段结束检查提到 `文件路径`/`接口签名`/`数据结构` |
| D11 | `准则 #1`/`准则 #4`/`Karpathy` 零匹配 |

## 可追溯性

| 需求 | 验证维度 |
|------|---------|
| 1. exploring-solution-space 增强 | D1, D2, D3, D9, D10, D11 |
| 2. detailed-design 增强 | D1, D2, D4, D9, D10, D11 |
| 3. verification-designing 增强 | D5, D8, D9, D11 |
| 4. verifying 增强 | D6, D7, D9, D11 |
| 5. 术语统一 | D9 |

所有 5 项必须交付的结果均有对应的验证维度。无缺口。

## 风险接受

| 风险 | 接受理由 |
|------|---------|
| grep 命令无法验证 "停点措辞是否清晰、AI 是否会误解" | 由 qualitative 双轨审核的语义确认维度覆盖（D2, D5, D6, D10 均需人类审阅者确认） |
| 改动后 skill 在实际对话中的效果无法在验证阶段测试 | 本轮 skill 改动是协议级别，效果验证需要实际执行任务包才能观测。后续可通过使用新 skill 的任务包反馈收集改进信号 |
| `design_review_mode` 字段缺失时停点行为未定义 | 由 requirements gate（`_check_requirements_gate`）保证字段一定存在，不会出现此场景 |

## 验证执行计划

- **执行时机**：implementing 阶段完成四个文件改动后，立即在 verifying 阶段执行
- **执行者**：子 Agent（`subagent_type: general-purpose`）逐项审核 + 人类审阅者逐项确认
- **执行环境**：无特殊环境要求；grep 命令在仓库根目录执行即可
