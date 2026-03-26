# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py -k help`，验证顶层与关键子命令帮助文案。
  - 执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k help`，验证协议级帮助断言。
  - 执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 task package 协议有效。
- Executed Path:
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py`，结果为 3 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k help`，结果为 1 passed。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，结果为通过，校验了 31 个 task package。
  - 已人工检查 `openharness update --help` 与 `openharness bootstrap --help`，确认帮助页包含 description 和 example，而不再只是 `-h`。
- Path Notes:
  - 本轮主要验证的是帮助页文本质量，因此以 parser 帮助输出断言和命令行帮助页人工抽查为主，不需要额外运行有副作用的命令。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py -k help`
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k help`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 顶层帮助页列出完整命令总览和示例。
- `update --help` 说明 `git pull` 与 `uv tool upgrade openharness` 的顺序。
- `bootstrap --help` 等子命令包含用途说明和示例。

## Traceability
- 需求 1 到 4 由 `test_entrypoint.py` 的帮助页断言和人工抽查共同覆盖。
- `test_protocol_docs.py` 证明协议级文档与命令面保持一致。
- `check-tasks` 证明本轮 task package 本身没有破坏仓库协议。

## Risk Acceptance
- 当前接受的残余风险是：帮助页仍为静态文案，未来如果子命令行为变化而文案未同步，仍可能漂移。
- 这个风险目前可接受，因为已经把关键帮助文本纳入自动化测试，后续新增命令时只需沿用同一模式。

## Latest Result
- 最近一次验证已通过。帮助页测试、协议帮助测试和 `check-tasks` 都返回成功。
- Latest Artifact:
  - `docs/archived/task-packages/openharness-help-polish/04-verification.md`
