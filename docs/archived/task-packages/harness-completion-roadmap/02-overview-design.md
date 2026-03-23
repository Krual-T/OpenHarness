# Overview Design

## System Boundary
This package is a meta-level roadmap package for the remaining major OpenHarness product gaps. It does not implement all of them at once; it organizes them into the next durable streams.

## Current Baseline
OpenHarness already has these repository-level primitives:

- `AGENTS.md` as the repository map
- a machine-readable manifest and CLI for task-package discovery and validation
- a fixed task-package shape under `docs/task-packages/<task>/`
- a workflow that now explicitly includes exploration, overview design, detailed design, reflection, implementation, runtime verification, verification, and evidence
- archived packages that document the self-hosting, workflow redesign, and reflective design-review rounds

The remaining gap is not absence of structure. The gap is that several product-level operating modes are still only implied by the workflow, not yet defined tightly enough to reuse across repositories.

One workflow ambiguity is now explicit: exploration should produce architectural conclusions in `02-overview-design.md` first. It may inform `03-detailed-design.md`, but it should not be read as permission to draft detailed design before overview design is coherent and reflected. The core skill docs should say this directly so the process does not self-contradict.

Another workflow ambiguity is now explicit too: brainstorming should make design explicit before action, but it should not impose mandatory user approval pauses during normal autonomous execution. The protocol should stop for review only when the user asked for it or when unresolved ambiguity makes continuation risky.

## Proposed Structure
Keep `OH-004` as the historical umbrella roadmap for the completion work that has already been productized.

There are no unfinished streams left under this roadmap:

1. `maintenance and entropy reduction`
   - This stream completed through archived `OH-017 Maintenance And Entropy Reduction`.
   - `OH-017` now serves as the reusable baseline for recurring cleanup, memory freshness review, and skill-surface drift handling.
   - Future maintenance waves should open a new focused package only when they introduce a new bounded cleanup round or a new maintenance-oriented product surface.

The completed baseline streams remain authoritative historical inputs:

- `runtime verification baseline`
- `project runtime capability integration`
- `status semantics tightening`
- `task package semantic validation`
- `workflow transition and verification artifacts`
- `python verification maturity`
- `skill taxonomy and compatibility cleanup`
- `skill taxonomy and stage model`

## Stream Dependencies And Order
- `runtime verification baseline` and `status semantics tightening` are already complete enough to act as upstream baselines, because both changed what `ready`, `verifying`, and `done` mean.
- `python verification maturity` is already captured as a historical design baseline, so the remaining dependency is to decide where its wording should eventually land in live docs and templates.
- `skill taxonomy and compatibility cleanup` plus `skill taxonomy and stage model` are now complete enough to act as the upstream skill-surface baseline, because the live repository no longer ships the old plan-oriented skill surface and the live docs now describe protocol status, workflow stage, and the Python-first pytest floor explicitly.
- `project runtime capability integration` is now an archived completed baseline, because `OH-013`, `OH-014`, and `OH-016` together cover the contract, the runtime surface map, and the focused helper-addition workflow.
- `maintenance and entropy reduction` was the last unfinished roadmap stream and is now complete through archived `OH-017`, which consumed the stabilized runtime and skill taxonomy surfaces instead of redefining them.

## Split Triggers
This roadmap is now archival. If future work uncovers a new major gap, open a new focused package when a request satisfies one of these triggers:

- A stream has a narrow enough problem statement to produce concrete file-level changes in one round.
- A stream needs repository exploration or external comparison that would overwhelm this parent roadmap.
- A stream needs its own verification contract beyond the generic `check-tasks` plus repository tests.
- A stream needs to introduce or revise reusable artifacts such as templates, automation, or project-memory conventions.

When those triggers are met, the agent should scaffold a new focused package rather than reopening `OH-004` with fresh implementation detail.

