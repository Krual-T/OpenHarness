# Overview Design

## System Boundary
This package is a meta-level roadmap package for the remaining major OpenHarness product gaps. It does not implement all of them at once; it organizes them into the next durable streams.

## Current Baseline
OpenHarness already has these repository-level primitives:

- `AGENTS.md` as the repository map
- a machine-readable manifest and CLI for design-package discovery and validation
- a fixed design package shape under `docs/designs/<task>/`
- a workflow that now explicitly includes exploration, overview design, detailed design, reflection, implementation, runtime verification, verification, and evidence
- archived packages that document the self-hosting, workflow redesign, and reflective design-review rounds

The remaining gap is not absence of structure. The gap is that several product-level operating modes are still only implied by the workflow, not yet defined tightly enough to reuse across repositories.

One workflow ambiguity is now explicit: exploration should produce architectural conclusions in `02-overview-design.md` first. It may inform `03-detailed-design.md`, but it should not be read as permission to draft detailed design before overview design is coherent and reflected. The core skill docs should say this directly so the process does not self-contradict.

Another workflow ambiguity is now explicit too: brainstorming should make design explicit before action, but it should not impose mandatory user approval pauses during normal autonomous execution. The protocol should stop for review only when the user asked for it or when unresolved ambiguity makes continuation risky.

## Roadmap Structure
Keep `OH-004` as the parent roadmap package and treat the remaining work as five durable streams:

1. `runtime verification baseline`
   - Define what every no-harness repository must be able to verify before a task can credibly claim completion.
   - Focus on minimum acceptable defaults, evidence shape, and escalation paths when there is no existing runtime harness.
2. `python verification maturity`
   - Define the default verification floor for Python work when runtime tests are incomplete.
   - Focus on when `pytest` is enough, when runtime tests are required, and how weaker evidence must be recorded honestly.
3. `maintenance and entropy reduction`
   - Define recurring cleanup and review work so the repository does not decay into stale design packages, stale memory, or drifting skill docs.
   - Focus on periodic review loops rather than one-off feature work.
4. `status semantics tightening`
   - Align the workflow checkpoints with stronger machine- and human-readable meaning for each status.
   - Focus on readiness criteria, transition rules, and when a package should remain active versus archive.
5. `skill taxonomy and compatibility cleanup`
   - Clarify which skills are core protocol, optional helpers, compatibility shims, or legacy imports.
   - Focus on reducing ambiguity in the skill hub and in per-skill messaging.

## Stream Dependencies And Order
- `runtime verification baseline` and `status semantics tightening` should lead, because both change what `ready`, `verifying`, and `done` mean.
- `python verification maturity` depends on the minimum runtime verification baseline and status semantics, because it sharpens what acceptable Python evidence looks like inside completion and status claims.
- `maintenance and entropy reduction` depends on clearer status semantics and skill taxonomy, because maintenance needs stable definitions of stale, active, archived, core, and optional.
- `skill taxonomy and compatibility cleanup` can start earlier as a documentation cleanup, but it should finalize after status semantics are tightened so vocabulary does not drift again.

## Split Triggers
This roadmap should stay broad until a request satisfies one of these triggers:

- A stream has a narrow enough problem statement to produce concrete file-level changes in one round.
- A stream needs repository exploration or external comparison that would overwhelm this parent roadmap.
- A stream needs its own verification contract beyond the generic `check-designs` plus repository tests.
- A stream needs to introduce or revise reusable artifacts such as templates, automation, or project-memory conventions.

When those triggers are met, the agent should scaffold a focused child package rather than expanding `OH-004` with implementation detail.

## Key Flows
- A future task asks `what's still missing?`
- The agent enters `OH-004`.
- The roadmap identifies which stream the request belongs to and whether it is discovery work, design work, or implementation work.
- If the request is still broad, the agent updates `OH-004` first so the remaining product boundary stays explicit.
- If one stream is concrete enough, the agent scaffolds a focused child package derived from this roadmap and keeps `OH-004` as the umbrella view.
- `OH-005 Runtime Verification Baseline` is the first such child package and is now archived as the completed baseline for the runtime-verification stream.
- `OH-006 Status Semantics Tightening` is now archived as the completed baseline for stronger workflow checkpoint meaning and transition gates.
- `OH-007 Python Verification Maturity` is now archived as the completed design baseline for the Python verification stream and should be reused by the implementation wave rather than reopened casually.
- Completed child packages should feed evidence or durable decisions back into this roadmap only when they materially change what remains.

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
- I checked whether the next actionable stream was still ambiguous after `OH-005` and `OH-006` completed. It no longer is; the Python verification stream now has enough upstream structure to split into `OH-007`.
- No bounded subagent discussion was needed in this round because the uncertainty is about prioritization and scope control inside this repository, not about a hard architectural fork.
