# 验证证据

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 文件

| 文件 | 改动说明 |
|------|---------|
| `skills/using-openharness/states/exploring-solution-space/SKILL.md` | 逐项设计确认改强制+分支控制、多方案显式展示、新增文档审阅停点、Exit Check → 阶段结束检查+章节号证据引用 |
| `skills/using-openharness/states/detailed-design/SKILL.md` | 逐项设计确认改强制+分支控制、接口多选一显式展示、新增阶段结束检查确认清单、Exit Check → 阶段结束检查+产物证据引用 |
| `skills/using-openharness/states/verification-designing/SKILL.md` | 新增验证策略确认停点章节、可选提前验证 RED、Exit Check → 阶段结束检查 |
| `skills/using-openharness/states/verifying/SKILL.md` | 新增验证结论确认停点章节、循环验证增量目标、Exit Check → 阶段结束检查 |

## 语义审核

### D1-D11 审核命令执行结果

以下在 implementing 阶段 GREEN 后执行：

```bash
# D1+D2: 停点存在性和分支控制
grep -n "必须逐项确认设计" skills/using-openharness/states/exploring-solution-space/SKILL.md
# 37:对于非 `mechanical` 任务且 `design_review_mode: stepwise`，必须逐项确认设计。...
grep -n "design_review_mode: auto.*可选" skills/using-openharness/states/exploring-solution-space/SKILL.md
# 37:...`design_review_mode: auto` 时保持为可选。

grep -n "必须逐项确认设计" skills/using-openharness/states/detailed-design/SKILL.md
# 28:对于非 `mechanical` 任务且 `design_review_mode: stepwise`，必须逐项确认设计。...
grep -n "design_review_mode: auto.*可选" skills/using-openharness/states/detailed-design/SKILL.md
# 28:...`design_review_mode: auto` 时保持为可选。

# D3: 多方案显式展示
grep -n "不得默不作声地选一个" skills/using-openharness/states/exploring-solution-space/SKILL.md
# 14:   - 如果存在多个可行方向，必须列出候选+各自取舍，不得默不作声地选一个...

# D4: 接口多选一显式展示
grep -n "不得默不作声地选一个" skills/using-openharness/states/detailed-design/SKILL.md
# 13:   - 接口精度...如果接口精度存在多个合理选择...必须列出选项+各自代价，不得默不作声地选一个

# D5: 验证策略确认停点
grep -n "验证策略确认停点" skills/using-openharness/states/verification-designing/SKILL.md
# 23:## 验证策略确认停点

# D6: 验证结论确认停点
grep -n "验证结论确认停点" skills/using-openharness/states/verifying/SKILL.md
# 42:## 验证结论确认停点

# D7: 循环验证
grep -n "增量目标" skills/using-openharness/states/verifying/SKILL.md
# 46:回退修复后重新进入 verifying 时，先明确本轮验证的增量目标...

# D8: 可选提前验证
grep -n "\[可选\]" skills/using-openharness/states/verification-designing/SKILL.md
# 33:[可选] 在设计阶段就跑一次验证命令确认能正确失败...

# D9: Exit Check 残留（期望：零匹配）
grep -rn "Exit Check" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# exit: 1 (零匹配)

# D9: 阶段结束检查存在（期望：四文件均有匹配）
grep -rn "阶段结束检查" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# exploring-solution-space:22:## 阶段结束检查
# detailed-design:60:## 阶段结束检查
# verification-designing:21:4. **自检 阶段结束检查**
# verification-designing:35:## 阶段结束检查
# verifying:22:6. **自检 阶段结束检查**
# verifying:74:## 阶段结束检查

# D10: 证据引用（文件1）
grep -n "章节号" skills/using-openharness/states/exploring-solution-space/SKILL.md
# 24:...每项答案必须引用 `overview-design.md` 的具体章节号作为证据...

# D10: 证据引用（文件2）
grep -n "文件路径.接口签名.数据结构" skills/using-openharness/states/detailed-design/SKILL.md
# 60:...每项答案必须引用具体产物——文件路径、接口签名、数据结构定义——作为证据...

# D11: 外部标签（期望：零匹配）
grep -rn "准则.*#1\|准则.*#4\|Karpathy" skills/using-openharness/states/exploring-solution-space/SKILL.md skills/using-openharness/states/detailed-design/SKILL.md skills/using-openharness/states/verification-designing/SKILL.md skills/using-openharness/states/verifying/SKILL.md
# exit: 1 (零匹配)

# D12: 文档审阅停点（文件1）
grep -n "文档审阅停点" skills/using-openharness/states/exploring-solution-space/SKILL.md
# 22:## 文档审阅停点

# D13: 确认清单停点（文件2）
grep -n "确认清单" skills/using-openharness/states/detailed-design/SKILL.md
# 72:自检通过后，将 7 条答案整理为确认清单...
```

## 验收标准覆盖表

| 需求 | 验证维度 | 结果 |
|------|---------|------|
| 1. exploring-solution-space 增强 | D1, D2, D3, D9, D10, D11, D12 | 全部通过 |
| 2. detailed-design 增强 | D1, D2, D4, D9, D10, D11, D13 | 全部通过 |
| 3. verification-designing 增强 | D5, D8, D9, D11 | 全部通过 |
| 4. verifying 增强 | D6, D7, D9, D11 | 全部通过 |
| 5. 术语统一 | D9 | 全部通过 |

## 语义审核

### 子 Agent 审核

子 Agent 按 11 维审核矩阵逐项审核，全部 11 维通过，无不符合项。

### 人类审阅者反馈

用户逐项确认全部 11 维通过，无异议。随后用户指令新增 D12（文档审阅停点）和 D13（确认清单停点），两处改动已实施且 grep 验证通过。

### 审核综合结论

子 Agent 与人类审阅者无分歧，全部 13 维通过。

## 验证结果

**通过。**

- 四个阶段 skill 文件均已有至少一个强制性停点（非 `mechanical` 下）
- `Exit Check` 全部替换为 `阶段结束检查`
- 无外部标签（Karpathy 准则 #1/#4）引入
- 文档审阅停点为强制（不受 auto 模式影响）

## 残余风险

| 风险 | 接受理由 |
|------|---------|
| 停点在新 skill 指令下的实际执行效果尚待观测 | 后续使用这些 skill 的任务包将自然验证停点是否到位 |
| `detailed-design` 目录命名与 `detailed_designing` 状态枚举不一致 | 属于独立的重命名任务，不影响本轮功能 |
