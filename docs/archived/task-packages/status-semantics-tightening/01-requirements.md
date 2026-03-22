# Requirements

## Goal
Define stronger, reusable status semantics for OpenHarness task packages so status names communicate real readiness and evidence constraints rather than acting as loose progress labels.

## Problem Statement
OpenHarness already has a default status flow:

- `proposed`
- `requirements_ready`
- `overview_ready`
- `detailed_ready`
- `in_progress`
- `verifying`
- `archived`

That list is now machine-readable in the manifest and partially visible in CLI behavior, but the repository still lacks a durable contract for what each status actually means.

This creates several risks:

- packages can move between statuses based on agent preference instead of explicit readiness conditions
- `verifying` can collapse into a vague “almost done” label rather than a narrow evidence-gathering stage
- bootstrap and maintenance flows cannot tell whether a package is legitimately ready for implementation, verification, or archive
- future CLI or template enforcement could encode the wrong behavior because the repository has not yet settled the semantics

`OH-005 Runtime Verification Baseline` removed one major ambiguity by defining what runtime verification evidence means, but that work now needs to be tied back into the status flow. Without that connection, the repository still has named statuses without reliable entry and exit criteria.

## Required Outcomes
1. Define the semantic meaning of each status in the default status flow.
2. Define the minimum entry and exit conditions for each later-stage status, especially `overview_ready`, `detailed_ready`, `in_progress`, `verifying`, and `archived`.
3. Define how runtime verification outcomes and evidence quality constrain status transitions.
4. Define which parts of the contract should remain documentation-level rules versus which parts should later be enforced by CLI validation or templates.
5. Provide enough structure that follow-up implementation can tighten status checks without inventing a second workflow system.

## Success Conditions
- A future agent can explain why a package is in a given status using repository-defined rules rather than intuition.
- The repository has an explicit answer for when `verifying` starts, when it is blocked, and when a package may archive.
- Runtime verification semantics from `OH-005` are reflected in status-transition rules instead of remaining adjacent but disconnected.
- Follow-up changes to manifest schema, CLI validation, templates, and skill wording can be scoped from this package without rediscovering the core model.

## Non-Goals
- Replace the existing design-package workflow with a new state machine framework.
- Fully implement every downstream CLI, template, or skill change in this package.
- Add per-package bespoke statuses outside the shared default flow in this round.
- Design the no-harness bootstrap workflow or maintenance workflow here except where they depend directly on status semantics.

## Constraints
- The solution must preserve the fixed design-package model and the single OpenHarness CLI.
- The status model must stay simple enough to teach in docs and templates without creating ritualized bureaucracy.
- The model must align with the runtime verification baseline already defined in `OH-005`.
- Machine enforcement should follow clarified semantics, not replace the need to define them.
