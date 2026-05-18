# OpenHarness 理想流程逐步演绎与优化

> 以"新增 `openharness status` 命令"为具体案例，从 Agent 收到用户请求开始，逐步演绎完整流程。每个节点暂停，发现问题即讨论修正，直到任务归档。

---

## 场景

用户对 Agent 说：

> 加一个 `openharness status` 命令，显示所有活跃任务包及其当前状态、owner、更新时间。

不涉及跨模块契约、不改变状态模型、改动范围明确。

---

## 第 1 步：会话入口

Agent 读 `AGENTS.md`，获取仓库地图、`uv run` 约定、提交要求、中文输出。调用 `using-openharness`。

`using-openharness` 判断此请求需要任务上下文 → 运行 `openharness bootstrap` → 无匹配活跃任务包 → 创建任务包：

```
openharness new-task add-status-command --auto-id
```

任务包创建，状态 `proposing`。

**讨论**：`using-openharness` SKILL.md 当前是一张目录——36 行、5 个"详见 X 文件"的外部引用。其中 `session-routing.md`（bootstrap 三路分支）、`task-classification.md`（任务类型矩阵）、`state-routing-table.md`（状态路由表）是每次必读的执行内容，不是可选参考资料。这导致 Agent 读 4 个文件累计 250+ 行才能开始干活。所有其他 11 个 skill 都是自包含的（0-2 个引用），唯独入口 skill 把执行体拆到了外部。

**优化方向**：入口 skill 的执行内容应内联，参考类内容（CLI 速查）保留外部文件。但本次演绎聚焦状态流转，入口问题留作后续。

---

## 第 2 步：proposing — 需求收敛

Agent 调用 `brainstorming`。

### 判断任务清晰度

- 用户说了**做什么**：加 CLI 命令
- 用户说了**输出什么**：活跃任务包、状态、owner、时间
- 用户**没说**的：输出格式（表格？JSON？）、是否支持 flag

判定为"偏清晰的模糊任务"——核心行为明确，但接口精度有一处歧义。

### 完整流程

1. **读上下文**：打开 `openharness_cli/commands.py`，看现有 CLI 命令的注册和输出模式。
2. **挑战前提**：用户说"加 status 命令"，但真正问题可能是"现在看任务状态要翻 task-info.yaml 文件不方便"。需求本质：提供比直接读 YAML 更便捷的任务概览方式。
3. **识别歧义**——只需问一个问题：

   > 默认输出格式用表格（类似 `docker ps`），另外提供 `--json` flag 给脚本用。这样可以吗？

   用户说可以。歧义关闭。

   （"只列活跃包"用户已明确说了，不需要再问。）

4. **写 `01-requirements.md`**：目标用户、核心场景、成功指标、验收标准、边界、至少一个反例。
5. **Exit Check**：7 个问题全部能回答。

### 确定任务分类和验证策略

Agent 判断：
- 单一命令、无架构决策 → **task_type: mechanical**
- CLI 命令有明确输入输出、可自动测试 → **verify_by: unit_test**

Agent 将两者写入 `task-info.yaml`：

```yaml
collaboration:
  task_type: mechanical
  design_review_mode: auto
verification:
  verify_by: unit_test
```

用户确认 task_type。

---

**此时引出第一个优化。**

### 优化 1：`requirements_designed` 不应停留

当前流程：brainstorming 完成 → `openharness transition <task> requirements_designed` → 停在 gate → Agent 读路由表 → 再 transition 到下一状态。

改进后：

```
Agent 执行 openharness transition <task> requirements_designed

CLI 检查 task-info.yaml：
  task_type 为空？
    → 报错："task_type 未确认。请向用户提议分类并写入 task-info.yaml.collaboration.task_type"
  verify_by 为空？
    → 报错："verify_by 未确定。请确定验证策略（unit_test / qualitative / rwp）并写入 task-info.yaml.verification.verify_by"

  全部通过？
    → task_type == mechanical → 自动推进到 implementing
    → task_type == standard / protocol → 自动推进到 overview_designing
    → 输出："当前状态：implementing"，以及下一步指令
```

`requirements_designed` 不再是一个停留态。CLI 在推进时一次性检查所有必须写入的字段，通过即自动跳转。`design_review_mode` 由 CLI 按 task_type 默认填充（`protocol/architecture` → `stepwise`，其他 → `auto`），Agent 后续可改。

---

**此时引出第二个优化。**

### 优化 2：接手已有任务包时不需要 brainstorming

brainstorming 是"需求从无到有"，不是"每次进入 proposing 都重跑"。区分三种场景：

