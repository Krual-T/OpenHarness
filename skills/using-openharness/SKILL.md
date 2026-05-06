---
name: using-openharness
description: Use when starting any conversation - establishes how to find and use repository workflow skills before ANY response including clarifying questions.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill unless the task is explicitly about repository harness protocol.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a repository skill applies, you must invoke the relevant skill before responding or acting.

`using-openharness` is the first repository workflow skill to check whenever work may affect task packages, task docs, verification flow, repo protocol, or skill routing.
</EXTREMELY-IMPORTANT>

# Using OpenHarness

## Skill Role

- Protocol status: core protocol skill
- Primary stage: entry and routing
- Trigger: default first skill for repository workflow, task-package protocol, and skill routing

## Intent

Use this skill to work inside repositories that organize tasks as end-to-end `task package` records under `docs/task-packages/<task>/` rather than a centralized task board.

## Supporting Files

`openharness` owns the canonical harness runtime support files under:

- `references/templates/`
- `references/requirements-writing-guidance.md`
- `references/overview-design-writing-guidance.md`
- `references/detailed-design-writing-guidance.md`
- `references/verification-writing-guidance.md`
- `references/evidence-writing-guidance.md`
- `references/author-entry.md`
- `references/skill-hub.md`
- `references/runtime-capability-contract.md`
- `references/runtime-workflow-packages.md`

OpenHarness repository self-tests live under the top-level `tests/` tree, not under the skill directory.

## Role

`openharness` is the parent workflow skill for this repository's skill hub.

It is also the repository entry skill.
Do not look for or preserve a parallel entry layer inside this repo.

It decides:

- whether a repository or process skill applies before any response
- where task truth lives
- which package must be read and updated
- when to stay in task-package docs
- when to invoke `brainstorming`
- when to invoke `exploring-solution-space`
- when runtime work should use a Runtime Workflow Package (RWP), record a missing RWP gap, or keep the task code-only
- when to run harness verification

All repo-facing workflow skills should be treated as subordinate to `openharness`, not as parallel systems.

## Skill Invocation Rule

Invoke relevant or requested repository skills before response or action.

Use this routing order:

1. `using-openharness` first for repository workflow and task-package protocol
2. process skills next, such as `brainstorming`, `exploring-solution-space`, or `systematic-debugging`
3. execution skills after that, such as `subagent-driven-development`

If a skill applies, use it. Do not bypass it by improvising a parallel workflow.

Repository entry-skill responsibilities live here:

- check for applicable skills before any response, including clarifying questions
- announce the skill being used and why
- follow the selected skill's checklist instead of freeforming a second workflow
- treat user instructions and `AGENTS.md` as higher priority than skill defaults

## Entry Protocol

Before choosing the first visible action, decide whether active task context is actually needed before foregrounding `openharness bootstrap`.

1. Read `references/manifest.yaml` to discover the required task-package structure.
2. Decide whether the user is primarily asking to continue active task-package work, inspect current workflow state, or choose among active packages.
3. Only foreground `openharness bootstrap` when the next action depends on active task-package state.
4. When active task context is not the current task axis, `openharness bootstrap` may stay background-only while you first inspect the repository surface that actually matches the request.
5. If you do need active task context, run `openharness bootstrap` to list active task packages.
6. If the user needs a Chinese-first writing entrypoint, open `references/author-entry.md` before diving into individual stage guidance docs.
7. Run `openharness` from the project root by default. If you are currently in a subdirectory, pass `--repo <project-root>` explicitly.
8. Open the chosen package in this order:
    - `README.md`
    - `STATUS.yaml`
    - `01-requirements.md`
    - `02-overview-design.md`
    - `03-detailed-design.md`
    - `04-verification.md`
    - `05-evidence.md`
9. Implement only after the task package is internally consistent enough to act on.

## Task Classification And Design Review Mode

`STATUS.yaml` may contain optional machine-readable collaboration state:

```yaml
collaboration:
  task_type: protocol/architecture
  design_review_mode: stepwise
```

`collaboration.task_type` is written only after the human confirms the task classification.
Valid values are `mechanical`, `standard development`, and `protocol/architecture`.
If the field is absent, do not treat the classification as confirmed.
Before entering `02-overview-design.md` or `03-detailed-design.md`, if `collaboration.task_type` is absent, propose one classification and wait for human confirmation before using the classification to choose the design flow.

