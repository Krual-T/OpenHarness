# 证据

## 验证结果
结论：通过。

本任务使用 `verify_by: qualitative`。verifying 阶段已按 `verification-design.md` 的审核矩阵检查入口 skill、阶段 skill、模板、CLI heading 校验、测试覆盖和收尾 skill 备份；未发现阻塞项。必需命令均已重新执行并通过。

## 文件
- `openharness_cli/models/task_package_document.py` — 将任务包必需章节 heading 切换为中文。
- `openharness_cli/models/task_status.py` — archived 状态不再注入已备份的收尾 skill。
- `tests/openharness_cases/test_cli_workflows.py` — 将 heading 校验测试数据改为中文。
- `tests/openharness_cases/test_protocol_docs.py` — 将模板和状态 skill 断言改为中文 heading 与当前 skill 集合。
- `tests/openharness_cases/test_task_package_core.py` — 验证收尾 skill 已移出主 states 并保留备份。
- `skills/using-openharness/SKILL.md` — 收窄入口 skill 为会话入口、任务包边界、进入任务包和阶段完成。
- `skills/using-openharness/states/*/SKILL.md` — 修正阶段职责、中文章节引用和 evidence 分工。
- `skills/using-openharness/references/templates/*` — 将任务包模板切换为中文 heading 和完成标准措辞。
- `.tmp/skills-backup/finishing-a-development-branch/` — 保存移出的收尾 skill 本地备份；该目录被 `.tmp/.gitignore` 忽略，不进入版本库。
- `docs/archived/task-packages/workflow-docs-skill-sharpening/*` — 归档本任务包需求、设计、验证设计和最终证据。

## 测试结果
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_protocol_docs.py`
  - verifying 最终结果：退出码 `0`，输出摘要为 `44 passed in 0.66s`。
- `uv run pytest`
  - verifying 补充结果：退出码 `0`，输出摘要为 `54 passed, 1 skipped in 0.73s`。
- `uv run openharness task-package view TASK-004`
  - verifying 最终结果：退出码 `0`，输出当前任务包状态为 `verifying`，并正常注入 `skills/using-openharness/states/verifying/SKILL.md`。

## 语义审核
审核对象和结论：

| 对象 | 维度 | 发现 | 结论 |
|------|------|------|------|
| `skills/using-openharness/SKILL.md` | 入口职责 | 只保留会话入口、任务包边界、进入任务包和阶段完成 transition；未重复 `AGENTS.md`、受保护文件或输出约定 | 通过 |
| `skills/using-openharness/states/*/SKILL.md` | 阶段方法 | 阶段 skill 保留阶段目的、步骤、Exit Check、阻塞和回退；没有退化为纯命令清单 | 通过 |
| `skills/using-openharness/references/templates/*` | 模板职责 | 模板承载章节结构、完成标准、质量标准和相邻边界；任务包 Markdown 模板切换为中文 heading | 通过 |
| `openharness_cli/models/task_package_document.py` | heading 校验 | 必需章节定义已切换为中文 heading，并由 targeted pytest 覆盖 | 通过 |
| `tests/openharness_cases/*` | 回归覆盖 | heading、模板文本、收尾 skill 移出主 states 的断言已同步；目标测试集通过 | 通过 |
| `.tmp/skills-backup/finishing-a-development-branch/` | 备份 | 原收尾 skill 文件已按任务要求移动到本地备份目录；主 `states/` 下不再保留该阶段目录；备份目录被忽略，不作为版本库门禁 | 通过 |

未闭合问题：无。

## 运行时观察
本任务不使用 RWP；无运行时工作流 stdout、stderr 或产物路径。

## 残余风险
- 未批量重写 archived 历史任务包 heading。接受理由：本轮需求明确不扩展到 archived 历史包；未来如需对历史包执行新的严格校验，应单独开任务。
- 当前本机全局 `openharness` 命令可能仍是旧安装版本；本轮验证使用 `uv run openharness` 验证源码行为。接受理由：仓库内改动已通过源码 CLI 和测试验证，工具安装刷新属于部署步骤，不改变本轮代码结论。
- `.tmp/skills-backup/finishing-a-development-branch/` 是本地备份，不进入 git 记录。接受理由：用户明确要求不把这两个备份文件加入 git；主 workflow 已通过删除 live state skill 和测试断言体现。
- 文档语义质量无法完全自动化判定。接受理由：本任务核心是职责边界，已用审核矩阵逐项覆盖，并用 pytest 覆盖可编程的 heading 校验路径。

## 后续事项
无必须跟进项。
