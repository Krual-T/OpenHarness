# Requirements

## Goal
Define the OpenHarness-level contract for project-specific runtime capabilities so repositories can build runtime feedback loops without pretending that one universal runtime debugging skill can cover every runtime surface.

## Problem Statement
OpenHarness already has a minimum runtime verification vocabulary, but it still lacks a stable answer for the next practical question:

- when a repository has several runtime surfaces such as API, browser, queue worker, migration, or observability, how should OpenHarness represent them
- how should the entry workflow decide whether to use an existing runtime helper skill or bootstrap a new runtime capability first
- what facts must be recorded so runtime verification remains discoverable, repeatable, and reviewable

Without this contract, later runtime work risks drifting into ad hoc project-specific prompts:

- some repositories may add one oversized debug skill that becomes vague and unmaintainable
- some may create several runtime helpers with no shared declaration shape
- `using-openharness` has no principled routing rule for runtime tasks beyond generic debugging
- runtime evidence may remain trapped in chat or shell history instead of task packages

The system therefore needs a protocol that is generic enough to reuse across repositories but narrow enough to avoid becoming a fake universal runtime harness.

## Required Outcomes
1. Define the minimum declaration shape for a project-specific runtime capability.
2. Define how OpenHarness should route runtime work across multiple runtime surfaces instead of one global debug skill.
3. Define when a repository should bootstrap a runtime capability package before attempting runtime verification or debugging.
4. Define what task-package documents must contain so runtime capabilities stay repository-visible and reviewable.
5. Identify the live OpenHarness surfaces that should later teach this protocol.

## Success Conditions
- A future agent can explain runtime support in terms of capabilities and surfaces rather than a single generic runtime skill.
- A repository can add one or many runtime helper skills without breaking the core workflow model.
- `using-openharness` can distinguish between "use an existing runtime helper" and "first build the missing runtime capability".
- Runtime capability design remains inside task packages and repository docs rather than chat-only guidance.

## Non-Goals
- Implement browser automation, API runners, log collectors, or observability adapters in this package.
- Force every project to expose the same runtime surfaces.
- Define the detailed content of any one project-specific helper skill template; that belongs in a follow-up package.
- Replace `systematic-debugging`; this package defines runtime capability routing, not a new root-cause methodology.

## Constraints
- The protocol must support repositories that have zero, one, or many project-specific runtime helper skills.
- The protocol must preserve `using-openharness` as the only repository entry skill.
- The protocol must keep runtime evidence inside the existing task-package and verification writeback model.
- The contract should stay small enough that projects can adopt it incrementally instead of needing a full custom platform first.
