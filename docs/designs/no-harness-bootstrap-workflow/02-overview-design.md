# Overview Design

## System Boundary
This package defines the product-level bootstrap workflow for entering a repository that does not yet have OpenHarness-shaped repo-local artifacts. It does not implement the support changes yet, but it must define the target entry sequence, artifact boundary, and decision points tightly enough that follow-up implementation can proceed without rediscovering the problem.

## Proposed Structure
Treat bootstrap as a package-first adoption workflow, not as a one-shot generator and not as a docs-only checklist.

The workflow should have four explicit phases:

1. `repository scan`
   - Inspect what already exists locally: repo map files, task docs, tests, scripts, CI, and any obvious verification commands.
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
   - Create or adapt one focused first package that describes the bootstrap round itself or the first concrete repository task.
   - The package must record requirements, overview design, detailed design, verification plan, and evidence placeholders from the start, even if the initial content is narrow.
4. `verification-path establishment`
   - Before implementation claims begin, record the strongest available verification path:
     - repository automation when it exists
     - task-local automation when the repo lacks a broader harness
     - explicit manual runtime verification when automation is not yet credible
   - If none of these are credible, bootstrap is incomplete and cannot claim the repository is ready.

Three architectural options were considered:

1. `docs-only bootstrap guide`
   - Document the sequence, but leave all artifact creation to manual judgment.
   - Lowest implementation cost, but too easy to drift and too dependent on agent improvisation.
2. `generator-first bootstrap command`
   - Add a heavy scaffolding command that writes the whole repo shape in one pass.
   - Faster when the assumptions are right, but too rigid for partially-structured repos and likely to create a second product surface.
3. `package-first bootstrap workflow`
   - Use lightweight repo inspection plus selective scaffolding to get to the first valid package, then let normal package workflow take over.
   - This is the recommended direction.

Recommended direction: `package-first bootstrap workflow`.

Reasoning:

- It matches OpenHarness's core belief that repository-visible artifacts are the source of truth.
- It can adopt repositories that already have partial structure instead of flattening them under a generator's assumptions.
- It keeps the first-round workflow compatible with `OH-005` verification semantics and `OH-006` status semantics.
- It reduces product surface area because bootstrap becomes an explicit entry recipe plus minimal CLI/template help, not a second orchestration framework.

The implementation wave that follows this design should likely touch:

- `AGENTS.md` guidance about first entry into a foreign repository
- `README.md` product explanation and setup examples
- `skills/using-openharness/SKILL.md` entry protocol wording
- package templates and supporting references
- `skills/using-openharness/scripts/openharness.py` only where small CLI assistance materially reduces bootstrap ambiguity

## Key Flows
1. An agent enters a repository and determines that no valid design packages exist yet.
2. The agent scans for existing repo-map, task-tracking, and verification surfaces instead of assuming a blank slate.
3. The agent establishes the minimum repo-local artifacts needed for OpenHarness to operate.
4. The agent scaffolds or adapts the first active design package and writes explicit requirements before broad implementation starts.
5. The package records the intended verification path and the status progression needed to make completion claims credible.
6. Once the first package is valid, the repository leaves bootstrap mode and returns to the normal `openharness -> brainstorming -> exploring-solution-space -> detailed design -> implementation -> verification` workflow.

## Trade-offs
- A package-first bootstrap is slower than a one-command generator, but it handles partially-structured repositories more honestly.
- Deferring optional artifacts keeps round one light, but it means maintenance and taxonomy improvements still need later focused packages.
- Requiring an explicit verification path during bootstrap raises the bar, but it prevents a repository from being called "bootstrapped" while remaining unverifiable.
- Adding small CLI help may reduce ambiguity, but the design should resist turning bootstrap into another opaque automation layer.

## Overview Reflection
- I challenged whether bootstrap should be a pure generator problem. That was rejected because many target repositories will already contain docs, tests, or task context that should be adopted rather than overwritten.
- I challenged whether bootstrap should stay docs-only. That was also rejected because it would leave too much sequencing logic in chat and would not produce a repeatable entry contract.
- I checked whether the proposed flow depends on runtime verification and status semantics that are still unstable. It does depend on them, but `OH-005` and `OH-006` now provide enough baseline to treat them as upstream inputs.
- I checked whether the workflow accidentally broadens bootstrap into maintenance or taxonomy cleanup. It does not; those streams remain downstream unless they are directly needed to create the first valid package.
- No bounded subagent discussion was used here because the main decision is a repository-local product-shape choice, and the viable alternatives are legible enough to compare directly.
