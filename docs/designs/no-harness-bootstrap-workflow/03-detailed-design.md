# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - Docs-first design verification in this round.
  - Follow-up implementation rounds should verify cold-start behavior with `check-designs`, `bootstrap`, and repository `pytest` runs on the supported Python default path.
  - When a task materially depends on runtime behavior, the package should explicitly recommend adding runtime tests next or building them in parallel rather than pretending `pytest` alone closes the gap.
- Fallback Path:
  - If a full cold-start scenario cannot yet be automated, capture the sequence as explicit manual steps and record the gap that blocks stronger automation.
- Planned Evidence:
  - `05-verification.md` should record design-package validation, bootstrap inventory output, and repository `pytest` results for the implementation wave on the Python default path.
  - `06-evidence.md` should record any manual cold-start transcript or reproduction steps, plus the explicit note about whether runtime tests still need to be constructed.

Move to `in_progress` only when detailed design is concrete enough to execute.

## Files Added Or Changed
- Update `docs/designs/no-harness-bootstrap-workflow/*` so the package defines bootstrap requirements, architecture, and implementation landing points.
- Update `docs/designs/harness-completion-roadmap/*` so `OH-004` clearly treats `OH-007` as the active child package for the bootstrap stream.
- In the implementation wave, likely update:
  - `AGENTS.md`
  - `README.md`
  - `skills/using-openharness/SKILL.md`
  - `skills/using-openharness/references/templates/*`
  - `skills/verification-before-completion/SKILL.md`
  - `skills/using-openharness/scripts/openharness.py` only if minimal guidance output is still necessary
  - `skills/using-openharness/tests/test_openharness.py`

## Interfaces
The cold-start workflow should expose these stable decisions:

- `entry detection`
  - If valid active packages already exist, bootstrap mode does not apply; use the normal workflow.
  - If no valid packages exist, the workflow must decide whether to adopt existing repo structure or scaffold missing pieces.
- `minimum artifact contract`
  - Required after cold start:
    - repo map entrypoint
    - manifest-backed package protocol
    - one active design package with the required files
    - declared `pytest`-based verification floor for the cold-start round
  - Optional after cold start:
    - populated `.project-memory/`
    - maintenance review artifacts
    - deeper taxonomy cleanup
- `first package selection`
  - If there is one obvious repository-shaping first task, bootstrap should create a focused package for that task.
  - If the repository first needs harness-enabling work before any product task is safe, bootstrap should create a package for the bootstrap round itself.
- `verification guidance`
  - `pytest` is the default minimum gate for the supported Python cold-start path.
  - If runtime behavior is central to the task, the package must explicitly say whether runtime tests are required now or recommended next.
  - "Recommended next" and "required now" must not be mixed together implicitly.
  - Non-Python repositories may reuse the package protocol, but they do not inherit an equally defined default verification floor from this package.
- `status progression`
  - The first package should begin at `proposed` or `requirements_ready`, then follow `OH-006` readiness checkpoints normally.
  - Cold-start completion does not skip directly to later statuses without the corresponding design artifacts.

## Error Handling
- If the repository already has partial docs or workflow files, cold start should adopt and normalize them rather than blindly replacing them.
- If `pytest` cannot credibly run and there is no stronger existing automated path on the Python default path, the repository is not yet ready to claim a usable cold start there.
- If multiple unrelated first tasks compete for priority, cold start should create a narrow package that resolves repository entry first, then split later work into follow-up packages.
- If lightweight CLI help would force a rigid generator assumption, prefer explicit docs and templates over premature automation.

## Migration Notes
- `OH-007` should stay active through the implementation wave even if the first patch only lands docs, templates, and verification wording.
- Once the Python-first cold-start workflow is implemented and verified, archive this package and feed any remaining maintenance implications back into `OH-004`.

## Detailed Reflection
- I challenged whether this package still needed a generic verification ladder at cold start. It does not need one for every language; the supported default path can stay simpler, with Python using `pytest` as the minimum floor.
- I challenged the testing strategy first. The key risk is not absence of perfect runtime tests on day one; it is silent ambiguity about whether `pytest` is enough for now and when runtime tests must be added. The design now makes that distinction explicit.
- I checked whether the interfaces were still too abstract to implement. They were initially; this revision now states explicit entry detection, minimum artifact contract, verification guidance, and status progression rules.
- I checked whether runtime verification was concrete enough. For a design-only round, it is concrete enough because it names `pytest` as the floor and requires packages to state whether runtime tests are required now or recommended next.
- No bounded subagent discussion was used because the remaining uncertainty is implementation staging, not a contested architectural fork.
