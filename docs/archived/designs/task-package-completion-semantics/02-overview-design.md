# Overview Design

## System Boundary
This package repairs the repository's core workflow object. The object remains the single end-to-end unit that carries requirements, design, implementation, verification, and archive evidence. The change is not to split the object in two. The change is to rename it truthfully and align archive semantics with that truth.

## Local Findings
Repository exploration shows three important facts:

- The repository already uses one package for the whole lifecycle, not a design-only artifact.
- Human-facing protocol surfaces still call that object `design package` in `AGENTS.md`, the manifest, workflow skills, templates, CLI help text, and tests.
- The current status flow already has a natural non-archived landing point for "design complete, implementation not started yet": `detailed_ready`.

The failure happened because the name and the lifecycle did not match. `OH-007` then amplified the mismatch by being archived as a completed design baseline while still documenting a later implementation wave.

## Options Considered
1. Keep `design package`, only tighten archive wording.
   - Lowest migration cost.
   - Rejected because the name would keep teaching the wrong lifecycle.
2. Rename to `task package`, but leave archive semantics mostly unchanged.
   - Better naming.
   - Rejected because the main operational bug is false completion, not vocabulary alone.
3. Rename to `task package` and tighten completion semantics together.
   - Higher migration cost.
   - Recommended because it fixes the mental model and the state contract at the same time.

Recommended direction: option 3.

## Proposed Structure
Adopt these repository-level rules:

1. `task package` is the primary name for the end-to-end unit.
   - Use it in repository map docs, workflow skills, CLI help text, templates, and tests.
2. `archived` means the task package is fully completed.
   - Implementation is done.
   - Verification evidence is recorded.
   - The work is no longer active.
3. `detailed_ready` is the holding status for packages whose requirements and design are complete but whose implementation has not yet been carried out.
4. Older archived packages created under the previous semantics must be treated as legacy historical records.
   - They should not keep teaching that design-complete implies archive-ready.
   - Where necessary, add explicit wording that they were archived under superseded semantics.

## Compatibility Strategy
Do not move the filesystem roots in this round.

- Keep `docs/designs/<task>/` and `docs/archived/designs/<task>/` as compatibility paths.
- Keep manifest keys such as `designs_root` for now if changing them would create broad churn.
- Rename human-facing protocol text to `task package`.
- Add CLI aliases such as `check-tasks` and `new-task` while preserving existing `check-designs` and `new-design` entrypoints for compatibility.

This keeps the migration bounded while changing the user-facing mental model immediately.

## Key Flows
1. A new task starts.
2. The repository creates or updates a task package under the existing compatibility path.
3. The package moves through `requirements_ready`, `overview_ready`, and `detailed_ready`.
4. If design is done but implementation has not started, the package remains `detailed_ready`.
5. Only after implementation and verification are complete can the package move through `verifying` to `archived`.

## Trade-offs
- Keeping the old disk path avoids large mechanical churn, but it leaves a legacy naming seam in the repository layout.
- Adding CLI aliases increases short-term maintenance cost, but it prevents a flag day rename while still steering users toward the correct concept.
- Treating some historical archives as legacy records is slightly awkward, but it is safer than pretending those packages satisfy a stricter modern archive contract that did not actually govern them.

## Overview Reflection
- I challenged whether the right fix was to split the model into separate design and execution packages. That would add another workflow root and worsen complexity.
- I challenged whether renaming alone would be enough. It would not, because the real failure was false archive semantics.
- I checked whether an extra status was needed for design-complete but not implemented work. It was not; `detailed_ready` already fills that role.
- I checked whether renaming the filesystem paths was necessary for correctness. It is not; the user-facing protocol can be corrected now while path migration remains optional.
- No bounded subagent discussion was used. The main uncertainty is repository-local protocol cleanup, and the local evidence is sufficient.
## System Boundary

## Proposed Structure

## Key Flows

## Trade-offs
