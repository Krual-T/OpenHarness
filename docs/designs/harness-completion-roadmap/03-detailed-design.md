# Detailed Design

## Testing-First Design
This roadmap package does not add runtime code directly. Its `tests` are repository-legibility checks:

- the package must remain valid under `openharness.py check-designs`
- the package must state a decomposition clear enough that a future agent can create a child package without rediscovery
- the package must record verification expectations and follow-up boundaries instead of leaving them implicit

## Files Added Or Changed
- Update the `OH-004` design documents so they capture stream boundaries, dependency order, split triggers, and concrete expected outputs.
- Reframe `OH-007` as `Python Verification Maturity` now that the real gap is verification policy rather than bootstrap entry routing.
- Tighten workflow wording in core skill docs so exploration lands in `02-overview-design.md` first and only feeds `03-detailed-design.md` when implementation constraints are already justified.
- Tighten `brainstorming` so explicit design remains mandatory but default execution stays autonomous unless the user requested a review gate or unresolved ambiguity makes continuation risky.
- Do not add code or new automation in this round; this package should stay at roadmap level.

## Interfaces
Each future stream should produce its own focused package with these minimum outputs:

- `runtime verification baseline`
  - define acceptable minimum command, scenario, or manual-interaction evidence for repos with no existing harness
  - define what goes into `03-detailed-design.md`, `05-verification.md`, and `06-evidence.md` when runtime verification is weak or partly manual
  - likely touch `skills/using-openharness/SKILL.md`, verification-oriented skills, template docs, and possibly `openharness.py verify`
- `python verification maturity`
  - define the Python baseline, runtime-test escalation rules, and evidence wording when runtime verification is incomplete
  - define which verification expectations belong in detailed design versus verification and evidence docs
  - likely touch templates, verification-oriented skills, and completion guidance
- `maintenance and entropy reduction`
  - define regular cleanup loops for archived packages, stale evidence, stale memory, and protocol drift
  - define how maintenance work is triggered and where results are written back
  - likely touch skill docs, `.project-memory/` conventions if present, and maybe add maintenance checklists
- `status semantics tightening`
  - define entry and exit criteria for `proposed`, `requirements_ready`, `overview_ready`, `detailed_ready`, `in_progress`, `verifying`, and `archived`
  - define what evidence must exist before a package changes state
  - likely touch manifest references, `openharness.py`, tests, templates, and package docs
- `skill taxonomy and compatibility cleanup`
  - define a stable classification of core protocol, optional helpers, compatibility shims, and imported generic skills
  - define how skills should describe themselves so the hub does not imply parallel entry systems
  - likely touch `skill-hub.md`, per-skill `SKILL.md` files, and maybe README-level explanation

## Error Handling
- If a future task tries to solve several of these streams at once, this package should be used to decompose the request before implementation.
- If future discussions produce new major missing areas, they should be added here first unless they are already concrete enough for a focused package.
- If a child package changes the roadmap order or removes a stream entirely, `OH-004` must be updated in the same round so the parent roadmap stays authoritative.

## Migration Notes
- This package is intentionally broad and may stay active longer than a typical feature package.
- When a substream becomes concrete, prefer creating a dedicated follow-up package rather than overloading this roadmap with implementation detail.
- `runtime verification baseline` and `status semantics tightening` are now archived completed baselines.
- The current active next package is `OH-007 Python Verification Maturity`.

## Detailed Reflection
- I challenged whether `OH-004` needed file-level implementation steps now. It does not; adding them here would duplicate the work that belongs in child packages.
- I challenged whether the roadmap was still too abstract to verify. The answer was yes in its earlier form, so this revision adds expected outputs and likely repository touch points for each stream.
- I checked whether the detailed design made runtime verification concrete enough. It is now concrete at the roadmap level by defining the kinds of artifacts and semantics the next child package must settle.
- I checked whether `OH-004` still needed to hold the Python verification-policy detail itself. It does not; that detail now belongs in `OH-007`.
- No bounded subagent discussion was needed in this round because the main uncertainty is package decomposition, not a contested implementation path.
