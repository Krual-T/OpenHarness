# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先用会失败的测试锁住两类变化，再做实现并跑回归。第一类是 `bootstrap` 文本输出变薄，不再前置打印 manifest 路径和 task package 根目录；第二类是 `AGENTS.md` 退出默认工作流和方法论，只保留仓库地图与少量仓库级约定，同时 README 继续退出重复流程教学。实现完成后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`、`uv run pytest tests/openharness_cases/test_protocol_docs.py -q`、`uv run pytest -q`、`uv run openharness check-tasks` 和 `uv run openharness bootstrap --json`。
- Executed Path: 第一波已经完成 `bootstrap` 文本减重和 `AGENTS.md` / README 收口。本次继续按 TDD 方式先修改 `tests/openharness_cases/test_protocol_docs.py`，把断言从“这些总述内容存在”改成“`using-openharness` 与 `skill-hub` 不再重复讲角色注入、stage gate、runtime capability 总述和 writing guidance 面”。确认新增断言先失败后，再实现第二波减重：收缩 `skills/using-openharness/SKILL.md`，删去 role-injection、stage-gate、challenge-closure 总述，保留入口路由、task package 读取顺序、runtime routing 和 archive protocol；同步把 `skills/using-openharness/references/skill-hub.md` 收回成技能目录与引用索引，不再复述写作 guidance 和 runtime contract 正文。随后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`、`uv run pytest tests/openharness_cases/test_protocol_docs.py -q`、`uv run pytest -q`、`uv run openharness check-tasks` 和 `uv run openharness bootstrap --json`，结果均通过。
- Path Notes: 第二波实现后，重复表面进一步收敛为“entry skill 讲入口协议，stage skill 讲阶段动作，reference 文档讲长篇 contract”。本轮同时复查了 `brainstorming`、`exploring-solution-space` 与 `verification-before-completion`，当前没有继续改动它们，因为它们已主要保留阶段内动作约束，而不再是本轮重复面的主源头。

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
  - `tests/openharness_cases/test_protocol_docs.py` 第一波检查 `AGENTS.md` 不再承载默认工作流和语言策略；第二波进一步检查 `using-openharness` 与 `skill-hub` 不再自己复述角色注入、stage gate、runtime contract 总述和 writing guidance 面
- `02-overview-design.md` 关于“入口变自然但不丢状态”的要求，对应到：
  - `openharness_cli/commands.py` 不再在 `bootstrap` 文本输出前置路径信息
  - `tests/openharness_cases/test_cli_workflows.py` 锁住更薄的输出表面
- `03-detailed-design.md` 关于“先测再改”的要求，对应到本轮先改协议测试并观察失败，再做 skill 文案收口，最后跑全量回归。
- 当前仍未归档的原因不是验证不足，而是本轮先把包保留在 `verifying`，等待你决定是否还要继续做第三波入口 discoverability 减面，或直接接受当前边界并归档。

## Risk Acceptance
- 当前接受的风险一：child skills 仍保留少量边界提醒语句，例如“不定义 task roots / stage flow / archive rules”。之所以可接受，是因为这些句子当前用于防止重新膨胀成并行协议，本轮复查后它们不再是主要重复负担。
- 当前接受的风险二：`bootstrap --json` 仍保留较完整的结构化字段。之所以可接受，是因为这属于机器消费接口，比文本输出更应该优先稳定，而不是先压缩。
- 当前接受的风险三：此前观察到的状态不一致现象，本轮没有继续当作独立 bug 修复。之所以可接受，是因为顺序执行后没有再复现，当前更像执行竞态带来的读旧值现象；若后续在串行执行下再次复现，应重新触发审查。

## Latest Result
- 最近一次验证结果为通过：
  - `uv run pytest tests/openharness_cases/test_cli_workflows.py -q` 通过，17 条测试全部成功。
  - `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 通过，51 条测试全部成功。
  - `uv run pytest -q` 通过，186 条测试全部成功。
  - `uv run openharness check-tasks` 通过，验证了 39 个 task package。
  - `uv run openharness bootstrap --json` 通过，串行执行时当前 active package 只剩 `OH-036` 与 `OH-037`，二者都正确显示为 `verifying`。
  - `using-openharness` 已不再承载角色注入、stage gate 和 challenge closure 的总述；这些 stage-specific 约束回到阶段 skill 和 guidance。
  - `skill-hub` 已不再重复讲 writing guidance surface 和 runtime contract 正文，而是只保留技能目录与引用索引。
- Latest Artifact:
- console output only
