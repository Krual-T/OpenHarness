# OH-007 No-Harness Bootstrap Workflow

## Summary
- Define how OpenHarness should cold-start inside a Python repository that has no design packages and no mature runtime verification loop yet.
- Keep the first round immediately usable by falling back to `pytest` as the minimum verification gate, while explicitly guiding the repository toward stronger runtime tests later.

## Current Status
- Detailed design complete.
- Ready to drive the first implementation wave for Python-only bootstrap docs, templates, and verification guidance.

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
