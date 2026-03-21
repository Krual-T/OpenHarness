# Requirements

## Goal
Define a repeatable cold-start workflow for Python repositories that start with no OpenHarness package history and no mature runtime verification loop.

## Problem Statement
OpenHarness now explains how to operate inside a repository once the repository already has:

- `AGENTS.md` as a map
- `docs/designs/<task>/` packages as the active task system
- a manifest and templates that encode the harness protocol
- explicit runtime verification semantics
- tightened status meanings for design and completion checkpoints

What is still missing is the first-round operating model for a Python repository that has none of that yet.

Without an explicit cold-start workflow, agents have to improvise:

- whether they should create `AGENTS.md` first or start directly from a task package
- which minimal repo-local artifacts are required in round one versus optional later
- how to choose or scaffold the first active design package
- how to verify the round when there is no mature runtime test harness yet
- whether `pytest` is enough to proceed temporarily and how runtime tests should be introduced afterward

The user's scope also narrows the product boundary:

- OpenHarness does not need to support non-Python development scenarios in this stream.
- Cold start does not need a universal verification standard for every runtime shape.
- For Python repositories, the practical minimum is: `pytest` must run and be treated as the current verification floor.
- Runtime tests are still the desired end state for many tasks, but they can be introduced incrementally and recommended explicitly rather than blocking cold start from day one.

That means the earlier generic "no-harness bootstrap for any repository" framing was too broad. The real problem is narrower: make Python cold start immediate and honest without pretending the runtime-verification problem is already fully solved.

## Required Outcomes
1. Define the minimum cold-start sequence for a Python repository from first entry to first active design package.
2. Define the minimum repo-local artifacts that must exist after cold start and the artifacts that can remain deferred.
3. Define how the first package is selected, scoped, and written without creating a second task-tracking system.
4. Define `pytest` as the minimum acceptable verification gate for cold start when mature runtime tests do not yet exist.
5. Define how runtime tests should be recommended, planned, or built in parallel after cold start rather than treated as an all-or-nothing prerequisite.
6. Define how the tighter status meanings from `OH-006` apply during this Python cold-start round.
7. Keep the package concrete enough that a later implementation round can update docs, templates, and lightweight CLI guidance directly from it.

## Success Conditions
- A future agent can enter a Python repository and know what to inspect, what to create, and what to defer without improvising the order.
- The workflow distinguishes "adopt existing repo structure" from "scaffold missing harness artifacts" instead of assuming every repository starts from zero.
- The cold-start round ends with at least one valid active design package and a declared `pytest`-based verification floor.
- The package makes clear when runtime tests are merely recommended next work versus immediate requirements for the current task.
- `OH-004` no longer needs to carry Python cold-start detail that belongs in this focused child package.

## Non-Goals
- Implement the full bootstrap support in code, templates, and docs in this round.
- Define every optional maintenance or taxonomy cleanup rule here unless bootstrap depends on it directly.
- Require a heavy generator or new orchestration subsystem before OpenHarness can bootstrap a repository.
- Replace the fixed design-package protocol with a looser "first conversation only" mode.
- Generalize this package into a language-agnostic bootstrap system for non-Python repositories.

## Constraints
- The cold-start workflow must preserve the existing `AGENTS.md` plus design-package model rather than inventing a parallel entry layer.
- The workflow must reuse the readiness semantics from `OH-006`.
- The first round must stay lightweight enough for real Python repositories that start with weak automation and partial docs.
- `pytest` is the minimum default verification gate during cold start unless the repository already has a stronger automated path.
- The design should recommend constructing runtime tests when task risk justifies them, and allow those tests to be built in parallel with other Python tests.
