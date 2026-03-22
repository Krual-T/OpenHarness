# Overview Design

## System Boundary
This package defines the product-level semantics of minimum runtime verification inside OpenHarness. It does not yet implement all supporting CLI or template changes, but it must define the contract tightly enough that those changes become straightforward follow-up work.

## Proposed Structure
Treat runtime verification as a small verification ladder rather than a binary "tests exist / tests do not exist" rule.

The baseline should distinguish four verification paths:

1. `repository automation`
   - Use pre-existing repository commands such as tests, builds, linters, or scenario runners.
   - Preferred when available because it is repeatable and cheap to rerun.
2. `task-local automation`
   - Use temporary or newly added commands/scripts created specifically to verify the current task when the repository lacks broader harnesses.
   - Acceptable when repository-level automation does not yet exist but the task can still be checked mechanically.
3. `manual runtime verification`
   - Use explicit, reproducible manual steps when the behavior is inherently interactive or the repository lacks automation.
   - Must capture environment, inputs, observed outputs, and remaining blind spots.
4. `insufficient verification`
   - Used when none of the above can credibly establish the claimed behavior.
   - This path is not a completion path; it requires explicit escalation, reduced claim scope, or follow-up work before the package can be treated as done.

This gives OpenHarness a minimum common language:

- `03-detailed-design.md` states the intended verification path up front
- `05-verification.md` records which path actually ran and with what results
- `06-evidence.md` captures the exact commands, manual steps, artifacts, and residual risks
- `STATUS.yaml` and completion claims can distinguish "verification performed" from "verification still insufficient"

The recommended semantic rule is:

- `verifying` means implementation is complete enough to check, but the package is still gathering or finalizing the declared evidence
- a package should not exit its completion path on `insufficient verification`
- manual verification is acceptable only when it is explicit, reproducible, and paired with stated blind spots

This package should also define escalation rules:

- if repository automation exists, prefer it over weaker paths
- if only task-local automation is feasible, record why broader automation does not yet exist
- if only manual verification is feasible, record why and what remains unverified
- if no credible runtime verification can be produced, do not claim broad completion

External references support this structure:

- OpenAI's harness engineering favors explicit verification state and doc maintenance over hidden assumptions
- Anthropic's eval guidance supports starting with simple, legible evaluation loops before scaling sophistication
- GitHub's coding-agent guidance supports explicit repo-local validation instructions and human review gates

## Local Constraints And Viable Options
Current repository surfaces already shape the solution:

- `skills/verification-before-completion/SKILL.md` enforces "fresh evidence before claims", but it only reasons in terms of commands and does not distinguish stronger versus weaker verification paths.
- `skills/using-openharness/scripts/openharness.py verify` already runs `verification.required_commands` and prints `required_scenarios`, which means the repository already has a partial structure for command-backed and manual verification.
- task-package templates for `03`, `05`, and `06` are still generic and do not teach how intended verification, executed verification, and residual risk should be recorded.
- current tests validate package structure and CLI behavior, but they do not yet pin any semantics around verification-path vocabulary or blocked completion on insufficient evidence.

That leaves three viable architectural options:

1. `docs-first semantics, CLI-assisted`
   - Keep the verification ladder primarily in package docs and skill wording.
   - Reuse `required_commands` and `required_scenarios` as the CLI-facing declaration surface.
   - Add structured expectations to templates before adding more machine enforcement.
2. `status-schema-first`
   - Add new machine-readable fields immediately under `STATUS.yaml.verification` such as path type, blocking mode, or residual-risk markers.
   - Update CLI, validation, and tests in the same round.
3. `separate eval subsystem`
   - Introduce a new harness module or runner dedicated to evaluation paths and evidence.
   - Potentially more expressive, but much heavier and easier to let drift into a second parallel system.

## Recommended Direction
Choose `docs-first semantics, CLI-assisted` first.

Reasoning:

- It fits Anthropic's advice to start with simple, composable workflows instead of jumping to a heavier framework.
- It fits OpenAI's harness engineering emphasis on repository-visible artifacts and mechanically checked structure.
- It fits the current repository, because `required_commands` and `required_scenarios` already give the CLI a natural minimum interface without inventing another abstraction layer.
- It lets OpenHarness define what counts as acceptable evidence before it decides how much of that contract must be machine-enforced.

Concretely, the first implementation wave should:

- update `03-detailed-design.md` conventions so packages declare an intended verification path and fallback path
- update `05-verification.md` conventions so packages record which path actually ran, its result, and any mismatch versus plan
- update `06-evidence.md` conventions so commands, manual steps, artifacts, and residual risks are recorded in a comparable shape
- update `skills/verification-before-completion/SKILL.md` so it recognizes commands, manual scenarios, and blocked-completion cases rather than only command success
- update `skills/using-openharness/SKILL.md` and templates so runtime verification planning is explicit before implementation
- extend `openharness.py verify` only enough to expose or summarize declared scenarios and later structured verification metadata, not to become a second orchestration framework

The second implementation wave can then decide whether stronger machine-readable fields belong in `STATUS.yaml.verification`, informed by real package usage rather than speculation.

## Key Flows
1. A task reaches detailed design and chooses an intended verification path.
2. Implementation proceeds with that intended path recorded in `03-detailed-design.md`.
3. During `verifying`, the agent gathers fresh evidence using the strongest available path.
4. `05-verification.md` records results in a format that matches the chosen path.
5. `06-evidence.md` records commands, manual procedures, artifacts, and unresolved limits.
6. If evidence is insufficient, the task does not upgrade its claim; it either narrows scope, adds stronger verification, or records follow-up work.

This package is upstream of:

- `status semantics tightening`, because status transitions need verification gates
- `no-harness bootstrap workflow`, because bootstrap must establish at least one credible verification path
- `maintenance and entropy reduction`, because stale or weak evidence must later be reviewed consistently

The recommended dependency order inside the runtime-verification stream is:

1. define docs and skill semantics
2. teach templates the new verification contract
3. update CLI output and validation to reflect the contract
4. feed the resulting semantics into `status semantics tightening`

## Trade-offs
- A verification ladder is more explicit than a single "run tests" rule, but it introduces more vocabulary that skills and templates must teach clearly.
- Allowing manual verification preserves usability in weak-harness repositories, but it risks ritualized evidence unless the protocol requires concrete steps and blind-spot disclosure.
- Treating insufficient verification as a non-completion path is stricter, but it is necessary if OpenHarness wants "evidence before claims" to mean the same thing across repositories.
- A docs-first first phase is less rigid than a schema-first rollout, but it reduces the risk of encoding the wrong machine contract before the repository has validated the semantics in real packages.

## Overview Reflection
- I challenged whether the ladder should have only two categories: automated and manual. That was too coarse because task-local automation is materially stronger than manual checks and common in early-stage repositories.
- I challenged whether "manual verification" should be disallowed entirely. That would make OpenHarness unusable in many no-harness repos and would not match the stated product scope.
- I checked whether the proposed structure weakens the completion bar. It does not if `insufficient verification` is explicitly treated as a blocked completion path rather than a tolerated weak success state.
- I compared a docs-first rollout, a status-schema-first rollout, and a separate eval subsystem. The docs-first path is the best fit for the current repository because the CLI and package structure already provide enough surface to teach the semantics without introducing a second framework.
- No bounded subagent discussion was needed yet because the main architectural choice is now narrow and repository-local rather than a contested external integration.
