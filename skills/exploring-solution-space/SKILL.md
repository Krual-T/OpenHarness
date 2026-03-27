---
name: exploring-solution-space
description: Use after requirements are clear to explore the local repository and the web before locking in architecture or implementation details.
---

# Exploring Solution Space

## Skill Role

- Protocol status: core protocol skill
- Primary stage: exploration and architecture
- Trigger: use after requirements are clear and before architecture or implementation details are locked

Use this skill after `brainstorming` has clarified the task and written `01-requirements.md`.

Its job is to make exploration explicit:

- inspect the local repository
- inspect relevant task packages and recent code
- search the web when external references or current best practices matter
- record the findings that actually change architecture, boundaries, or verification strategy

It does not define a second repository protocol. Repository-level stage flow, stage gates, and archive rules stay in `using-openharness`.
Use bounded subagent discussion only when the architecture remains high-impact, uncertain, or hard to compare after the main exploration pass.

## Output

The primary output of this skill is:

- `02-overview-design.md`

This skill may also feed justified implementation constraints into `03-detailed-design.md`, but only after the overview is coherent enough to constrain implementation.
`overview_ready` is the normal checkpoint once `02-overview-design.md` and its reflection pass are both coherent.
`detailed_ready` is the normal checkpoint once `03-detailed-design.md` and its detailed reflection are concrete enough to execute.

## Process

1. Read `01-requirements.md` and restate the concrete question being explored.
2. Explore the local repository for relevant code, docs, tests, and recent changes.
3. Search the web when the task touches third-party APIs, current platform behavior, existing public solutions, or recent best practices.
4. Summarize local constraints, viable options, and the recommended direction.
5. Gather the overview-stage facts needed to write `02-overview-design.md`: coverage surface, excluded surface, main structure, key boundaries, main flow, fallback direction, and at least one rejected alternative.
6. Write the architectural conclusion into `02-overview-design.md` using `references/overview-design-writing-guidance.md`, including the overview-gate items required by `using-openharness`.
7. Run an overview reflection pass: challenge the main path, compare at least one viable alternative, and check for missing verification implications.
8. Only after `02-overview-design.md` is coherent, gather the detailed-stage facts needed for `03-detailed-design.md`: verification path, fallback path, implementation landing points, interfaces, migration order, expected evidence, and failure modes.
9. Write implementation-facing conclusions into `03-detailed-design.md` using `references/detailed-design-writing-guidance.md`.
10. Run a detailed reflection pass focused on testing strategy, interfaces, migration order, and expected evidence.
11. If important challenges are still open, keep exploring and write the challenge closure back into the package instead of force-advancing the stage.

Use stage-organized role injection during exploration:
- architecture perspective to challenge boundaries, interfaces, and main-path complexity
- testing perspective to challenge observability, rollback clarity, and evidence shape
- risk perspective to challenge high-impact residual risks without expanding scope indefinitely

Keep a visible decision list in the task package when the exploration rejects or defers viable alternatives.
Important challenges must be closed explicitly: accept the constraint, reject it with a reason, or defer it with a trigger and latest landing point.

What this stage must make answerable:

- For overview:
  - this round covers what and explicitly does not cover what
  - the recommended structure is what
  - the main boundaries and main flow are what
  - the rejected alternative failed for what reason
- For detailed:
  - how the work will be verified
  - where the implementation will land
  - what can fail silently or expensively
  - what order the work and migration should follow

## Rules

- Do not skip local exploration.
- Do not skip web research when the information is time-sensitive or external.
- Prefer primary sources for technical choices.
- Keep exploration focused on the active task.
- Make the reasoning legible in repository artifacts, not only in chat.
- Treat `02-overview-design.md` as the main artifact of exploration.
- Do not treat `02-overview-design.md` or `03-detailed-design.md` as ready until the reflection pass is written down.
- Keep challenge closure visible in the task package.
- Do not treat a stage gate as satisfied just because the prose is longer.
- If `02-overview-design.md` or `03-detailed-design.md` still cannot answer the questions defined in their matching guidance files, keep exploring instead of advancing.
