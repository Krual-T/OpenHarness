# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先执行聚焦 CLI 测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -q`。
  - 再执行全量测试：`uv run pytest -q`。
- Executed Path:
  - 先写入失败测试，并确认 `init` 尚未注册时聚焦测试失败。
  - 实现命令后执行聚焦测试并通过。
  - 更新协议子命令集合测试后执行相关测试并通过。
  - 归档任务包后执行 `uv run openharness check-tasks` 并通过。
  - 最后执行全量测试并通过。
- Path Notes:
  - 全量测试第一次失败是因为既有协议测试的子命令白名单尚未包含新增 `init`，补充断言后全量测试通过。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py -q`
- `uv run openharness check-tasks`
- `uv run pytest -q`

## Expected Outcomes
- 聚焦测试应验证 `openharness init --repo <repo>` 的 parser handler 和 `.harness/.gitignore` 内容。
- 全量测试应无失败，确认新增命令没有破坏现有 CLI 行为。

## Traceability
- 需求中的 `init` 子命令、`--repo` 参数和 `*\n` 文件内容分别由 `test_init_parser_accepts_repo_argument` 与 `test_init_creates_harness_gitignore_that_ignores_everything` 覆盖。
- 协议测试确认新增 `init` 被纳入公开子命令集合和当前 handler 集合。

## Risk Acceptance
- 本轮接受覆盖写入 `.harness/.gitignore` 的策略；如果后续需要保留用户自定义 `.harness/.gitignore` 内容，应单独设计幂等合并规则。
- 本轮不验证未来初始化项，因为用户明确只要求第一步。

## Latest Result
- 最近一次验证结果：`uv run pytest -q` 通过，`205 passed in 1.47s`。
- Latest Artifact: 无独立日志文件；验证证据来自命令输出和本文件记录。
