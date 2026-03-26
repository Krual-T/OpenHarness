# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 校验活跃协议文档已经统一改为 `openharness <cmd>` 入口，并且不再推荐 `skills/using-openharness/scripts/openharness.py` 这种脚本路径。
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
  - 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Executed Path:
  - 已新增协议测试 `test_active_protocol_docs_do_not_recommend_legacy_script_entrypoint`。
  - 已更新 `AGENTS.md`、`AGENTS.examaple.md`、`INSTALL.codex.md`、`skills/using-openharness/SKILL.md`，统一改为 `openharness <cmd>` 入口，并说明默认在项目根目录执行；若不在根目录，则显式传 `--repo <project-root>`。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -q`
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Path Notes:
  - 这轮刻意不改 CLI 运行时行为，只修正文档和 skills 约束，因此验证重点放在协议文档断言和 task package 协议完整性，而不是新增运行时测试。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 协议测试通过，说明活跃文档中不再推荐旧脚本路径入口。
- `check-tasks` 通过，说明 task package 结构和引用路径保持有效。

## Traceability
- `01-requirements.md` 要求统一协议入口并明确项目根目录约束。
- `02-overview-design.md` 与 `03-detailed-design.md` 将方案收缩为文档层统一，不修改 CLI 语义。
- 协议测试验证“活跃文档不再推荐脚本路径入口”，`check-tasks` 验证本任务包和仓库 task package 协议仍然有效。

## Risk Acceptance
- 仍然接受的风险是：CLI 目前依旧不会自动向上发现项目根目录，用户若在子目录执行命令，仍需要自己显式传 `--repo`。
- 这个风险在本轮可以接受，因为用户已经明确要求“只在 skills 中强调”，而不是把范围扩张成 CLI 行为改造。
- 如果后续有人再次要求“在子目录也能直接运行 `openharness` 而不用传 `--repo`”，应单独开新 task package 处理。

## Latest Result
- 最近一次验证已通过。`uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -q` 输出 `43 passed`；`uv run python skills/using-openharness/scripts/openharness.py check-tasks` 输出已校验 32 个 task package。
- Latest Artifact:
  - 无额外产物文件；证据以命令输出和本包文档为主。
