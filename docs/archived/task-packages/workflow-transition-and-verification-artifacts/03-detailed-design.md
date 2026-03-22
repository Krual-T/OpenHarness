# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - add targeted tests for legal and illegal status transitions
  - add targeted tests for verify artifact creation, status writeback, and archive gating
  - implement the new CLI behavior in `skills/using-openharness/scripts/openharness.py`
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if archive auto-move proves too risky in the first pass, keep the move inside `transition archived` but narrowly rewrite only the known path-bearing status fields instead of doing broad markdown replacement
  - if latest verification metadata on old archived packages becomes too disruptive, keep validation additive and enforce it primarily through the new transition path rather than retroactive hard failure
- Planned Evidence:
  - updated `OH-010` docs
  - new `transition` subcommand and helpers in `openharness.py`
  - JSON verification artifacts under `.harness/artifacts/`
  - updated templates that teach latest verification metadata and artifact references
  - tests covering transition legality, verify artifacts, and archive relocation

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/archived/task-packages/workflow-transition-and-verification-artifacts/*`
- `docs/task-packages/harness-completion-roadmap/*`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `skills/using-openharness/references/templates/task-package.06-evidence.md`

## Interfaces
- Add small internal helpers in `openharness.py` for:
  - loading and saving `STATUS.yaml`
  - resolving a package by slug or task id
  - computing legal transitions from the manifest flow
  - validating a package against a temporary target status
  - recording a verification-run artifact and copying `latest.json`
  - moving an archived package and rewriting package-local path references
- Public CLI surface:
  - `openharness.py transition <task> <target-status>`
  - `openharness.py verify [task] [--check-tasks-only]`
- Additive `STATUS.yaml` fields under `verification`:
  - `last_run_at`
  - `last_run_result`
  - `last_run_artifact`
- Verification artifact JSON should include at least:
  - package id, slug, and title
  - status at run time
  - timestamps
  - package fingerprint
  - required command/scenario snapshot
  - per-command results
  - declared manual scenarios
  - overall result
  - `latest.json` is only an index to the latest time-stamped artifact, not a separate truth source

## Error Handling
- Reject unknown target statuses and skipped forward moves with targeted messages that name the current status and expected next status.
- Reject transition to `archived` unless the current status is `verifying`, the latest verification artifact exists, and its `overall_result` is `passed`.
- Also reject archive if the artifact fingerprint no longer matches the current package content.
- If `verify` runs commands and one fails, still write the artifact with `overall_result: failed` before returning a non-zero exit code.
- If a package declares only manual scenarios, record that fact in the artifact and return success without pretending those steps were executed automatically.
- If a package declares no verification path, record `insufficient_verification` in the artifact and return a non-zero exit code.
- Keep artifact-path validation deterministic: only referenced paths that actually exist should be accepted.

## Migration Notes
- The new workflow should be additive: existing packages remain readable, but new verification runs start producing structured artifacts immediately.
- `OH-004` should be updated to list this package as the next active follow-up under the workflow-semantics stream.
- Once `transition` exists, this package itself should use it to move through `requirements_ready`, `overview_ready`, `detailed_ready`, `in_progress`, `verifying`, and `archived`.
- Historical archived packages do not need reconstructed command-by-command artifacts to remain useful fact sources; the stronger archive gate applies to packages archived through the new path.
- Archive should be implemented as a small filesystem transaction: prepare the archived result first, switch roots, then validate the post-move package and restore the active package if the archived state is invalid.

## Detailed Reflection
- I challenged whether rollback should be disallowed entirely. That would make honest correction awkward and would push users back toward direct YAML edits, so I kept rollback to earlier active statuses allowed.
- I challenged whether archive transition should allow `in_progress -> archived` when the latest verify artifact passed. It should not. Keeping `verifying` as an explicit penultimate stage preserves the workflow meaning already defined in earlier packages.
- I checked whether artifact writeback should happen only on successful verify runs. It should not. Failed and insufficient runs are exactly the cases where durable evidence is most useful.
- I checked whether `latest.json` is redundant if `STATUS.yaml` stores the path to a timestamped artifact. It is still useful as a stable file path for future tooling and human inspection.
- I checked whether `latest.json`, the timestamped artifact, and `STATUS.yaml` together create a multi-source-truth problem. The design stays coherent only if the timestamped artifact remains authoritative and the other two are treated as pointers or summaries.
- I checked whether broad path rewriting inside an archived package risks overreach. The implementation should keep the rewrite narrow to the package's own active-root path prefix.
- Runtime verification is concrete enough because the change can be pinned with targeted tests plus the repository-wide `check-tasks` and `pytest` baseline.
