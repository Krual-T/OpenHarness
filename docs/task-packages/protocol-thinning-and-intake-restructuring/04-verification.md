# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先用会失败的测试锁住两类变化，再做实现并跑回归。第一类是 `bootstrap` 文本输出变薄，不再前置打印 manifest 路径和 task package 根目录；第二类是 `AGENTS.md` 退出默认工作流和方法论，只保留仓库地图与少量仓库级约定，同时 README 继续退出重复流程教学。实现完成后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`、`uv run pytest tests/openharness_cases/test_protocol_docs.py -q`、`uv run pytest -q`、`uv run openharness check-tasks` 和 `uv run openharness bootstrap --json`。
- Executed Path: 已先修改 `tests/openharness_cases/test_cli_workflows.py` 与 `tests/openharness_cases/test_protocol_docs.py`，并确认新增断言先失败；随后实现了 `openharness_cli/commands.py`、`README.md`、`AGENTS.md` 的对应改动；本次接手后又依次重新执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`、`uv run pytest tests/openharness_cases/test_protocol_docs.py -q`、`uv run pytest -q`、`uv run openharness check-tasks` 和 `uv run openharness bootstrap --json`，结果均通过。
- Path Notes: 本轮继续确认了 `AGENTS.md` 的职责边界应当更窄：它只保留仓库地图和仓库级约定，不再承载默认工作流、方法论或 task package 结构协议。这样可以把流程编排稳定收回 `using-openharness`，但还不足以宣称所有重复协议表面都已清空。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`
- `uv run pytest -q`
- `uv run openharness check-tasks`
- `uv run openharness bootstrap --json`

## Expected Outcomes
- `bootstrap` 文本输出保留 active task 和阶段信息，但不再前置打印 manifest 路径和 task package 根目录。
- README 不再充当完整流程手册，`AGENTS.md` 回到仓库地图与仓库级约定。
- 新增协议测试通过，说明上述减重没有破坏仓库入口约束。
- 全量测试与 `check-tasks` 通过，说明这轮调整没有破坏现有协议与实现。

## Traceability
- `01-requirements.md` 关于“减少重复协议表面”的要求，对应到：
  - `README.md` 删去重复的反思流程教学
  - `AGENTS.md` 收回到仓库地图、`Python / uv` 约定、提交要求和信息输出要求，不再描述 task package 结构协议
  - `tests/openharness_cases/test_protocol_docs.py` 更新为检查 `AGENTS.md` 不再承载默认工作流和语言策略，而这些内容继续留在 `using-openharness`
- `02-overview-design.md` 关于“入口变自然但不丢状态”的要求，对应到：
  - `openharness_cli/commands.py` 不再在 `bootstrap` 文本输出前置路径信息
  - `tests/openharness_cases/test_cli_workflows.py` 锁住更薄的输出表面
- `03-detailed-design.md` 关于“先测再改”的要求，对应到本轮先改测试并观察失败，再做实现，再跑全量回归。
- 当前缺口是：`using-openharness` 与 child skills 的进一步减重尚未落地，因此本包虽已具备 fresh verification evidence，但还不能直接归档。

## Risk Acceptance
- 当前接受的风险一：entry skill 与 child skills 仍有一部分制度说明没有收干净。之所以可接受，是因为这轮先解决了更硬的入口表面和仓库地图问题，而且相关 follow-up 已经明确。
- 当前接受的风险二：`bootstrap --json` 仍保留较完整的结构化字段。之所以可接受，是因为这属于机器消费接口，比文本输出更应该优先稳定，而不是先压缩。
- 当前接受的风险三：此前观察到的状态不一致现象，本轮没有继续当作独立 bug 修复。之所以可接受，是因为顺序执行后没有再复现，当前更像执行竞态带来的读旧值现象；若后续在串行执行下再次复现，应重新触发审查。

## Latest Result
- 最近一次验证结果为通过：
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q` 通过，17 条测试全部成功。
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 通过，51 条测试全部成功。
  - `uv run pytest -q` 通过，186 条测试全部成功。
  - `uv run openharness check-tasks` 通过，验证了 39 个 task package。
  - `uv run openharness bootstrap --json` 通过，串行执行时当前能正确把 `OH-037`、`OH-036`、`OH-033` 都读为 `verifying`。
  - `AGENTS.md` 已不再承载默认工作流、方法论与 task package 结构协议，相关职责现在明确保留在 `using-openharness` 与 `manifest.yaml`。
- Latest Artifact:
- console output only
