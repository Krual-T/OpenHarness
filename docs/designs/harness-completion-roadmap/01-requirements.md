# Requirements

## Goal
Provide one durable active package that tracks the remaining major gaps in OpenHarness so the project can move from a strong workflow protocol to a more complete harness-building system for no-harness repositories.

## Problem Statement
OpenHarness now has:

- self-hosting
- a fixed design package protocol
- requirements -> exploration -> overview -> detailed -> implementation -> runtime verification -> completion workflow
- reflection and bounded subagent discussion for design stages

But there are still major product gaps:

- runtime verification exists as a workflow slot, but not yet as a concrete minimum protocol
- there is no explicit “bootstrap a no-harness repository” operating model
- maintenance / entropy reduction is not yet a first-class workflow
- status semantics are still looser than the workflow now implies
- compatibility / optional skill boundaries are clearer than before, but not yet fully productized

If these gaps are tracked only in conversation, they will be forgotten or rediscovered inconsistently.

## Required Outcomes
1. Capture the remaining major work as a coherent roadmap in one active package.
2. Define the target shape of the minimal runtime verification protocol.
3. Define the target shape of the no-harness bootstrap workflow.
4. Define the target shape of maintenance / entropy-reduction work.
5. Define the target shape of status semantics and skill classification cleanup.
6. Keep the package large and explicit enough that future follow-up tasks can branch from it without losing context.

## Success Conditions
- A future agent can map an incoming request to one of the roadmap streams without re-reading the whole repository.
- Each stream has a concrete trigger for when it should split into its own focused package.
- Each stream names the expected artifacts, verification concerns, and repository surfaces likely to change.
- The roadmap captures dependencies between streams so follow-up work can be ordered intentionally instead of ad hoc.
- The package documents what is already true in the repository today versus what still remains productized only as intent.

## Non-Goals
- Implement all remaining streams inside this single round.
- Freeze every downstream design choice before exploration.
- Replace future smaller design packages that split off from this roadmap once a stream becomes actionable.

## Constraints
- The package should be intentionally broad and roadmap-oriented.
- It should still remain specific enough to drive future implementation packages.
- It should preserve the fixed design package model instead of creating a parallel planning system.
- It should acknowledge the current repository baseline instead of pretending OpenHarness starts from zero.
