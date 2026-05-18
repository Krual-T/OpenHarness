# 验证策略

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **本文件在 `verification_designing` 阶段编写（TDD 红阶段，先于实现）**。
> 定义验证策略——计划怎么验证、用什么命令、期望什么结果。
> 实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。
>
> **使用前先确认你能回答这些问题**：
> - 每项 Required Outcome 是否有对应的验证方法？
> - 验证命令是否具体到可以直接复制粘贴执行？
> - 是否有边界或错误场景的验证？
> - 哪些风险本轮不覆盖，接受理由是什么？
> - 计划路径和回退路径分别是什么？

## 验证路径
- **计划路径**：运行核心任务包测试和 CLI workflow 测试，覆盖新建任务包、validate、transition、archive 等路径；用 `rg` 检查模板和必填常量中字段已删除。
- **回退路径**：如果测试失败，按失败点回到实现修正模板、校验常量或测试夹具；如果 `rg` 命令失败，说明字段仍残留在新 schema 表面。
- **路径说明**：本轮修改影响 schema 和测试夹具，单元测试能自动判定；历史归档不批量迁移，因此搜索范围限定在模板、CLI 和测试。

## 必需命令
1. `uv run pytest tests/openharness_cases/test_task_package_core.py tests/openharness_cases/test_cli_workflows.py -q`
   - 期望退出码：`0`
   - 期望输出：两个测试文件全部通过。
2. `! rg -n 'done_criteria|depends_on|scope:|areas:' skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：无输出。
3. `! rg -n '"done_criteria"' openharness_cli/constants.py`
   - 期望退出码：`0`
   - 期望输出：无输出。
4. `! rg -n 'done_criteria|depends_on|scope:|areas:' openharness_cli tests/openharness_cases skills/using-openharness/references/templates/task-package.task-info.yaml`
   - 期望退出码：`0`
   - 期望输出：无输出。

## 预期结果
- 新模板不包含 `done_criteria`、`depends_on`、`scope.areas`。
- `done_criteria` 不再是必填状态键。
- 任务包核心和 CLI workflow 测试通过。
- `TaskInfo` 不再暴露 `done_criteria` 一等字段，旧字段仅通过 `_extra` 通用机制兼容。

## 可追溯性
- 需求结果 1 由命令 2 覆盖。
- 需求结果 2 由命令 3 和命令 1 覆盖。
- 需求结果 3 由命令 4 和命令 1 覆盖。
- 需求结果 4 由命令 1 覆盖。

## 风险接受
- 接受风险：历史归档任务包仍包含这些字段。理由是本轮目标是新 schema 表面，批量重写历史证据风险更高。
- 接受风险：历史 YAML 中旧字段只通过 `_extra` 通用机制兼容，没有专门业务语义。
- 接受风险：没有为 `depends_on` 和 `scope.areas` 写迁移测试。理由是它们当前只作为 `_extra` 字段存在，没有显式 CLI 消费路径。

## 验证执行计划
- 执行人：当前实现者。
- 执行时机：实现前运行命令观察失败；实现后和 verifying 阶段各运行一次全部命令。
- 执行环境：仓库根目录 `/home/Shaokun.Tang/Projects/openharness`，使用 `uv run`。
- **Fallback**：验证失败则回到 `implementing`；如果验证命令无法代表需求，回到 `verification_designing`。
