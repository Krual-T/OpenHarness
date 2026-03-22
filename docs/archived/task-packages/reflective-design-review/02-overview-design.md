# Overview Design

## System Boundary
This task covers the workflow semantics around overview and detailed design readiness. It does not redesign the whole package protocol again; it only adds a reflective review layer to the two most important design artifacts.

## Proposed Structure
- After exploration informs `02-overview-design.md`, the agent performs a mandatory reflection pass:
  - challenge the main path
  - compare against at least one viable alternative
  - check whether runtime verification implications were considered
  - check whether the architecture is too broad, too narrow, or too coupled
- For high-impact or uncertain design choices, the agent should dispatch a bounded subagent discussion/review before marking overview as ready.
- After drafting `03-detailed-design.md`, the agent performs a second mandatory reflection pass:
  - challenge the test strategy
  - challenge module boundaries and interface choices
  - challenge migration/risk assumptions
  - check whether runtime verification is concrete enough
- For complex or risky detailed designs, the agent should dispatch a bounded subagent discussion/review before implementation.

## Key Flows
- Requirements are clarified.
- Exploration gathers local and web evidence.
- Overview design is drafted.
- Reflection pass 1 happens, optionally with subagent discussion.
- Detailed design is drafted.
- Reflection pass 2 happens, optionally with subagent discussion.
- Only then does implementation begin.

## Trade-offs
- This adds process overhead, but it targets the highest-leverage design mistakes rather than every step.
- Optional subagent discussion preserves flexibility while still making design challenge a first-class activity.
- The main risk is ritualized review with no substance; the workflow must specify concrete questions to avoid that.

## Overview Reflection
- I checked whether the reflection loop should be lightweight guidance or a hard requirement. It should be a hard requirement at the design-readiness layer, with bounded subagent discussion remaining conditional on risk.
- I checked whether overview and detailed reflection should be merged into one generic review pass. They should not; architecture and implementation-facing risks show up at different points.
- I checked whether this package needed dedicated runtime tooling. It did not; the first value was to record the workflow contract in core docs and skills.
