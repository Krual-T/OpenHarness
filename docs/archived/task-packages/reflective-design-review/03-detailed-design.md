# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if unrelated repository failures block verification, record the blocker in `04-verification.md` and do not claim completion until the package state is honest again
- Planned Evidence:
  - updated workflow skills and core docs
  - tests that pin the reflection-loop wording
  - a clean repository validation run after the package is archived

## Files Added Or Changed
- Update `skills/using-openharness/SKILL.md` to describe reflection checkpoints in the fixed workflow.
- Update `skills/exploring-solution-space/SKILL.md` or adjacent core docs so exploration hands off into overview reflection instead of directly assuming readiness.
- Update core docs (`AGENTS.md`, `README.md`, maybe `skill-hub.md`) to mention reflection and bounded subagent discussion for `02` and `03`.
- Optionally add a dedicated lightweight skill or prompt reference later if the reflection/subagent loop needs sharper structure.

## Interfaces
- Overview-ready should mean:
  - overview drafted
  - reflection questions answered
  - subagent discussion performed when required by risk/uncertainty
- Detailed-ready should mean:
  - detailed design drafted
  - testing-first structure reviewed
  - runtime verification approach reviewed
  - subagent discussion performed when required by complexity/risk
- Reflection output should be recorded in the design docs themselves, likely as a dedicated section rather than a hidden conversation.

## Error Handling
- If the agent cannot answer the reflection questions confidently, it should not silently proceed; it should either revise the design or trigger bounded subagent discussion.
- If the subagent review conflicts with the main agent's judgment, the disagreement should be summarized explicitly instead of hidden.

## Migration Notes
- Start by documenting the reflection loop in workflow docs before introducing any new dedicated automation.
- The first version can use existing subagent capabilities and bounded prompts rather than adding a heavy new subsystem immediately.

## Detailed Reflection
- I checked whether this package needed more file-level implementation detail. It did not; the main job was to land the reflection requirement in the protocol surfaces that agents actually read.
- I checked whether runtime verification needed custom commands. It did not; the standard repository validation path was enough for this documentation-focused package.
