# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py -k update`，验证 `update` 的顺序、repo root 与失败中断。
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k update`，验证 parser 与安装文档已经暴露 `update`。
  - 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 task package 协议仍然成立。
- Executed Path:
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py -k update`，结果为 2 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k update`，结果为 2 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，结果为 42 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py`，结果为 15 passed。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，结果为通过，校验了 30 个 task package。
- Path Notes:
  - 本轮没有直接执行真实 `openharness update`，因为它会对当前仓库触发真正的 `git pull`。这里刻意用 monkeypatch 行为测试替代，以验证命令契约而不污染工作树。
  - 对这类带副作用的安装层命令，顺序、参数、目标 repo root 和失败中断比“真实联网执行一次”更能证明实现是否正确。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py -k update`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k update`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- `update` 子命令被 parser 识别并绑定到当前 handler。
- 命令默认以 OpenHarness 自身仓库根作为执行目录。
- `git pull` 失败时，`uv tool upgrade openharness` 不会继续执行。
- 文档改为推荐 `openharness update`。

## Traceability
- 需求 1 到 4 由 `test_cli_workflows.py` 的两个 `update` 测试覆盖，证明子命令存在、执行顺序正确、目标 repo root 正确且失败会中断。
- 需求 5 由 `test_protocol_docs.py` 和更新后的 `INSTALL.codex.md`、`skills/using-openharness/SKILL.md` 覆盖，证明用户文档已经切换到 `openharness update`。
- `check-tasks` 证明新增 task package 与文档没有破坏仓库协议。

## Risk Acceptance
- 当前接受“没有在真实远程仓库上执行一次 `openharness update`”这一残余风险，因为命令本身会修改安装源仓库，自动化环境里更应优先保护工作树不被副作用污染。
- 如果未来需要验证非标准安装路径、 detached HEAD 或未提交改动等复杂 git 状态，再单独为这些场景开 task package。

## Latest Result
- 最近一次验证已通过。局部 `update` 测试、完整协议测试、完整 CLI 工作流测试和 `check-tasks` 都返回成功。
- Latest Artifact:
  - `docs/archived/task-packages/openharness-update-command/05-verification.md`
