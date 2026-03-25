# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先在 `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 中补 live sibling reference 与 retired skill path 的断言。
  - 再执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，验证新增断言先失败后通过。
  - 最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，并在归档后再次复核 task package 协议。
- Executed Path:
  - 已先补 `test_runtime_reference_docs_use_existing_sibling_paths` 与 `test_systematic_debugging_docs_do_not_advertise_retired_path` 两条断言。
  - 已先运行一次 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，确认新增断言因为旧路径与错误引用而失败。
  - 已修复 `skills/using-openharness/references/` 下三份 live docs 的 sibling path，并清理 `skills/systematic-debugging/` 下五份材料中的旧入口路径。
  - 已重新执行 `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`，确认 38 个测试全部通过。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，并在任务包移动到 `docs/archived/task-packages/skill-reference-path-cleanup/` 后继续复核归档状态。
- Path Notes:
  - 本轮采用严格的红绿流程：先写失败测试，再修文档，再跑 fresh verification。
  - `check-tasks` 只验证任务包协议，不覆盖 live docs 的具体引用有效性，因此需要与目标 `pytest` 搭配作为闭环。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- live runtime capability docs 中的关键交叉引用都能指向真实文件。
- 文本协议测试能在这些引用重新失效时直接失败。
- 任务包结构与状态写回通过 `check-tasks` 校验。

## Traceability
- `01-requirements.md` 定义了本轮只修 live surface 的真实失效路径，并要求补自动校验。
- `02-overview-design.md` 说明了采用“局部修复 + 轻量防回归”的结构，而不是做全仓库通用链接治理。
- `03-detailed-design.md` 指定了实施文件、断言落点和验证命令。
- 实际执行结果与设计一致：live runtime capability docs 的 sibling path 已收敛到当前目录可解析写法，`systematic-debugging` 维护材料已切换到当前真实入口，且两条必跑命令均已 fresh 通过。

## Risk Acceptance
- 当前接受的残余风险是：除已确认的 runtime capability 文档链路与 `systematic-debugging` 维护材料外，其他 live docs 里仍可能存在未被本轮白名单覆盖的低频路径漂移。
- 之所以可接受，是因为本轮已经把已知失效点修复并纳入自动断言；若后续出现跨目录同类问题，应再开新包扩展覆盖面，而不是在本包中继续膨胀范围。
- 如果后续发现 live surface 中有更多目录普遍存在同类错误，或需要跨目录统一解析 Markdown 路径，应重新开包评估是否抽象成通用校验器。

## Latest Result
- 最近一次结果为“passed”：`uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 显示 `38 passed in 0.10s`，`uv run python skills/using-openharness/scripts/openharness.py check-tasks` 显示已校验 25 个 task packages。
Latest Artifact: `docs/archived/task-packages/skill-reference-path-cleanup/06-evidence.md`
