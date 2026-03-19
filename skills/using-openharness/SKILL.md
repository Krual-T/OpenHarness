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
- when to invoke `writing-plans`
- when to run harness verification

All repo-facing workflow skills should be treated as subordinate to `openharness`, not as parallel systems.

## Skill Invocation Rule

Invoke relevant or requested repository skills before response or action.

Use this routing order:

1. `using-openharness` first for repository workflow and task-package protocol
2. process skills next, such as `brainstorming` or `systematic-debugging`
3. execution skills after that, such as `writing-plans`, `subagent-driven-development`, or `executing-plans`

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
    - `04-implementation-plan.md`
    - `05-verification.md`
    - `06-evidence.md`
5. Implement only after the design package is internally consistent enough to act on.

## Skill Routing

Use child skills under `using-openharness` like this:

- `brainstorming`
    - use when the task is still ambiguous, under-specified, or needs design convergence
    - output goes into `01-requirements.md`, `02-overview-design.md`, and `03-detailed-design.md`
- `writing-plans`
    - use only when the task needs explicit staged execution beyond `03-detailed-design.md`
    - output goes into `04-implementation-plan.md`
- direct implementation
    - use when the package is already clear enough and no separate execution plan is needed

Default flow:

1. `openharness`
2. `brainstorming` if the design is not yet clear
3. `writing-plans` only if the task needs explicit execution slicing
4. implementation
5. verification and evidence updates

For non-package work that still touches repository workflow, start from `openharness`, decide whether a child skill applies, then continue under that child skill. Do not reintroduce a separate entry skill for this routing step.

## Update Protocol

- Keep `README.md` short; it is the human entrypoint.
- Keep `STATUS.yaml` machine-readable; it is the harness state source.
- Put problem framing in `01-requirements.md`.
- Put boundary and architecture choices in `02-overview-design.md`.
- Put file-level or protocol-level implementation details in `03-detailed-design.md`.
- Put explicit staged execution planning in `04-implementation-plan.md` when the task needs it.
- Put verification plan and results in `05-verification.md`.
- Put changed files, commands, and remaining follow-ups in `06-evidence.md`.

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
- `writing-plans` must not redefine requirements or architecture already owned by `01` to `03`.
- `04-implementation-plan.md` is part of the harness package, not an external planning artifact.

## Verification

- Run `scripts/openharness.py check-designs` before claiming completion.
- Run `scripts/openharness.py new-design <design_name> <design_id> <title>` to scaffold a new design package.
- Run `scripts/openharness.py verify <design-name-or-id>` when a package declares required commands.
- `openharness.py` is the single harness CLI; use its subcommands instead of introducing parallel wrapper scripts.
- If the package adds new reusable project knowledge, update `.project-memory/` in the same turn.
- If a completed package is archived, rerun harness validation after the move and confirm it no longer appears in the default `bootstrap` active-package list.
