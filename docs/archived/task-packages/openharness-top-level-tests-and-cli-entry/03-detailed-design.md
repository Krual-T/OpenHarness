# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先把聚合测试入口和若干路径断言改到顶层 `tests/`，让相关测试先红后绿。
  - 执行 `uv run pytest tests/openharness_cases/test_entrypoint.py`
  - 执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py`
  - 执行 `uv run pytest tests/openharness_cases/test_task_package_core.py`
  - 执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py`
  - 执行 `uv run openharness check-tasks`
- Fallback Path:
  - 如果某一组测试因迁移路径失败，需要先修复导入和路径假设；在没有 fresh verification evidence 前不能宣称完成。
- Planned Evidence:
  - 顶层 `tests/` 新路径下的通过记录。
  - 删除兼容脚本后的工作树 diff。
  - `docs/archived/legacy/skills/using-openharness/...` 历史快照路径。
  - `check-tasks` 通过记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `pyproject.toml`：把 `pytest` 默认测试路径改到顶层。
- `tests/`：承接 OpenHarness 仓库自测。
- `openharness_cli/__init__.py` 等导出文件：必要时补齐测试可直接导入的表面。
- `skills/using-openharness/scripts/openharness.py`：删除。
- `docs/archived/legacy/skills/using-openharness/`：保存被移除旧树的历史快照，供 archived package 引用校验使用。
- 活跃协议文档与自测文档：改到新测试路径和新 CLI 入口。

## Interfaces
- 正式 CLI 入口是 `openharness_cli.main:main` 与 `python -m openharness_cli.main`。
- 顶层测试直接依赖 `openharness_cli` 的公开导出，不再依赖 skill 脚本桥接。
- `skills/using-openharness/references/` 仍然是 skill runtime 资产，不参与这轮迁移。
- archived package 的引用校验允许回退到 `docs/archived/legacy/<原路径>`。

## Stage Gates
- 必须先让顶层测试路径存在并可以被 `pytest` 发现。
- 必须删掉兼容脚本，而不是只停止引用它。
- 必须同步更新至少所有活跃文档与当前测试中的旧路径引用。
- 必须确认 `check-tasks` 可以在不改旧 archived package 内容的前提下继续通过。

## Decision Closure
- 接受：把测试迁到顶层 `tests/`，因为它们是仓库自测，不是 skill 运行时资产。
- 接受：删除兼容脚本，因为用户明确要求不要兼容。
- 接受：为 archived package 保留 legacy 快照回退，而不是修改旧 task package。
- 拒绝：保留脚本但只在文档中隐藏，因为这仍会继续制造双入口。

## Error Handling
- 如果删除脚本后有测试或文档仍然引用它，相关测试必须显式失败，不能静默保留死引用。
- 如果顶层测试迁移后导入失败，需要通过包导出或 `sys.path` 最小化调整修正，而不是恢复兼容脚本。
- 如果 archived package 引用旧路径，验证应当只在 archived 状态下回退到 legacy 快照；active package 不应享受这个回退。

## Migration Notes
- 先迁测试，再改 `pytest` 配置，再删脚本，最后清理文档与验证命令。
- 运行时没有兼容策略；删除脚本后，仓库内所有活跃引用都必须完成切换。
- 历史证据层通过 `docs/archived/legacy/` 保留快照，不要求逐个改旧包。
- 如果需要回滚，应整体回滚这一轮，而不是单独把脚本加回去。

## Detailed Reflection
- 这轮最大的风险不是删除脚本本身，而是路径迁移后留下很多隐式导入假设，所以验证必须覆盖路径断言、CLI 工作流和协议文档。
- 只要顶层测试和 `uv run openharness check-tasks` 都成立，就能证明兼容层已经不再是必要条件。
