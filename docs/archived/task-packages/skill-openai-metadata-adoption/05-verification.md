# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 运行聚焦 metadata 的 pytest 用例，确认缺失 metadata 或策略回退会被测试拦住。
  - 运行完整 `skills/using-openharness/tests/test_openharness.py`，确认不会破坏现有 harness 协议测试。
  - 运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 task package 协议完整。
- Executed Path:
  - 先执行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k "skill_openai_metadata or openai_yaml or implicit_invocation"`，确认新增 metadata 相关断言通过。
  - 再执行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，确认完整 harness 测试 70 条全部通过。
  - 最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 active 与 archived task packages 结构有效。
- Path Notes:
  - 在执行完整 pytest 时，先暴露出 `brainstorming` 与 `exploring-solution-space` 的既有协议文案缺口；本轮已同步补齐缺失短语，随后完整测试转绿。
  - 这条路径足以覆盖本轮要求的 metadata 覆盖率、策略分类与仓库协议回归。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "skill_openai_metadata or openai_yaml or implicit_invocation"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 新增 metadata 相关断言通过。
- 完整 harness 测试通过。
- `check-tasks` 不报告 023 或其他 active task package 的结构错误。

## Traceability
- 需求中的“metadata 全覆盖、策略分类、工具依赖下沉、防回归测试”分别对应：
  - `agents/openai.yaml` 文件落地；
  - metadata 中的 `policy.allow_implicit_invocation` 分类；
  - metadata 中的 `dependencies.tools`；
  - pytest 与 `check-tasks` 结果。
- 其中 `project-memory` 明确声明 `shell` 依赖，满足本轮“把真实依赖前移到 metadata 层”的要求。
- 完整 pytest 通过也证明本轮新增 metadata 没有破坏既有 harness 协议测试。

## Risk Acceptance
- 当前仍接受的风险是：`receiving-code-review` 与 `project-memory` 的 implicit 分类未来可能因为真实使用体验需要微调。
- 之所以可以接受，是因为这两个策略已经被收敛成单点 metadata 决策，后续若调整只需同步修改 `openai.yaml`、测试与任务包证据。
- 其余风险已通过全量测试和 `check-tasks` 收敛到可接受范围。

## Latest Result
- 验证通过。聚焦 metadata 测试通过，完整 harness 测试 70/70 通过，`check-tasks` 通过。
- Latest Artifact:
