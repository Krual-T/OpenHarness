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
This package is design-only. Its immediate tests are:

- `check-tasks` passes with the new package included
- the package is concrete enough that a later implementation wave can add examples, templates, or helper guidance without redoing the design
- the package makes helper-skill boundaries and bootstrap conditions explicit enough to avoid one oversized runtime-debug skill

## Files Added Or Changed
- Add `OH-014` package documents for project runtime surface mapping and helper-skill structure.
- Update `OH-004` so the roadmap includes this follow-up package.
- In a later implementation wave, likely update:
  - `skills/using-openharness/SKILL.md`
  - `skills/using-openharness/references/skill-hub.md`
  - README or reference docs that explain project runtime adoption
  - example project package docs or templates that show a runtime surface map in practice

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
- This package should stay design-only until a later task productizes the pattern in live docs, examples, or templates.
- This package depends conceptually on `OH-013`, because project-level mapping should consume the shared capability contract instead of inventing local rules first.

## Detailed Reflection
- I challenged whether helper skill boundaries should be prescribed too tightly. That would overfit the repository model; the design should require narrowness and clarity, not one fixed taxonomy.
- I checked whether the package needed example surfaces to stay concrete. It did, so the structure now includes API, browser, worker, migration, and observability as representative surface families without making them mandatory.
- I checked whether the bootstrap path was optional. It is not; without it, the first task on a new runtime surface will always improvise.
