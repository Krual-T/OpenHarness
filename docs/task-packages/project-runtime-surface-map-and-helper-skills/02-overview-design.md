# Overview Design

## System Boundary
This package defines the project-facing adoption pattern for runtime support. It assumes the OpenHarness-side runtime capability contract exists and focuses on how a real repository records its runtime surfaces and attaches multiple helper skills.

## Proposed Structure
Each repository should maintain a `runtime surface map` that answers, at minimum:

- what runtime surfaces exist in this repository
- what each surface is used to validate or debug
- what prerequisites are required before use
- what driver scripts or commands trigger the surface
- what evidence sources confirm or explain behavior
- which helper skill or bootstrap package owns that surface

The map may point to one or more helper skills such as:

- API runtime loop
- browser runtime loop
- worker or queue runtime loop
- migration or state-change verification loop
- observability or log-triage loop

The repository should prefer several small helpers because each one can stay concrete:

- one surface
- one dominant driver style
- one observation strategy
- one evidence shape

This package also defines a bootstrap branch:

- if a task needs a runtime surface that is not yet mapped, the agent should create a focused bootstrap package for that surface
- the bootstrap package should define the minimum prerequisites, driver, observations, assertions, and evidence flow for that surface before later tasks rely on it

## Key Flows
1. An incoming task needs runtime verification or runtime debugging.
2. `using-openharness` checks the repository runtime surface map.
3. If a matching surface exists, the agent uses the linked runtime helper skill and follows its declared loop.
4. The active task package records planned runtime verification in `03`, executed verification in `05`, and artifacts or residual risks in `06`.
5. If no matching surface exists, the agent opens a bootstrap package for the missing surface and defines the minimum viable runtime loop first.
6. Once the helper exists, later tasks can reuse it instead of rediscovering the setup.

## Trade-offs
- A runtime surface map adds one more repository artifact, but it keeps runtime knowledge discoverable.
- Many small helpers require more curation, but they remain far clearer than one universal runtime skill.
- Requiring bootstrap before unsupported runtime work slows the first task on a new surface, but it prevents low-quality improvisation from becoming pseudo-standard behavior.
- Keeping helper outputs inside normal task packages avoids a second evidence system, but it means runtime helpers must stay disciplined about writeback.

## Overview Reflection
- I challenged whether the repository should just keep a list of scripts instead of a runtime surface map. That would not be enough because scripts alone do not explain when to use them, what they validate, or what evidence they produce.
- I considered putting all runtime onboarding guidance into one giant helper skill. That would make the skill bloated and would still leave repositories without a stable inventory of their runtime surfaces.
- I checked whether helper skills should be grouped by technology instead of runtime surface. Surface-based grouping is better because it follows the validation path and evidence shape, not the implementation language.
- I checked whether the bootstrap branch duplicates the capability contract. It does not; the contract defines shared rules, while the bootstrap branch defines how one repository applies those rules when a surface is missing.
