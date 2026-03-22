# Overview Design

## System Boundary
This package changes how the live repository explains and routes skills. It does not redesign the whole harness protocol. The work stays focused on:

- the live skill hub
- affected repository docs
- affected skill docs
- repository tests that pin the intended model

It also productizes one live verification statement for Python-first repositories: `uv run pytest` is the default minimum automated verification floor, while stronger runtime verification remains task-specific.

## Proposed Structure
Use a two-layer model instead of one mixed taxonomy.

### Layer 1: Protocol Status
Keep one small, stable classification for what the harness owns:

1. `core protocol skill`
   - part of the fixed OpenHarness workflow
   - defines repository routing, required design flow, or completion discipline
2. `optional helper skill`
   - repository-owned and useful, but not part of the mandatory default path
   - enters the workflow only when task conditions justify it
3. `imported generic skill`
   - available in the repository, but not part of the OpenHarness protocol itself

### Layer 2: Workflow Stage And Trigger
Describe when a skill is normally used:

- entry and routing
- requirements convergence
- exploration and architecture
- implementation execution
- debugging and repair
- verification and closure
- repository memory and maintenance

This second layer answers the question the current hub does not answer cleanly: not just "what kind of skill is this," but "when should the agent reach for it?"

### Python Verification Baseline
The live repository docs should state one simple product rule:

- OpenHarness is Python-first
- `uv run pytest` is the default minimum automated verification floor
- passing `pytest` does not automatically imply strong runtime evidence
- project-specific runtime verification must be defined in task packages rather than frozen globally in the hub

That keeps the harness reusable across Python repositories without pretending every repo already has the same runtime test surface.

## Key Flows
1. A new agent enters a repository and needs to know the default path.
2. The skill hub first shows protocol status so the agent can distinguish fixed protocol from optional or imported helpers.
3. The hub then shows workflow stages and triggers so the agent can follow the default path and branch only when conditions justify it.
4. The README reinforces the product goal: this is a plug-and-play Agent Harness for Python-first repositories.
5. Verification wording tells the agent what the minimum Python evidence floor is today, while leaving stronger runtime verification to project-level task packages.

## Trade-offs
- A two-layer model is slightly longer than a single set of theme buckets, but it maps much better to actual routing decisions.
- Keeping protocol status small reduces taxonomy drift, but it means some nuanced skill differences are expressed through stage and trigger wording rather than extra categories.
- Declaring `pytest` as the Python floor makes the harness immediately usable, but it also requires explicit honesty that stronger runtime evidence may still be missing.
- Making runtime verification project-specific avoids a false universal rule, but it requires task packages to stay disciplined about recording stronger verification when risk justifies it.

## Overview Reflection
- I challenged whether the existing `Core / Execution / Quality / Repository Memory` buckets were already good enough. They are not, because they mix ownership with theme and force agents to infer trigger conditions.
- I considered adding many more categories instead of adding a second layer. That would make the hub more detailed but also more brittle; the stable split is protocol status plus workflow stage.
- I checked whether the Python verification baseline belonged in this package. It does, because the user asked for the final product goal to be reflected in the live harness surface, and the current live docs still understate this baseline.
- I checked whether this package should define a universal runtime-test rule. It should not; the live docs should state the Python floor and leave stronger runtime verification to specific task packages.
- No bounded subagent discussion was used in this round. The design fork is local, legible, and narrow enough to resolve directly.
