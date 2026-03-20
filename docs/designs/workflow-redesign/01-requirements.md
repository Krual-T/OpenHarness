# Requirements

## Goal
Redesign OpenHarness around a fixed self-hosting workflow that fits greenfield, no-harness repositories better than the inherited brainstorming -> plan -> implementation flow.

## Problem Statement
The current repository protocol still reflects an inherited split between `03-detailed-design.md` and `04-implementation-plan.md`, and it lacks an explicit exploration step between requirements and design. That causes three problems:

- the core workflow does not match the intended requirements-first, exploration-driven process
- `04-implementation-plan.md` overlaps heavily with `03-detailed-design.md`
- the skill hub does not model the important “explore local repo + web research before architecture choices” phase

For a no-harness target repository, OpenHarness needs to impose a clearer default path rather than asking users to infer missing stages.

## Required Outcomes
1. The fixed protocol explicitly treats `01-requirements.md` as the brainstorming output.
2. Exploration becomes a first-class step and skill in the core workflow.
3. `02-overview-design.md` captures solution synthesis after exploration.
4. `03-detailed-design.md` becomes the testing-first design artifact, including runtime verification approach and implementation order.
5. `04-implementation-plan.md` is removed from the fixed required package protocol.
6. Core docs, templates, manifest, and tests all agree on the new protocol.

## Non-Goals
- Implement all future optional modules such as runtime-debug extensions or maintenance automation in this round.
- Fully remove every imported execution skill that still references plans, if a smaller compatibility bridge is sufficient for now.

## Constraints
- Keep the design package approach fixed and non-configurable.
- Preserve a clear migration path for existing docs in this repository.
- Favor a coherent repo-wide protocol over backward compatibility with inherited wording.
