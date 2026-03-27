# Openharness Skill Hub

OpenHarness uses a two-layer model:

- `protocol status` answers whether a skill is part of the fixed harness
- `workflow stage and trigger` answers when the skill should actually be used

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

### Entry And Routing
- `using-openharness`
  - default first step for repository workflow and task-package routing
  - the only repository entry skill

### Requirements Convergence
- `brainstorming`
  - default when the task needs requirement convergence or design clarification before implementation

### Exploration And Architecture
- `exploring-solution-space`
  - default after requirements are clear and before architecture or implementation details are locked

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
- `requesting-code-review`
  - optional before merge or after major implementation waves
- `finishing-a-development-branch`
  - optional when the work is implemented and verified and needs final integration handling

### Repository Memory And Maintenance
- `project-memory`
  - optional when a validated fact, workflow, or decision should be saved or checked for staleness
- `dispatching-parallel-agents`
  - generic helper for parallel task dispatch when that pattern is explicitly desired

## Reference Surfaces
- Writing guidance lives in:
  - `author-entry.md`
  - `requirements-writing-guidance.md`
  - `overview-design-writing-guidance.md`
  - `detailed-design-writing-guidance.md`
  - `verification-writing-guidance.md`
  - `evidence-writing-guidance.md`
- Runtime capability references live in:
  - `runtime-capability-contract.md`
  - `project-runtime-surface-map.md`
  - `adding-project-runtime-helper.md`

## Current Cleanup Rule
- Prefer `using-openharness` when referring to the concrete repository entry skill.
- Reserve `OpenHarness` for the harness product or protocol, not the concrete skill id.
- Do not advertise retired plan-writing or plan-execution skills anywhere in the live repository surface.
- Treat imported skills as reusable helpers unless they become part of the core repository workflow.
- Do not keep a separate repository entry layer beside `using-openharness`.
- Remove duplicated entry skills and parallel workflow roots rather than maintaining aliases forever.
