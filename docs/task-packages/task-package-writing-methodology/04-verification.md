# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 删除原先的总指南 `task-package-writing-guide.md`。
  - 新增五份分文档 guidance，并把它们分别接入 `using-openharness`、`brainstorming`、`exploring-solution-space`、`verification-before-completion` 和 `skill-hub`。
  - 基于调研和 5 个子智能体的分文档评估，把 guidance 从“问题清单”升级为“章节映射 + 最低判定 + Exit Check”的方法论文档。
  - 运行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q` 验证 guidance 存在、总指南已删除、每份 guidance 都具备新的方法论骨架，并且相应 skill 已接入新 guidance。
  - 运行 `uv run openharness check-tasks` 验证 `OH-033` 在完成本轮实现后仍满足 task package 协议。
- Executed Path:
  - 已执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`。
  - 已执行 `uv run openharness check-tasks`。
- Path Notes:
  - 本轮验证覆盖了五份 guidance 文件存在、旧总指南已删除、阶段 skill 已接入对应 guidance、每份 guidance 都具有 `Section Mapping` 和 `Exit Check`，以及 task package 协议未被破坏。
  - 当前没有把模板升级成长篇教程，而是继续保持模板短提示定位，把更强的方法论压到 guidance 中。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run openharness check-tasks

## Expected Outcomes
- 协议文档测试通过，证明分阶段 guidance 已成为正式仓库表面的一部分，并且旧总指南已被移除。
- 协议文档测试通过，证明五份 guidance 已不再只是问题清单，而是包含章节映射、最低判定和阶段出口检查。
- `check-tasks` 通过，证明 `OH-033` 在完成本轮实现后没有破坏 task package 校验。

## Traceability
- 需求要求补齐 task package 文档写作方法论，并把阶段动作与文档写法拆开。
- 最新设计把方法论落点收敛为五份分文档 guidance，并要求 skill 明确阶段信息采集要求和必答问题。
- 这轮深化实现把 guidance 进一步升级为“问题清单 + Section Mapping + Minimum Acceptable Shape + Exit Check”的可执行结构。
- 本轮验证通过测试证明五份 guidance 文件存在、旧总指南已删除、对应 skill 已引用新 guidance，且新的方法论骨架已经落地。
- `check-tasks` 通过，说明仓库协议和 task package 结构仍然成立。

## Risk Acceptance
- 当前接受的风险是：模板本身仍然只提供短提示，没有直接内嵌 guidance 的章节映射或 Exit Check，因此作者仍需通过 skill 或 reference 进入完整方法论。
- 之所以可以接受，是因为这正是本轮设计选择的职责边界，而不是遗漏。
- 如果后续发现作者仍频繁写出空壳文档，再考虑增强模板提示或增加更强校验。

## Latest Result
- 最近一次验证已通过：协议文档测试通过，`check-tasks` 通过。
- Latest Artifact:
- console output only
