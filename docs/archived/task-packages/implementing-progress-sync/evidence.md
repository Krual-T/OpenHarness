# 证据

> **语言规则**：章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 验证结果

- **method**: qualitative
- **rwp_enabled**: false
- **Result**: 有条件通过
- **条件说明**：计划中的命令验证均通过，审核矩阵已逐项自审并未发现阻塞问题；但当前会话没有可调用的独立子 Agent 或人类逐项反馈工具，因此双轨审核只能记录为有条件通过。

## 变更文件

- `skills/using-openharness/states/implementing/instructions.md` — 新增任务进度同步规则，要求环境任务工具和 `plan.md` 的实施步骤同步更新；补充阶段结束检查、要点、常见失败模式和反合理化。
- `pyproject.toml` — 版本从 `3.0.1` 提升到 `3.0.2`。
- `uv.lock` — 同步 `openharness` 锁定版本到 `3.0.2`。
- `docs/task-packages/implementing-progress-sync/requirements.md` — 记录需求边界。
- `docs/task-packages/implementing-progress-sync/overview-design.md` — 记录总体设计和取舍。
- `docs/task-packages/implementing-progress-sync/detailed-design.md` — 记录落地细节、状态语义和验证准备。
- `docs/task-packages/implementing-progress-sync/plan.md` — 记录实施步骤、验证设计和进度。
- `docs/task-packages/implementing-progress-sync/evidence.md` — 记录实现阶段中间事实。

## 测试结果

```bash
uv run pytest tests/openharness_cases/test_protocol_docs.py -q
```

结果：18 passed，退出码 0。

verifying 阶段复跑结果：18 passed，退出码 0。

```bash
uv run pytest tests/ -q
```

结果：73 passed，退出码 0。

verifying 阶段复跑结果：73 passed，退出码 0。

### 验收标准覆盖

| 标准 | 证据 |
|------|------|
| 读取 `plan.md` 实施步骤作为事实来源 | `implementing/instructions.md` 的 `## 任务进度同步` 第一段 |
| 有任务进度工具时使用，且不绑定单一工具 | `## 任务进度同步` 第二段列出工具示例并说明不绑定某一个工具 |
| 更新进度为 `in_progress` 或 `completed` 时同步 `plan.md` | `## 任务进度同步` 第三段 |
| 禁止最后一次性补勾 | `## 任务进度同步` 第四段、`## 要点`、`## 常见失败模式` |
| 无任务工具时仍逐步维护 `plan.md` | `## 任务进度同步` 第四段 |
| evidence 边界不被破坏 | `## 与相邻文档的边界` 保留原有 implementing / verifying 分工 |

## 语义审核

### 审核交接包摘要

- 审核对象：`skills/using-openharness/states/implementing/instructions.md`
- 任务背景：实现阶段已有 `plan.md` 实施步骤和环境任务工具两类进度载体，但原提示词没有要求同步。
- 审核目标：检查新规则是否要求每次更新进度：改成 `in_progress` 或 `completed` 时同步写回 `plan.md`，并避免绑定单一工具名。
- 非审核范围：不审核 CLI 自动同步、hook、IDE 插件或任务工具实现。
- 输出格式：按审核矩阵逐项记录观察，最终结论留给 verifying 阶段。

### 实现阶段审核观察

| 审核对象 | 审核维度 | 观察 |
|----------|----------|------|
| `implementing/instructions.md` | 规则落点 | 已新增 `## 任务进度同步`，位于 `Goal-Driven Execution` 前，覆盖所有验证方法分支。 |
| `implementing/instructions.md` | 环境任务工具 | 文案使用“如果当前环境提供任务进度工具”，并将 Codex `update_plan`、Claude Code 任务工具、旧版 `TodoWrite` 写为常见例子，不绑定单一工具。 |
| `implementing/instructions.md` | 用户指定表述 | 已使用“每次使用环境任务工具更新进度：改成 `in_progress` 或 `completed`”。 |
| `implementing/instructions.md` | `plan.md` 同步 | 已要求同一轮同步更新 `plan.md` 中对应实施步骤或 `## 进度记录`。 |
| `implementing/instructions.md` | 禁止最后补勾 | 已写入“禁止实现全部完成后才一次性把 `## 实施步骤` 全部勾选”，并在要点和失败模式中重复约束。 |
| `implementing/instructions.md` | 无工具降级 | 已要求没有任务进度工具时仍逐步维护 `plan.md`。 |
| `implementing/instructions.md` | 证据边界 | 原有 implementing / verifying 边界保留；新增规则只要求一致性检查，没有把最终结论提前放入 implementing。 |

