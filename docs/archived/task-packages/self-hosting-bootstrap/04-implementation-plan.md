# Implementation Plan

## Applicability
- Use this file when the task needs explicit staged execution beyond `03-detailed-design.md`.

## Execution Slices
- Slice 1: make the repo runnable with declared Python dependencies and working CLI bootstrap.
- Slice 2: scaffold and populate the first active design package for self-hosting.
- Slice 3: realign the test suite and top-level docs to the current repository layout.

## Verification Gates
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Commit Plan
- One focused commit for the self-hosting bootstrap round after verification passes.
