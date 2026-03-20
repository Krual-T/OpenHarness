---
name: exploring-solution-space
description: Use after requirements are clear to explore the local repository and the web before locking in architecture or implementation details.
---

# Exploring Solution Space

## Overview

Use this skill after `brainstorming` has clarified the task and written `01-requirements.md`.

Its job is to make exploration explicit:

- inspect the local repository
- inspect relevant design packages and recent code
- search the web when external references or current best practices matter
- record the important findings that shape the architecture

## Output

This skill informs:

- `02-overview-design.md`
- `03-detailed-design.md`

Both documents must go through reflection before they are treated as ready.

## Process

1. Read `01-requirements.md` and restate the concrete question being explored.
2. Explore the local repository for relevant code, docs, tests, and recent changes.
3. Search the web when the task touches third-party APIs, current platform behavior, existing public solutions, or recent best practices.
4. Summarize local constraints, viable options, and the recommended direction.
5. Write the architectural conclusion into `02-overview-design.md`.
6. Run an overview reflection pass:
   - challenge the main path
   - compare against at least one viable alternative
   - check for missing runtime verification implications
   - check for overscoping, underscoping, or coupling mistakes
7. If the architecture is high-impact, uncertain, novel, or still contested after reflection, dispatch a bounded subagent discussion/review with only the relevant design context.
8. Feed implementation-facing findings into `03-detailed-design.md`.
9. Run a detailed-design reflection pass:
   - challenge the testing strategy first
   - challenge interfaces, boundaries, and migration assumptions
   - check whether runtime verification is concrete enough to trust
10. If detailed design remains uncertain or risky, dispatch a bounded subagent discussion/review with only the relevant design context.

## Rules

- Do not skip local exploration.
- Do not skip web research when the information is time-sensitive or external.
- Prefer primary sources for technical choices.
- Keep exploration focused on the active task.
- Make the reasoning legible in repository artifacts, not only in chat.
- Do not treat `02-overview-design.md` or `03-detailed-design.md` as ready until the reflection pass is written down.
- When using subagents for design discussion, provide bounded context rather than the entire session history.
