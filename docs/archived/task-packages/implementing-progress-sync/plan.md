# 计划

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> 本文件在 `planning` 阶段编写。它把已经确认的需求和设计转成可执行步骤，并把每一步的验证方式放在同一份清单里。实际执行结果写入 `evidence.md`。

## 实施步骤

- [x] 写入需求、总体设计和详细设计
  - 修改对象：`docs/task-packages/implementing-progress-sync/requirements.md`、`overview-design.md`、`detailed-design.md`、`task-info.yaml`
  - 完成条件：设计明确规则落点、状态语义、同步边界和验证方式。
  - 验证方式：阶段流转命令已推进到 `planning`。

- [x] 更新 implementing 阶段提示词
  - 修改对象：`skills/using-openharness/states/implementing/instructions.md`
  - 完成条件：新增任务进度同步规则，并补充阶段结束检查、要点、常见失败模式。
  - 验证方式：审核矩阵检查规则是否覆盖环境任务工具、`plan.md` 同步、无工具降级和禁止最后补勾。

- [x] 更新版本和锁文件
  - 修改对象：`pyproject.toml`、`uv.lock`
  - 完成条件：patch 版本从 `3.0.1` 提升到 `3.0.2`，锁文件同步。
  - 验证方式：检查版本 diff 只包含本项目版本变化。

- [x] 执行验证并写入证据
  - 修改对象：`docs/task-packages/implementing-progress-sync/evidence.md`
  - 完成条件：记录审核结果、辅助命令结果、变更文件和残余风险。
  - 验证方式：定性审核矩阵逐项有结论，辅助命令退出码记录清楚。

## 验证设计

本轮主要验证方式是 `qualitative`，因为改动对象是提示词语义和执行协议。稳定命令只作为辅助，确认仓库基础行为没有被破坏。

- **主要验证方式**：按审核矩阵逐项审核 `skills/using-openharness/states/implementing/instructions.md`。
- **必需命令**：

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

预期结果：退出码 0；协议文档结构相关测试通过。

```bash
uv run pytest tests/ -q
```

预期结果：退出码 0；全量测试通过。

- **边界或错误场景**：
  - 提示词只提某个平台工具名，导致其他环境无法执行。
  - 提示词允许环境任务工具更新后不写回 `plan.md`。
  - 提示词仍允许最后一次性补勾。
  - 提示词要求发明新的 `plan.md` 复选框语法。

### 审核交接包

审核对象：`skills/using-openharness/states/implementing/instructions.md`，重点是新增或调整的任务进度同步规则、阶段结束检查、要点和常见失败模式。

任务背景：OpenHarness 的 `plan.md` 已有可勾选实施步骤，但实现阶段提示没有要求环境任务工具进度与 `plan.md` 同步，导致任务包事实源可能滞后。

审核目标：判断新提示词是否能让 Codex、Claude Code 和其他 agent 环境在实现时逐步同步进度，而不是最后一次性补勾。

非审核范围：不评价 CLI 自动化、hook、IDE 插件、任务工具实现，也不要求重写 `planning` 阶段模板。

输出格式：按审核矩阵逐项给出“通过 / 有条件通过 / 不通过”，每项附简短证据；最后给出残余风险和是否允许进入 verifying。

### 审核矩阵

| 审核对象 | 审核维度 | 通过标准 | 证据要求 |
|----------|----------|----------|----------|
| `implementing/instructions.md` | 规则落点 | 任务进度同步规则位于实现阶段通用流程中，覆盖不同验证方法 | 指出对应章节 |
| `implementing/instructions.md` | 环境任务工具 | 文案要求有任务进度工具时使用，但不把某一个工具名写成硬依赖 | 列出工具名作为示例还是强制依赖 |
| `implementing/instructions.md` | 用户指定表述 | 明确出现“更新进度：改成 `in_progress` 或 `completed`”这类短句 | 引用对应句子 |
| `implementing/instructions.md` | `plan.md` 同步 | 每次更新进度为 `in_progress` 或 `completed` 时，同步更新 `plan.md` | 指出同步要求 |
| `implementing/instructions.md` | 禁止最后补勾 | 明确禁止实现完成后一次性把实施步骤全勾 | 指出要点或失败模式 |
| `implementing/instructions.md` | 无工具降级 | 没有环境任务工具时仍要求逐步维护 `plan.md` | 指出降级说明 |
| `implementing/instructions.md` | 证据边界 | 保持 `evidence.md` 写中间事实，不把最终验证结论提前写进 implementing | 指出未破坏原有 evidence 边界 |

## 文件修改计划

- `skills/using-openharness/states/implementing/instructions.md`：承载本轮行为规则，是唯一技能提示词落点。
- `pyproject.toml`：按仓库约定提升 patch 版本。
- `uv.lock`：同步项目版本锁定信息。
- `docs/task-packages/implementing-progress-sync/evidence.md`：记录实现阶段中间事实、审核结果、命令结果和残余风险。

## 进度记录

- [x] 需求已写入。
- [x] 总体设计已写入。
- [x] 详细设计已写入。
- [x] 计划已写入并进入实现。
- [x] 提示词和版本已修改。
- [x] 验证通过并写入证据。

## 决策与发现

- 决策：不修改 `planning` 模板。原因是当前缺口在实现时同步，不在计划格式。
- 决策：不把规则绑定到 `update_plan` 或 `TodoWrite`。原因是工具名随平台变化，OpenHarness 应要求“环境任务进度工具”。
- 发现：当前仓库没有可用 RWP，且本轮不需要运行时工作流证据。

## 完成判定

写清什么时候可以从 `planning` 进入 `implementing`，什么时候可以从 `implementing` 进入 `verifying`，以及最终 `verifying` 需要判定什么。

- **进入实现的条件**：本计划的实施步骤、文件修改计划、审核矩阵和辅助命令均已写清。
- **实现完成的条件**：`implementing/instructions.md`、版本文件和 `evidence.md` 已按计划更新，实施步骤逐步同步勾选。
- **验证完成的条件**：审核矩阵逐项通过或有明确风险接受，辅助命令结果已记录，任务包可以 transition 到 `verified`。

## 风险接受

- 不实现自动同步。接受理由：本轮要解决的是提示词行为缺口，自动同步需要跨平台读取任务工具内部状态，属于另一个任务包。
- 不强制新增 `plan.md` 状态语法。接受理由：`completed` 可用复选框表达，`in_progress` 可用进度记录表达；新增语法会扩大协议表面。
- 不对官方工具名做长期保证。接受理由：工具名会随平台版本变化，规则以环境能力和同步动作作为稳定契约。
