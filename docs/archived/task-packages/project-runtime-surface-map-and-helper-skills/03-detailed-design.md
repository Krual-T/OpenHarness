# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - validate the new packages with `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest` to confirm no repository regressions
- Fallback Path:
  - if unrelated tests fail, keep the package at design status and record the blocker rather than claiming onboarding guidance is verified
- Planned Evidence:
  - design documents that define the runtime surface map contents
  - guidance for how helper skills are split and linked from a repository map
  - a bootstrap path for new runtime surfaces

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Testing-First Design
This package is now productized through a documentation-and-template implementation wave. The execution order is:

- add targeted runtime-surface-map assertions to `skills/using-openharness/tests/test_openharness.py`
- watch those assertions fail before the live reference, template, and wording updates exist
- update the live docs, reference contract, project runtime surface map reference, and starter template until the targeted assertions pass
- run `check-tasks` and the full repository test suite to confirm the repository still validates cleanly

## Files Added Or Changed
- Update `README.md` so the live repository docs mention the project runtime surface map explicitly.
- Update `skills/using-openharness/SKILL.md` so runtime routing looks for a project runtime surface map, not only the shared contract.
- Update `skills/using-openharness/references/runtime-capability-contract.md` and `skills/using-openharness/references/skill-hub.md` so the live protocol surface links the project-facing map guidance.
- Add `skills/using-openharness/references/project-runtime-surface-map.md` as the reusable repository-facing reference.
- Add `skills/using-openharness/references/templates/project-runtime-surface-map.md` as the starter template/example artifact.
- Update `skills/using-openharness/tests/test_openharness.py` with targeted assertions for the runtime surface map productization.
- Update `docs/archived/task-packages/harness-completion-roadmap/*` so roadmap references treat `OH-014` as a completed baseline after archive.
- Update `.project-memory/` with a reusable fact for the runtime surface map protocol.

## Interfaces
- Runtime surface map interface:
  - surface name
  - purpose
  - prerequisites
  - driver method
  - evidence sources
  - owning helper skill or bootstrap package
- Helper-skill interface:
  - one dominant runtime surface
  - concrete execution loop
  - expected writeback to `03`, `05`, and `06`
- Bootstrap interface:
  - task package opened when a needed surface is missing or too weakly defined

## Error Handling
- If a repository tries to use runtime helpers without a runtime surface map, the onboarding flow should stop and create the missing map or bootstrap package first.
- If a helper skill covers several unrelated surfaces, split it before treating it as reusable.
- If a surface cannot state its prerequisites or evidence sources clearly, it is not ready to be advertised as a supported runtime loop.

## Migration Notes
- This package now productizes the pattern in live docs, examples, templates, and project memory.
- This package depends conceptually on `OH-013`, because project-level mapping should consume the shared capability contract instead of inventing local rules first.
- `OH-016` should consume this package as an archived baseline rather than redefining the runtime surface map structure.

## Detailed Reflection
- I challenged whether helper skill boundaries should be prescribed too tightly. That would overfit the repository model; the design should require narrowness and clarity, not one fixed taxonomy.
- I checked whether the package needed example surfaces to stay concrete. It did, so the structure now includes API, browser, worker, migration, and observability as representative surface families without making them mandatory.
- I checked whether the bootstrap path was optional. It is not; without it, the first task on a new runtime surface will always improvise.
