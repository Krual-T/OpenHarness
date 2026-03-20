# Requirements

## Goal
Make the two most important design stages less linear and more self-correcting by adding explicit reflection and optional subagent discussion before design is considered ready for implementation.

## Problem Statement
The current redesigned workflow is better than the inherited plan-first flow, but it still risks treating `02-overview-design.md` and `03-detailed-design.md` as one-pass outputs. In practice these are the two stages where agent overconfidence causes the most damage:

- `02-overview-design.md` can lock in the wrong architecture too early
- `03-detailed-design.md` can make testing strategy and implementation landing points too shallow or too coupled

For no-harness projects, the agent often needs to pause, reflect, challenge its own design, and sometimes discuss the design with a bounded subagent before continuing.

## Required Outcomes
1. `02-overview-design.md` includes an explicit reflection checkpoint before the status can advance beyond overview-ready.
2. `03-detailed-design.md` includes an explicit reflection checkpoint before the status can advance beyond detailed-ready.
3. The workflow defines when the reflection can stay local and when it should involve a bounded subagent discussion or review.
4. Reflection focuses on architecture quality, testing strategy, coupling, missing runtime verification, and over/under-scoping.
5. The resulting protocol remains practical for no-harness projects and does not require heavyweight infrastructure.

## Non-Goals
- Require subagent discussion for every tiny task regardless of complexity.
- Add a fully automatic architecture-review system in this round.

## Constraints
- Reflection must remain legible in repository artifacts, not only in chat.
- Any subagent discussion must use bounded context rather than dumping full session history.
- The workflow should remain compatible with projects that start with no runtime harness.
