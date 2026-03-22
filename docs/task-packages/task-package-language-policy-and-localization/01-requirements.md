# Requirements

## Goal
Define a language policy for OpenHarness task packages that prioritizes Chinese readability for the human maintainer while preserving the English identifiers, commands, and validation surfaces that the repository currently depends on.

## Problem Statement
The repository now has a practical usability gap:

- the human maintainer often does not want to read long English task-package content
- task packages are one of the highest-frequency fact surfaces in the repository
- current templates and validation rules still assume English section titles and English-first wording

This creates a direct mismatch between protocol correctness and maintainer usability:

- task packages may remain structurally valid but become hard for the maintainer to review
- localization may be desired, but naive full translation would break `check-tasks`, tests, and template consistency
- without an explicit policy, the repository may drift into inconsistent half-Chinese, half-English documents

The project therefore needs a clear answer to four questions:

- which repository surfaces should be Chinese-first
- which surfaces must remain English because they are machine-checked or protocol-stable
- whether task-package section titles should stay English, become Chinese, or support both
- how localization should roll out without breaking current repository validation

## Required Outcomes
1. Define the recommended language policy for active and archived task packages.
2. Define which structured elements should remain English, including status names, keys, commands, and other protocol identifiers.
3. Define a staged rollout plan for localization, including what should change first and what should wait for a later implementation wave.
4. Define the policy for section-title localization and its interaction with `check-tasks` and templates.
5. Identify the repository surfaces that a later implementation package should update.

## Success Conditions
- A future maintainer can read task-package content comfortably without losing protocol consistency.
- The repository gains a stable answer for "中文正文、英文结构" versus "全面本地化".
- Future localization work can proceed intentionally rather than editing files ad hoc.
- The package makes clear that readability for the human maintainer is a product requirement, not a personal preference.

## Non-Goals
- Translate all live repository files in this round.
- Localize code, CLI commands, YAML keys, or status values.
- Rewrite all skill files into Chinese in this package.
- Implement the template and validator changes immediately; this package only defines the policy and rollout shape.

## Constraints
- Current `check-tasks` validation depends on English section titles in several task-package documents.
- Commands, status names, YAML keys, and protocol identifiers should remain stable unless a later implementation deliberately changes them.
- The solution should improve readability without creating a second parallel documentation protocol.
- The policy should distinguish human-readable narrative text from machine-sensitive structure.

## Required Outcomes
1. 

## Non-Goals
- 

## Constraints
- 
