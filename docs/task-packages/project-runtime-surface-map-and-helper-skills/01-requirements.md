# Requirements

## Goal
Define the project-facing workflow for building runtime feedback loops: a repository should describe its runtime surfaces, attach one or more narrow runtime helper skills, and route runtime work through those helpers without pretending that one generic debug skill can cover every case.

## Problem Statement
Even with a runtime capability contract, a repository still needs practical onboarding guidance:

- what runtime surfaces should be mapped
- where those facts should live
- how helper skills should be split
- how `using-openharness` should behave when the needed runtime helper does not yet exist

This matters because real repositories rarely have one runtime shape:

- a web product may need browser, API, worker, and observability loops
- a backend service may need API, migration, and queue loops
- an infrastructure repository may need deployment, health-check, and log-triage loops

If OpenHarness does not define a project-facing structure, repositories will improvise:

- one giant debug skill with fuzzy scope
- runtime setup hidden in shell history instead of task packages
- duplicated helper skills with no shared shape
- no clear bootstrap path when a new runtime surface appears

The project therefore needs a package that explains how a repository should grow several runtime helpers naturally.

## Required Outcomes
1. Define the minimum contents of a project runtime surface map.
2. Define how runtime helper skills should be split and bounded.
3. Define the bootstrap workflow for adding a new runtime surface or helper skill.
4. Define how runtime helper usage writes back into task packages and verification artifacts.
5. Provide enough structure that later examples or templates can teach repositories how to adopt this model.

## Success Conditions
- A future agent can onboard into a repository and identify which runtime surface applies to the task.
- A repository can host several runtime helper skills without creating a parallel root workflow.
- When no helper exists for a surface, the agent has a clear bootstrap path instead of improvising unsupported runtime verification.
- Runtime helper outputs are written back into the same task-package and evidence system as other work.

## Non-Goals
- Define one canonical list of runtime surfaces for all repositories.
- Implement specific browser, API, or worker helper skills in this package.
- Replace project-specific scripts or infrastructure with OpenHarness abstractions.
- Turn helper-skill choice into a fully automatic classifier in this round.

## Constraints
- The model must work even when a repository starts with no runtime helper skills at all.
- The model must support many small runtime helpers rather than one universal skill.
- The workflow must preserve `using-openharness` as the only entry skill and keep runtime helpers as optional project-level extensions.
- The writeback model must stay compatible with `03-detailed-design.md`, `05-verification.md`, and `06-evidence.md`.
