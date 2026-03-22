# Requirements

## Goal
Make OpenHarness mechanically enforce the supported task-package workflow all the way through verification and archiving, instead of relying on direct `STATUS.yaml` edits and ephemeral command output.

## Problem Statement
OpenHarness already rejects many dishonest status claims, but two important workflow gaps remain.

First, status progression is still mostly social convention. An agent can directly edit `STATUS.yaml` and claim a later status without using a supported transition path. `check-tasks` now catches many bad end states, but there is still no single CLI entrypoint that says which transitions are legal, when timestamps should update, and how archive relocation should happen.

Second, `verify` execution is still mostly transient. The command runs declared checks and prints results to stdout, but it does not leave behind a structured, machine-readable run record that later archive decisions can depend on. That weakens the evidence chain that OpenHarness is trying to build: execution happened, but the repository cannot point to a stable artifact and say this exact run backs the current completion claim.

## Required Outcomes
1. Add a supported `transition` command that enforces the default status flow from the harness manifest instead of treating status changes as free-form file edits.
2. Reject skipped forward transitions, illegal archive requests, and target states whose required semantic anchors are not yet satisfied.
3. Make `verify` write a structured JSON artifact for every run, including failed and insufficient-verification outcomes, under `.harness/artifacts/<task-id>/verification-runs/`.
4. Bind each verification artifact to the current task-package content, at minimum by storing a content fingerprint and a snapshot of the declared verification commands.
5. Update `STATUS.yaml` with the latest verification artifact path, timestamp, and result so the current package state can be tied back to a concrete run without making `STATUS.yaml` the evidence source of truth.
6. Require archive transition through the supported CLI path to depend on a successful latest verification artifact that still matches the current package content, and to move the package into the archive root while keeping internal path references correct.
7. Teach the new behavior in templates, tests, and package docs so future work does not rediscover the protocol.

## Non-Goals
- Introduce per-package custom workflow graphs or a general workflow engine beyond the manifest's ordered default flow.
- Automatically execute manual verification scenarios that are intentionally human-run.
- Replace task-package markdown docs with a database, service, or external state store.
- Retroactively rewrite every historical verification note into a richer schema than the repository can credibly reconstruct.

## Constraints
- Keep the task-package model and default status vocabulary defined by the current manifest.
- Keep the implementation repository-local and file-based; no daemon, background service, or network dependency is allowed.
- Prefer additive `STATUS.yaml` fields and small CLI extensions over a second state file or parallel orchestration layer.
- A failed or insufficient verification run must still leave a durable artifact so later debugging is evidence-based.
- Time-stamped artifact JSON files are the evidence source of truth; `latest.json` is only an index and `STATUS.yaml` stores only a summary plus pointer.
- The solution must remain compatible with existing archived packages as historical fact sources, even if only new runs produce the richer artifacts automatically.
