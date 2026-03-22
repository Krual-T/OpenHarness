# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if unrelated repository failures occur, keep the package at design status and record the blocker rather than claiming policy verification is complete
- Planned Evidence:
  - a concrete Chinese-first language policy for task packages
  - a phased rollout plan that separates prose localization from section-title localization
  - identified repository surfaces for later implementation

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Testing-First Design
This is a design package. Its immediate tests are repository-legibility and regression tests:

- the package must satisfy `check-tasks`
- the package must define a rollout path precise enough for later template and validator implementation
- the package must make the English-structure versus Chinese-content boundary explicit enough to stop ad hoc localization drift

## Files Added Or Changed
- Add `OH-015` package documents for task-package language policy and localization.
- In a later implementation wave, likely update:
  - `skills/using-openharness/references/templates/*`
  - `skills/using-openharness/scripts/openharness.py`
  - `skills/using-openharness/tests/test_openharness.py`
  - selected live task packages if the policy is adopted

## Interfaces
- Language policy interface:
  - Chinese-first narrative text in task-package prose
  - English protocol-stable identifiers
- Validator interface:
  - phase one keeps English section anchors intact
  - later phase may add dual-title or Chinese-title support
- Template interface:
  - later implementation must decide whether templates emit English titles with Chinese guidance, dual-language titles, or Chinese titles only

## Error Handling
- If contributors start translating titles without validator support, `check-tasks` will fail; the implementation wave must change validators and templates together.
- If contributors localize commands, statuses, or YAML keys, they risk breaking protocol surfaces; those elements should remain English.
- If the repository finds English section titles too costly even after Chinese body localization, open a focused second package for title-localization implementation instead of mixing changes opportunistically.

## Migration Notes
- Recommended rollout order:
  1. adopt Chinese-first narrative content for task packages
  2. keep section titles, file names, statuses, commands, and keys in English
  3. evaluate whether title localization is still worth the extra validator and template churn
- This package should remain design-only until a focused implementation package performs the validator and template changes, if any.

## Detailed Reflection
- I challenged whether the policy needed to choose title-localization now. It does not; the repository can get most of the readability benefit without taking on immediate validator changes.
- I checked whether the package was too conservative by keeping English titles in phase one. It is conservative, but deliberately so: it reduces migration risk while solving the primary maintainer-readability problem.
- I checked whether this package should also define whole-repository localization. It should not. The most urgent and highest-value surface is task packages.
