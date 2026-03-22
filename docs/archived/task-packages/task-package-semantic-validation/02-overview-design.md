# Overview Design

## System Boundary
This package strengthens repository-local semantic validation for task packages. It does not redesign the status model, introduce per-package custom states, or add a separate transition engine. The output should remain a lightweight extension of `check-tasks` plus the minimum template and test updates needed to make the new rules legible and stable.

## Proposed Structure
Use a `docs-first semantic anchors, CLI-enforced` model.

For each status that claims a meaningful readiness checkpoint, define a small set of minimum document anchors:

1. `requirements_ready`
   - `01-requirements.md` must contain non-placeholder content for:
     - `## Goal`
     - `## Problem Statement`
     - `## Required Outcomes`
     - `## Constraints`
2. `overview_ready`
   - requirements anchors must already be satisfied
   - `02-overview-design.md` must contain non-placeholder content for:
     - `## System Boundary`
     - `## Proposed Structure`
     - `## Key Flows`
     - `## Trade-offs`
     - `## Overview Reflection`
3. `detailed_ready`
   - overview anchors must already be satisfied
   - `03-detailed-design.md` must contain non-placeholder content for:
     - `## Runtime Verification Plan`
     - `## Files Added Or Changed`
     - `## Interfaces`
     - `## Error Handling`
     - `## Detailed Reflection`
4. `verifying`
   - detailed anchors must already be satisfied
   - existing verification-path rule from `OH-006` still applies
   - `05-verification.md` must contain non-placeholder content for:
     - `Planned Path`
     - `Executed Path`
     - `Latest Result`
5. `archived`
   - verifying anchors must already be satisfied
   - `06-evidence.md` must contain non-placeholder content for:
     - `## Files`
     - `## Commands`
     - `## Residual Risks`

The implementation should treat these anchors as minimum honesty checks, not as quality scoring. A package may still be badly designed and pass; the goal is to reject obvious contradictions between claimed status and missing document content.

## Key Flows
1. An agent or human scaffolds a package from the standard templates.
2. As the package advances, the relevant docs are filled with real content rather than placeholders.
3. `check-tasks` reads `STATUS.yaml.status`.
4. Validation maps that status to the required document anchors.
5. If a required section is missing or still placeholder content, validation fails with a targeted error explaining which anchor is missing.
6. Templates and tests teach the same anchors so the failure mode is predictable instead of surprising.

## Trade-offs
- `heading-and-placeholder checks`
  - cheapest and most predictable first wave
  - aligned with the current markdown-first protocol
  - cannot prove document quality, only minimum semantic completeness
- `schema-first readiness metadata in STATUS.yaml`
  - more explicit and machine-friendly
  - would duplicate document structure and create another layer to keep in sync
  - too heavy for the current workflow maturity
- `full transition engine plus execution artifacts`
  - strongest enforcement path long term
  - useful for later work, but would expand this package into workflow control and evidence logging at the same time
  - rejected for this round because it mixes several unfinished streams

Recommended direction: `heading-and-placeholder checks`.

Reasoning:
- the repository already teaches stable section headings through templates
- the current gap is honesty, not expressiveness
- the first valuable move is to reject obviously misleading status claims without making every package author learn a new schema

## Overview Reflection
- I considered limiting this round to `verifying` and `archived` only, following the earlier conservative stance from `OH-006`. I rejected that narrower scope because the current templates for `01`, `02`, and `03` are now stable enough that early readiness checks can be implemented cheaply.
- I considered checking only for heading presence. That is too weak because a package could keep the default placeholder shell and still pass.
- I considered a richer markdown parser that scores prose quality or diagram presence. That is too subjective and brittle for a first enforcement wave.
- I checked whether requiring reflection sections would overfit to current workflow wording. It should not; reflection is already part of the current repository protocol and is explicitly taught in workflow skills.
- I checked whether `06-evidence.md` should require every section for `archived`. It should not in the first wave; requiring `Files`, `Commands`, and `Residual Risks` captures the minimum evidence shape without over-constraining manual-step edge cases.
- No bounded subagent discussion was used because the main design decision is local, incremental, and already framed by archived `OH-006`.
