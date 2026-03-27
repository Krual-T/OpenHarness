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
- `references/project-runtime-surface-map.md`
- `references/adding-project-runtime-helper.md`

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
- when stage-organized role injection is required versus optional
- when runtime work should reuse an existing helper, add one new narrow helper, or open a bootstrap package
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

When a task depends on real runtime behavior rather than code-only changes, `using-openharness` should route through the runtime capability contract instead of improvising a universal debug flow.

Use this runtime routing loop:

1. Check whether the task is code-only or requires runtime-aware verification.
2. Look for the repository's runtime capability contract, project runtime surface map, linked helper guidance, and helper-addition guidance.
3. If a matching runtime surface exists and a linked helper already fits the task, reuse the linked project runtime helper and write the planned plus executed evidence back into the active task package.
4. If the surface exists but helper coverage is missing, add one new narrow helper, link it from the runtime surface map, and record the helper contract plus writeback plan in the active task package.
5. If no matching capability exists or the surface is still underspecified, open or update a bootstrap package for that runtime surface before claiming runtime verification coverage.
6. Keep project runtime helpers optional and narrow. One repository may host multiple runtime helper skills, but they must not become parallel entry skills.

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
5. run an overview reflection pass with role injection and stage gates; use bounded subagent discussion when the architecture is high-impact, uncertain, or hard to compare against alternatives
6. draft `03-detailed-design.md` only after the explored architecture is coherent enough to constrain implementation
7. run a detailed-design reflection pass with role injection and challenge closure; use bounded subagent discussion when test strategy, module boundaries, migration risk, or runtime verification remain uncertain
8. move to `in_progress` only when the package is ready to execute against a stable detailed design
9. move to `verifying` only when implementation is complete enough to gather fresh verification evidence
10. update verification and evidence before `archived`, and archive only after implementation is done and verified

For non-package work that still touches repository workflow, start from `openharness`, decide whether a child skill applies, then continue under that child skill. Do not reintroduce a separate entry skill for this routing step.

## Stage-Organized Role Injection

OpenHarness keeps stages as the main axis and uses role injection inside those stages rather than building a second role-driven workflow.

- requirements convergence should inject the product perspective and CEO perspective
- overview design should inject the architecture perspective and, when still relevant, the product perspective
- detailed design should inject the architecture perspective and testing perspective
- verification should inject review perspective and risk perspective

Role injection is not free-form commentary. The main agent still owns the draft, while injected roles challenge the draft inside a bounded problem domain.

## Stage Gates

Stages are not ready just because the prose is longer. Each stage needs a gate before the package advances.

- requirements gate
  - target user and core scenario
  - single success metric
  - non-goals
  - cost cap
  - acceptance criteria
  - at least one counterexample
- overview gate
  - key constraints
  - boundary and interface decisions
  - key failure modes
  - degradation or rollback direction
- detailed gate
  - test strategy
  - observability requirements
  - implementation landing points
  - migration order
  - expected evidence types
- verification gate
  - requirement-to-verification traceability
  - residual risks
  - explicit risk acceptance reasoning

## Challenge Closure

Injected roles do not merely comment. Their substantive challenges must be closed before the stage can be treated as ready.

The main agent must handle each important challenge in one of three ways:

- accept it and turn it into a constraint
- reject it and record the reason plus the chosen alternative
- defer it with a trigger condition and latest allowed landing point

Do not advance a stage while material challenges still float without a recorded disposition.

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
- Put testing-first implementation details, runtime verification path, fallback path, and implementation order in `03-detailed-design.md`.
- Record stage gates in the design docs when they materially shape readiness.
- Record challenge closure when role injection or bounded subagent discussion changes the design.
- Record the overview reflection pass in `02-overview-design.md`, including when a bounded subagent discussion was used and what it changed.
- Record the detailed-design reflection pass in `03-detailed-design.md`, including when a bounded subagent discussion was used and what it changed.
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
- runtime capability routing belongs in `openharness`, but project-specific runtime helpers remain optional project-level extensions.
- `brainstorming` must not invent a parallel spec system or a second task root.
- `exploring-solution-space` must not become a parallel task system; it exists to produce `02` first and only then inform `03` where justified.
- `03-detailed-design.md` owns testing-first implementation detail inside the fixed package protocol.
- Design is not ready after a first draft alone; `02` and `03` each require a reflection pass before they are treated as ready.
- Role injection supports the stages; it must not replace the stages.
- Stage gates and challenge closure are part of readiness, not optional polish.
- Bounded subagent discussion is the preferred escalation path when reflection reveals uncertainty that the main agent cannot confidently resolve alone.

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
