# Requirements

## Goal
Define a repeatable bootstrap workflow for repositories that start with no OpenHarness package history, no repo-local harness artifacts, and no stable verification loop.

## Problem Statement
OpenHarness now explains how to operate inside a repository once the repository already has:

- `AGENTS.md` as a map
- `docs/designs/<task>/` packages as the active task system
- a manifest and templates that encode the harness protocol
- explicit runtime verification semantics
- tightened status meanings for design and completion checkpoints

What is still missing is the first-round operating model for a repository that has none of that yet.

Without an explicit bootstrap workflow, agents have to improvise:

- whether they should create `AGENTS.md` first or start directly from a task package
- which minimal repo-local artifacts are required in round one versus optional later
- how to choose or scaffold the first active design package
- how to record verification when the repository has no reliable automation yet
- when the repository is "bootstrapped enough" to switch back to the normal package workflow

That gap keeps the product incomplete. The repository has a strong steady-state protocol, but not yet a productized entry path for greenfield or weakly structured repos.

## Required Outcomes
1. Define the minimum bootstrap sequence for a no-harness repository from first entry to first active design package.
2. Define the minimum repo-local artifacts that must exist after bootstrap and the artifacts that can remain deferred.
3. Define how the first package is selected, scoped, and written without creating a second task-tracking system.
4. Define how bootstrap establishes a credible verification path using the runtime-verification ladder from `OH-005`.
5. Define how the tighter status meanings from `OH-006` apply during the bootstrap round.
6. Keep the package concrete enough that a later implementation round can update docs, templates, and CLI behavior directly from it.

## Success Conditions
- A future agent can enter a no-harness repository and know what to inspect, what to create, and what to defer without improvising the order.
- The workflow distinguishes "adopt existing repo structure" from "scaffold missing harness artifacts" instead of assuming every repository starts from zero.
- The bootstrap round ends with at least one valid active design package and a declared verification path.
- The package makes clear which repository surfaces are likely to change in the implementation wave.
- `OH-004` no longer needs to carry bootstrap detail that belongs in this focused child package.

## Non-Goals
- Implement the full bootstrap support in code, templates, and docs in this round.
- Define every optional maintenance or taxonomy cleanup rule here unless bootstrap depends on it directly.
- Require a heavy generator or new orchestration subsystem before OpenHarness can bootstrap a repository.
- Replace the fixed design-package protocol with a looser "first conversation only" mode.

## Constraints
- The bootstrap workflow must preserve the existing `AGENTS.md` plus design-package model rather than inventing a parallel entry layer.
- The workflow must reuse the runtime-verification ladder from `OH-005` and the readiness semantics from `OH-006`.
- The first round must stay lightweight enough for real repositories that start with weak automation and partial docs.
- The design should prefer repository-visible artifacts over hidden chat-state assumptions.
