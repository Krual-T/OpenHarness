# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - Run `uv run python skills/using-openharness/scripts/openharness.py check-tasks` to confirm the parent roadmap and the archived child package still satisfy harness protocol.
  - Run `uv run python skills/using-openharness/scripts/openharness.py bootstrap` to confirm the maintenance stream no longer appears as active once `OH-017` archives and `OH-004` closes.
  - Run `uv run pytest` to confirm the final roadmap writeback and archive move do not introduce repository regressions.
- Fallback Path:
  - If `OH-017` cannot archive cleanly, `OH-004` must remain active because the final remaining stream would still be open.
  - If `bootstrap` still shows an active roadmap or maintenance package after archival work, stop and repair the remaining active-path references before claiming closure.
  - If `check-tasks` or `pytest` fails, fix the repository regression before archiving `OH-004`.
- Planned Evidence:
  - The archived `OH-017` package with a passing verification artifact and refreshed maintenance evidence.
  - The archived `OH-004` roadmap docs stating that no unfinished completion streams remain.
  - Fresh `check-tasks`, `bootstrap`, and `pytest` results captured in `04-verification.md` and `05-evidence.md`.

## Testing-First Design
This roadmap package does not add runtime code directly. Its `tests` are repository-legibility checks:

- the package must remain valid under `openharness.py check-tasks`
- the package must state a decomposition clear enough that a future agent can create a child package without rediscovery
- the package must record verification expectations and follow-up boundaries instead of leaving them implicit

## Files Added Or Changed
- Update the `OH-004` design documents so they capture stream boundaries, dependency order, split triggers, and concrete expected outputs.
- Archive `OH-017 Maintenance And Entropy Reduction` after its first maintenance implementation wave closes the last remaining stream.
- Archive `OH-004` itself once the roadmap no longer has unfinished streams.
- Keep `OH-004` at roadmap level rather than letting later implementation detail accumulate here.

## Interfaces
This roadmap no longer owns any unfinished stream. Future work should create a new focused package with these minimum outputs instead of reopening `OH-004`:

- a narrow problem statement and verification path
- explicit writeback locations
- bounded implementation scope that does not rely on reviving the old roadmap as an active backlog

The already-completed baselines should be reused instead of re-designed here:

- `runtime verification baseline`
- `status semantics tightening`
- `task package semantic validation`
- `workflow transition and verification artifacts`
- `python verification maturity`
- `skill taxonomy and compatibility cleanup`
- `skill taxonomy and stage model`

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
- `OH-008 Skill Taxonomy And Compatibility Cleanup` is now the archived baseline for stable skill categories and retirement of the old plan-oriented surface.
- `OH-012 Skill Taxonomy And Stage Model` is now the archived follow-up that turns the taxonomy baseline into live protocol-status and workflow-stage wording and productizes the Python-first pytest floor.
- `OH-010 Workflow Transition And Verification Artifacts` is now archived as the completed implementation wave for supported transitions and verification artifact closure.
- `OH-017 Maintenance And Entropy Reduction` is now the archived completed child package that owns the reusable maintenance baseline.

## Detailed Reflection
- I challenged whether `OH-004` needed file-level implementation steps now. It does not; adding them here would duplicate the work that belongs in child packages.
- I challenged whether the roadmap was still too abstract to verify. The answer was yes in its earlier form, so this revision adds expected outputs and likely repository touch points for each stream.
- I checked whether the detailed design made runtime verification concrete enough. It is now concrete at the roadmap level by defining the kinds of artifacts and semantics the next child package must settle.
- I checked whether `OH-004` still needed to hold taxonomy implementation detail itself. It does not; that detail now belongs in archived `OH-008`.
- I checked whether an archived umbrella roadmap was still useful once all streams completed. It is, but only as a historical fact source; new work should branch into a new focused package instead of reactivating `OH-004`.
- No bounded subagent discussion was needed in this round because the main uncertainty is package decomposition, not a contested implementation path.
