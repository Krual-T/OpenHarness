# Requirements

## Goal
Make the live OpenHarness repository describe skills the way the product actually works: as a plug-and-play Agent Harness with a small fixed protocol, a larger set of optional helpers, explicit workflow stages and triggers, and a Python-first verification baseline that starts at `uv run pytest`.

## Problem Statement
The repository already completed one cleanup wave in archived `OH-008 Skill Taxonomy And Compatibility Cleanup`. That wave retired the old plan-oriented surface and reduced obvious wording drift.

But the current live surface still has a mismatch:

- the archived design says the canonical taxonomy should be about protocol status
- the live skill hub still leads with mixed buckets like `Core`, `Execution`, `Quality`, and `Repository Memory`
- those theme buckets blur two different questions:
  - is this skill part of the fixed OpenHarness protocol?
  - when or why would this skill actually be used?
- the product goal is not abstract taxonomy purity; it is a plug-and-play Agent Harness that lets an agent discover the default path quickly and branch only when task conditions justify it
- Python verification policy is already captured historically in archived `OH-007`, but the live docs still do not state the practical baseline clearly enough: for Python-first repositories, `uv run pytest` is the minimum automated verification floor, and stronger runtime verification must be decided per project and per task package

Without this correction, future agents still have to infer too much from mixed labels and archived packages.

## Required Outcomes
1. Define the live classification model as two layers:
   - protocol status
   - workflow stage or trigger
2. Keep protocol status small and stable:
   - core protocol skill
   - optional helper skill
   - imported generic skill
3. Describe the main workflow stages and trigger conditions that explain when skills are actually used.
4. Update the live skill hub so it uses that two-layer model directly.
5. Update the affected live docs and skill docs so they align with the new model instead of relying on mixed theme buckets.
6. Productize the Python verification baseline in live docs:
   - OpenHarness is Python-first
   - `uv run pytest` is the default minimum automated verification floor
   - stronger runtime verification is project-specific and must be chosen in task packages rather than imposed globally
7. Add repository tests that pin the new taxonomy and verification wording.

## Non-Goals
- Invent a large matrix of subcategories for every niche skill edge case.
- Define non-Python verification defaults in this round.
- Pretend `pytest` is equivalent to strong runtime or integration evidence.
- Reopen the retired plan-oriented surface from `OH-008`.

## Constraints
- Preserve `using-openharness` as the only repository entry skill.
- Preserve the archived task packages as historical fact sources rather than rewriting history away.
- Keep the model small enough that future maintenance work can audit it mechanically.
- The live wording must reflect the product goal of a reusable Agent Harness, not just internal cleanup terminology.