`collaboration.design_review_mode` is written only after the human confirms the design-stage collaboration mode.
Valid values are `stepwise` and `auto`.
If the field is absent for a non-mechanical task entering design, propose the mode instead of assuming it.

When a development task is not clearly mechanical and is about to enter `02-overview-design.md` or `03-detailed-design.md`, proactively offer stepwise design confirmation.
Use this shape:

```text
这个任务已确认属于 <classification>。接下来会进入 <overview/detailed> 设计阶段。

我建议按逐项设计确认推进：我会每次提出一个设计点，包含推荐方案、理由、影响范围和确认问题；你确认后我写回 task package，再进入下一个点。

当前预计有 N 个设计点。先从 1/N 开始。
```

For `mechanical` tasks, do not default to stepwise confirmation; state that the task is mechanical, then modify and verify directly.
For `standard development` tasks, proactively offer stepwise confirmation before design, while allowing the human to choose coarser granularity or `auto`.
Coarser design-point granularity is still `stepwise`; only write `auto` when the human authorizes the agent to continue without stopping at each point.
For `protocol/architecture` tasks, default to stepwise confirmation unless the human explicitly authorizes `auto`.

This section only owns entry-time interpretation and routing.
The task classification rule lives in `brainstorming`; stepwise execution rules live in `exploring-solution-space`.

When you enter a new workflow stage, explicitly tell the user:

- current stage
- what was just completed
- next planned step

When reporting that stage context to the user, translate workflow state into natural task-oriented language.

- Keep the update centered on the user request, the key fact you just established, and the next move that follows from it.
- Do not paste raw execution logs, path dumps, or tool-status labels into the main reply.
- Avoid presenting `Explored`, `Ran ...`, or similar command-playback markers as the headline structure of the user-visible update.

If no package exists and brainstorming has just converged enough to hand off into exploration, scaffold the package first, then report the new package path and continue.

## Runtime Capability Routing

When a task depends on real runtime behavior rather than code-only changes, `using-openharness` should route through the Runtime Workflow Package (RWP) protocol instead of improvising a universal debug flow.

Use this runtime routing loop:

1. Check whether the task is code-only or requires runtime-aware verification.
2. If runtime-aware verification may apply, prefer assigning a subagent to run `openharness rwp list` and select candidate RWPs from the summary descriptions.
3. Have the subagent use `openharness rwp show <workflow>` only for strong candidates, then report the recommended RWP, rejected near matches, and writeback points.
4. Record the selected RWP or the missing-RWP gap in `03-detailed-design.md`; do not leave the decision only in chat.
5. During verification, run the chosen workflow script with `openharness rwp run <workflow> <script.py> [args...]` when prerequisites allow it.
6. Write executed commands, stdout/stderr summaries, runtime observations, blockers, artifact paths, and residual risks back into `04-verification.md` and `05-evidence.md`.

## Skill Routing

Use child skills under `using-openharness` like this:

- `brainstorming`
    - use when the task is still ambiguous, under-specified, or needs requirements convergence
    - primary output goes into `01-requirements.md`
    - Chinese-first routing should also point the author at `references/author-entry.md` and then `references/requirements-writing-guidance.md`
- `exploring-solution-space`
    - use after requirements are clear and before architecture or implementation details are locked in
    - combines local repository exploration with web research when external/current information matters
    - writes architectural conclusions into `02-overview-design.md` first, and only feeds implementation constraints into `03-detailed-design.md` when exploration has made them concrete enough
    - Chinese-first routing should also point the author at `references/author-entry.md`, then `references/overview-design-writing-guidance.md` or `references/detailed-design-writing-guidance.md` as needed
- direct implementation
    - use only when `01`, `02`, and `03` are already clear enough

Default flow:

1. `openharness`
2. `brainstorming` to converge and write `01-requirements.md`
3. `exploring-solution-space` to explore local code and the web before architecture is locked
4. draft `02-overview-design.md`
5. let the stage skill finish its reflection pass before treating the design as ready
6. draft `03-detailed-design.md` only after the explored architecture is coherent enough to constrain implementation
7. let the detailed-design stage close its own open challenges before execution
8. move to `in_progress` only when the package is ready to execute against a stable detailed design
9. move to `verifying` only when implementation is complete enough to gather fresh verification evidence
10. update verification and evidence before `archived`, and archive only after implementation is done and verified

