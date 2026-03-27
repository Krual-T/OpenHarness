# Openharness Skill Hub

OpenHarness uses a two-layer model:

- `protocol status` answers whether a skill is part of the fixed harness
- `workflow stage and trigger` answers when the skill should actually be used

The live workflow also uses stage-organized role injection:

- stages remain the main path
- roles are injected inside those stages to challenge specific decisions
- stage gates and challenge closure determine readiness

## Protocol Status

### Core Protocol Skills
- `using-openharness`
  - parent workflow skill
  - repository entry skill
  - owns repository protocol, skill routing, package routing, supporting scripts, and templates
- `brainstorming`
  - core protocol skill for converging requirements before implementation when the task needs design work
- `exploring-solution-space`
  - core protocol skill for repository and web exploration before architecture is locked
  - includes reflection before overview or detailed design is treated as ready
- `verification-before-completion`
  - core protocol skill that enforces evidence-before-claims at the end of work

### Optional Helper Skills
- `test-driven-development`
  - optional helper skill for failing-test-first implementation discipline
- `systematic-debugging`
  - optional helper skill for root-cause-first debugging when a bug, failure, or unexpected behavior appears
- `subagent-driven-development`
  - optional helper skill for multi-task execution when the package is detailed enough and tasks are mostly independent
- `using-git-worktrees`
  - optional helper skill for isolated execution workspaces when the task needs them
- `requesting-code-review`
  - optional helper skill for bounded review before merge or after major work
- `receiving-code-review`
  - optional helper skill for evaluating review feedback rigorously before implementation
- `finishing-a-development-branch`
  - optional helper skill for integrating verified work at the end of an implementation wave
- `project-memory`
  - optional helper skill for storing validated facts, workflows, and decisions under `.project-memory/`

### Imported Generic Skills
- `dispatching-parallel-agents`
  - imported generic skill available in the repository
  - not part of the fixed OpenHarness protocol unless explicitly promoted later

## Workflow Stages And Triggers

## Writing Guidance Surface

- `author-entry.md`
  - Chinese-first author routing page for task-package writing
  - points maintainers to the current stage and the matching writing guidance without duplicating the guidance bodies
- `requirements-writing-guidance.md`
  - repository reference for how to write `01-requirements.md`
- `overview-design-writing-guidance.md`
  - repository reference for how to write `02-overview-design.md`
- `detailed-design-writing-guidance.md`
  - repository reference for how to write `03-detailed-design.md`
- `verification-writing-guidance.md`
  - repository reference for how to write `04-verification.md`
- `evidence-writing-guidance.md`
  - repository reference for how to write `05-evidence.md`
- these references complement stage skills by explaining document purpose, required questions, document boundaries, and common failure modes
- they keep long-form writing guidance out of `SKILL.md` and out of task-package templates
- `author-entry.md` sits above them as the shortest discoverability layer for Chinese-first users

### Entry And Routing
- `using-openharness`
  - default first step for repository workflow and task-package routing
  - the only repository entry skill

### Requirements Convergence
- `brainstorming`
  - default when the task needs requirement convergence or design clarification before implementation
  - injects product perspective and CEO perspective before requirements are treated as ready

### Exploration And Architecture
- `exploring-solution-space`
  - default after requirements are clear and before architecture or implementation details are locked
  - injects architecture perspective, testing perspective, and later verification-facing review/risk expectations through stage gates

### Implementation Execution
- `test-driven-development`
  - default implementation discipline for feature work and bugfixes
- `subagent-driven-development`
  - optional when execution can be decomposed into independent tasks
- `using-git-worktrees`
  - optional when isolation or branch/worktree management is required

### Debugging And Repair
- `systematic-debugging`
  - default when the task centers on a failure, regression, or unexplained behavior
- `receiving-code-review`
  - optional when review feedback arrives and needs technical evaluation before action

### Verification And Closure
- `verification-before-completion`
  - mandatory before completion claims, archive claims, or merge-ready claims
  - works best when earlier stages already recorded challenge closure and requirement-to-evidence links
- `requesting-code-review`
  - optional before merge or after major implementation waves
- `finishing-a-development-branch`
  - optional when the work is implemented and verified and needs final integration handling

## Role Injection Model

- product perspective
  - challenge user value, scenarios, priorities, and success semantics
- CEO perspective
  - challenge timing, cost cap, strategic fit, and worst acceptable downside
- architecture perspective
  - challenge boundaries, complexity, and main-path stability
- testing perspective
  - challenge testability, observability, rollback clarity, and evidence quality
- review perspective
  - challenge whether the finished work actually matches the package and its declared evidence
- risk perspective
  - challenge high-impact residual risks without expanding into infinite caution

## Stage Gates And Challenge Closure

- stage gates define what must be concretely present before a stage is treated as ready
- challenge closure means each substantive challenge is accepted, rejected, or deferred with a visible disposition
- if role injection adds commentary without changing constraints, evidence shape, or decisions, the workflow has failed

### Repository Memory And Maintenance
- `project-memory`
  - optional when a validated fact, workflow, or decision should be saved or checked for staleness
- `dispatching-parallel-agents`
  - generic helper for parallel task dispatch when that pattern is explicitly desired

## Python Verification Baseline
- OpenHarness is Python-first.
- `uv run pytest` is the default minimum automated verification floor for Python-first repositories.
- Passing `pytest` alone does not automatically mean runtime behavior is fully verified.
- Stronger project-specific runtime verification belongs in task packages, especially `03-detailed-design.md` and `04-verification.md`.

## Runtime Capability Contract
- OpenHarness uses a runtime capability contract instead of pretending one universal runtime-debug skill can fit every repository.
- The core protocol defines when runtime work is recognized, how routing works, and where evidence must be written back.
- Repositories should keep a runtime surface map that inventories supported runtime surfaces, their evidence shape, and the linked helper or bootstrap package.
- A repository may expose multiple runtime helper skills across different runtime surfaces, but those helpers remain optional project-level helpers rather than new entry skills.
- When a matching runtime capability exists, `using-openharness` should reuse the linked helper guidance.
- When the runtime surface is mapped but helper coverage is missing, add one new narrow helper instead of hiding the gap inside task-local notes.
- When no matching capability exists, the agent should open a bootstrap package before claiming supported runtime verification on that surface.
- The shared contract lives in `runtime-capability-contract.md`.
- The project-facing map guidance lives in `project-runtime-surface-map.md`.
- The focused helper-addition workflow lives in `adding-project-runtime-helper.md`.

## Current Cleanup Rule
- Prefer `using-openharness` when referring to the concrete repository entry skill.
- Reserve `OpenHarness` for the harness product or protocol, not the concrete skill id.
- Do not advertise retired plan-writing or plan-execution skills anywhere in the live repository surface.
- Treat imported skills as reusable helpers unless they become part of the core repository workflow.
- Do not keep a separate repository entry layer beside `using-openharness`.
- Remove duplicated entry skills and parallel workflow roots rather than maintaining aliases forever.
