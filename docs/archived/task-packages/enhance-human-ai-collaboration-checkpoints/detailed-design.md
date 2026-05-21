# 详细设计

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 可观察性与验证准备

- **验证路径**：qualitative——子 Agent + 人类审阅者双轨审核四个 skill 文件的改动是否正确
- **降级路径**：如果 qualitative 双轨审核发现某个停点的表述有歧义，回退到 `detailed_designing` 修正对应文件的接口描述
- **预期证据**：
  - 四个 skill 文件中 `grep "停点"` 均返回结果（停点标记存在）
  - 四个 skill 文件中 `grep "Exit Check"` 均返回零结果（术语统一完成）
  - 四个 skill 文件中 `## 阶段结束检查` 均存在
  - exploring-solution-space 和 detailed-design 的逐项设计确认章节中 `必须` 替代了 `建议`（且受 `design_review_mode` 分支控制）
  - verification-designing 中存在 `验证策略确认停点`
  - verifying 中存在 `验证结论确认停点`

## 新增或修改文件

| 文件 | 变更说明 |
|------|---------|
| `skills/using-openharness/states/exploring-solution-space/SKILL.md` | 逐项设计确认改强制+分支控制、多方案显式展示、Exit Check 改为阶段结束检查+证据引用 |
| `skills/using-openharness/states/detailed-design/SKILL.md` | 逐项设计确认改强制+分支控制、接口多选一显式展示、Exit Check 改为阶段结束检查+产物引用 |
| `skills/using-openharness/states/verification-designing/SKILL.md` | 新增验证策略确认停点、可选提前验证 RED、Exit Check 改为阶段结束检查 |
| `skills/using-openharness/states/verifying/SKILL.md` | 新增验证结论确认停点、循环验证增量目标、Exit Check 改为阶段结束检查 |

## 接口

### exploring-solution-space/SKILL.md

改动接口（在现有章节内修改，不新增章节）：

**位置 1：`## 逐项设计确认` 章节第一段**

旧：
```
对于非 `mechanical` 任务，建议逐项确认设计：
```

新：
```
对于非 `mechanical` 任务且 `design_review_mode: stepwise`，必须逐项确认设计。
架构级决策（边界、主路径、推荐结构）至少有一个停点，在写完这三节后先让用户确认方向，再补其他章节。
`design_review_mode: auto` 时保持为可选。
```

**位置 2：`## 步骤` 章节，步骤 4 之后插入**

在步骤 4"总结本地约束、可行选项和推荐方向"之后，步骤 5 之前，插入：

```
如果存在多个可行方向，必须列出候选+各自取舍，不得默不作声地选一个。将此展示作为第一个逐项设计确认停点。
```

**位置 3：`## Exit Check` 标题**

```
- ## Exit Check
+ ## 阶段结束检查
```

**位置 4：阶段结束检查的前导段落**

在"离开 overview 阶段前..."之后、"1. 这轮设计..."之前，增加：

```
（每项答案必须引用 `overview-design.md` 的具体章节号作为证据，不能只答"是"或"否"）
```

### detailed-design/SKILL.md

改动接口（在现有章节内修改，不新增章节）：

**位置 1：`## 逐项设计确认` 章节第一段**

旧：
```
对于非 `mechanical` 任务，建议逐项确认设计：
```

新：
```
对于非 `mechanical` 任务且 `design_review_mode: stepwise`，必须逐项确认设计。
接口精度决策至少有一个停点，`design_review_mode: auto` 时保持为可选。
```

**位置 2：`## 步骤` 章节，步骤 3"接口精度"子项之后插入**

```
如果接口精度存在多个合理选择（参数传标识还是传对象、错误是抛异常还是返回 Result 类型、同步还是异步），必须列出选项+各自代价，不得默不作声地选一个。
```

**位置 3：`## Exit Check` 标题**

```
- ## Exit Check
+ ## 阶段结束检查
```

**位置 4：阶段结束检查的前导段落**

```
（每项答案必须引用具体产物——文件路径、接口签名、数据结构定义——作为证据，不能只答"是"或"否"）
```

### verification-designing/SKILL.md

改动接口（新增一个章节 + 修改标题）：

**位置 1：在 `## Exit Check` 之前，插入新章节：**

```markdown
## 验证策略确认停点

写完 `verification-design.md` 后，必须向用户展示：

- 验证命令清单（可复制粘贴执行的命令）
- 覆盖矩阵（每项验收标准 → 对应验证命令）
- 本轮不覆盖的风险和接受理由

获得用户确认后才可 transition。用户否定 → 修正验证策略。

[可选] 在设计阶段就跑一次验证命令确认能正确失败，提前暴露验证策略自身的 bug。
```

**位置 2：`## Exit Check` 标题**

```
- ## Exit Check
+ ## 阶段结束检查
```

