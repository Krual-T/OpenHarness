# OH-010 Workflow Transition And Verification Artifacts

## Summary
- Close the remaining workflow-control gap in OpenHarness by making status changes go through a supported CLI path instead of ad hoc `STATUS.yaml` edits.
- Record each `verify` run as a structured artifact under `.harness/artifacts/` and bind the latest run back to `STATUS.yaml` so archive claims have machine-checkable evidence.

## Current Status
- Active child package of `OH-004 Harness Completion Roadmap`.
- Follow-up to archived `OH-006 Status Semantics Tightening` and `OH-009 Task Package Semantic Validation`.
- This package owns the last major workflow-semantic gaps left after document-anchor validation: legal status transitions and verification artifact closure.

## Read This First
- `STATUS.yaml`
- `01-requirements.md`
- `02-overview-design.md`
- `03-detailed-design.md`
- `05-verification.md`
- `06-evidence.md`
