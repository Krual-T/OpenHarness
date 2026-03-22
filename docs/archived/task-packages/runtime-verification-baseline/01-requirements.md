# Requirements

## Goal
Define the minimum runtime verification protocol that OpenHarness can require for task completion claims in repositories that may start with no reusable harness, no stable test suite, and only partial automation.

## Problem Statement
OpenHarness already requires runtime verification before completion, but the repository does not yet define what that means when a target repo has weak or nonexistent verification infrastructure.

That creates several risks:

- agents can claim completion with inconsistent evidence quality
- `verifying` is a named workflow stage but not a tightly defined gate
- bootstrap guidance cannot say what minimum loop a no-harness repository must establish
- future packages may overfit to strong-test repositories and ignore the weaker but common starting case

External exploration reinforces the need for a minimal but explicit contract:

- OpenAI's harness engineering guidance stresses versioned design docs, explicit verification status, and ongoing doc maintenance rather than relying on chat memory
- Anthropic's agent/evals guidance stresses starting with simple, composable workflows and using evaluation criteria to make success legible before scaling automation
- GitHub's coding-agent guidance stresses repository-local instructions for how to validate work and human review before merge

OpenHarness therefore needs a reusable baseline that is credible in low-automation repositories without pretending that all verification is already fully automated.

## Required Outcomes
1. Define a verification ladder for no-harness or weak-harness repositories.
2. Define the minimum evidence shape expected for each verification path.
3. Define how the ladder affects completion claims, especially `verifying` and the handoff into `05-verification.md` and `06-evidence.md`.
4. Define when weak verification is acceptable and when the agent must escalate, defer completion, or explicitly record residual risk.
5. Provide enough structure that follow-up implementation can update skills, templates, and CLI behavior intentionally.

## Success Conditions
- A future agent can classify a task's verification path without improvising its own categories.
- The repository has an explicit answer for what to do when only manual or task-local verification is available.
- Verification evidence becomes comparable across packages rather than ad hoc prose.
- The package makes clear which parts are minimum baseline semantics and which stronger practices remain optional future work.

## Non-Goals
- Design a full runtime-debug subsystem in this round.
- Require every repository to have mature automated integration or end-to-end tests before OpenHarness is usable.
- Replace human review with automated checks.
- Fully implement all downstream skill, template, or CLI changes in this package.

## Constraints
- The baseline must work for repositories that begin with no existing harness.
- The protocol must be strict enough to prevent empty completion claims, but flexible enough to represent manual verification honestly when automation is absent.
- The solution should preserve the fixed task-package model and evidence writeback flow.
- The baseline should be simple enough to explain in skills and templates without creating a second verification framework beside OpenHarness.