| 场景 | 行为 |
|------|------|
| 任务包在非 proposing 状态 | 按路由表直接跳到当前状态对应 skill |
| 任务包在 proposing，01 已有内容 | 读取现有 01，增量收敛——续写，不是重写 |
| 任务包在 proposing，01 为空 | 完整 brainstorming |

---

**此时引出第三个优化。**

### 优化 3：新建任务包时 CLI 直接返回 brainstorming 内容

当前模型：CLI 返回"创建成功" → Agent 自己记得调用 brainstorming。Agent 的"记得"就是控制论盲区。

改进后：`openharness new-task <name> --auto-id` 创建任务包后**直接输出 brainstorming skill 的执行内容**：

```
任务包 add-status-command 已创建。
当前状态：proposing

在 01-requirements.md 中收敛需求：
1. 判断任务清晰度（快通道 or 完整流程）
2. 读上下文、挑战前提、识别歧义
3. 写 01-requirements.md（模板路径：...）
4. Exit Check：7 个问题逐项确认
5. 提议 task_type 和 verify_by，等用户确认后写入 task-info.yaml

完成后执行：openharness transition add-status-command requirements_designed
```

Agent 没有选择——内容已在上下文中，必须执行。

**原则**：凡是必须执行的下一步，由 CLI 输出直接给出指令，不让 Agent 自己查路由表决定。

---

## 第 3 步：implementing

task_type == mechanical，CLI 自动推进到 implementing。Agent 进入 TDD 循环。

### RED → GREEN → REFACTOR

**第一个测试**：`openharness status` 默认表格输出，包含活跃包、不含 archived。

RED — 命令还不存在。亲眼看到失败。GREEN — 最小实现。REFACTOR — 提取函数。全绿。

**第二个测试**：`--json` flag 输出合法 JSON。

RED → GREEN → REFACTOR。两轮结束。

---

**此时引出第四个优化。**

### 优化 4：`implemented` 也不应停留

和 `requirements_designed` 同逻辑：

```
Agent 执行 openharness transition <task> implemented

CLI 检查 → 自动推进到 verifying，同时输出：

  当前状态：verifying
  验证方式：unit_test
  执行：运行你写的测试，确认全部通过。
  完成后：将测试命令、结果和变更文件清单写入 evidence.md，
          然后执行 openharness transition <task> archived。
```

---

**此时引出第五个优化。**

### 优化 5：并行调度是执行策略，不是 skill 路径

当前 `subagent-driven-development` 被放在 implementing 决策树里，前置条件是"用户明确要求子代理或并行工作"。这有两个问题：

1. 并行决策推给用户——用户不应关心 Agent 用什么执行策略
2. 把"并发"绑定在代码实现阶段——实际上实现阶段是最不适合并发的

真正高频的并行场景在知识工作：

| 场景 | 适合并行？ | 理由 |
|------|----------|------|
| 多份设计文档的语义审计 | 是 | 互不修改，纯读取+判断 |
| 多个技术方向的调研 | 是 | 搜索范围不同，无共享写入 |
| 多个文件的代码实现 | 极少 | 文件间有隐式依赖，合并冲突风险高 |
| 调试一个 bug | 否 | 需要串行的假设-验证循环 |

并行调度应从 implementing 决策树中移除，变为 Agent 在任何阶段都可自行选择的横切执行策略。

---

## 第 4 步：verifying

CLI 在推进到 verifying 时已输出指令。Agent 不需要读任何 skill——直接跑测试。

```
pytest tests/test_cli_status.py
```

全部通过。Agent 写 `evidence.md`：

```markdown
# 验证证据

## 测试

pytest tests/test_cli_status.py -v

结果：2 passed, 0 failed

## 变更文件

- openharness_cli/commands.py — 新增 status 子命令
- tests/test_cli_status.py — 新增测试

## 验收标准覆盖

| 标准 | 证据 |
|------|------|
| 显示所有活跃任务包 | test_status_lists_active_task_packages ✓ |
| 支持 --json flag | test_status_json_output ✓ |
```

然后：

```
openharness transition add-status-command archived
```

CLI 检查 `evidence.md` 存在且非空 → 将任务包移至 `docs/archived/task-packages/` → 更新 task-info.yaml 为 archived。终态。

---

**此时引出第六个优化。**

### 优化 6：删除验证中间层——skill、CLI 命令、artifacts 目录

`verification-before-completion` skill：CLI 在推进时已经通过 `verify_by` 输出验证方法了，Agent 不需要再读一个 skill 才知道做什么。这个 skill 是纯中间人，可以移除。

