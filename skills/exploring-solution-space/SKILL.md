---
name: exploring-solution-space
description: Use after requirements are clear to explore the local repository and the web before locking in architecture or implementation details.
---

# Exploring Solution Space

## Skill Role

- Protocol status: core protocol skill
- Primary stage: exploration and architecture
- Trigger: use after requirements are clear and before architecture or implementation details are locked

## Overview

Use this skill after `brainstorming` has clarified the task and written `01-requirements.md`.

Its job is to make exploration explicit:

- inspect the local repository
- inspect relevant task packages and recent code
- search the web when external references or current best practices matter
- record the important findings that shape the architecture

It also turns the stage-organized role-injection model into architecture and design discipline:

- overview work should use the architecture perspective and, when the user-value boundary is still active, the product perspective
- detailed design should use the architecture perspective and testing perspective
- verification planning should anticipate the later review perspective and risk perspective

## Output

The primary output of this skill is:

- `02-overview-design.md`

This skill may also feed implementation-facing constraints into `03-detailed-design.md` when exploration has already made interfaces, test strategy, or migration boundaries concrete enough to write down.

Do not treat exploration as permission to fully draft `03-detailed-design.md` before `02-overview-design.md` exists and its architecture is reflected.

## Process

1. Read `01-requirements.md` and restate the concrete question being explored.
2. Explore the local repository for relevant code, docs, tests, and recent changes.
3. Search the web when the task touches third-party APIs, current platform behavior, existing public solutions, or recent best practices.
4. Summarize local constraints, viable options, and the recommended direction.
5. Write the architectural conclusion into `02-overview-design.md`.
   - When the overview is coherent and reflected, the package is ready for `overview_ready`.
   - include the stage gate items that make the architecture ready rather than merely described.
6. Run an overview reflection pass:
   - challenge the main path
   - compare against at least one viable alternative
   - check for missing runtime verification implications
   - check for overscoping, underscoping, or coupling mistakes
   - use the architecture perspective to challenge boundaries, constraints, and complexity
   - use the product perspective only to challenge value drift, scope drift, or broken success semantics
7. If the architecture is high-impact, uncertain, novel, or still contested after reflection, dispatch a bounded subagent discussion/review with only the relevant design context.
8. Only after `02-overview-design.md` is coherent, feed implementation-facing findings into `03-detailed-design.md` if those findings are already concrete enough to constrain implementation.
   - When detailed design is concrete and reflected, the package is ready for `detailed_ready`.
9. Run a detailed-design reflection pass:
   - challenge the testing strategy first
   - challenge interfaces, boundaries, and migration assumptions
   - check whether runtime verification is concrete enough to trust
   - use the testing perspective to force testability, observability, and rollback clarity
   - prepare the review perspective and risk perspective by identifying what evidence later verification must produce
10. If detailed design remains uncertain or risky, dispatch a bounded subagent discussion/review with only the relevant design context.

## Stage Gates

Exploration should harden the package against vague readiness claims.

- overview stage gate
  - decision list for key constraints and interface boundaries
  - key failure modes
  - degradation or rollback direction
- detailed stage gate
  - test strategy
  - observability requirements
  - migration order
  - expected evidence types

If these are not clear, continue exploring and revising instead of marking the stage ready.

## Challenge Closure

Exploration must leave a visible challenge closure trail, not just a stronger narrative.

For each material challenge raised by the architecture perspective, testing perspective, or bounded review:

- accept it and convert it into a design constraint
- reject it and record the chosen alternative plus reason
- defer it and record the trigger condition and latest landing point

This challenge closure keeps reflection from collapsing into comment threads that do not change the package.

## Rules

- Do not skip local exploration.
- Do not skip web research when the information is time-sensitive or external.
- Prefer primary sources for technical choices.
- Keep exploration focused on the active task.
- Make the reasoning legible in repository artifacts, not only in chat.
- Treat `02-overview-design.md` as the main artifact of exploration; update `03-detailed-design.md` only for implementation-facing conclusions that are already justified by the explored architecture.
- Do not treat `02-overview-design.md` or `03-detailed-design.md` as ready until the reflection pass is written down.
- Carry the decision list from the prior stage before injecting new perspectives.
- Use role injection to sharpen the design, not to reopen already-closed questions without cause.
- When using subagents for design discussion, provide bounded context rather than the entire session history.
