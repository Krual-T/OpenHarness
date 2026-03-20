# Evidence

## Files
- `pyproject.toml`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `AGENTS.md`
- `README.md`
- `docs/archived/designs/self-hosting-bootstrap/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design self-hosting-bootstrap OH-001 "OpenHarness Self-Hosting Bootstrap" --owner codex --summary "Bootstrap the OpenHarness repository into a self-hosted minimal harness repo with runnable CLI, tests, and an initial active design package."`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `mv docs/designs/self-hosting-bootstrap docs/archived/designs/self-hosting-bootstrap`

## Follow-ups
- Continue protocol simplification work under `OH-002`, especially the workflow change that removes the duplicated implementation-plan artifact from the fixed protocol.
- Add explicit exploration / maintenance skills in later rounds.
- Continue the next package by realigning the workflow around requirements -> exploration -> overview -> detailed -> implementation -> runtime verification -> completion.
