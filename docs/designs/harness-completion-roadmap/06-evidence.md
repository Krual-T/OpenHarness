# Evidence

## Files
- `docs/designs/harness-completion-roadmap/README.md`
- `docs/designs/harness-completion-roadmap/01-requirements.md`
- `docs/designs/harness-completion-roadmap/02-overview-design.md`
- `docs/designs/harness-completion-roadmap/03-detailed-design.md`
- `docs/designs/harness-completion-roadmap/05-verification.md`
- `docs/designs/harness-completion-roadmap/06-evidence.md`
- `docs/designs/harness-completion-roadmap/STATUS.yaml`
- `skills/exploring-solution-space/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/tests/test_openharness.py`
- `docs/archived/designs/runtime-verification-baseline/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design harness-completion-roadmap OH-004 "Harness Completion Roadmap" --owner codex --summary "Track the remaining major work needed to make OpenHarness a complete no-harness bootstrap and maintenance-oriented skill hub, including runtime verification defaults, bootstrap workflow, maintenance, and status semantics."`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `mv docs/designs/runtime-verification-baseline docs/archived/designs/runtime-verification-baseline`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Re-check whether `status semantics tightening` should become the second child package before bootstrap work, now that `OH-005 Runtime Verification Baseline` is archived.
- Consider whether a future focused package should tighten the transition contract between overview reflection and detailed-design drafting beyond wording-only safeguards.
- Decide whether the no-harness bootstrap stream can now reuse the archived `OH-005` baseline directly or needs one more focused discovery round first.
