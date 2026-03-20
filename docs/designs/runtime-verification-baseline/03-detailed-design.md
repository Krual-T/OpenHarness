# Detailed Design

## Testing-First Design
This package is still in early design. The first test for this round is document-level:

- the package must validate under `openharness.py check-designs`
- the package must make the verification ladder and completion semantics concrete enough to drive follow-up implementation
- the package must identify likely repository surfaces before code changes begin

## Files Added Or Changed
- Update `01-requirements.md` with the minimum verification problem statement and scope.
- Update `02-overview-design.md` with the verification ladder, completion semantics, and upstream/downstream dependencies.
- After overview stabilization, update verification-oriented skills, templates, and CLI behavior in that order.

## Interfaces
- Likely follow-up touch points:
  - `skills/using-openharness/SKILL.md`
  - `skills/verification-before-completion/SKILL.md`
  - design-package templates under `skills/using-openharness/references/templates/`
  - `skills/using-openharness/scripts/openharness.py verify`
  - tests under `skills/using-openharness/tests/`
- Expected future interfaces to define:
  - a stable vocabulary for verification paths
  - package-document expectations for intended versus executed verification
  - rules for when a package may remain in `verifying` versus when it must not claim completion

## Implementation Order
1. Update templates for `03`, `05`, and `06` so every new package records:
   - intended verification path
   - fallback path if the preferred path fails
   - executed verification path
   - residual risks or blind spots
2. Update `skills/verification-before-completion/SKILL.md` so:
   - command-backed verification remains the default strongest path
   - manual scenario evidence is recognized as weaker but valid when explicit
   - insufficient verification is treated as a blocked completion state
3. Update `skills/using-openharness/SKILL.md` so detailed design is expected to name runtime verification path before implementation.
4. Extend `openharness.py verify` and tests only enough to:
   - preserve current command execution behavior
   - surface declared scenarios more intentionally
   - optionally validate any newly added structured verification metadata

## Test Design
- Template tests should assert that new packages include the verification sections needed to record intended path, executed path, and residual risk.
- CLI tests should assert that `verify` continues to run `required_commands` and expose declared scenarios without claiming they were executed automatically.
- Skill-level tests should assert that completion guidance distinguishes command-backed, manual, and insufficient verification paths.

## Error Handling
- If later exploration shows the four-path ladder is too coarse or too fine, revise it here before changing skills or templates.
- If downstream work discovers repository classes that need a separate path, add them only if they materially change evidence expectations.
- If the package cannot produce a simple vocabulary that skills can teach consistently, stop and narrow the scope before implementation.
- Do not let `openharness.py verify` imply that printed manual scenarios were actually executed; the CLI must distinguish declaration from execution.

## Migration Notes
- This package is the first concrete child of `OH-004` and should remain focused on semantics before automation.
- The next likely round after this one is to bind these semantics into status transitions and verification-oriented skill wording.

## Detailed Reflection
- I challenged whether this package already had enough information to write file-level implementation steps. It does not yet; that would lock in interfaces before the verification semantics are stable.
- I checked whether the current detailed design was now concrete enough to add an implementation order. It is, because local exploration exposed a small, ordered set of repository surfaces and showed that templates and skills should move before CLI enforcement.
- I checked whether a CLI-first implementation would be cleaner. It would be riskier, because machine fields would be chosen before the repository validated how packages actually record verification paths and residual risk.
- No bounded subagent discussion was needed because the remaining work is now a straightforward repository-local rollout sequence.
