# Overview Design

## System Boundary
This package defines the narrow onboarding workflow for adding one project runtime helper skill. It assumes the shared runtime capability contract from `OH-013` and the project-facing runtime surface map model from `OH-014` already exist. It does not replace those packages and it does not define the content of any single concrete helper implementation.

## Proposed Structure
Treat helper creation as a three-way decision, not as a default action:

1. `reuse existing helper`
   - If the runtime surface map already points to a helper whose surface, driver style, and evidence shape match the task, use that helper and write back into the active task package.
2. `add new helper`
   - If the surface is mapped but there is no reusable helper for the needed loop, add one new narrow helper skill and link it from the runtime surface map.
3. `bootstrap first`
   - If the repository cannot yet state the runtime surface, prerequisites, driver, or evidence sources clearly, open a focused bootstrap task package before creating a reusable helper.

Each new helper should declare at least:

- owning runtime surface
- purpose and dominant validation loop
- prerequisites
- driver commands or scripts
- observation points and evidence sources
- success criteria
- failure evidence expectations
- writeback expectations for `03`, `05`, and `06`

The main design choice is to make helper creation conditional and explicit. A repository should not add a new helper merely because a runtime problem appeared once.

## Key Flows
1. A task needs runtime verification or runtime debugging.
2. `using-openharness` routes the task into runtime-aware handling.
3. The agent checks the runtime surface map for a matching surface.
4. If a matching reusable helper already exists, the agent reuses it.
5. If the surface exists but helper coverage is missing, the agent creates one new narrow helper and updates the repository surfaces that advertise it.
6. If the surface itself is missing or underspecified, the agent creates a bootstrap package first and delays reusable-helper claims.
7. The active task package records the planned loop in `03`, executed verification in `05`, and artifacts plus residual risk in `06`.

## Trade-offs
- A dedicated helper-creation workflow adds one more protocol surface, but it prevents helper sprawl and duplicate runtime folklore.
- Requiring a runtime surface map before helper creation adds friction to the first runtime loop on a new surface, but it keeps helper boundaries legible.
- Forcing one dominant surface per helper increases the number of helpers, but it is much easier to maintain than one giant runtime-debug skill.
- Keeping helper results inside task packages avoids a parallel evidence system, but it means helper docs must stay disciplined about writeback responsibilities.

## Overview Reflection
- I challenged whether this package should be a generic `create harness skill` workflow. That would be too broad and would overlap with both `skill-creator` and `using-openharness`.
- I checked whether helper creation could live only as one subsection in `OH-014`. That would leave a high-frequency action path under-specified, because `OH-014` explains the repository model but not the step-by-step decision to add a new helper.
- I considered making helper creation the default whenever no exact helper match exists. That was rejected because missing helper coverage and missing runtime surface definition are not the same problem.
- I checked whether this package should promote project runtime helpers into core protocol skills. It should not. The core protocol stays in routing and declaration rules; project runtime helpers remain optional extensions.
