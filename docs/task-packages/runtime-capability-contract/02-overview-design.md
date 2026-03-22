# Overview Design

## System Boundary
This package defines the OpenHarness-side protocol for runtime capability integration. It does not define one universal runtime helper and it does not implement project-specific runtime workflows directly. Its job is to define the stable contract that lets many runtime helpers coexist under one repository workflow.

## Proposed Structure
Treat runtime support as a capability layer with three distinct parts:

1. `core protocol`
   - OpenHarness defines when runtime work is recognized, what documents must record it, and how routing works.
   - This layer stays repository-agnostic.
2. `project runtime capability map`
   - Each repository documents its runtime surfaces such as API, browser, queue worker, migration, or observability.
   - Each surface points to its prerequisites, driver commands, evidence sources, and owning helper skill or task package.
3. `runtime helper skills`
   - Repositories may attach multiple helper skills, each bounded to one runtime surface or one narrow family of runtime behaviors.
   - These skills are optional helpers, not new entry skills.

Each runtime capability should declare at least:

- applicable runtime surface
- prerequisites such as services, accounts, fixtures, environment variables, or seed data
- driving method such as command, script, API call, browser flow, or queue trigger
- observation points such as logs, metrics, traces, screenshots, response bodies, or state assertions
- success criteria
- failure evidence requirements
- writeback expectations for `03`, `05`, and `06`

The key design choice is that OpenHarness should standardize this declaration shape, not the implementation details of every runtime helper.

## Key Flows
1. A task requires validation of real runtime behavior.
2. `using-openharness` recognizes it as runtime work instead of pure code-level work.
3. The agent checks whether the repository already declares a matching runtime capability.
4. If a matching capability exists, the agent uses the linked project runtime helper skill and records results back into the active task package.
5. If no matching capability exists, the agent creates or updates a bootstrap task package for that runtime surface before claiming runtime verification.
6. `systematic-debugging` remains the root-cause discipline inside any runtime investigation once evidence has been gathered.

## Trade-offs
- A capability contract is less magical than a single universal runtime skill, but it matches real repositories more honestly.
- Supporting many helper skills increases surface area, but it keeps each helper narrow enough to remain legible.
- Requiring explicit capability declarations adds documentation work, but it prevents runtime verification from degrading into chat-only folklore.
- Keeping routing in `using-openharness` preserves one entrypoint, but it means the routing rules must stay small and clear.

## Overview Reflection
- I challenged whether OpenHarness should ship one default runtime-debug skill. That would look simpler at first, but it would immediately blur API, browser, worker, and observability workflows together.
- I considered making runtime capability mapping purely a project-doc concern with no OpenHarness protocol. That would keep the core repository smaller, but it would leave no stable routing rule and no shared expectation for evidence shape.
- I checked whether this design conflicts with the earlier runtime-verification baseline. It does not; the baseline defines evidence semantics, while this package defines how repositories expose the runtime surfaces that produce that evidence.
- I checked whether the contract should promote runtime helpers to core protocol skills. It should not. The stable core is the routing and declaration protocol, while runtime helpers remain optional and project-specific.
