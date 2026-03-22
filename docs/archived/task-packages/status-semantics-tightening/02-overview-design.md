# Overview Design

## System Boundary
This package defines the shared meaning of workflow statuses inside OpenHarness design packages. It does not create a new workflow model. It tightens the existing default status flow so package docs, templates, CLI behavior, and tests refer to the same readiness contract.

## Proposed Structure
Treat statuses as explicit readiness checkpoints, not as informal progress labels.

The proposed baseline semantics are:

1. `proposed`
   - A package has been scaffolded, but requirements are still incomplete or unstable.
   - The package may contain placeholders, but it should not be treated as ready for architecture exploration.
2. `requirements_ready`
   - `01-requirements.md` is concrete enough to explore solutions without rediscovering the basic problem framing.
   - This is the earliest status that may justify focused solution-space exploration.
3. `overview_ready`
   - `02-overview-design.md` defines a coherent architecture and includes an explicit reflection pass.
   - The package is now ready to constrain detailed design rather than still debating system boundary.
4. `detailed_ready`
   - `03-detailed-design.md` defines testing-first implementation landing points, runtime verification planning, and a detailed reflection pass.
   - This is the last design-only checkpoint before implementation starts.
5. `in_progress`
   - Execution against the detailed design is underway, or the package is actively bringing the implementation into the state required for verification.
   - The package should not enter this status until detailed design is concrete enough to execute.
6. `verifying`
   - Implementation is complete enough to run the declared verification path and gather fresh evidence.
   - This is not a synonym for “basically done”; it is a narrow evidence-finalization stage constrained by the verification contract from `OH-005`.
7. `archived`
   - The package is complete, verification and evidence docs are updated, and the package has moved to `docs/archived/task-packages/<task>/`.
   - Archived packages remain evidence, but they are no longer active work.

The key rule is that every later status must imply the work of earlier design checkpoints is already materially complete. Statuses therefore form a cumulative readiness ladder, not separate labels an agent can jump between casually.

The transition model should stay simple:

- `proposed -> requirements_ready`: problem framing is explicit enough to explore
- `requirements_ready -> overview_ready`: architecture and boundary choices are coherent and reflected
- `overview_ready -> detailed_ready`: implementation/test strategy is concrete and reflected
- `detailed_ready -> in_progress`: execution has started against a stable detailed design
- `in_progress -> verifying`: implementation is complete enough to gather fresh verification evidence
- `verifying -> archived`: evidence is complete, completion claims are credible, and the package is moved to the archive root

The runtime verification baseline from `OH-005` tightens the last two transitions:

- a package should not enter `verifying` without a declared verification path
- `insufficient verification` may block completion and archive even if implementation work is finished
- manual verification may support `verifying`, but only when its steps and blind spots are explicit

That implies a small but important CLI alignment:

- `bootstrap` may continue to treat all non-archived statuses as active work
- `verify` should no longer imply that early design statuses are verification-ready by default
- validation should remain lightweight, but it should be able to reject obvious status/location contradictions and later grow into semantic transition checks

Three viable architectural options emerged:

1. `documentation-only semantics`
   - Define status meanings only in design docs and skills.
   - Lowest effort, but too weak because CLI defaults would still encode looser behavior.
2. `docs-first semantics, CLI-assisted`
   - Define the semantics in package docs first, then align CLI defaults, tests, and templates with those meanings.
   - Strong enough to matter without introducing a new state engine.
3. `schema-first transition engine`
   - Add explicit transition metadata and machine-enforced gates to `STATUS.yaml` immediately.
   - More expressive, but premature before the repository has validated the core status meanings.

Recommended direction: `docs-first semantics, CLI-assisted`.

Reasoning:

- It matches the repository's current maturity level: status names already exist, but their shared meaning does not.
- It fixes the largest current contradiction, where CLI verification scope is broader than the intended meaning of `verifying`.
- It leaves room for stronger machine enforcement later without forcing a new schema before the semantics are stable.

## Key Flows
1. A package is scaffolded and starts as `proposed`.
2. Once `01-requirements.md` is explicit enough to support exploration, it moves to `requirements_ready`.
3. Exploration produces a coherent `02-overview-design.md`, which after reflection moves the package to `overview_ready`.
4. Detailed design produces a concrete `03-detailed-design.md`, which after reflection moves the package to `detailed_ready`.
5. Implementation or execution work moves the package to `in_progress`.
6. Once execution is complete enough to run the declared verification path, the package enters `verifying`.
7. Fresh evidence is written into `05-verification.md` and `06-evidence.md`.
8. Only after that evidence is credible and complete does the package move to `archived` and relocate to the archive root.

Current local constraints that shape the solution:

- `skills/using-openharness/references/manifest.yaml` already defines the ordered status vocabulary, so this package should refine meaning before changing the list.
- `skills/using-openharness/scripts/openharness.py` currently treats every status except `proposed` and `archived` as verifyable by default, which is semantically too broad.
- Templates currently teach verification planning but do not yet teach how status readiness relates to document completeness.
- Existing tests validate allowed status names and archive placement, but they do not yet assert stronger semantics around verification eligibility or transition meaning.

## Trade-offs
- Stronger status meanings reduce ambiguity, but they also make it harder to hide incomplete design work behind optimistic labels.
- Aligning CLI defaults with the semantics makes the workflow more honest, but it may expose existing packages that were relying on loose status usage.
- Keeping the first wave docs-first avoids premature schema churn, but it means some transition rules will still be social/documentary before later machine enforcement lands.
- Treating statuses as cumulative checkpoints improves legibility, but it requires agents to update package docs more deliberately rather than treating status as a casual note.

## Overview Reflection
- I challenged whether status semantics should stay documentation-only. That would leave the current CLI contradiction intact, especially around which packages `verify` should target by default.
- I challenged whether this package should immediately introduce a richer transition schema in `STATUS.yaml`. That is too early; the repository has not yet validated the core meaning of each status.
- I checked whether `bootstrap` should narrow its active-status set too. It should not in the first wave; early design statuses are still active work even if they are not verification-ready.
- I checked whether `verifying` should remain a broad “wrap-up” label. It should not. `OH-005` already established that verification evidence is a real gate, so `verifying` needs to become a narrow evidence-gathering stage.
- I checked whether `archived` needs new meaning beyond location. It does: archive should imply verified completion and evidence writeback, not just physical movement to another directory.
- No bounded subagent discussion was used because the main design choice is repository-local and the strongest alternative, a schema-first transition engine, is clearly premature at this stage.
