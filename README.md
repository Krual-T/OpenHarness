# OpenHarness

**OpenHarness is an agent-first, plug-and-play repository scaffold for Codex.**

It is built around a simple belief: the bottleneck is no longer typing code. The bottleneck is giving coding agents a repository they can actually reason about.

OpenHarness packages the workflow patterns, skills, and repository structure we found most useful when adapting agent-driven development inside [`openrelay`](https://github.com/Krual-T/OpenRelay). It directly reuses and adapts code and skill content from [`obra/superpowers`](https://github.com/obra/superpowers), and it is also conceptually aligned with OpenAI's article on [harness engineering](https://openai.com/index/harness-engineering/).

OpenHarness is intentionally Python-first. For Python-first repositories, `uv run pytest` is the default minimum automated verification floor, while stronger project-specific runtime verification still needs to be defined in task packages.

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
- each task has a structured task package
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

### 2. Task packages instead of vague task memory

Every meaningful task lives in `docs/task-packages/<task>/` as a package with stable files for:
- requirements
- exploration-backed overview design
- overview design
- detailed design
- verification
- evidence
- machine-readable status

That gives both humans and agents a shared source of truth that can be reviewed, diffed, validated, and archived.

### 3. Skills that enforce process, not just style

OpenHarness includes a copied and adapted skills library under `skills/`, including workflows for:
- brainstorming before implementation
- systematic debugging
- TDD-oriented execution
- verification before claiming success
- code review loops
- project memory capture

These skills are meant to shape how work gets done, not merely how answers are phrased.

The live skill model separates two questions:
- protocol status: is this part of the fixed harness or an optional helper?
- workflow stage: when should the agent actually use it?

That keeps the harness plug-and-play instead of forcing every repository to rediscover which skills are mandatory, optional, or only conditionally triggered.

### 4. A bias toward agent legibility

OpenHarness assumes a practical truth of agentic software work:

**If the agent cannot discover it from the repository, it effectively does not exist.**

That means key decisions should move out of chat threads and into versioned artifacts. The repo becomes the working memory, not just the code container.

### 5. A runtime capability contract instead of a fake universal debug skill

OpenHarness does not assume one generic runtime-debug skill can cover API, browser, worker, migration, and observability work equally well.

Instead, it defines a runtime capability contract:
- the core harness decides when runtime-aware routing applies
- repositories should keep a runtime surface map and can expose multiple narrow runtime helper skills for different runtime surfaces
- if a task needs a mapped runtime surface but no reusable helper yet, the agent should add one new narrow helper instead of stretching one generic debug skill
- if a task needs a surface the repository has not declared yet, the agent should open a bootstrap task package before claiming runtime verification coverage

## The OpenHarness workflow

A typical task looks like this:

1. `AGENTS.md` routes the agent into the correct workflow.
2. `using-openharness` checks the manifest and active task packages.
3. `brainstorming` converges the requirements first.
4. `exploring-solution-space` explores the local repo and the web before architecture is locked in.
5. The agent drafts overview design, then runs a reflection pass and can use bounded subagent discussion before treating architecture as ready.
6. The agent drafts detailed testing-first design, then runs a second reflection pass and can use bounded subagent discussion before implementation.
7. The agent implements against the package contract.
8. Runtime verification, verification, and evidence are written back into the package.
9. Completed packages are archived without losing history.

The result is a repo that accumulates usable knowledge instead of accumulating invisible assumptions.

## Verification baseline

OpenHarness does not pretend every repository already has the same runtime harness.

For Python-first repositories, `uv run pytest` is the default minimum automated verification floor.
That floor is intentionally weaker than full runtime or integration evidence.
When a task depends on project-specific runtime behavior, project-specific runtime verification must be designed and recorded in the task package rather than guessed globally.
When repositories mature beyond that minimum, the runtime capability contract is what tells the agent whether to reuse an existing helper, add one new narrow helper, or open a bootstrap task package first.

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
docs/task-packages/<task>/               # active task packages
docs/archived/task-packages/<task>/      # archived task packages
.project-memory/                   # reusable validated project knowledge
```

## Who this is for

OpenHarness is a good fit if you want to:
- run Codex against real repositories, not toy demos
- keep architecture and workflow decisions in version control
- make agent output more consistent without writing giant prompts
- scale multi-step work through task packages and verification loops
- build a repo that gets more legible as it grows

It is probably not a fit if you want a minimal one-file setup with no process overhead.

## Upstream attribution

OpenHarness is a derivative work.

This repository directly reuses and adapts code from [`obra/superpowers`](https://github.com/obra/superpowers). In particular:
- the project was bootstrapped by copying the adapted skills library from [`openrelay`](https://github.com/Krual-T/OpenRelay), which itself includes code and skill content derived from `superpowers`
- the Codex install flow in `INSTALL.codex.md` intentionally follows the same "Fetch and follow instructions from ..." pattern popularized by `superpowers`

OpenHarness is therefore not presented as an original invention of the entire workflow. It is a derivative adaptation that reuses upstream code and restructures it into a repository-centered harness model.

Please preserve attribution when redistributing substantial portions of this repository.

## License

MIT. See `LICENSE`.

This repository includes attribution to the upstream MIT-licensed work from `obra/superpowers`.

## Recommended next step

After installing, open a real repo and give Codex a task that normally goes off the rails. Then compare the difference between:
- a repo with scattered context and no harness
- a repo with a map, task packages, verification gates, and reusable skills

That comparison is the product.
