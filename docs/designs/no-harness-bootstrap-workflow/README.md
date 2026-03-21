# OH-007 No-Harness Bootstrap Workflow

## Summary
- Define how OpenHarness should cold-start inside a repository through a Python-first default path when no design packages and no mature runtime verification loop exist yet.
- Keep the first round immediately usable by falling back to `pytest` as the minimum verification gate for the supported Python path, while explicitly guiding the repository toward stronger runtime tests later.

## Current Status
- Detailed design complete.
- Ready to drive the first implementation wave for Python-first cold-start docs, templates, and verification guidance.

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
