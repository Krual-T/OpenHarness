# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - Docs-first design verification in this round.
  - Follow-up implementation rounds should verify bootstrap behavior with `check-designs`, `bootstrap`, and repository tests, plus targeted manual bootstrap scenarios when needed.
- Fallback Path:
  - If a full bootstrap scenario cannot yet be automated, capture the bootstrap sequence as explicit manual steps and record the gap that blocks stronger automation.
- Planned Evidence:
  - `05-verification.md` should record design-package validation, bootstrap inventory output, and repository test results for the implementation wave.
  - `06-evidence.md` should record any manual bootstrap transcript or reproduction steps used to validate no-harness entry.

Move to `in_progress` only when detailed design is concrete enough to execute.

## Files Added Or Changed
- Update `docs/designs/no-harness-bootstrap-workflow/*` so the package defines bootstrap requirements, architecture, and implementation landing points.
- Update `docs/designs/harness-completion-roadmap/*` so `OH-004` clearly treats `OH-007` as the active child package for the bootstrap stream.
- In the implementation wave, likely update:
  - `AGENTS.md`
  - `README.md`
  - `skills/using-openharness/SKILL.md`
  - `skills/using-openharness/references/skill-hub.md` if bootstrap wording changes affect taxonomy
  - `skills/using-openharness/references/templates/*`
  - `skills/using-openharness/scripts/openharness.py`
  - `skills/using-openharness/tests/test_openharness.py`

## Interfaces
The bootstrap workflow should expose these stable decisions:

- `entry detection`
  - If valid active packages already exist, bootstrap mode does not apply; use the normal workflow.
  - If no valid packages exist, the workflow must decide whether to adopt existing repo structure or scaffold missing pieces.
- `minimum artifact contract`
  - Required after bootstrap:
    - repo map entrypoint
    - manifest-backed package protocol
    - one active design package with the required files
    - declared verification path for the bootstrap round
  - Optional after bootstrap:
    - populated `.project-memory/`
    - maintenance review artifacts
    - deeper taxonomy cleanup
- `first package selection`
  - If there is one obvious repository-shaping first task, bootstrap should create a focused package for that task.
  - If the repository first needs harness-enabling work before any product task is safe, bootstrap should create a package for the bootstrap round itself.
- `status progression`
  - The first package should begin at `proposed` or `requirements_ready`, then follow `OH-006` readiness checkpoints normally.
  - Bootstrap completion does not skip directly to later statuses without the corresponding design artifacts.

## Error Handling
- If the repository already has partial docs or workflow files, bootstrap should adopt and normalize them rather than blindly replacing them.
- If no credible verification path can be established, the repository is not yet bootstrapped enough to claim normal completion semantics.
- If multiple unrelated first tasks compete for priority, bootstrap should create a narrow package that resolves repository entry first, then split later work into follow-up packages.
- If lightweight CLI help would force a rigid generator assumption, prefer explicit docs and templates over premature automation.

## Migration Notes
- `OH-007` should stay active through the implementation wave even if the first patch only lands doc and template support.
- Once the bootstrap workflow is implemented and verified, archive this package and feed any remaining maintenance or taxonomy implications back into `OH-004`.

## Detailed Reflection
- I challenged whether this package needed file-by-file code edits already. It does not; the current round only needs the landing zones and interface contracts that the implementation wave will follow.
- I challenged the testing strategy first. A pure unit-test view would miss the core product risk, which is the end-to-end first-entry sequence in a weakly structured repository. The design now treats scenario-level bootstrap validation as a first-class concern.
- I checked whether the interfaces were still too abstract to implement. They were initially; this revision now states explicit entry detection, minimum artifact contract, first-package selection, and status progression rules.
- I checked whether runtime verification was concrete enough. For a design-only round, it is concrete enough because it names the executed commands and the fallback to explicit manual bootstrap transcripts.
- No bounded subagent discussion was used because the remaining uncertainty is implementation staging, not a contested architectural fork.
