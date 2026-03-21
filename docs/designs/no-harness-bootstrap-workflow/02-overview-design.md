# Overview Design

## System Boundary
This package defines the product-level cold-start workflow for entering a Python repository that does not yet have OpenHarness-shaped repo-local artifacts or mature runtime tests. It does not implement the support changes yet, but it must define the target entry sequence, artifact boundary, and verification floor tightly enough that follow-up implementation can proceed without rediscovering the problem.

## Proposed Structure
Treat cold start as a Python-specific, package-first adoption workflow, not as a one-shot generator and not as a docs-only checklist.

The workflow should have four explicit phases:

1. `repository scan`
   - Inspect what already exists locally: repo map files, task docs, Python tests, scripts, CI, and any obvious verification commands.
   - Classify the repository as one of:
     - already-harnessed
     - partially-structured
     - no-harness
2. `minimum artifact establishment`
   - For a no-harness or partially-structured repository, establish the minimum repo-local truth surfaces needed for OpenHarness to operate:
     - `AGENTS.md` or equivalent repo map entrypoint
     - harness manifest/reference location used by the workflow
     - `docs/designs/<first-task>/` as the first active package
   - Defer optional artifacts such as `.project-memory/` population, maintenance checklists, and deeper taxonomy cleanup until after the first package exists.
3. `first-package bootstrap`
   - Create or adapt one focused first package that describes the cold-start round itself or the first concrete repository task.
   - The package must record requirements, overview design, detailed design, verification plan, and evidence placeholders from the start, even if the initial content is narrow.
4. `verification-floor establishment`
   - Before implementation claims begin, record the strongest available automated Python verification path:
     - existing repository automation when it exists
     - `pytest` as the minimum cold-start floor
     - task-local Python tests when repository automation is still incomplete
   - Explicit runtime tests remain recommended when the task depends on runtime behavior, but they are not a universal blocker for cold start.
   - If even `pytest` cannot credibly run, the repository is not yet ready to claim a usable Python cold start.

Three architectural options were considered:

1. `docs-only cold-start guide`
   - Document the sequence, but leave all artifact creation to manual judgment.
   - Lowest implementation cost, but too easy to drift and too dependent on agent improvisation.
2. `generator-first bootstrap command`
   - Add a heavy scaffolding command that writes the whole repo shape in one pass.
   - Faster when the assumptions are right, but too rigid for partially-structured repos and likely to create a second product surface.
3. `python-only package-first cold start`
   - Use lightweight repo inspection plus selective scaffolding to get to the first valid package, then let normal package workflow take over.
   - Standardize on `pytest` as the minimum verification floor and recommend runtime-test construction as a follow-up when needed.
   - This is the recommended direction.

Recommended direction: `python-only package-first cold start`.

Reasoning:

- It matches OpenHarness's core belief that repository-visible artifacts are the source of truth.
- It can adopt repositories that already have partial structure instead of flattening them under a generator's assumptions.
- It matches the actual product scope the user wants: Python development only, not generic multi-language bootstrapping.
- It keeps the first-round workflow compatible with `OH-006` status semantics while simplifying verification expectations to a practical Python baseline.
- It reduces product surface area because cold start becomes an explicit entry recipe plus minimal docs/template help, not a second orchestration framework.

The implementation wave that follows this design should likely touch:

- `AGENTS.md` guidance about first entry into a foreign Python repository
- `README.md` product explanation and setup examples
- `skills/using-openharness/SKILL.md` entry protocol wording
- package templates and supporting references, especially the verification wording
- `skills/using-openharness/scripts/openharness.py` only where small CLI assistance materially reduces bootstrap ambiguity

## Key Flows
1. An agent enters a Python repository and determines that no valid design packages exist yet.
2. The agent scans for existing repo-map, task-tracking, Python test, and verification surfaces instead of assuming a blank slate.
3. The agent establishes the minimum repo-local artifacts needed for OpenHarness to operate.
4. The agent scaffolds or adapts the first active design package and writes explicit requirements before broad implementation starts.
5. The package records `pytest` as the current verification floor and explicitly notes whether runtime tests are already present, recommended next, or required in parallel for the task.
6. Once the first package is valid, the repository leaves cold-start mode and returns to the normal `openharness -> brainstorming -> exploring-solution-space -> detailed design -> implementation -> verification` workflow.

## Trade-offs
- A package-first cold start is slower than a one-command generator, but it handles partially-structured Python repositories more honestly.
- Using `pytest` as the minimum floor makes the system immediately usable, but it is weaker than true runtime verification for many tasks.
- Recommending runtime tests after cold start is more pragmatic than blocking on them, but it requires the docs to be explicit about the gap so weak verification is not mistaken for full coverage.
- Adding small CLI help may reduce ambiguity, but the design should resist turning cold start into another opaque automation layer.

## Overview Reflection
- I challenged whether this stream still needed to be language-agnostic. It does not; the user has now made the product scope explicitly Python-only.
- I challenged whether cold start should still block on full runtime verification. It should not; `pytest` is a practical floor, while runtime tests become an explicit recommended follow-up or parallel work item depending on task risk.
- I checked whether the proposed flow still helps with real first-entry ambiguity. It does, because the main ambiguity was sequencing and minimum verification honesty, not universal language support.
- I checked whether the workflow accidentally broadens cold start into maintenance or taxonomy cleanup. It does not; those streams remain downstream unless they are directly needed to create the first valid package.
- No bounded subagent discussion was used here because the main decision is a repository-local product-shape choice, and the viable alternatives are legible enough to compare directly.
