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

## Output

The primary output of this skill is:

- `02-overview-design.md`

This skill may also feed justified implementation constraints into `03-detailed-design.md`, but only after the overview is coherent enough to constrain implementation.

## Process

1. Read `01-requirements.md` and restate the concrete question being explored.
2. Explore the local repository for relevant code, docs, tests, and recent changes.
3. Search the web when the task touches third-party APIs, current platform behavior, existing public solutions, or recent best practices.
4. Summarize local constraints, viable options, and the recommended direction.
5. Write the architectural conclusion into `02-overview-design.md`, including the overview-gate items required by `using-openharness`.
6. Run an overview reflection pass: challenge the main path, compare at least one viable alternative, and check for missing verification implications.
7. Only after `02-overview-design.md` is coherent, write implementation-facing conclusions into `03-detailed-design.md`.
8. Run a detailed reflection pass focused on testing strategy, interfaces, migration order, and expected evidence.
9. If important challenges are still open, keep exploring and write the challenge closure back into the package instead of force-advancing the stage.

## Rules

- Do not skip local exploration.
- Do not skip web research when the information is time-sensitive or external.
- Prefer primary sources for technical choices.
- Keep exploration focused on the active task.
- Make the reasoning legible in repository artifacts, not only in chat.
- Treat `02-overview-design.md` as the main artifact of exploration.
- Do not treat `02-overview-design.md` or `03-detailed-design.md` as ready until the reflection pass is written down.
- Keep challenge closure visible in the task package.
