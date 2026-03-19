# Openharness Skill Hub

## Core
- `openharness`
  - parent workflow skill
  - repository entry skill
  - owns repository protocol, skill routing, package routing, supporting scripts, and templates
- `brainstorming`
  - converges ambiguous work into `01-requirements.md`, `02-overview-design.md`, `03-detailed-design.md`
- `writing-plans`
  - writes `04-implementation-plan.md` when explicit staged execution is needed
- `verification-before-completion`
  - enforces evidence-before-claims at the end of work

## Execution
- `executing-plans`
  - executes `04-implementation-plan.md` in-session
- `subagent-driven-development`
  - executes `04-implementation-plan.md` with subagents and review stages
- `finishing-a-development-branch`
  - completes verified development work
- `using-git-worktrees`
  - creates isolated workspaces when required by execution flow

## Quality
- `systematic-debugging`
  - root-cause-first debugging discipline
- `test-driven-development`
  - failing-test-first implementation discipline
- `requesting-code-review`
  - dispatches review with bounded context
- `receiving-code-review`
  - evaluates review feedback rigorously before implementation

## Repository Memory
- `project-memory`
  - stores validated facts, workflows, and decisions under `.project-memory/`

## Imported Generic Skills
- `dispatching-parallel-agents`
- `writing-skills`

These are still generic imported skills. They are available in the hub, but they are not part of the core openharness protocol.

## Current Cleanup Rule
- Prefer `openharness` vocabulary over legacy external-skill vocabulary.
- Treat imported skills as reusable helpers unless they become part of the core repository workflow.
- Do not keep a separate repository entry layer beside `openharness`.
- Remove duplicated entry skills and parallel workflow roots rather than maintaining aliases forever.
