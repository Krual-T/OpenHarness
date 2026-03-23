# Runtime Capability Contract

OpenHarness treats project-specific runtime support as a repository protocol, not as one universal runtime-debug skill.

This contract defines the minimum shared shape that lets repositories expose runtime-aware workflows without creating a second entry system.

## Capability Layers

OpenHarness separates runtime support into three layers:

1. `core protocol`
   - `using-openharness` decides whether a task is code-only or runtime-aware.
   - The core protocol keeps routing, evidence expectations, and writeback rules stable across repositories.
2. `project runtime surface map`
   - Each repository may declare the runtime surfaces it supports, such as API, browser, worker, migration, or observability.
   - Each surface should point to its current helper guidance or to the bootstrap package that is still defining that surface.
   - The project-facing map shape lives in `references/project-runtime-surface-map.md`.
3. `runtime helper skills`
   - Repositories may attach multiple runtime helper skills.
   - These helpers stay narrow, surface-oriented, and optional. They do not replace the repository entry skill.

## Declaration Shape

Each project-specific runtime capability should declare at least:

- runtime surface
- prerequisites
- driving method
- observation points
- success criteria
- failure evidence
- writeback expectations

The writeback expectations must stay inside the normal task-package flow:

- `03-detailed-design.md`
  - record whether runtime verification is required
  - record the chosen runtime surface, prerequisites, driving method, and expected observations
  - state whether the task will reuse an existing helper or needs a bootstrap package first
- `05-verification.md`
  - record the executed runtime path and what evidence was actually gathered
  - state deviations, blockers, and blind spots explicitly
- `06-evidence.md`
  - record artifact paths, commands, helper references, residual risks, and follow-up actions

## Routing Contract

When a task needs runtime-aware evidence, `using-openharness` should choose exactly one of these paths:

1. `code-only execution`
   - the task does not require runtime-aware evidence beyond the existing package verification plan
2. `reuse an existing runtime helper`
   - a matching runtime surface already exists
   - the repository already has helper guidance whose prerequisites, driving method, and evidence shape fit the task
3. `open a bootstrap package`
   - the repository cannot yet describe the needed runtime surface clearly enough
   - no helper exists whose contract matches the task

The bootstrap package path is mandatory when the repository cannot state the surface, prerequisites, driving method, or evidence flow clearly. Do not claim supported runtime verification before that package exists.

## Boundary Rules

- Do not collapse unrelated runtime surfaces into one oversized helper.
- Do not create a second repository entry skill for runtime work.
- Do not keep runtime evidence only in chat or shell history; write it back into the task package.
- Do not promote a helper as reusable until it can state its prerequisites, observations, and failure evidence clearly.

## Relationship To Other OpenHarness Work

- This contract is the OpenHarness-side protocol layer.
- The project-facing surface-map guidance lives in `references/project-runtime-surface-map.md`.
- Repository-specific runtime surface maps and helper-skill examples belong in downstream work.
- Helper-creation workflow guidance belongs in downstream work too.
