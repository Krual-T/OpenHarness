# Requirements

## Goal
Define a repeatable Python verification policy for work that does not yet have a complete runtime test system.

## Problem Statement
OpenHarness now has:

- `AGENTS.md` as a map
- `docs/task-packages/<task>/` packages as the active task system
- a manifest and templates that encode the harness protocol
- explicit runtime verification semantics
- tightened status meanings for design and completion checkpoints

What is still missing is a concrete default verification policy for Python work when runtime tests are incomplete.

Without an explicit Python verification baseline, agents have to improvise:

- whether `pytest` is enough for the current task
- when runtime tests are mandatory versus merely desirable
- how to record that a task passed Python tests but still lacks runtime-level evidence
- whether runtime tests should be added now or planned as explicit follow-up work
- how completion claims should read when verification is still on the weaker side

The intended boundary is:

- This stream is about Python verification policy, not repository entry routing.
- For Python repositories, the practical minimum is: `pytest` must run and be treated as the current verification floor.
- Runtime tests are still the desired end state for many tasks, but they can be introduced incrementally and recommended explicitly rather than blocking every task from day one.
- This package does not need to define non-Python defaults.

That means the earlier bootstrap framing was solving the wrong problem. The real problem is narrower and more important: define what OpenHarness should ask for, accept, and record when Python verification is still maturing from plain `pytest` toward stronger runtime coverage.

## Required Outcomes
1. Define `pytest` as the minimum acceptable verification floor for Python work when runtime tests are incomplete.
2. Define how packages should distinguish `required now` from `recommended next` for runtime tests.
3. Define how runtime tests may be built in parallel with other Python tests when task risk justifies it.
4. Define how `03-detailed-design.md`, `04-verification.md`, and `05-evidence.md` should record verification strength and remaining gaps.
5. Define how the tighter status meanings from `OH-006` apply when a task has only the Python baseline versus stronger runtime evidence.
6. Keep the package concrete enough that a later implementation round can update docs, templates, and verification guidance directly from it.

## Success Conditions
- A future agent can explain the Python verification expectation for a task without improvising the standard from scratch.
- The workflow distinguishes clearly between the minimum Python baseline and stronger runtime verification.
- A package can say `pytest passed, runtime tests still missing` in a structured and non-misleading way.
- The package makes clear when runtime tests are merely recommended next work versus immediate requirements for the current task.
- `OH-004` no longer needs to carry Python verification-maturity detail that belongs in this focused child package.

## Non-Goals
- Implement the full docs/template/skill rollout in this round.
- Redefine repository entry routing or add a new bootstrap entry mode in this package.
- Pretend `pytest` and runtime tests are equivalent evidence.
- Define non-Python verification defaults in this round.

## Constraints
- The policy must preserve the existing `AGENTS.md` plus task-package model rather than inventing a parallel entry layer.
- The workflow must reuse the readiness semantics from `OH-006`.
- `pytest` is the minimum default verification floor for Python work unless the repository already has stronger automated evidence.
- The design must encourage runtime tests when task risk justifies them and allow those tests to be built in parallel with other Python tests.
- The protocol should prefer explicit disclosure of weaker evidence over fake certainty.
