---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## Skill Role

- Protocol status: imported generic skill
- Primary stage: implementation execution
- Trigger: use only when the user explicitly wants parallel agent work and the task decomposition is genuinely independent

Parallel delegation is useful when multiple bounded problems can be investigated or implemented without shared state, shared write scopes, or sequencing dependencies.

**Core principle:** one independent problem domain per agent.

## When to Use

Use this skill when all of the following are true:

- there are multiple independent failures or subtasks
- each agent can succeed with bounded context
- agents will not edit the same files
- the user explicitly wants parallel agent work

Do not use it for exploratory debugging, tightly coupled refactors, or tasks that block the very next local step.

## The Pattern

1. Group work by independent problem domain.
2. Prepare one bounded prompt per domain.
3. Dispatch in parallel.
4. Review each result.
5. Run integrated verification after combining the changes.

## Agent Prompt Structure

Each agent prompt should include:

1. specific scope
2. concrete goal
3. constraints
4. expected output

Do not ask an agent to "fix everything."

## Example

Scenario: six failures across three unrelated test files after a refactor.

Dispatch:

- Agent 1 → fix `agent-tool-abort.test.ts`
- Agent 2 → fix `batch-completion-behavior.test.ts`
- Agent 3 → fix `tool-approval-race-conditions.test.ts`

Each agent gets the failing tests, relevant error output, and constraints for that file only.

## Verification

After agents return:

1. review each summary
2. check for file conflicts
3. run the full verification path
4. spot-check high-risk areas
