# Requirements

## Goal
Repair the repository's core work-unit semantics so the package name matches its real lifecycle and archive status can no longer be read as "design finished, implementation later."

## Problem Statement
OpenHarness currently uses one package object for the full lifecycle:

- requirements
- overview design
- detailed design
- implementation
- verification
- archive

But the object is still called `design package` in many repository surfaces. That naming leaks the wrong mental model:

- it suggests the package primarily exists for design work
- it makes `design complete` sound dangerously close to `package complete`
- it makes later implementation waves feel external to the package rather than part of the same unit

`OH-007` exposed the failure mode clearly. Its archived docs say the design work is complete while implementation waves still remain. That conflicts with the repository-wide archive contract, which says archived packages are completed, evidenced, and no longer active work.

This is not just a wording blemish. It causes real handoff errors:

- agents can misread archived packages as fully done when they are only design-complete
- roadmap packages can treat archived design baselines as completed streams
- follow-up implementation can be split incorrectly because the package model no longer tells the truth about what remains

The repository needs one consistent answer to two questions:

1. What is the end-to-end unit called?
2. What does it mean for that unit to be complete enough to archive?

## Required Outcomes
1. Rename the primary end-to-end object from `design package` to `task package` across core repository protocol surfaces.
2. Define `archived` to mean the task package is implemented, verified, and no longer active.
3. Define which status applies when requirements and design are complete but implementation has not yet been carried out.
4. Audit the current protocol and archived-package wording for places that still imply `design complete` is enough for archive.
5. Keep the package compatible with the existing `docs/task-packages/<task>/` directory layout unless there is a strong reason to migrate paths separately.
6. Make the fix concrete enough that CLI text, templates, skills, and tests can be updated without re-arguing semantics in a later round.

## Success Conditions
- A future handoff can read an archived package and assume the underlying task is actually done.
- A package that has finished design but not implementation stays in an active non-archived status.
- Core docs and skills stop mixing `design package` and end-to-end task semantics.
- The repository has an explicit migration story for older archived packages that were written under the old naming/semantics.

## Non-Goals
- Rebuild the whole filesystem layout in this same round if terminology-only compatibility is sufficient.
- Rewrite every archived package in the repository unless its wording materially affects the active protocol.
- Introduce a second parallel object model for design-only packages unless analysis proves that renaming to `task package` is insufficient.

## Constraints
- The fix must preserve a single authoritative workflow rather than creating separate `design package` and `task package` systems side by side.
- The fix must remain compatible with `OH-006` status-semantics work, while correcting the gap it left around end-to-end completion.
- The repair should prefer straightforward, durable semantics over compatibility wording that keeps both interpretations alive.
