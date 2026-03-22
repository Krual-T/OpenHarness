# Overview Design

## System Boundary
This package defines the language policy for task-package documentation and related maintainer-facing repository surfaces. It does not yet implement template or validator changes, and it does not attempt a whole-repository translation.

## Proposed Structure
Use a layered language policy instead of a repository-wide one-line rule.

### Layer 1: Human narrative content becomes Chinese-first
The following surfaces should default to Chinese narrative text because they are read frequently by the maintainer and exist primarily to communicate intent, design, verification meaning, and evidence interpretation:

- `docs/task-packages/*/*.md`
- `docs/archived/task-packages/*/*.md`
- maintainer-facing roadmap and evidence text

Under this policy, paragraphs, bullet explanations, requirements, trade-offs, verification notes, and follow-up reasoning should be written in Chinese.

### Layer 2: Protocol-stable structure remains English
The following elements should remain English because they are protocol identifiers, machine-checked anchors, or direct command surfaces:

- status values such as `proposed`, `detailed_ready`, `archived`
- YAML keys and field names
- CLI commands
- file names
- path names
- current validator-sensitive section titles, at least in the first rollout phase

### Layer 3: Section-title localization is a second-phase decision
The repository should not immediately translate task-package section titles because current validation hard-codes English titles such as:

- `## Goal`
- `## Problem Statement`
- `## Proposed Structure`
- `## Runtime Verification Plan`

The first rollout should therefore be:

- keep section titles in English
- translate the content under those titles into Chinese
- keep commands and identifiers in English

If full localization is still desired after that, a later implementation package can decide between:

1. `dual-title support`
   - validator accepts either English or Chinese canonical titles
2. `Chinese-title migration`
   - validator, templates, and tests move to Chinese titles
3. `English-title permanent`
   - titles stay English permanently while body content is Chinese-first

The recommended first decision is `English-title permanent for phase one`, because it delivers most readability gains immediately with the least protocol churn.

## Key Flows
1. A maintainer reads a task package and finds the English prose too costly to parse.
2. The repository follows the language policy instead of ad hoc translation.
3. Narrative content in task packages is written in Chinese.
4. Commands, statuses, YAML keys, and machine-sensitive anchors remain English.
5. If the repository later decides to localize section titles too, it opens a focused implementation package that updates validators, templates, and tests together.

## Trade-offs
- Chinese-first task-package prose improves maintainer readability immediately, but it introduces a stronger distinction between narrative text and machine-sensitive structure.
- Keeping section titles English in phase one is less aesthetically pure, but it avoids breaking the validator and keeps rollout risk low.
- Full localization could make the docs feel more internally consistent, but it requires coordinated changes across templates, tests, and `check-tasks`.
- Not localizing at all preserves technical stability, but it keeps one of the repository's most important fact surfaces harder for the maintainer to use.

## Overview Reflection
- I challenged whether the policy should simply say "everything becomes Chinese". That would be easy to state but would immediately collide with validator assumptions and stable protocol identifiers.
- I considered keeping task packages fully English and only changing assistant replies. That would not solve the underlying repository-usability problem because the maintainer still needs to read the task packages themselves.
- I checked whether skill files should be included in the first localization wave. They should not. Task packages are the highest-value readability target, while skill localization is a much larger and riskier second-order change.
- I checked whether English section titles with Chinese body content would be too mixed-language to accept. It is a compromise, but it is a controlled and intentional compromise rather than accidental drift.