`openharness verify <task>`：只能泛化地跑命令，处理不了 `qualitative`（语义审核）和 `rwp`（运行时观察）。假通用验证器，移除。

`.harness/artifacts/`：存了一堆 JSON 但没人回头看。`last_run_artifact` 路径记录永远指向一个没人读的文件。产物就是证据——证据在 evidence.md 里，路径不是证据本身。移除。

`04-verification.md` 和 `05-evidence.md` 模板：mechanical + unit_test 的场景下，验证就是跑测试，证据就是测试结果 + 变更文件。两个独立文档各自一份 Exit Check 是形式主义的开销。合并为一个 `evidence.md`，作为任务包附录，不要求模板格式。

#### evidence.md 按 verify_by 类型有不同的自然内容

| verify_by | evidence.md 包含 |
|-----------|-----------------|
| unit_test | 测试命令 + 结果 + 变更文件 + 验收标准覆盖 |
| qualitative | 审核对象 + 发现 + 结论 + 问题是否闭合 |
| rwp | 工作流名 + 观察结果 + 产物路径 + 盲区说明 |

`openharness transition <task> archived` 只有一个硬门禁：

```
evidence.md 存在且非空？
  ✗ → 报错："证据文件不存在或内容为空，请先写入验证证据后再归档"
  ✓ → 归档
```

---

## 优化后的完整状态流

### mechanical

```
new-task → proposing → implementing → verifying → archived
              │                          │
         brainstorming            CLI 输出 verify_by
         确定 task_type            指令，Agent 执行
         确定 verify_by            验证，写 evidence.md
```

中间无 gate 状态滞留。CLI 在 transition 时检查字段完整性，通过即自动推进。

### standard development / protocol

```
new-task → proposing → overview_designing → detailed_designing → implementing → verifying → archived
              │              │                     │                 │              │
         brainstorming  exploring-          detailed-design     TDD/subagent/  CLI输出指令
         确定 task_type  solution-space                         直接实现        写 evidence.md
         确定 verify_by  写 02                                  (并行是横切
         写 01                                                  策略，非独立
                                                               路径)
```

`overview_designed` 和 `detailed_designed` 两个 gate 是否也应自动推进，本次演绎未涉及（案例是 mechanical），需要后续针对标准流程做同样的步进推演来验证。

---

## task-info.yaml 最终状态

```yaml
id: <DESIGN_ID>
title: <TITLE>
status: <STATUS>
summary: <SUMMARY>
owner: <OWNER>
created_at: <DATE>
updated_at: <DATE>
depends_on: []
scope:
  areas: []

collaboration:
  task_type: mechanical              # mechanical / standard development / protocol/architecture
  design_review_mode: auto           # stepwise / auto，由 CLI 按 task_type 默认填充

entrypoints: []

done_criteria: []

verification:
  verify_by: unit_test               # unit_test / qualitative / rwp
  last_run_result: ""                # passed / failed / ""
```

移除的字段：`required_commands`、`required_scenarios`、`last_run_at`、`last_run_artifact`、`evidence` 下的 `code_review` 子块。

---

## 已移除的内容

| 移除项 | 原因 |
|--------|------|
| `verification-before-completion` skill | CLI 在推进时直接输出验证指令，skill 是纯中间人 |
| `openharness verify` 命令 | 只能跑命令，处理不了 qualitative 和 rwp，假通用 |
| `.harness/artifacts/` 目录 | 产物 JSON 没人读，形式主义 |
| `04-verification.md` 模板 | 合并进 evidence.md |
| `05-evidence.md` 模板 | 合并进 evidence.md |
| `required_commands` 字段 | 需求阶段不知道测试文件叫什么名字，必然填不准 |
| `last_run_artifact` 字段 | 路径指向一个没人读的 JSON，证据本身在 evidence.md |

---

## 核心设计原则

1. **CLI 输出即指令**：每一个 mandatory 的下一步，由 CLI 在 transition 时直接输出。Agent 不需要查路由表或 skill 才知道做什么。

2. **字段检查替代 Gate 状态**：`requirements_designed`、`implemented` 等中间停留态消失。CLI 在 transition 时检查必需字段完整性，通过即自动推进到下一个活跃态。

3. **task_type 和 verify_by 在需求阶段一起确定**：验证策略不是实现完成后才冒出来的——它从 01 的验收标准中可以直接推出。

4. **并行调度是横切策略，不在决策树中**：Agent 在任何阶段自行选择，高频场景是知识工作而非代码实现。

5. **证据是附录，不是独立层**：evidence.md 按 verify_by 类型自然生成，不要求模板化结构。archived 的门禁只有一条：evidence.md 存在且非空。
