# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- `OH-037` 虽已存在，但当前只处于需求层；如果后续有人跳过 `OH-036` 的正式结论，直接展开 `OH-037` 设计，仍可能把个人偏好重新包装成方案。
- 对固定 `reflection` 义务的收益判断，目前主要来自归档包中留下的结构变化与验证写回；如果后续需要更强证据，仍可能需要补真实会话级案例。
- 先前怀疑过 `bootstrap` 与 `STATUS.yaml` 可能存在阶段不一致，但本次串行验证没有复现，当前仍缺最小复现场景。

## Manual Steps
- 无额外人工运行时步骤。
- 若后续要补你个人真实使用案例，应在新的 follow-up 中单独记录，不混入本轮已有仓库事实。
- `OH-037` 在进入 overview 前，应先把本包列为事实前提，而不是重新做一轮泛评估。

## Files
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/README.md
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/STATUS.yaml
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/01-requirements.md
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/02-overview-design.md
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/03-detailed-design.md
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/04-verification.md
- docs/task-packages/openharness-evaluation-and-refactor-boundaries/05-evidence.md
- docs/archived/task-packages/workflow-transition-and-verification-artifacts/STATUS.yaml
- docs/archived/task-packages/workflow-transition-and-verification-artifacts/04-verification.md
- docs/archived/task-packages/workflow-transition-and-verification-artifacts/05-evidence.md
- docs/archived/task-packages/task-package-completion-semantics/STATUS.yaml
- docs/archived/task-packages/task-package-completion-semantics/02-overview-design.md
- docs/archived/task-packages/task-package-completion-semantics/03-detailed-design.md
- docs/archived/task-packages/task-package-completion-semantics/04-verification.md
- docs/archived/task-packages/task-package-completion-semantics/05-evidence.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/STATUS.yaml
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/02-overview-design.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/03-detailed-design.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/04-verification.md
- docs/archived/task-packages/workflow-stage-visibility-and-task-intake/05-evidence.md
- docs/archived/task-packages/workflow-redesign/STATUS.yaml
- docs/archived/task-packages/workflow-redesign/02-overview-design.md
- docs/archived/task-packages/workflow-redesign/03-detailed-design.md
- docs/archived/task-packages/workflow-redesign/04-verification.md
- docs/archived/task-packages/workflow-redesign/05-evidence.md
- docs/archived/task-packages/python-verification-maturity/STATUS.yaml
- docs/archived/task-packages/python-verification-maturity/02-overview-design.md
- docs/archived/task-packages/python-verification-maturity/03-detailed-design.md
- docs/archived/task-packages/python-verification-maturity/04-verification.md
- docs/archived/task-packages/python-verification-maturity/05-evidence.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/STATUS.yaml
- docs/archived/task-packages/maintenance-and-entropy-reduction/04-verification.md
- docs/archived/task-packages/maintenance-and-entropy-reduction/05-evidence.md
- docs/archived/task-packages/skill-protocol-deduplication/STATUS.yaml
- docs/archived/task-packages/skill-protocol-deduplication/02-overview-design.md
- docs/archived/task-packages/skill-protocol-deduplication/03-detailed-design.md
- docs/archived/task-packages/skill-protocol-deduplication/04-verification.md
- docs/archived/task-packages/skill-protocol-deduplication/05-evidence.md
- https://github.com/obra/superpowers
- https://github.com/Fission-AI/OpenSpec
- https://github.com/github/spec-kit
- https://openai.com/index/harness-engineering/
- https://platform.openai.com/docs/guides/agent-evals
- https://github.com/openai/openai-agents-python
- https://www.anthropic.com/engineering/building-effective-agents
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## Commands
- `openharness bootstrap`
- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' skills/using-openharness/references/manifest.yaml`
- `sed -n '1,260p' skills/exploring-solution-space/SKILL.md`
- `sed -n '1,240p' README.md`
- `sed -n '1,260p' openharness_cli/commands.py`
- `sed -n '1,320p' openharness_cli/validation.py`
- `sed -n '1,320p' openharness_cli/lifecycle.py`
- `uv run openharness check-tasks`
- `uv run pytest -q`
- `uv run openharness new-task openharness-evaluation-and-refactor-boundaries --auto-id --title "OpenHarness Evaluation And Refactor Boundaries" --owner codex --summary "Objectively evaluate OpenHarness against internal evidence and external comparators, then define the next refactor boundary without compatibility-preserving design."`
- `uv run openharness transition openharness-evaluation-and-refactor-boundaries overview_ready`
- `uv run openharness transition openharness-evaluation-and-refactor-boundaries detailed_ready`
- `uv run openharness transition openharness-evaluation-and-refactor-boundaries in_progress`
- `uv run openharness transition openharness-evaluation-and-refactor-boundaries verifying`
- `uv run openharness check-tasks`
- `uv run openharness bootstrap --json`
- `final verification command: uv run openharness check-tasks`

## Artifact Paths
- 无独立 verification artifact。
- 当前证据位置主要在本 task package 文档和归档 task package 文档中。

## Assessment Matrix
- 内部案例对“减少假完成”的结论最强，主要来自 `workflow-transition-and-verification-artifacts`、`task-package-completion-semantics`、`python-verification-maturity`。
- 内部案例对“固定 reflection 是否必要”的结论较弱，但对“明确 stage gate 和语义约束比增加制度文本更有效”的结论较强，主要来自 `workflow-stage-visibility-and-task-intake`、`skill-protocol-deduplication`、`maintenance-and-entropy-reduction`。
- 外部对照支持的不是“照搬别人的结构”，而是两个更窄的判断：
  - OpenAI / Anthropic 都强调评估、工具、技能、观察与迭代修正，但没有支持把大量重复制度文本铺在多个入口表面。
  - `superpowers`、`OpenSpec`、`spec-kit` 各自覆盖执行增能或 spec 驱动协作的一部分，但都没有直接替代 OpenHarness 的仓库内 archive / evidence 闭环。
- 因此正式评估结论是：
  - OpenHarness 值得保留的不是“流程感”，而是“带证据的完成闭环”。
  - OpenHarness 下一轮最该减掉的不是验证，而是重复解释验证的制度表面。
- 当前 fresh verification 没有再次观察到 `bootstrap --json` 与 `STATUS.yaml` 不一致，因此这部分仍应视为待复核的历史怀疑，而不是本次新增证据。

## Follow-ups
- `OH-037` 仅在 `OH-036` 被接受为事实源后，才进入 `02-overview-design.md`；在此之前不要继续展开设计。
- 基于本包结论，下一轮 focused package 的主题应围绕“协议减重与入口重组”，而不是继续补更多 guidance。
- 单独调查 `openharness transition` 成功后 `bootstrap` / `bootstrap --json` 仍读到旧阶段的原因，判断是否为真实 CLI 缺陷。
- 如果后续需要更强的收益证据，再补充你个人真实使用案例，但不要让它替代已有仓库事实源。
