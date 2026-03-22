# Requirements

## Goal
Make `openharness` self-hosting enough that it can use its own repository workflow instead of being only a copied skill bundle.

## Problem Statement
The repository currently ships `skills/` and documentation, but it does not yet satisfy its own minimum harness contract:

- there is no `docs/task-packages/` package tree
- the Python-based harness CLI cannot run in a clean checkout because `PyYAML` is undeclared
- the repo tests still target legacy layout assumptions and historical task-package fixtures from another repository
- a few core docs still contain stale identity/path mistakes

That means the repo cannot demonstrate the most basic OpenHarness promise on itself.

## Required Outcomes
1. The repository can bootstrap itself with `uv run python skills/using-openharness/scripts/openharness.py bootstrap`.
2. The repository has at least one valid active task package that documents this self-hosting round.
3. The harness CLI and tests run from declared project dependencies rather than undeclared environment state.
4. The test suite validates the current `skills/`-based repo layout and the current task-package inventory.
5. The first round remains minimal: enough to make the repo runnable and self-describing, without trying to finish the whole product redesign in one pass.

## Non-Goals
- Redesign the full OpenHarness workflow from `04-implementation-plan.md` to a different package protocol in this round.
- Implement runtime-debug modules or broader optional harness modules yet.
- Complete all future self-hosting improvements beyond the minimal bootstrap needed to continue development safely.

## Constraints
- Keep the existing fixed `docs/task-packages/<task>/` package model for this round.
- Preserve the current `skills/` top-level repository layout instead of introducing another internal skill root.
- Prefer the smallest change set that gets the repo onto a self-hosting footing.
