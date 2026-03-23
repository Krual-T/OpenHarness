# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or runtime_surface_map or runtime_helper_reference or readme_describes_runtime_capability_contract or skill_hub_describes_runtime_capability_layer or openharness_skill_routes_runtime_work_through_capability_contract'` to lock the helper-addition assertions
  - validate the updated package set with `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest` to confirm the repository still passes after productizing `OH-016`
  - run `uv run python skills/using-openharness/scripts/openharness.py bootstrap` after archiving to confirm `OH-016` no longer appears in the active package list
- Fallback Path:
  - if unrelated tests fail or archive validation fails, keep the package in `verifying` and record the blocker rather than claiming workflow productization
- Planned Evidence:
  - live docs and reference docs that define helper-addition decision rules and repository update surfaces
  - repository tests that prove the new helper-addition wording was missing before implementation and present after it
  - project memory that captures the new helper-addition rule as reusable repository knowledge

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Testing-First Design
This package is now productized through a documentation-and-protocol implementation wave. The execution order is:

- add targeted helper-addition assertions to `skills/using-openharness/tests/test_openharness.py`
- watch those assertions fail before the live-doc updates exist
- update the entry skill, runtime references, runtime-surface-map template, public README, and project memory until the targeted assertions pass
- run `check-tasks`, the full repository test suite, and `bootstrap` after archival to confirm the repository still validates cleanly

## Files Added Or Changed
- Keep `OH-016` package documents aligned with the implementation wave and later archive them as the completed helper-addition baseline.
- Update `README.md` so the public repository surface states the three-way runtime-helper decision: reuse, add, or bootstrap.
- Update `skills/using-openharness/SKILL.md` so runtime routing explicitly supports `add one new narrow helper` when the runtime surface is already mapped.
- Add `skills/using-openharness/references/adding-project-runtime-helper.md` as the focused helper-addition reference.
- Update `skills/using-openharness/references/runtime-capability-contract.md`, `skills/using-openharness/references/project-runtime-surface-map.md`, and `skills/using-openharness/references/skill-hub.md` so the live protocol surface links the helper-addition workflow.
- Update `skills/using-openharness/references/templates/project-runtime-surface-map.md` so the starter template explains when to add helper coverage instead of staying on a bootstrap link.
- Update `skills/using-openharness/tests/test_openharness.py` with targeted assertions for helper-addition productization.
- Update `docs/archived/task-packages/harness-completion-roadmap/*` so roadmap references treat `OH-016` as a completed archived follow-up.
- Update `.project-memory/` with a reusable fact for the helper-addition protocol.

## Interfaces
- Helper-addition decision interface:
  - `reuse existing helper`
  - `add new helper`
  - `bootstrap first`
- Minimum helper contract interface:
  - owning runtime surface
  - purpose and dominant validation loop
  - prerequisites
  - driver commands or scripts
  - observation points and evidence sources
  - success criteria
  - failure evidence expectations
  - explicit writeback targets in `03`, `05`, and `06`
- Repository update interface:
  - runtime surface map entry
  - helper skill path
  - skill-hub or onboarding references where applicable
  - `.project-memory/` when the rule becomes reusable

## Error Handling
- If a repository tries to create a new helper without a clear runtime surface map entry, stop and bootstrap that surface first.
- If a proposed helper spans unrelated surfaces such as API plus browser plus worker, split it before treating it as reusable.
- If a proposed helper cannot state prerequisites, observations, and evidence clearly, keep it as task-local exploration instead of promoting it to a reusable helper.
- If an existing helper already covers the same surface and evidence shape, reuse or refine it instead of creating a near-duplicate.

## Migration Notes
- This package now productizes the helper-addition workflow in live docs, reference docs, repository tests, and project memory.
- Conceptually it sits downstream of `OH-013` and `OH-014`, because helper creation consumes the runtime capability contract and the runtime surface map instead of inventing new local rules.
- A later follow-up may still add a concrete helper template or example surface artifact if repositories need more onboarding scaffolding in practice.

## Detailed Reflection
- I challenged whether this round needed a concrete helper template immediately. It does not yet; the higher-value missing piece was the reusable decision workflow and its cross-links into the live protocol surface.
- I checked whether the implementation duplicated `OH-013` or `OH-014`. It does not. Those packages still own the contract and the runtime-surface-map model; this package productizes the narrow operational step between them.
- I checked whether adding a dedicated helper-addition reference would create a second entry workflow. It does not, because `using-openharness` remains the only entry skill and the new reference is linked as downstream guidance, not as a parallel root.
