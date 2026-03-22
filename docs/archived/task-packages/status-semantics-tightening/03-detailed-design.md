# Detailed Design

## Runtime Verification Plan
- Verification Path: repository automation for this design package, using harness validation and repository tests
- Fallback Path: if repository tests fail for unrelated reasons, record the blocking failure in `05-verification.md` and keep the package below any completion claim
- Planned Evidence:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - targeted tests for any new CLI status-semantics behavior added in this stream

## Files Added Or Changed
- Update `docs/task-packages/status-semantics-tightening/README.md`, `STATUS.yaml`, and `01-requirements.md` to establish the focused package.
- Update `02-overview-design.md` with the status ladder semantics, transition rules, CLI alignment points, and reflection.
- In the first implementation wave for this package, likely update:
  - `skills/using-openharness/scripts/openharness.py`
  - `skills/using-openharness/tests/test_openharness.py`
  - `skills/using-openharness/references/manifest.yaml` only if the status vocabulary itself changes, which is not currently recommended
  - design-package templates and workflow wording where status expectations need to become explicit
- Update `OH-004` evidence and follow-up notes so the parent roadmap reflects that `status semantics tightening` is now active child work.
- First implementation wave now completed for CLI default verification scope:
  - `cmd_verify` defaults to `in_progress` and `verifying`
  - explicit package targeting still allows earlier-stage manual inspection when intentionally requested
- Second implementation wave now completed for lightweight semantic validation:
  - `validate_design_package` rejects `verifying` packages that declare no verification path
  - `validate_design_package` rejects `archived` packages that declare no verification path
- Third implementation wave now completed for template guidance:
  - design-package templates now remind authors that status should match the highest completed workflow checkpoint
  - `03-detailed-design.md` and `05-verification.md` templates now call out the intended boundary for `in_progress` and `verifying`
- Fourth implementation wave now completed for workflow skill wording:
  - `using-openharness` now states the intended boundary for `in_progress`, `verifying`, and `archived`
  - `exploring-solution-space` now ties coherent reflected design output to `overview_ready` and `detailed_ready`

## Interfaces
- Current status surfaces that this package must reconcile:
  - `manifest.yaml` as the ordered source of allowed statuses
  - `openharness.py` constants such as `ACTIVE_STATUSES` and `VERIFYABLE_STATUSES`
  - design-package templates that imply when docs are considered complete enough to progress
  - workflow skills that refer to design readiness, implementation start, verification, and archiving
- Expected implementation-facing interfaces to define:
  - which statuses count as active work versus verification-ready work
  - whether semantic checks belong in `validate_design_package`, `cmd_verify`, or both
  - how explicit status expectations should be surfaced in templates without duplicating the full workflow docs

## Implementation Order
1. Tighten the status semantics in package docs first:
   - define each status
   - define the intended transition edges
   - define how `OH-005` verification rules constrain `verifying` and `archived`
2. Add tests that expose the current semantic mismatch:
   - default `verify` scope is too broad
   - later validation should reject obvious status/readiness contradictions if introduced
3. Update `openharness.py` with the smallest behavior changes that reflect the settled semantics:
   - narrow default verification scope toward `in_progress` and `verifying`
   - preserve explicit package targeting for exceptional/manual inspection
4. Decide whether templates and workflow wording need lightweight status guidance in the same round or a follow-up round.
5. Only after repository usage validates the semantics, consider stronger machine-readable transition metadata.

## Test Design
- Add CLI tests that pin the default verification scope to the intended later-stage statuses rather than all post-requirements statuses.
- Add validation tests if the implementation introduces new semantic checks for status/readiness contradictions.
- Keep existing package-structure tests green so status tightening does not silently break current harness protocol guarantees.

## Error Handling
- If local exploration shows that some archived packages historically used statuses inconsistently, treat those as migration inputs rather than as proof that the loose semantics should be preserved.
- If tightening default `verify` scope would hide a legitimate workflow, preserve explicit package targeting instead of widening the default again.
- If a proposed semantic rule cannot be explained clearly in templates and skills, it is probably too complicated for this repository's current workflow maturity.
- Do not let status semantics drift into a second workflow system with parallel per-package state machines.

## Migration Notes
- This package depends conceptually on `OH-005` but should avoid re-litigating the verification ladder itself.
- The first rollout should clarify semantics and fix the most visible CLI mismatch before attempting richer transition enforcement.
- Downstream streams such as no-harness bootstrap and maintenance should consume the settled status meanings rather than defining their own status vocabulary.

## Detailed Reflection
- I challenged whether this package already needed a new manifest schema. It does not; the biggest current value is to settle meaning and fix the default CLI mismatch.
- I checked whether the testing strategy should start from package-doc assertions or CLI behavior. CLI behavior should lead, because it is where the current semantic contradiction is already encoded.
- I challenged whether templates should be updated before CLI behavior. They may need updates in the same round, but they should follow the status semantics and test outcomes rather than lead them.
- I checked whether narrowing `verify` to later-stage statuses would make the workflow too rigid. It would not, because explicit package targeting still provides an escape hatch while the default behavior becomes more honest.
- I re-checked whether `overview_ready` or `detailed_ready` should stay in the default verification scope. They should not. Those statuses may still support targeted verification when explicitly requested, but they are not the default stage for repository-wide verification runs.
- I checked whether lightweight semantic validation should extend all the way back to earlier statuses immediately. It should not. The best next step is to catch only obvious contradictions for `verifying` and `archived`, where the verification contract is already settled by `OH-005`.
- I checked whether template guidance should wait for stronger machine validation. It should not. Lightweight prompts in templates are cheap and reduce drift without pretending to be enforcement.
- I checked whether workflow skill wording needed the same treatment after templates were updated. It did. Otherwise new packages and ongoing work would still learn different status cues depending on whether the agent was reading templates or skills.
- No bounded subagent discussion was used because the remaining design questions are concrete, local, and already shaped by repository evidence.
