# Overview Design

## System Boundary
This package covers how the repository classifies and describes skills. It is not a redesign of the underlying workflow logic. The output should be a stable vocabulary and a small set of doc and test updates that make the vocabulary enforceable.

## Proposed Structure
Use three live repository-facing categories:

1. `core protocol`
   - skills that define the fixed OpenHarness workflow and repository protocol
   - these skills can decide task-package routing or gate completion claims
2. `optional helper`
   - repository-local helpers that support execution or quality but are not part of the fixed required path
3. `imported generic skill`
   - skills available in the repo but not owned by the OpenHarness protocol itself

The hub should present these live categories directly. Retired plan-oriented skills should disappear from the live repository surface instead of being preserved under a compatibility label. Per-skill docs should describe themselves using the same vocabulary rather than ad hoc phrases.

## Key Flows
- A future agent asks whether a skill is part of the fixed repository workflow.
- The agent reads the skill hub first.
- The hub points to a stable category and the meaning of that category.
- The individual skill doc confirms the same role and does not imply a second repository entry path.
- Repository tests fail if a known optional or imported skill drifts back toward retired plan-oriented wording.
- When the user decides an old bridge should be retired instead of preserved, the skill hub, cross-references, archived history, and tests should all be updated in the same round so the repository surface stops advertising the removed skill.

## Trade-offs
- A stricter taxonomy reduces improvisation, but it also makes the repository more willing to break with older wording.
- Removing the old plan-oriented skills eliminates ambiguity, but it also erases a fallback path that some historical docs still assumed existed.
- A small fixed set of categories is less expressive than bespoke wording in each skill, but it is easier to maintain and audit.

## Overview Reflection
- I considered using the existing hub sections as the taxonomy itself. That was rejected because section names like `Execution` and `Quality` describe theme, not protocol strength or compatibility status.
- I considered keeping a `compatibility helper` category after retirement. That would preserve a concept with no surviving live members and would keep the old plan-oriented surface half-alive in the docs, so I rejected it.
- I checked whether imported generic skills should be treated as optional helpers. They should not, because the roadmap specifically needs to distinguish repository-owned protocol from generic imported capabilities.
- I checked whether this package should also define maintenance checks. It should not; maintenance should consume this taxonomy, not be designed implicitly inside it.
- I checked whether retiring `writing-plans`, `writing-skills`, and `executing-plans` conflicts with this package's scope. It does not, because those removals are direct outcomes of skill-taxonomy cleanup once the user chooses the non-compatibility path.