## Key Flows
- A future task asks `what completion work already landed?`
- The agent enters `OH-004`.
- The roadmap identifies which stream already solved the request's concern and which archived child package should be reused as the baseline.
- If the request exposes a genuinely new gap instead of a previously completed stream, the agent scaffolds a new focused package rather than reviving `OH-004`.
- `OH-017 Maintenance And Entropy Reduction` is now the archived completed child package for the maintenance stream.
- `OH-005 Runtime Verification Baseline` is the first such child package and is now archived as the completed baseline for the runtime-verification stream.
- `OH-006 Status Semantics Tightening` is now archived as the completed baseline for stronger workflow checkpoint meaning and transition gates.
- `OH-007 Python Verification Maturity` remains a legacy archived design-baseline package from the older semantics period; future work may reuse it as historical design input, but not as an example that design-complete work is archive-ready.
- `OH-008 Skill Taxonomy And Compatibility Cleanup` is now the archived completed child package for the taxonomy stream.
- `OH-012 Skill Taxonomy And Stage Model` is now the archived completed follow-up that turns the taxonomy stream into the live two-layer skill model and productizes the Python-first pytest baseline in the live repository docs.
- `OH-009 Task Package Semantic Validation` is now archived as the follow-up that turns status semantics into stronger minimum document-anchor checks.
- `OH-010 Workflow Transition And Verification Artifacts` is now archived as the follow-up that turns status semantics and verification evidence into supported CLI mechanics.
- `OH-013 Runtime Capability Contract` is now the archived completed baseline that defines the OpenHarness-side runtime capability contract.
- `OH-014 Project Runtime Surface Map And Helper Skills` is now the archived completed baseline that defines the project-facing onboarding structure for multiple runtime helper skills.
- `OH-016 Adding Project Runtime Helper` is now the archived completed follow-up that defines the narrow helper-addition workflow on top of archived `OH-013` and `OH-014`.
- Active or completed child packages should feed evidence or durable decisions back into this roadmap only when they materially change what remains. That writeback is now complete for all original `OH-004` streams.

## Trade-offs
- One large package is less implementation-ready than a focused package, but it is better for preserving product memory across multiple rounds.
- Keeping the package broad risks vagueness, so the detailed design must name concrete future artifacts, decision fronts, and split triggers.
- Stronger stream boundaries reduce rediscovery cost, but they also make the roadmap more opinionated and may force some future tasks to be decomposed before implementation.
- Tightening workflow wording reduces agent improvisation, but it also makes the protocol less forgiving of ambiguous phrasing in skill docs. That is acceptable because protocol clarity matters more than flexible but conflicting wording.

## Overview Reflection
- I challenged whether this roadmap should immediately split into five packages. That would create premature package sprawl before the repository has agreed definitions for runtime verification and status semantics.
- I considered keeping the roadmap as a simple unordered backlog. That was rejected because the current repo already has enough workflow structure that unordered backlog items would hide real dependencies.
- I checked whether the proposed ordering ignored runtime verification implications. It did initially; the revised structure now makes runtime verification and status semantics upstream of Python verification maturity and maintenance.
- I checked whether the current skill wording accidentally let exploration jump ahead into detailed design. It did leave that ambiguity, so the workflow docs should explicitly state that `02` is the primary output of exploration and `03` only follows when implementation-facing constraints are already justified.
- I checked whether the brainstorming skill overfit to interactive approval loops. It did, so the workflow should default to autonomous continuation once design is explicit and only introduce user review gates when the task or risk profile justifies them.
- I re-checked whether runtime capability integration still belongs in the active roadmap after archiving `OH-016`. It does not; the remaining active stream is now maintenance, while the runtime helper flow should be reused from the archived baselines.
- I re-checked whether the maintenance stream still belonged in the active roadmap after `OH-017` completed its cleanup wave. It does not; with no unfinished streams remaining, `OH-004` should archive as the historical umbrella roadmap.
- No bounded subagent discussion was needed in this round because the uncertainty is about prioritization and scope control inside this repository, not about a hard architectural fork.