### verifying/SKILL.md

改动接口（新增一个章节 + 修改标题）：

**位置 1：在 `## evidence.md 完整性检查` 之前，插入新章节：**

```markdown
## 验证结论确认停点

`evidence.md` 写完最终结论（通过/有条件通过/不通过 + 残余风险清单）后，必须向用户展示并获确认后才可 transition。

回退修复后重新进入 verifying 时，先明确本轮验证的增量目标（"上次失败的是 X，本轮只验证 X 是否修复 + 已有通过的 Y 不退化"），再执行验证命令。
```

**位置 2：`## Exit Check` 标题**

```
- ## Exit Check
+ ## 阶段结束检查
```

## 模块内部设计

无内部模块——四个文件各自独立，改动模式统一但不共享状态。每个文件的改动职责：

```
exploring-solution-space/SKILL.md  — 负责方案探索阶段的人机停点
detailed-design/SKILL.md           — 负责详细设计阶段的人机停点
verification-designing/SKILL.md    — 负责验证策略设计的确认停点
verifying/SKILL.md                 — 负责验证执行的结论确认停点
```

每个改动在各自文件内自封闭：改动的接口均在本文件现有章节内部或之后，不影响相邻章节的职责边界（要点、边界、失败模式、反合理化均不动）。

## 数据语义

本轮无新增数据结���。关键语义约定：

| 术语 | 语义 |
|------|------|
| 停点 | 在 skill 步骤中的强制性人机交互节点，标注"必须向用户展示 X，获得确认后才继续" |
| 阶段结束检查 | 原名 Exit Check，退出当前阶段前的自检清单 |
| `design_review_mode: stepwise` | 逐项设计确认为强制 |
| `design_review_mode: auto` | 逐项设计确认为可选，AI 自主推进 |

## 阶段门禁

进入 `implementing` 前必须确定：

1. 四个文件的改动接口（精确到行）已明确
2. 术语统一方案（`Exit Check` → `阶段结束检查`）已确认
3. `design_review_mode` 对停点强制性的分支控制逻辑已明确
4. verification-designing 和 verifying 的新增章节（"验证策略确认停点""验证结论确认停点"）内容已确认

## 决策闭合

| 挑战 | 结论 | 理由 |
|------|------|------|
| 停点是否做成 CLI 硬门禁 | 拒绝 | CLI 无法感知聊天层面的"用户确认"，过度工程 |
| 准则 #2/#3 是否一起落地 | 延期 | 属于 implementing 阶段关注点，应放入 TASK-021 |
| verification-designing 提前跑验证命令是否强制 | 接受为可选 | 环境差异大，不能假设设计阶段就能执行验证命令 |
| 要不要在 skill 文件中标注"准则 #1""准则 #4"等来源 | 拒绝 | 不应引入外部标签，行为落地为 OpenHarness 原生指令 |
| 要不要改 `references/templates/` 下的模板标题 | 拒绝 | 模板标题独立于 skill 文件，本轮不涉及 |

## 错误处理

| 风险 | 处理 |
|------|------|
| implementation 阶段 AI 误解停点位置 | 防范：detailed-design 中已指定精确的插入位置（章节名+上下文），不需 AI 自行判断 |
| 改动后章节编号偏移 | 风险低——所有改动均在现有章节内部或之前插入，不删除、不重排章节 |
| `design_review_mode` 字段缺失 | 由 requirements gate 保证（`_check_requirements_gate`），已在 brainstorming 阶段强制确认 |
| auto 模式下 AI 误将停点视为强制 | 防范：每个停点明确标注 `design_review_mode: auto 时保持为可选` |

## 迁移说明

改动均在一个 commit 内完成，切换点为 commit 合并的时间点。实施顺序：

1. exploring-solution-space/SKILL.md
2. detailed-design/SKILL.md
3. verification-designing/SKILL.md
4. verifying/SKILL.md

顺序无关（文件独立），但统一在一个 commit 内提交。回滚：`git revert` 即可。

无兼容性风险——所有改动都是 skill 指令文本，CLI 层无变更，现有任务包不受影响。

## 推荐图示

不需要 PlantUML 图。四个文件的改动模式统一且结构简单，文字描述已足够精读到行。

## 详细设计反思

- **验证策略**：qualitative 双轨审核可以逐项对照"预期证据"中的 6 条 grep 检查项——每项是可判定的事实，不是主观评价
- **接口边界**：所有改动精确到行和上下文，implementation 阶段 AI 不需要自行判断插入位置，降低了误改风险
- **迁移顺序**：四个文件独立改动，无依赖关系，顺序无关。单 commit 提交使回滚简单
- **预期证据**：6 条 grep 可判定项覆盖了停点存在性、术语统一和分支控制三大改动维度，足够判断改动是否到位
