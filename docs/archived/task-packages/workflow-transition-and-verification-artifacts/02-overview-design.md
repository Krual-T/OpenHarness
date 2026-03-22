# Overview Design

## System Boundary
This package extends the existing `openharness.py` CLI, task-package templates, and tests. It does not introduce a new workflow system. The goal is to make the current manifest-defined status flow and verification path executable as repository-local mechanics.

## Proposed Structure
Use a `single supported transition path plus structured verification artifacts` model.

The implementation has four parts:

1. `transition` as the supported workflow mutator
   - Add `openharness.py transition <task> <target-status>`.
   - Resolve the package by task slug or task id.
   - Use the manifest's ordered status flow as the legal forward path.
   - Allow only one-step forward transitions.
   - Allow conservative rollback to an earlier non-archived status so an overstated package can be corrected without manual YAML surgery.
   - Disallow transitions out of `archived` in this first wave.

2. Transition-time semantic enforcement
   - Before persisting a target status, validate the package as if it already had that status.
   - Reuse the existing semantic-anchor checks from `OH-009` so the transition gate and `check-tasks` speak the same language.
   - Treat `archived` as a stronger gate than other statuses:
     - current status must already be `verifying`
     - latest verification artifact must exist
     - latest verification result must be successful
     - `05-verification.md` and `06-evidence.md` must already satisfy archive anchors

3. Structured verification-run artifacts
   - Every `verify` invocation writes a JSON record under `.harness/artifacts/<task-id>/verification-runs/`.
   - Each record captures:
     - task identity and status at run time
     - start and finish timestamps
     - a fingerprint of the current package content
     - a snapshot of `required_commands` and `required_scenarios`
     - required commands and their exit codes
     - declared manual scenarios
     - overall result such as `passed`, `failed`, or `insufficient_verification`
   - The time-stamped JSON file is the evidence source of truth.
   - Also write a stable `latest.json` copy so later tooling can find the newest run without scanning filenames, but it is only an index.

4. STATUS binding and archive relocation
   - After each verify run, update `STATUS.yaml.verification` with:
     - `last_run_at`
     - `last_run_result`
     - `last_run_artifact`
   - Archive gating must read the artifact file itself, not trust these summary fields alone.
   - When archiving through `transition`, move the package directory into `docs/archived/task-packages/<task>/`.
   - Rewrite package-local path strings from `docs/task-packages/<task>/...` to `docs/archived/task-packages/<task>/...` so evidence and entrypoint references remain correct after the move.
   - Scan the rest of the repository for lingering active-root references and report them so follow-up fixes are explicit.

Three viable architecture choices were considered:

1. `docs-only plus stronger social rules`
   - Add more wording to task docs and skills.
   - Lowest effort, but it leaves the important mechanics outside the tool.
2. `additive CLI control plus file artifacts`
   - Extend the existing CLI and keep the source of truth in repository files.
   - Strong enough to close the main honesty gap without inventing a second system.
3. `full workflow ledger`
   - Add explicit transition history, custom schemas, or a dedicated trace store for every state mutation.
   - More complete, but premature for the repository's current complexity.

Recommended direction: `additive CLI control plus file artifacts`.

Reasoning:
- It keeps the workflow legible inside the existing repository contract.
- It reuses the semantics already established by `OH-006` and `OH-009` instead of redefining them.
- It makes archive claims depend on durable evidence without forcing the repository to adopt a heavyweight state engine.

## Key Flows
1. A package author completes the docs for the next checkpoint.
2. They run `openharness.py transition <task> <next-status>`.
3. The CLI checks that the requested move is legal under the manifest order and that the target checkpoint's semantic anchors are satisfied.
4. If valid, the CLI writes the new status and refreshes `updated_at`.
5. While implementation is in progress or verification is being gathered, `openharness.py verify <task>` runs the declared commands and records a JSON artifact plus latest-run metadata in `STATUS.yaml`.
6. When verification is complete enough to support closure, `transition <task> archived` checks the latest verification artifact result, then moves the package to the archive root and rewrites package-local references.
7. Archive should be treated as a two-phase action:
   - preconditions against the current active package
   - post-move validation against the archived package state
8. `check-tasks` continues to validate the final repository state, including any referenced latest verification artifact path.

## Trade-offs
- `single-step forward transitions`
  - makes optimistic skipping impossible through the supported path
  - slightly more verbose when moving a package several stages in one session
- `allow rollback to earlier active statuses`
  - supports correcting overstated status claims
  - leaves full transition history out of scope for now
- `JSON artifacts under .harness/artifacts`
  - durable and tool-friendly
  - requires a small amount of repository-local generated state
- `latest-run metadata in STATUS.yaml`
  - creates a direct binding from current state to evidence
  - adds a few mutable fields to the otherwise mostly human-authored status file
  - must remain summary-only so it does not become a second evidence truth source
- `archive only through transition`
  - closes the strongest remaining gap in completion semantics
  - still cannot stop a determined human from editing files manually outside the supported workflow

## Overview Reflection
- I considered making `transition` merely a convenience wrapper around direct YAML edits. I rejected that because the point of this package is to make the supported workflow mechanically stronger, not just easier to type.
- I considered requiring a richer transition-history ledger before allowing any workflow control. That would delay the high-value fix. The repository does not yet need immutable event sourcing to solve its current honesty gap.
- I checked whether verification artifacts should live only in markdown docs. They should not. Docs remain the human narrative, but archive gating needs a structured run record the CLI can inspect directly.
- I checked whether archive gating can rely on a simple `latest passed` flag. It should not. The artifact must also prove that it covers the current package content, otherwise old successful runs could be misused after later edits.
- I checked whether `verify` should also auto-transition the package. It should not in this first wave. Verification execution and workflow intent are related but still distinct actions.
- I checked whether archive gating should trust only `05-verification.md`. It should not. The docs should explain the evidence, but the archive gate should rely on the latest structured artifact so the check remains deterministic.
- No bounded subagent discussion was used while drafting the overview because the main alternatives were already narrowed by archived `OH-006` and `OH-009`.
