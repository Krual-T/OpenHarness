# Detailed Design

## Testing-First Design
This roadmap package does not add runtime code directly. Its `tests` are repository-legibility checks:

- the package must remain valid under `openharness.py check-tasks`
- the package must state a decomposition clear enough that a future agent can create a child package without rediscovery
- the package must record verification expectations and follow-up boundaries instead of leaving them implicit

## Files Added Or Changed
- Update the `OH-004` design documents so they capture stream boundaries, dependency order, split triggers, and concrete expected outputs.
- Scaffold the next focused child package when one stream becomes concrete enough to stand on its own.
- Keep `OH-004` at roadmap level rather than letting child-package implementation detail accumulate here.

## Interfaces
Each remaining future stream should produce its own focused package with these minimum outputs:

- `maintenance and entropy reduction`
  - define regular cleanup loops for archived packages, stale evidence, stale memory, and protocol drift
  - define how maintenance work is triggered and where results are written back
  - likely touch skill docs, `.project-memory/` conventions if present, and maybe add maintenance checklists
- `skill taxonomy and compatibility cleanup`
  - define a stable classification of core protocol, optional helpers, compatibility shims, and imported generic skills
  - define how skills should describe themselves so the hub does not imply parallel entry systems
  - likely touch `skill-hub.md`, per-skill `SKILL.md` files, and maybe README-level explanation

The already-completed baselines should be reused instead of re-designed here:

- `runtime verification baseline`
- `status semantics tightening`
- `task package semantic validation`
- `workflow transition and verification artifacts`
- `python verification maturity`

## Error Handling
- If a future task tries to solve several of these streams at once, this package should be used to decompose the request before implementation.
- If future discussions produce new major missing areas, they should be added here first unless they are already concrete enough for a focused package.
- If a child package changes the roadmap order or removes a stream entirely, `OH-004` must be updated in the same round so the parent roadmap stays authoritative.

## Migration Notes
- This package is intentionally broad and may stay active longer than a typical feature package.
- When a substream becomes concrete, prefer creating a dedicated follow-up package rather than overloading this roadmap with implementation detail.
- `runtime verification baseline` and `status semantics tightening` are archived completed baselines.
- `task package semantic validation` is the archived completed follow-up that adds the next semantic-enforcement wave on top of `OH-006`.
- `OH-007 Python Verification Maturity` is a legacy archived design baseline written before task-package completion semantics were tightened; future work should not treat it as proof that design-complete alone is archive-ready.
- `OH-008 Skill Taxonomy And Compatibility Cleanup` now carries the next implementation-ready design work for this roadmap.
- `OH-010 Workflow Transition And Verification Artifacts` is now archived as the completed implementation wave for supported transitions and verification artifact closure.

## Detailed Reflection
- I challenged whether `OH-004` needed file-level implementation steps now. It does not; adding them here would duplicate the work that belongs in child packages.
- I challenged whether the roadmap was still too abstract to verify. The answer was yes in its earlier form, so this revision adds expected outputs and likely repository touch points for each stream.
- I checked whether the detailed design made runtime verification concrete enough. It is now concrete at the roadmap level by defining the kinds of artifacts and semantics the next child package must settle.
- I checked whether `OH-004` still needed to hold taxonomy implementation detail itself. It does not; that detail now belongs in `OH-008`.
- No bounded subagent discussion was needed in this round because the main uncertainty is package decomposition, not a contested implementation path.
