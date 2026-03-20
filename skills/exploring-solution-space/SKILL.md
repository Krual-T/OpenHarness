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

## Process

1. Read `01-requirements.md` and restate the concrete question being explored.
2. Explore the local repository for relevant code, docs, tests, and recent changes.
3. Search the web when the task touches third-party APIs, current platform behavior, existing public solutions, or recent best practices.
4. Summarize local constraints, viable options, and the recommended direction.
5. Write the architectural conclusion into `02-overview-design.md`.
6. Feed implementation-facing findings into `03-detailed-design.md`.

## Rules

- Do not skip local exploration.
- Do not skip web research when the information is time-sensitive or external.
- Prefer primary sources for technical choices.
- Keep exploration focused on the active task.
- Make the reasoning legible in repository artifacts, not only in chat.
