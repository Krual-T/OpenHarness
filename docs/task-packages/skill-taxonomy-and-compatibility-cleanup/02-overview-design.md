# Overview Design

## System Boundary
This package covers how the repository classifies and describes skills. It is not a redesign of the underlying workflow logic. The output should be a stable vocabulary and a small set of doc and test updates that make the vocabulary enforceable.

## Proposed Structure
Use four repository-facing categories:

1. `core protocol`
   - skills that define the fixed OpenHarness workflow and repository protocol
   - these skills can decide task-package routing or gate completion claims
2. `optional helper`
   - repository-local helpers that support execution or quality but are not part of the fixed required path
3. `compatibility helper`
   - legacy helpers kept to bridge older workflows or derived artifacts without making them part of the current protocol
4. `imported generic skill`
   - skills available in the repo but not owned by the OpenHarness protocol itself

The hub should present these categories directly. Per-skill docs should describe themselves using the same vocabulary rather than ad hoc phrases like "legacy execution helper" in one file and "optional helper" in another unless both labels are intentionally combined.

## Key Flows
- A future agent asks whether a skill is part of the fixed repository workflow.
- The agent reads the skill hub first.
- The hub points to a stable category and the meaning of that category.
- The individual skill doc confirms the same role and does not imply a second repository entry path.
- Repository tests fail if a known compatibility or optional skill drifts back toward core wording.
- When the user decides a compatibility bridge should be retired instead of preserved, the skill hub, cross-references, and tests should all be updated in the same round so the repository surface stops advertising the removed skill.

## Trade-offs
- A stricter taxonomy reduces improvisation, but it also makes some older wording look harsher or more final than before.
- Keeping compatibility helpers instead of removing them immediately preserves usability for older workflows, but it requires explicit warnings so they are not mistaken for core protocol.
- A small fixed set of categories is less expressive than bespoke wording in each skill, but it is easier to maintain and audit.

## Overview Reflection
- I considered using the existing hub sections as the taxonomy itself. That was rejected because section names like `Execution` and `Quality` describe theme, not protocol strength or compatibility status.
- I considered collapsing optional helpers and compatibility helpers into one category. That would hide an important distinction: some helpers are current but optional, while others exist mainly to bridge older workflows.
- I checked whether imported generic skills should be treated as optional helpers. They should not, because the roadmap specifically needs to distinguish repository-owned protocol from generic imported capabilities.
- I checked whether this package should also define maintenance checks. It should not; maintenance should consume this taxonomy, not be designed implicitly inside it.
- I checked whether retiring `writing-skills` and `executing-plans` conflicts with this package's scope. It does not, because both removals are direct outcomes of skill-taxonomy cleanup once the user chooses the non-compatibility path.
