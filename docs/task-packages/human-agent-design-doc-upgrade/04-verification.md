# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先修改协议测试，使其要求新的 human-agent 设计 contract 和 `PlantUML` 提示。
  - 再修改 guidance/template，让新增断言转绿。
  - 最后运行完整回归命令 `uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py`。
- Executed Path:
  - 已执行针对新增 contract 的定向测试：
    - `uv run pytest tests/openharness_cases/test_protocol_docs.py -k "task_package_writing_guidance_references_define_stage_contracts or design_package_templates_include_verification_path_sections"`
    - `uv run pytest tests/openharness_cases/test_task_package_core.py -k live_templates_scaffold_human_agent_design_prompts`
  - 已执行完整回归命令：
    - `uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py`
  - 已尝试执行 `openharness verify human-agent-design-doc-upgrade` 生成正式 harness artifact，但整仓验证被另一个无关 active package `project-memory-cli-integration` 的损坏 `STATUS.yaml` 阻塞。
- Path Notes:
  - 定向测试先失败后转绿，证明新增 contract 不是空转文案。
  - 完整回归覆盖 guidance 引用、模板文本、`new-task` 脚手架和相关 CLI 工作流，足以支撑本轮“写作 contract 已生效”的结论。
  - `openharness verify` 的失败不是本包测试失败，而是整仓发现无关 package YAML 解析错误；该 blocker 不应被伪装成本包实现回归。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py

## Expected Outcomes
- `test_protocol_docs.py` 中与 overview/detailed guidance、template 相关的断言全部通过。
- `test_cli_workflows.py` 继续通过，说明模板增强没有破坏现有协议工作流。
- `test_task_package_core.py` 中新的 live scaffold 探针通过，说明 `openharness new-task` 会真实产出新 contract。
- 如果仓库里没有无关坏包，`openharness verify human-agent-design-doc-upgrade` 应能把同一条测试命令记录为正式 harness artifact。

## Traceability
- `01-requirements.md` 要求 overview/detailed contract 更适合人和 agent 协作开发，并正式纳入 `PlantUML` 图示建议。
- `02-overview-design.md` 决定同步增强 `02` 与 `03`，并把模块、接口、关键数据/状态模型与图示边界重新纳入设计文档 contract。
- `03-detailed-design.md` 规定了测试先行、修改文件面、接口边界、模块内部职责、数据语义和异常处理的落点。
- 测试证据对应关系：
  - `test_protocol_docs.py` 证明 guidance 和模板文本已经包含新 contract。
  - `test_task_package_core.py` 证明 live scaffold 会生成这些提示。
  - `test_cli_workflows.py` 证明现有 CLI 工作流未被破坏。
  - `openharness verify` 的失败路径本身也提供了 traceability：它证明当前整仓验证 blocker 位于无关 package，而不是本包设计文档改造。

## Risk Acceptance
- 本轮接受的残余风险是：仓库尚未对 `PlantUML` 图是否真的存在、是否语法正确做自动校验。
- 之所以可以接受，是因为本轮目标是先把 diagram 约束升级为正式 guidance/template contract，而不是同时引入新的渲染或 lint 工具链。
- 重新触发审查的条件是：未来出现多个 package 明显依旧缺图、或图示质量问题反复导致误解时，再考虑增加更强校验。
- 另外一个暂时接受的外部风险是：当前仓库存在无关 active package 的 YAML 损坏，导致 harness 级验证暂时不能作为本包 closure 的唯一证据。

## Latest Result
- 最近一次完整回归命令执行通过，结果为 `91 passed`。
- 定向测试也都按预期先失败后转绿，说明新增 contract 真实进入了 guidance 与模板。
- 最近一次 `openharness verify human-agent-design-doc-upgrade` 未通过，原因是无关 package `project-memory-cli-integration/STATUS.yaml` 解析失败，而不是本包测试回归。
- Latest Artifact:
  - `.harness/artifacts/OH-038/verification-runs/20260330T080539614631Z.json`
