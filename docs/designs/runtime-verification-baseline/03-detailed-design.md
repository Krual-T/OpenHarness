# Detailed Design

## Testing-First Design
This package is still in early design. The first test for this round is document-level:

- the package must validate under `openharness.py check-designs`
- the package must make the verification ladder and completion semantics concrete enough to drive follow-up implementation
- the package must identify likely repository surfaces before code changes begin

## Files Added Or Changed
- Update `01-requirements.md` with the minimum verification problem statement and scope.
- Update `02-overview-design.md` with the verification ladder, completion semantics, and upstream/downstream dependencies.
- Defer file-level implementation changes until the overview is stable enough to constrain them.

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

## Error Handling
- If later exploration shows the four-path ladder is too coarse or too fine, revise it here before changing skills or templates.
- If downstream work discovers repository classes that need a separate path, add them only if they materially change evidence expectations.
- If the package cannot produce a simple vocabulary that skills can teach consistently, stop and narrow the scope before implementation.

## Migration Notes
- This package is the first concrete child of `OH-004` and should remain focused on semantics before automation.
- The next likely round after this one is to bind these semantics into status transitions and verification-oriented skill wording.

## Detailed Reflection
- I challenged whether this package already had enough information to write file-level implementation steps. It does not yet; that would lock in interfaces before the verification semantics are stable.
- I checked whether the current detailed design is still useful without implementation steps. It is, because it records the likely landing surfaces and the conditions under which the package is ready to advance.
- No bounded subagent discussion was needed yet because the remaining uncertainty is still about semantic shape, not code-level decomposition.
