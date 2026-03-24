# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先用聚焦测试锁住新增行为：
    - `uv run pytest skills/using-openharness/tests/test_openharness.py -k "allocate_next_task_id or scaffolds_task_package_before_exploration_when_missing or requires_explicit_stage_checkpoints or bootstrap_reports_stage_guidance_in_text_output or bootstrap_json_includes_stage_guidance"`
  - 再跑完整 `skills/using-openharness/tests/test_openharness.py`，确认 CLI、模板、技能协议和历史断言都保持通过。
  - 最后运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 active 与 archived task package 仍满足协议。
- Executed Path:
  - 先运行了聚焦测试并确认 6 条相关测试通过。
  - 之后运行了完整 `uv run pytest skills/using-openharness/tests/test_openharness.py`，62 条测试全部通过。
  - 再运行 `uv run python skills/using-openharness/scripts/openharness.py verify workflow-stage-visibility-and-task-intake`，让 harness 按 `STATUS.yaml.verification.required_commands` 顺序执行聚焦测试、完整测试和 `check-tasks`，并写入 verification artifact。
- Path Notes:
  - 实际执行路径与计划路径一致，没有出现需要降级的阻塞。
  - 由于本轮变化同时触及脚本与 skill 文案，完整测试比只跑聚焦测试更重要；否则容易放过文案协议漂移。
  - 最终以 harness 自己生成的 artifact 作为归档前的机械证据，避免只在 `05-verification.md` 里口头声明通过。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "allocate_next_task_id or scaffolds_task_package_before_exploration_when_missing or requires_explicit_stage_checkpoints or bootstrap_reports_stage_guidance_in_text_output or bootstrap_json_includes_stage_guidance"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 聚焦测试能证明新增阶段提示、自动编号和技能 handoff 规则都被锁住。
- 完整 `test_openharness.py` 不出现回归。
- `check-tasks` 能验证 active / archived task package 均符合协议。
- harness verification artifact 的 `overall_result` 为 `passed`，并且记录的 `package_fingerprint` 与当前包一致。

## Traceability
- 需求 1“阶段可见性”对应：
  - `openharness.py` 新增阶段描述与下一步建议输出。
  - `test_bootstrap_reports_stage_guidance_in_text_output`
  - `test_bootstrap_json_includes_stage_guidance`
- 需求 2“自动编号”对应：
  - `allocate_next_task_id`
  - `cmd_new_task` 的 `--auto-id`
  - `test_allocate_next_task_id_uses_existing_prefix_and_width`
  - `test_cmd_new_task_supports_auto_id`
- 需求 3“脑暴结束再建包、阶段切换主动播报”对应：
  - `skills/brainstorming/SKILL.md`
  - `skills/using-openharness/SKILL.md`
  - `test_brainstorming_scaffolds_task_package_before_exploration_when_missing`
  - `test_using_openharness_requires_explicit_stage_checkpoints`
- 需求 4 和 5“兼容旧用法并补测试”对应：
  - 旧 `new-task task_name task_id title` 解析仍保留。
  - 完整 `skills/using-openharness/tests/test_openharness.py` 通过。

## Risk Acceptance
- 仍接受的风险一：阶段提示目前主要落在 CLI 和 skill 文案层，agent 是否始终按文案执行，还依赖上层运行环境遵守这些 skills。
- 仍接受的风险二：自动编号基于仓库现有 task id 的前缀统计与最大值递增，适合当前 OpenHarness 协议，但如果未来一个仓库混用多个同等重要前缀，可能还需要更明确的仓库级前缀配置。
- 这些风险目前可接受，因为本轮的目标是把主要摩擦收敛到可见、可测、可落包的水平，而不是一次性引入更重的审批或配置系统。

## Latest Result
- 最近一次 harness 验证结果为通过：聚焦测试、完整测试与 `check-tasks` 全部成功，artifact 总结果为 `passed`。
- Latest Artifact: `.harness/artifacts/OH-018/verification-runs/latest.json`
