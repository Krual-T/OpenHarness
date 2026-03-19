# OpenHarness

**OpenHarness is an agent-first repository scaffold for Codex.**

It is built around a simple belief: the bottleneck is no longer typing code. The bottleneck is giving coding agents a repository they can actually reason about.

OpenHarness packages the workflow patterns, skills, and repository structure we found most useful when adapting agent-driven development inside [`openrelay`](https://github.com/Krual-T/OpenRelay), with direct inspiration from [`obra/superpowers`](https://github.com/obra/superpowers) and strong conceptual alignment with OpenAI's article on [harness engineering](https://openai.com/index/harness-engineering/).

If you want Codex to stop improvising and start operating inside a legible, verifiable system, this repo is for you.

## Why OpenHarness exists

Most agent failures are not model failures. They are environment failures.

Agents do badly when:
- the repository has no map
- the important context lives in chat, docs tools, or people's heads
- requirements, architecture, implementation notes, and verification evidence are mixed together
- there is no mechanical way to tell what is current, what is stale, and what is done

OpenHarness exists to fix that.

It gives Codex a working environment where:
- `AGENTS.md` is a map, not an encyclopedia
- repository-local docs are the system of record
- each task has a structured design package
- verification is explicit and repeatable
- reusable workflow knowledge lives in version control
- humans steer and review the system, while agents do the heavy execution

## The core idea

OpenHarness is not just a bundle of prompts.

It is a repository operating model.

The model is simple:
1. Keep the entrypoint small.
2. Put the truth in the repo.
3. Structure work so agents can discover what matters.
4. Make design, implementation, and verification separate artifacts.
5. Treat agent legibility as a first-class engineering goal.

That is the real harness.

## Install in Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/Krual-T/OpenHarness/refs/heads/main/.codex/INSTALL.md
```

Or install manually:

```bash
git clone https://github.com/Krual-T/OpenHarness.git ~/.codex/openharness
mkdir -p ~/.codex/skills
ln -s ~/.codex/openharness/skills ~/.codex/skills/openharness
```

Then restart Codex.

## What you get

### 1. A repository map instead of a giant prompt blob

OpenHarness uses `AGENTS.md` as the repository map.

It tells the agent where truth lives, what the default workflow is, what must be verified, and what needs to be written back before a task is considered complete.

This follows the same spirit described by OpenAI's harness engineering article: the entrypoint should orient the agent, not drown it.

### 2. Design packages instead of vague task memory

Every meaningful task lives in `docs/designs/<task>/` as a package with stable files for:
- requirements
- overview design
- detailed design
- implementation plan
- verification
- evidence
- machine-readable status

That gives both humans and agents a shared source of truth that can be reviewed, diffed, validated, and archived.

### 3. Skills that enforce process, not just style

OpenHarness includes a copied and adapted skills library under `skills/`, including workflows for:
- brainstorming before implementation
- writing plans for multi-step work
- systematic debugging
- TDD-oriented execution
- verification before claiming success
- code review loops
- project memory capture

These skills are meant to shape how work gets done, not merely how answers are phrased.

### 4. A bias toward agent legibility

OpenHarness assumes a practical truth of agentic software work:

**If the agent cannot discover it from the repository, it effectively does not exist.**

That means key decisions should move out of chat threads and into versioned artifacts. The repo becomes the working memory, not just the code container.

## The OpenHarness workflow

A typical task looks like this:

1. `AGENTS.md` routes the agent into the correct workflow.
2. `openharness` checks the manifest and active design packages.
3. The agent reads the task package in a fixed order.
4. If the task is still fuzzy, `brainstorming` converges the design first.
5. If execution needs staging, `writing-plans` creates the implementation plan.
6. The agent implements against the package contract.
7. Verification and evidence are written back into the package.
8. Completed packages are archived without losing history.

The result is a repo that accumulates usable knowledge instead of accumulating invisible assumptions.

## Why this works

OpenAI's harness engineering write-up makes a point that resonates strongly here: once agents can generate code quickly, the scarce resource becomes human attention.

OpenHarness is designed around that constraint.

It tries to reduce wasted human attention by making the repository:
- easier for agents to navigate
- easier to validate mechanically
- easier to review incrementally
- easier to clean up over time

In other words, this repo is optimized less for heroic one-shot prompting and more for sustained, compounding throughput.

## Repository layout

```text
AGENTS.md                          # repository map
skills/                            # workflow skills used by Codex
docs/designs/<task>/               # active design packages
docs/archived/designs/<task>/      # archived design packages
.project-memory/                   # reusable validated project knowledge
```

## Who this is for

OpenHarness is a good fit if you want to:
- run Codex against real repositories, not toy demos
- keep architecture and workflow decisions in version control
- make agent output more consistent without writing giant prompts
- scale multi-step work through design packages and verification loops
- build a repo that gets more legible as it grows

It is probably not a fit if you want a minimal one-file setup with no process overhead.

## Upstream attribution

OpenHarness is a derivative work.

This repository directly reuses source material from [`obra/superpowers`](https://github.com/obra/superpowers). In particular:
- the project was bootstrapped by copying the adapted skills library from [`openrelay`](https://github.com/Krual-T/OpenRelay)
- [`openrelay`](https://github.com/Krual-T/OpenRelay) itself contains work derived from and inspired by `superpowers`
- the Codex install flow in `.codex/INSTALL.md` intentionally follows the same "Fetch and follow instructions from ..." pattern popularized by `superpowers`

OpenHarness is therefore not presented as an original invention of the entire workflow. It is an adaptation, narrowing, and restructuring of upstream ideas into a repository-centered harness model.

Please preserve attribution when redistributing substantial portions of this repository.

## License

MIT. See `LICENSE`.

This repository includes attribution to the upstream MIT-licensed work from `obra/superpowers`.

## Recommended next step

After installing, open a real repo and give Codex a task that normally goes off the rails. Then compare the difference between:
- a repo with scattered context and no harness
- a repo with a map, design packages, verification gates, and reusable skills

That comparison is the product.
