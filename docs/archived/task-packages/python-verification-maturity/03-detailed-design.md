# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - Docs-first design verification in this round.
  - Follow-up implementation rounds should verify the new Python verification wording with `check-tasks`, `bootstrap`, and repository `pytest` runs.
  - When a task materially depends on runtime behavior, the package should explicitly choose between `runtime tests recommended next` and `runtime tests required now` rather than pretending `pytest` alone closes the gap.
- Fallback Path:
  - If implementation cannot yet enforce the wording mechanically, capture the expected package-writing rules in docs/templates first and record the remaining enforcement gap.
- Planned Evidence:
  - `05-verification.md` should record task-package validation, bootstrap inventory output, and repository `pytest` results for the implementation wave.
  - `06-evidence.md` should record the updated evidence wording and any remaining gap between baseline-only evidence and stronger runtime evidence.

Move to `in_progress` only when detailed design is concrete enough to execute.

## Files Added Or Changed
- Update `docs/archived/task-packages/python-verification-maturity/*` so the package preserves the Python verification baseline, escalation rules, and implementation landing points as an archived fact source.
- Update `docs/archived/task-packages/harness-completion-roadmap/*` so `OH-004` clearly treats `OH-007` as the completed archived package for the Python verification-maturity stream.
- In the implementation wave, likely update:
  - `skills/using-openharness/references/templates/*`
  - `skills/verification-before-completion/SKILL.md`
  - `skills/using-openharness/SKILL.md` only if verification planning wording needs alignment
  - `skills/using-openharness/tests/test_openharness.py`

## Interfaces
The Python verification workflow should expose these stable decisions:

- `verification guidance`
  - `pytest` is the default minimum gate for Python work.
  - If runtime behavior is central to the task, the package must explicitly say whether runtime tests are required now or recommended next.
  - `Recommended next` and `required now` must not be mixed together implicitly.
  - `pytest passed` alone must not be described as full evidence when runtime behavior is still weakly covered.
- `evidence wording`
  - `05-verification.md` should state the executed verification level.
  - `06-evidence.md` should state residual risk and the exact follow-up if runtime tests were deferred.
- `status progression`
  - The first package should begin at `proposed` or `requirements_ready`, then follow `OH-006` readiness checkpoints normally.
  - Later statuses must not imply stronger runtime verification than the package actually performed.

## Error Handling
- If `pytest` cannot credibly run and there is no stronger existing automated path, the package is not ready to claim even the Python baseline.
- If a task is marked baseline-only even though its main claim is runtime-heavy, the package should be revised rather than quietly accepted.
- If implementation cannot yet automate the distinction, prefer explicit docs/template wording over fake machine precision.

## Migration Notes
- `OH-007` no longer stays active under the older repository semantics that archived a completed design baseline once its design round finished.
- Under the newer task-package semantics, this should be read as a historical exception rather than as the rule for future archive decisions.
- The implementation wave should treat this archived package as the fact source for Python verification baseline and escalation wording, and feed any remaining maintenance implications back into `OH-004`.

## Detailed Reflection
- I challenged whether this package still needed to say anything about entry routing. It does not; that concern has been removed.
- I challenged the testing strategy first. The key risk is not absence of perfect runtime tests on day one; it is silent ambiguity about whether `pytest` is enough for now and when runtime tests must be added. The design now makes that distinction explicit.
- I checked whether the interfaces were still too abstract to implement. They were initially; this revision now states explicit verification guidance, evidence wording, and status implications.
- I checked whether runtime verification was concrete enough. For a design-only round, it is concrete enough because it names `pytest` as the floor and requires packages to state whether runtime tests are required now or recommended next.
- No bounded subagent discussion was used because the remaining uncertainty is implementation staging, not a contested architectural fork.
