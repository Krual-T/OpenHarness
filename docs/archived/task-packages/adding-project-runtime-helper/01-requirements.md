# Requirements

## Goal
Define a focused OpenHarness workflow for adding one new project runtime helper skill under an existing runtime capability model.

## Problem Statement
`OH-013` defines the OpenHarness-side runtime capability contract and `OH-014` defines the project-facing runtime surface map plus helper-skill structure, but there is still a practical gap: when a repository needs one new runtime helper, the agent needs a concrete workflow that decides whether to reuse, add, or bootstrap rather than improvising.

Without that focused package, the repository risks several failure modes:

- adding duplicate helper skills that cover the same runtime surface with slightly different wording
- creating oversized helpers that mix API, browser, worker, and observability loops into one pseudo-universal skill
- skipping the runtime surface map and encoding runtime knowledge only inside one skill body
- claiming runtime helper support without clear prerequisites, driving steps, observation points, or writeback rules

This package should define the narrow onboarding workflow for adding one reusable project runtime helper cleanly.

## Required Outcomes
1. Define the decision rule between `reuse existing helper`, `add new helper`, and `open bootstrap package first`.
2. Define the minimum contract that a new project runtime helper must satisfy before it is treated as reusable.
3. Define which repository surfaces must be updated when adding a new helper.
4. Define how helper usage and helper creation write back into `03-detailed-design.md`, `05-verification.md`, and `06-evidence.md`.
5. Keep `using-openharness` as the only entry skill while allowing repositories to grow multiple runtime helpers naturally.

## Non-Goals
- Define one universal runtime helper that spans all repositories.
- Define a fixed canonical list of runtime surfaces for every repository.
- Implement any specific API, browser, worker, or observability helper in this package.
- Replace the broader runtime capability contract from `OH-013` or the runtime surface map model from `OH-014`.

## Constraints
- The model must work for repositories that already have zero, one, or many runtime helpers.
- A helper should remain bounded to one dominant runtime surface or one very narrow family of behaviors with the same evidence shape.
- The workflow must stop and create or refine a bootstrap package when the needed runtime surface is not mapped clearly enough.
- The workflow must keep all runtime verification evidence inside the normal task-package flow rather than introducing a parallel evidence system.
