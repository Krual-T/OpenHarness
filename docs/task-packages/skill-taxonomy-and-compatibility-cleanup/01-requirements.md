# Requirements

## Goal
Define and implement a durable skill-classification model for OpenHarness so repository-facing workflow skills, optional helpers, compatibility skills, and imported generic skills are described consistently across the hub, individual skill docs, and tests.

## Problem Statement
The repository already has partial classification language:

- `skills/using-openharness/references/skill-hub.md` separates Core, Execution, Quality, Repository Memory, and Imported Generic Skills
- several per-skill docs already describe themselves as legacy or compatibility helpers
- tests already assert that some execution skills must not be described as core protocol

But the model is still incomplete:

- the hub uses one set of category words while some skill docs use another
- the boundary between optional helpers, compatibility helpers, and imported generic skills is not fully explicit
- maintenance work cannot reliably audit stale or misleading skills until the intended categories are stable
- future agents could still misread legacy helpers as part of the fixed repository protocol

Without one explicit taxonomy, the repository will keep re-explaining these boundaries package by package.

## Required Outcomes
1. Define the repository's canonical skill categories and the meaning of each category.
2. Identify which existing skills belong in each category without reintroducing a second entry system beside `openharness`.
3. Update the hub and the affected skill docs so their wording matches the canonical categories.
4. Add or adjust tests so category drift is caught automatically.
5. Record enough design and evidence that a later maintenance package can reuse this taxonomy instead of rediscovering it.
6. Retire `writing-skills` and `executing-plans` from the live repository surface when the user explicitly chooses the non-compatibility path.

## Non-Goals
- Redesign the whole workflow or remove every compatibility helper in this round beyond the explicitly requested retirements.
- Build a full maintenance workflow here; this package only supplies one prerequisite for that later stream.
- Rewrite imported generic skills that are merely present in the repository unless their wording conflicts with the taxonomy.

## Constraints
- Preserve `using-openharness` as the only repository entry skill.
- Prefer clear, durable language over maximal backward compatibility with older skill wording.
- Keep the taxonomy small enough that future maintenance checks can apply it mechanically.
