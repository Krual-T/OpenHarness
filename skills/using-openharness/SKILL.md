---
name: using-openharness
description: Use when starting any conversation - establishes how to find and use repository workflow skills before ANY response including clarifying questions.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill unless the task is explicitly about repository harness protocol.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a repository skill applies, you must invoke the relevant skill before responding or acting.

`using-openharness` is the first repository workflow skill to check whenever work may affect task packages, design docs, verification flow, repo protocol, or skill routing.
</EXTREMELY-IMPORTANT>

# Using OpenHarness

## Intent

Use this skill to work inside repositories that organize tasks as `docs/designs/<task>/` packages rather than a centralized task board.

## Supporting Files

`openharness` owns the canonical harness support files under:

- `scripts/`
- `tests/`
- `references/templates/`
- `references/skill-hub.md`

## Role

`openharness` is the parent workflow skill for this repository's skill hub.

It is also the repository entry skill.
Do not look for or preserve a parallel entry layer inside this repo.

It decides:

- whether a repository or process skill applies before any response
- where task truth lives
- which package must be read and updated
- when to stay in package design docs
- when to invoke `brainstorming`
- when to invoke `exploring-solution-space`
- when to run harness verification

All repo-facing workflow skills should be treated as subordinate to `openharness`, not as parallel systems.

## Skill Invocation Rule

Invoke relevant or requested repository skills before response or action.

Use this routing order:

1. `using-openharness` first for repository workflow and task-package protocol
2. process skills next, such as `brainstorming`, `exploring-solution-space`, or `systematic-debugging`
3. execution skills after that, such as `subagent-driven-development` or `executing-plans`

If a skill applies, use it. Do not bypass it by improvising a parallel workflow.

Repository entry-skill responsibilities live here:

- check for applicable skills before any response, including clarifying questions
- announce the skill being used and why
- follow the selected skill's checklist instead of freeforming a second workflow
- treat user instructions and `AGENTS.md` as higher priority than skill defaults

## Entry Protocol

1. Read `AGENTS.md` first. Treat it as the repository map, not as the only fact source.
2. Read `references/manifest.yaml` to discover the required design-package structure.
3. Run `scripts/openharness.py bootstrap` to list active design packages.
4. Open the chosen package in this order:
    - `README.md`
    - `STATUS.yaml`
    - `01-requirements.md`
    - `02-overview-design.md`
    - `03-detailed-design.md`
    - `05-verification.md`
    - `06-evidence.md`
5. Implement only after the design package is internally consistent enough to act on.

## Skill Routing

Use child skills under `using-openharness` like this:

- `brainstorming`
    - use when the task is still ambiguous, under-specified, or needs requirements convergence
    - primary output goes into `01-requirements.md`
- `exploring-solution-space`
    - use after requirements are clear and before architecture or implementation details are locked in
    - combines local repository exploration with web research when external/current information matters
    - writes architectural conclusions into `02-overview-design.md` first, and only feeds implementation constraints into `03-detailed-design.md` when exploration has made them concrete enough
- direct implementation
    - use only when `01`, `02`, and `03` are already clear enough

Default flow:

1. `openharness`
2. `brainstorming` to converge and write `01-requirements.md`
3. `exploring-solution-space` to explore local code and the web before architecture is locked
4. draft `02-overview-design.md`
5. run an overview reflection pass; use bounded subagent discussion when the architecture is high-impact, uncertain, or hard to compare against alternatives
6. draft `03-detailed-design.md` only after the explored architecture is coherent enough to constrain implementation
7. run a detailed-design reflection pass; use bounded subagent discussion when test strategy, module boundaries, migration risk, or runtime verification remain uncertain
8. implementation and runtime verification
9. verification and evidence updates

For non-package work that still touches repository workflow, start from `openharness`, decide whether a child skill applies, then continue under that child skill. Do not reintroduce a separate entry skill for this routing step.

## Update Protocol

- Keep `README.md` short; it is the human entrypoint.
- Keep `STATUS.yaml` machine-readable; it is the harness state source.
- Put problem framing in `01-requirements.md`.
- Put boundary and architecture choices in `02-overview-design.md`.
- Put testing-first implementation details, runtime verification path, fallback path, and implementation order in `03-detailed-design.md`.
- Record the overview reflection pass in `02-overview-design.md`, including when a bounded subagent discussion was used and what it changed.
- Record the detailed-design reflection pass in `03-detailed-design.md`, including when a bounded subagent discussion was used and what it changed.
- Put planned versus executed verification path and results in `05-verification.md`.
- Put changed files, commands, manual steps, residual risks, and remaining follow-ups in `06-evidence.md`.

## Archive Protocol

- Active work lives under `docs/designs/<task>/`.
- Completed packages that should no longer appear in active work move to `docs/archived/designs/<task>/`.
- Before moving a completed package, update `05-verification.md` and `06-evidence.md`, then set `STATUS.yaml.status` to `archived` and refresh `updated_at`.
- After moving the package, update package-local entrypoints/evidence paths and any repository references that still point to the old active location.
- Archived packages remain historical fact sources and verification evidence, but they must not remain in the active design root.

## Boundary Rules

- `openharness` defines the repository protocol and skill order.
- `openharness` is the only repository entry skill; do not maintain a second entry root.
- `brainstorming` must not invent a parallel spec system or a second task root.
- `exploring-solution-space` must not become a parallel task system; it exists to produce `02` first and only then inform `03` where justified.
- `03-detailed-design.md` owns testing-first implementation detail inside the fixed package protocol.
- Design is not ready after a first draft alone; `02` and `03` each require a reflection pass before they are treated as ready.
- Bounded subagent discussion is the preferred escalation path when reflection reveals uncertainty that the main agent cannot confidently resolve alone.

## Verification

- Run `scripts/openharness.py check-designs` before claiming completion.
- Run `scripts/openharness.py new-design <design_name> <design_id> <title>` to scaffold a new design package.
- Run `scripts/openharness.py verify <design-name-or-id>` when a package declares required commands.
- `openharness.py` is the single harness CLI; use its subcommands instead of introducing parallel wrapper scripts.
- If the package adds new reusable project knowledge, update `.project-memory/` in the same turn.
- If a completed package is archived, rerun harness validation after the move and confirm it no longer appears in the default `bootstrap` active-package list.
