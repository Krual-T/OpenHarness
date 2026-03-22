# Overview Design

## System Boundary
This round changes the OpenHarness repository protocol and the core skill narrative. It covers:

- manifest-required package files
- templates for new packages
- skill routing and skill-hub descriptions
- repository docs and tests

It does not yet add heavy runtime modules; it only defines where runtime verification belongs in the default path.

## Proposed Structure
- Fixed package files become:
  - `README.md`
  - `STATUS.yaml`
  - `01-requirements.md`
  - `02-overview-design.md`
  - `03-detailed-design.md`
  - `05-verification.md`
  - `06-evidence.md`
- Default workflow becomes:
  - `using-openharness`
  - `brainstorming` -> write `01`
  - `exploring-solution-space` -> local repo exploration + web research
  - overview synthesis -> write `02`
  - detailed testing-first design -> write `03`
  - implementation / debugging
  - runtime verification
  - completion
- The old plan-writing surface stops being part of the fixed core path and is fully retired in later cleanup.

## Key Flows
1. A new task enters `using-openharness`.
2. `brainstorming` clarifies goals and writes `01-requirements.md`.
3. `exploring-solution-space` gathers repository evidence and external references.
4. The agent writes `02-overview-design.md` from the explored solution space.
5. The agent writes `03-detailed-design.md` with test design first, then implementation landing points and runtime verification approach.
6. Implementation proceeds under TDD and finishes with explicit runtime verification plus evidence updates.

## Trade-offs
- Removing `04` simplifies the fixed protocol, but some imported execution skills will need wording updates.
- Making exploration explicit adds process, but it matches the intended harness behavior much better than hidden ad hoc research.
- Keeping runtime verification in `03` defines the slot without forcing every project to already have a sophisticated runtime-debug harness.

## Overview Reflection
- I checked whether removing `04` would leave planning homeless. It would not; detailed design already carries the implementation-facing planning that the fixed workflow needs.
- I checked whether exploration should stay implicit. It should not; the repository needed a visible step between requirements and detailed design.
- I checked whether runtime verification belonged only at the end. It does not; the intended verification path needs to be planned during detailed design even if execution happens later.
