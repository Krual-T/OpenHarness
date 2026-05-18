# 验证策略

> CLI、模板和当前任务包文档都应以中文章节标题作为本轮校验事实源。

## 验证路径
- **计划路径**：本任务使用 `verify_by: qualitative`。先执行定性审核矩阵，确认入口 skill、阶段 skill、模板和 CLI heading 校验符合设计；再执行 targeted pytest 和任务包 transition / view 命令，确认中文 heading 不破坏工具链。
- **回退路径**：如果定性审核不通过，回到 `implementing` 修正文档职责边界；如果 pytest 或 transition 失败，先判断是 CLI heading 定义、模板 heading、当前任务包文档还是非目标状态机改动导致。只有 heading / 文档同步问题可以在本任务内修复；状态机、hook、数据模型变化必须回退。
- **路径说明**：定性审核是主验证路径；pytest 只覆盖 CLI heading 校验行为，不能替代对文档语义边界的审核。

定性审核矩阵：

| 对象 | 审核维度 | 通过标准 |
|------|----------|----------|
| `skills/using-openharness/SKILL.md` | 入口职责 | 仅保留会话入口、任务包边界、进入任务包和完成态 transition；不重复 `AGENTS.md`、受保护文件、输出约定或完整状态机教学 |
| `skills/using-openharness/states/*/SKILL.md` | 阶段方法 | 每个阶段保留阶段目的、阶段方法、Exit Check、阻塞/回退和完成态；不退化为纯执行清单 |
| `skills/using-openharness/references/templates/*` | 模板职责 | 模板只写文档用途、章节结构、完成标准、不合格表现和相邻文档边界；不使用“最低要求”作为主导措辞 |
| `openharness_cli/models/task_package_document.py` | heading 校验 | 必需章节 heading 使用中文，且覆盖当前 workflow 所需文档 |
| `tests/openharness_cases/*` | 回归覆盖 | 依赖章节 heading 的测试数据和断言同步中文 heading，仍覆盖缺失章节和非占位内容校验 |
| `.tmp/skills-backup/finishing-a-development-branch/` | 备份 | 原收尾 skill 内容被移动到备份目录，主 workflow states 不再保留该阶段目录 |

## 必需命令
实现完成后必须执行：

| 命令 | 期望退出码 | 期望输出 |
|------|------------|----------|
| `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_protocol_docs.py` | 0 | pytest 通过；涉及 task package heading、模板文本和协议文档的回归不失败 |
| `uv run openharness task-package view TASK-004` | 0 | 输出当前任务包状态和对应阶段 skill；无任务包读取错误 |

验证阶段如果实现后新增或调整了更精确的 CLI 检查命令，可以在 `evidence.md` 中补充，但不得用补充命令替代表中的必需命令。

## 预期结果
- 入口 skill 不再是仓库约定、状态机教学和阶段写作指南的混合体。
- 阶段 skill 仍能指导 agent 解决当前阶段最重要的问题，不是纯命令清单。
- 模板使用中文章节标题和“完成标准”类措辞，不再把“最低要求”作为主导。
- CLI 必需章节校验识别中文 heading，当前任务包无需英文兼容 heading 也能推进。
- `task_type`、`design_review_mode`、`verify_by` 的确认入口集中在需求阶段，后续阶段只消费字段。
- `implementing` 与 `verifying` 对 `evidence.md` 的分工清晰：前者记录中间事实，后者写最终判定和残余风险。
- `finishing-a-development-branch` 已备份到 `.tmp/skills-backup/`，主 workflow states 不再把它作为当前优化对象。

## 可追溯性
| 需求结果 | 验证方法 | 证据位置 |
|----------|----------|----------|
| 修正流程文档不一致 | 定性审核入口 skill、阶段 skill、模板和 CLI heading 校验 | `evidence.md` 的语义审核与命令结果 |
| 明确 skill 与模板边界 | 审核阶段 skill 是否保留方法论、模板是否只承载文档结构 | `evidence.md` 的审核矩阵 |
| 收敛验证职责 | 审核 detailed / verification / evidence 模板与阶段 skill 分工 | `evidence.md` 的审核矩阵 |
| implementing / verifying evidence 分工 | 审核 implementing、verifying skill 和 evidence 模板 | `evidence.md` 的审核矩阵 |
| RWP 写回位置一致 | 审核 overview / detailed / verification 相关说明是否有明确写回位置或已移走不合适要求 | `evidence.md` 的审核矩阵 |
| 分类规则入口统一 | 审核 brainstorming skill、requirements 模板、后续阶段引用关系 | `evidence.md` 的审核矩阵 |
| 降低重复文本 | 审核阶段 skill 和模板没有复制大段相同章节写作指导 | `evidence.md` 的审核矩阵 |
| 移走收尾 skill | 检查 `.tmp/skills-backup/finishing-a-development-branch/` 和 `skills/using-openharness/states/` | `evidence.md` 文件清单 |
| 中文章节标题 | pytest、transition、当前任务包文档审查 | pytest 输出和 transition 结果 |
| `task-info.yaml` 自然语言字段 | 审核模板与当前任务包 `task-info.yaml` | `evidence.md` 的审核矩阵 |

## 风险接受
- 不批量重写 archived 历史包 heading。接受理由：需求明确不做 archived 历史包批量重写；未来如果需要对 archived 包运行严格中文 heading 校验，应单独开任务。
- 不重新设计 CLI 状态机、hook 或任务包数据模型。接受理由：本轮只解决文档职责和 heading 校验冲突；这些行为变化会扩大为另一个任务包。
- 定性审核无法像单元测试一样完全自动判定文档质量。接受理由：本任务核心是语义边界，必须由审核矩阵判定；pytest 只覆盖可编程的 CLI heading 校验部分。
- 不新增 RWP。接受理由：本任务验证对象是文档和 CLI 本地校验，不需要端到端运行时工作流。

## 验证执行计划
- 责任人：实施者在 `implementing` 完成后立即执行，不能延后到归档前补验。
- 环境：仓库根目录 `/home/Shaokun.Tang/Projects/openharness`；Python 命令使用 `uv run ...`；不需要网络。
- 执行顺序：
  1. 先按审核矩阵人工检查所有目标文件。
  2. 再运行 `## 必需命令` 中的 pytest。
  3. 后续 verifying 阶段重新运行命令并写最终证据。
- Fallback：审核失败回 `implementing` 修文档；命令失败且是验证策略不精确时回 `verification_designing` 修策略；命令失败且是实现问题时回 `implementing` 修实现。