### AI 子 Agent 审核

当前会话没有可调用的独立子 Agent 工具。未执行独立子 Agent 审核；以下为主 Agent 按 `plan.md` 审核矩阵逐项自审结果，不能替代双轨审核。

| 审核对象 | 审核维度 | 通过标准 | 审核结论 | 发现（问题/改进点） | 严重程度 |
|----------|----------|----------|----------|---------------------|----------|
| `implementing/instructions.md` | 规则落点 | 任务进度同步规则位于实现阶段通用流程中，覆盖不同验证方法 | 通过 | 新小节位于 `Goal-Driven Execution` 前 | 无 |
| `implementing/instructions.md` | 环境任务工具 | 要求有任务进度工具时使用，但不把某一个工具名写成硬依赖 | 通过 | 工具名作为常见例子出现，并说明规则不绑定某一个工具 | 无 |
| `implementing/instructions.md` | 用户指定表述 | 明确出现“更新进度：改成 `in_progress` 或 `completed`” | 通过 | 对应短句已写入新小节和要点 | 无 |
| `implementing/instructions.md` | `plan.md` 同步 | 每次更新进度为 `in_progress` 或 `completed` 时同步更新 `plan.md` | 通过 | 新小节要求“同一轮同步更新 `plan.md`” | 无 |
| `implementing/instructions.md` | 禁止最后补勾 | 明确禁止最后一次性全勾 | 通过 | 新小节、要点和失败模式均覆盖 | 无 |
| `implementing/instructions.md` | 无工具降级 | 没有环境任务工具时仍要求逐步维护 `plan.md` | 通过 | 新小节第四段覆盖 | 无 |
| `implementing/instructions.md` | 证据边界 | 保持 `evidence.md` 写中间事实，不提前写最终结论 | 通过 | 原有边界章节保留，新规则只增加一致性检查 | 无 |

- 子 Agent 审核结论：未执行；当前记录为主 Agent 自审。

### 人类审阅者反馈

用户在实施前明确要求文案不要展开为“改成什么”，而是直接写“更新进度：改成 `in_progress` 或 `completed`”。该要求已采纳并写入提示词。

未获得 verifying 阶段的人类逐项审核反馈，因此本轮最终只能给出有条件通过。

| 审核对象 | 审核维度 | 子 Agent 结论 | 人类审阅意见（同意/异议/补充） | 说明 |
|----------|----------|---------------|-------------------------------|------|
| `implementing/instructions.md` | 用户指定表述 | 主 Agent 自审通过 | 补充 | 用户已明确要求采用“更新进度：改成 `in_progress` 或 `completed`”表述 |
| `implementing/instructions.md` | 其他审核维度 | 未执行独立子 Agent 审核 | 未获得逐项反馈 | 记录为残余审核缺口 |

- 人类审阅者总体意见：未获得 verifying 阶段逐项反馈。

### 发现处理

| 来源 | 审核对象 | 问题 | 处理状态（采纳/拒绝/延后） | 处理理由 | 是否闭合 |
|------|----------|------|----------------------------|----------|----------|
| 用户 | `implementing/instructions.md` | 文案应直接写“更新进度：改成 `in_progress` 或 `completed`” | 采纳 | 已按要求写入新小节和要点 | 是 |
| 验证流程 | `evidence.md` | 缺少独立子 Agent 和人类逐项反馈 | 延后 | 当前会话没有可调用子 Agent 或人类逐项反馈工具；不伪装为完整双轨审核 | 否 |

### 综合结论

- 子 Agent 与人类审阅者是否存在分歧：未形成双轨分歧，因为独立子 Agent 审核和人类逐项反馈未执行。
- 分歧处理方式：无分歧可处理；缺口作为残余风险记录。
- 最终结论：有条件通过。
- 未闭合问题的 follow-up 计划：如后续需要严格执行 `qualitative` 双轨审核，应在具备子 Agent 和人类逐项反馈入口的环境中补审；若补审发现问题，回到 implementing 修正提示词。

## 运行时观察

未启用 RWP；`uv run openharness rwp list` 返回没有可用运行时工作流包。

## 残余风险

- 规则仍依赖 agent 遵循提示词，不能机械阻止漏同步。接受理由：本轮明确不实现跨平台自动同步。
- `in_progress` 在 `plan.md` 中没有专用语法。接受理由：可写入 `## 进度记录`，避免扩展任务包格式。

## 后续事项

- 如后续仍频繁出现进度不同步，再评估是否需要 CLI、hook 或平台适配层支持。
- 如需要完整闭合 qualitative 双轨审核，在具备子 Agent 和人类逐项反馈入口时补充审核。
