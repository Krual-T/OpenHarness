# Overview Design

## System Boundary
This package defines the product-level Python verification baseline when runtime tests are incomplete. It does not implement the support changes yet, but it must define the verification floor, escalation path, and documentation contract tightly enough that follow-up implementation can proceed without rediscovering the problem.

## Proposed Structure
Treat Python verification maturity as a small ladder rather than a binary `tests exist / tests do not exist` rule.

The default policy should distinguish three practical states:

1. `python baseline only`
   - `pytest` or an equivalent repository-level Python test run passes.
   - This is the minimum acceptable automated verification floor when runtime tests are incomplete.
   - Packages must disclose that the result is baseline-only if runtime behavior remains weakly covered.
2. `runtime tests recommended`
   - The task touches runtime behavior meaningfully enough that stronger runtime evidence would materially reduce risk.
   - The current round may still complete on the Python baseline, but the package must record runtime tests as explicit follow-up work.
3. `runtime tests required now`
   - The task's main claim depends directly on runtime behavior, integration behavior, user-visible flows, or failure modes that `pytest` baseline coverage does not credibly establish.
   - In this state, runtime tests are not optional polish; they are part of the current completion path.

The package contract should land in the existing design docs:

- `03-detailed-design.md`
  - declare the current verification floor
  - say whether runtime tests are required now or recommended next
  - explain the trigger for that choice
- `04-verification.md`
  - record what actually ran
  - say whether the result only satisfies the Python baseline or includes stronger runtime evidence
- `05-evidence.md`
  - capture residual risk when completion rests on baseline-only evidence
  - capture explicit follow-up work if runtime tests were deferred

Three architectural options were considered:

1. `runtime-tests-or-bust`
   - Require runtime tests for every meaningful Python task.
   - Too rigid for real repositories that are still building up test maturity.
2. `pytest-is-always-enough`
   - Treat passing Python tests as sufficient across the board.
   - Too weak because it hides when runtime evidence is materially missing.
3. `python baseline with explicit escalation`
   - Accept `pytest` as the default floor.
   - Require packages to say when runtime tests are required now versus recommended next.
   - This is the recommended direction.

Recommended direction: `python baseline with explicit escalation`.

Reasoning:

- It matches OpenHarness's core belief that repository-visible artifacts are the source of truth.
- It keeps Python work immediately usable without pretending weak verification is strong verification.
- It puts the real decision where it belongs: not in repository entry routing, but in per-task verification planning and completion claims.
- It keeps the workflow compatible with `OH-006` status semantics while making verification strength legible.

The implementation wave that follows this design should likely touch:

- `skills/verification-before-completion/SKILL.md`
- `skills/using-openharness/references/templates/*`
- `skills/using-openharness/SKILL.md` only where verification planning wording needs to be clarified
- package docs and examples that describe verification expectations for Python tasks

## Key Flows
1. A Python task reaches detailed design.
2. The package records `pytest` as the current verification floor.
3. The agent decides whether runtime tests are:
   - not yet needed beyond the baseline
   - recommended next
   - required now
4. Verification and evidence docs record the strength of the evidence honestly.
5. Completion claims match that strength instead of collapsing everything into a generic `tests passed`.

## Trade-offs
- Using `pytest` as the minimum floor makes the system immediately usable, but it is weaker than true runtime verification for many tasks.
- Allowing `recommended next` runtime tests is more pragmatic than blocking every task, but it requires the docs to be explicit about the gap so weak verification is not mistaken for full coverage.
- Requiring `required now` runtime tests on riskier tasks raises the bar, but that is the point; otherwise verification language becomes performative.

## Overview Reflection
- I challenged whether this package still needed to talk about repository entry or cold start. It does not; that was the wrong problem framing.
- I challenged whether `pytest` should always be enough. It should not; the package now makes escalation explicit when runtime behavior is central.
- I checked whether the design was still too vague to change behavior. It is now concrete enough because it names three verification states and where each one must be written down.
- I checked whether the package accidentally broadened into non-Python policy. It does not; it is intentionally a Python verification package.
- No bounded subagent discussion was used here because the main decision is a repository-local product-shape choice, and the viable alternatives are legible enough to compare directly.