For non-package work that still touches repository workflow, start from `openharness`, decide whether a child skill applies, then continue under that child skill. Do not reintroduce a separate entry skill for this routing step.

## Update Protocol

- task-package Markdown narrative should be Chinese-first for maintainer readability.
- In phase one, section titles, commands, status values, YAML keys, file names, and paths stay English.
- Use the stage-matched writing guidance when you need to know how to write a task-package document:
  - `references/author-entry.md` as the Chinese-first author routing page
  - `references/requirements-writing-guidance.md` for `01-requirements.md`
  - `references/overview-design-writing-guidance.md` for `02-overview-design.md`
  - `references/detailed-design-writing-guidance.md` for `03-detailed-design.md`
  - `references/verification-writing-guidance.md` for `04-verification.md`
  - `references/evidence-writing-guidance.md` for `05-evidence.md`
- Keep skill text focused on stage actions rather than duplicating long-form writing guidance.
- Keep `README.md` short; it is the human entrypoint.
- Keep `STATUS.yaml` machine-readable; it is the harness state source.
- Put problem framing in `01-requirements.md`.
- Put boundary and architecture choices in `02-overview-design.md`.
- Put implementation details, object-appropriate testing or verification order, runtime verification path, fallback path, and implementation order in `03-detailed-design.md`.
- Record the overview reflection pass in `02-overview-design.md`.
- Record the detailed-design reflection pass in `03-detailed-design.md`.
- Put planned versus executed verification path and results in `04-verification.md`.
- Put changed files, commands, manual steps, residual risks, and remaining follow-ups in `05-evidence.md`.
- Keep `STATUS.yaml.status` aligned with the highest workflow checkpoint that is actually complete; later statuses imply earlier checkpoints are already materially complete.

## Archive Protocol

- Active work lives under `docs/task-packages/<task>/`.
- Completed task packages that should no longer appear in active work move to `docs/archived/task-packages/<task>/`.
- Before moving a completed package, update `04-verification.md` and `05-evidence.md`, then set `STATUS.yaml.status` to `archived` and refresh `updated_at`.
- After moving the package, update package-local entrypoints/evidence paths and any repository references that still point to the old active location.
- Archived packages remain historical fact sources and verification evidence, but they must not remain in the active task root.
- `archived` should mean the task package is implemented, verified, and no longer active, not merely design-complete or relocated.

## Boundary Rules

- `openharness` defines the repository protocol and skill order.
- `openharness` is the only repository entry skill; do not maintain a second entry root.
- runtime capability routing belongs in `openharness`, while project-specific Runtime Workflow Packages remain project-level extensions under `.harness/rwp/workflows/`.
- `brainstorming` must not invent a parallel spec system or a second task root.
- `exploring-solution-space` must not become a parallel task system; it exists to produce `02` first and only then inform `03` where justified.
- `03-detailed-design.md` owns implementation design plus object-appropriate testing or verification order inside the fixed package protocol; this does not mean writing tests before detailed design.
- Design is not ready after a first draft alone; `02` and `03` each require a reflection pass before they are treated as ready.
- Stage-specific rules belong in the matching stage skill, not here.

## Verification

- Run `openharness check-tasks` before claiming completion.
- Run `openharness new-task <task_name> --task-id <task-id> --title <title>` to scaffold a new task package.
- Run `openharness update` to refresh the OpenHarness clone and installed CLI after setup. If the global command is not installed yet, fall back to the documented manual update steps.
- Run `openharness verify <task-name-or-id>` when a package declares required commands.
- `openharness` is the only documented harness CLI entry for workflow instructions.
- For Python-first repositories, prefer `uv run ...` commands unless the repository documents a stronger automated path.
- Do not treat that Python floor as full runtime evidence; project-specific runtime verification still belongs in task packages.
- If the package adds new reusable project knowledge, update `.project-memory/` in the same turn.
- If a completed package is archived, rerun harness validation after the move and confirm it no longer appears in the default `bootstrap` active-package list.
