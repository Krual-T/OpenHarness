# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认新的 task package、live docs 与 archive 协议没有破坏仓库健康度。
  - 再运行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，确认 README、skills 与文本断言同时收敛。
  - 最后运行 `uv run python skills/using-openharness/scripts/openharness.py verify capability-model-alignment`，把声明的验证命令落成标准 verification artifact。
  - 手工检查 README、`brainstorming`、`exploring-solution-space`、skill hub 与测试断言是否同时体现“浏览器可选、方法论优先”的能力模型。
- Executed Path:
  - 运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，通过。
  - 运行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，57 个测试全部通过。
  - 运行 `uv run python skills/using-openharness/scripts/openharness.py verify capability-model-alignment`，再次执行声明命令并记录 artifact。
  - 通过 bounded reviewer 审阅一轮需求与实现表面；审阅确认没有 blocker，并促成对测试脆弱性、流程图 wording 与状态语义的收敛。
  - 手工核对 README、skills 与测试，确认 visual companion 被压回可选工具边界，核心叙事转为设计、测试、review 和 multi-agent collaboration。
  - 把 package 移动到 `docs/archived/task-packages/capability-model-alignment/` 后，再次运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，通过。
  - 归档后运行 `uv run python skills/using-openharness/scripts/openharness.py bootstrap`，确认 active task package 列表为空，`OH-018` 不再出现在 active root。
  - 归档后再次运行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，57 个测试全部通过。
- Path Notes:
  - 本包的交付物是文本协议与测试保护层，不涉及浏览器 runtime、前端渲染或项目级 helper，因此不需要补浏览器运行时验证。
  - `verify` CLI 记录的 artifact 仍保留了执行时的包状态快照，这是可接受的，因为最终 archive 决策以本包文档、状态文件和归档后校验为准。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`

## Expected Outcomes
- task package 结构、状态与引用保持合法。
- README、核心技能与 skill hub 同时把方法论能力放到主叙事中。
- visual companion 仍可用，但不再被表述成默认前置步骤。
- 针对这轮能力模型的 pytest 断言全部通过。
- verification artifact 被记录到 `.harness/artifacts/OH-018/verification-runs/`。

## Latest Result
- 2026-03-24 最近一次验证结果为 `passed`。
- `check-tasks` 通过。
- `uv run pytest skills/using-openharness/tests/test_openharness.py` 通过，57 个测试全部通过。
- package 归档后，`bootstrap` 返回 `No matching task packages found.`，说明当前 active root 中已无活动包。
- Latest Artifact: `.harness/artifacts/OH-018/verification-runs/20260324T032344281959Z.json`
