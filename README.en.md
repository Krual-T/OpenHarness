<p align="center">
  <img src="https://img.shields.io/github/license/Krual-T/OpenHarness?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Python-3.14+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/uv-package_manager-8A2BE2?style=flat-square" alt="uv">
</p>

<h1 align="center">OpenHarness</h1>

<p align="center">
  <strong>Not a tool for giving orders to AI agents.<br>An engineering framework for human-machine symbiotic collaboration.</strong>
</p>

<p align="center">
  The bottleneck has never been code generation speed.<br>
  The bottleneck is: <strong>do the human and the agent share a collaboration protocol that enables equal participation, joint decision-making, and traceable verification?</strong>
</p>

<p align="center">
  <a href="#design-philosophy">Philosophy</a> ·
  <a href="#core-model">Core Model</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#design-principles">Principles</a> ·
  <a href="#the-feedback-loop">Feedback Loop</a> ·
  <a href="#command-reference">Commands</a>
</p>

---

## Design Philosophy

OpenHarness is neither a prompt collection nor a skills bundle. What sits underneath is a set of **engineering design principles** that together form the cybernetic skeleton of agent collaboration.

### Man-Computer Symbiosis: A Collaboration System, Not a Command Executor

In 1960, J.C.R. Licklider published "Man-Computer Symbiosis," opening with:

> The hope is that, in not too many years, human brains and computing machines will be coupled together very tightly, and that the resulting partnership will think as no human brain has ever thought and process data in a way not approached by the information-handling machines we know today.

Licklider was not describing a master-servant model of "input command → receive output." He was describing a **peer collaboration system** — human and machine each doing what they do best, advancing together within a shared workspace.

Sixty years later, AI coding agents arrived. Yet most people still use them in **command-execute mode**:

```
Human: Implement a user login feature for me
Agent: Here's the code
Human: No, add two-factor authentication
Agent: Done, updated
Human: Still wrong, shouldn't use JWT, switch to sessions
...
```

This is not collaboration. This is **using natural language as a command line**.

OpenHarness's first design principle is: **the agent is not a tool — it is a collaborator**. This means the entire system must be designed not around "how to make the agent obey," but around "how to make human and agent an effective joint cognitive system."

This shift requires answering four questions:

| Question | Command-Execute Mode | OpenHarness Collaboration Mode |
|----------|---------------------|-------------------------------|
| Who knows "what to build"? | Only the human, who must describe complete requirements | Human and agent converge on requirements together; the task package is a shared cognitive artifact |
| Who judges "is it correct"? | Human eyes on every output | Three-tier verification spectrum: automated tests (unit_test), semantic review (qualitative), runtime observation (rwp) — the verification method matches the task nature; all evidence is recorded in the task package |
| Where does work state live? | Chat history, scattered, unqueryable | Task packages, versioned, `git diff`-able, auditable |
| What does the agent learn? | Zero accumulation; every session starts from scratch | Archived task packages become the project's structured memory, feeding future tasks |

OpenHarness does not make the agent "more obedient." It makes the agent a **bidirectionally accountable collaborator**: the human must articulate acceptance criteria explicit enough to verify; the agent must produce verifiable, traceable evidence. Both parties' contributions are recorded in the same documents, equally visible.

This vision directly inherits from three academic traditions:

- **Man-Computer Symbiosis** (Licklider, 1960) — tight coupling of human and computer, not substitution but augmentation
- **Augmenting Human Intellect** (Engelbart, 1962) — the goal of computing is to amplify human cognitive capability
- **Joint Cognitive Systems** (Woods & Hollnagel, 2006) — human and machine should be viewed as a single cognitive unit, each with distinct strengths

What OpenHarness does, at its core, is translate these half-century-old academic insights into an **engineering-practical protocol**. The task package is the shared workspace. Stage gates are the collaboration handoff points. Evidence records are the bidirectional audit trail. `AGENTS.md` is the collaboration interface specification between human and agent.

### Engineering Cybernetics: Turning Feedback Principles into Engineering Practice

In 1948, Norbert Wiener laid the theoretical foundation in *Cybernetics*: **systems self-correct through feedback loops**. But the leap from mathematical theory to actionable engineering discipline came in 1954, when Qian Xuesen published *Engineering Cybernetics* — answering the question: "how do you actually design feedback, gates, and self-correcting mechanisms into real systems?"

Translate this engineering approach to the AI coding domain:

```
Agent without feedback = Open-loop system
Prompt → Output → Human judges correctness → Re-prompt → Re-output → ...

Agent with feedback = Closed-loop system
Propose → Design → Implement → Verify as designed → Record evidence → Stage gate → Advance or Retreat
```

What OpenHarness does, at its core, is Qian-style engineering: **translating the feedback principle into checkable gates between every stage**. No gate pass, no forward progress. Correctness enforced not by gut feeling, but by pre-designed, evidence-backed verification.

### Progressive Disclosure: Don't Pay for Information You Don't Need Yet

A well-known HCI principle from Jakob Nielsen: **information should be pulled at the moment of need, not pushed at the entry point**.

OpenHarness structures this as three tiers:

| Tier | Content | Trigger |
|------|---------|---------|
| Entry | `AGENTS.md` — repository map | Session start, once |
| Task | Task package details + current stage skill | Entering a specific task |
| Execution | RWP runtime workflow | Only when runtime verification is needed |

The agent never loads the entire knowledge base at once. It sees only the context relevant to the current stage. This controls both token cost and cognitive load.

### Information Entropy Reduction: From Chaos to Structure

Claude Shannon taught us: **the higher the uncertainty, the higher the entropy**.

Entropy sources in AI coding:

- Requirements buried in chat history → high entropy, unqueryable
- Design decisions in people's heads → high entropy, invisible to the agent
- Verification results in terminal scrollback → high entropy, untraceable

OpenHarness performs **entropy reduction engineering**:

```
Chat history (high entropy)       →  Requirements doc (low entropy, structured)
Mental decisions (high entropy)   →  Design doc (low entropy, reviewable)
Terminal output (high entropy)    →  Evidence record (low entropy, traceable)
```

Every stage transition is an **entropy reduction operation**: converging scattered information into a versioned, queryable, verifiable artifact.

### Constraints as Liberation: Structure Reduces Decision Cost

Barry Schwartz's *Paradox of Choice* demonstrated: **more options lead to worse decisions**.

Give an agent total freedom, and it reinvents the workflow at every turn. OpenHarness takes the opposite approach:

- Each stage has explicit entry and exit conditions
- Each gate has explicit pass criteria
- Each artifact has explicit template boundaries

These constraints eliminate the "what do I do next?" decision cost. The agent doesn't need to re-think process at every step — it just does the best work possible within the current stage's boundaries.

---

## Core Model

```
                        ┌──────────────────────┐
                        │     AGENTS.md         │
                        │    Repository Map     │
                        │ (Entry tier, progressive│
                        │     disclosure)        │
                        └──────────┬───────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
     │  Task Package   │  │  Skills Library │  │  RWP Runtime   │
     │                 │  │                 │  │  Workflows     │
     │  Requirements   │  │  Process shape  │  │                │
     │  Overview Design│  │  Stage guidance │  │  Discover on   │
     │  Detailed Design│  │  Role injection │  │  demand        │
     │  Verification   │  │                 │  │  Load on demand│
     │  Evidence        │  │                 │  │  Run on demand │
     └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │         Stage Gates (Feedback Loop)   │
              │                                      │
              │  proposing ──→ overview_designing    │
              │      │              │                │
              │      ▼              ▼                │
              │  requirements_  overview_            │
              │  designed       designed             │
              │                                   │
              │  detailed_designing ──→ implementing │
              │      │                    │          │
              │      ▼                    ▼          │
              │  detailed_           implemented     │
              │  designed                            │
              │                                   │
              │  verification_ ──→ verifying         │
              │  designing           │               │
              │      │               ▼               │
              │      ▼          verified ──→ archived│
              │  verification_                       │
              │  designed                            │
              └──────────────────────────────────────┘
```

This is a **self-correcting system**. Each gate performs a feedback check: does the output match the requirements from the previous stage? If not, retreat and fix. If yes, advance.

---

## Quick Start

**Prerequisites**: [Git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/).

**Linux / macOS:**

```bash
curl -fsSL https://raw.githubusercontent.com/Krual-T/OpenHarness/refs/heads/main/install.sh | bash
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Krual-T/OpenHarness/refs/heads/main/install.ps1" | Invoke-Expression
```

Initialize your project:

```bash
openharness init --agent all
```

Directories, skill symlinks, and session hooks are all set up automatically. See [INSTALL.md](INSTALL.md) for details.

---

## Design Principles

Every module in OpenHarness maps to an explicit design principle. Nothing is accidental.

### 1. Single Source of Truth → Task Packages

**Principle**: Every piece of work has exactly one authoritative source.

A task package under `docs/task-packages/<task>/` is a fixed structure:

```
task/
├── task-info.yaml        ← State machine (machine-readable)
├── requirements.md        ← Problem + goals + constraints
├── overview-design.md     ← Architectural decisions
├── detailed-design.md     ← Implementation path + test plan
├── verification-design.md ← How to prove completion
└── evidence.md            ← Actual execution results
```

Humans and agents share the same set of files. They are `git diff`-able, reviewable, archivable, and auditable.

### 2. Separation of Concerns → Stage Gates

**Principle**: Different kinds of work should not be mixed in the same step.

OpenHarness splits the task lifecycle into 6 stages, each focused on one concern:

| Stage | Focus | Artifact |
|-------|-------|----------|
| `proposing` | What problem to solve | Requirements |
| `overview_designing` | Is the architecture correct | Overview design |
| `detailed_designing` | Is the implementation viable | Detailed design |
| `verification_designing` | How to prove completion | Verification plan |
| `implementing` | Writing code | Code changes |
| `verifying` | Does it meet acceptance criteria | Evidence |

Each stage has independent **completion criteria**. No transition without passing. This prevents the "design-while-implementing-while-verifying" pattern — the single most reliable source of hidden defects.

### 3. Progressive Disclosure → RWP Runtime Workflows

**Principle**: Don't load information you don't need yet.

Not all debugging is alike. API debugging needs HTTP clients and mock services. Frontend debugging needs headless browsers. Data migrations need database snapshots. Each demands a different runtime environment.

RWP follows a three-tier progressive disclosure:

```bash
# Tier 1: Summaries only — near-zero token cost
openharness rwp list

# Tier 2: Load details only after selecting a candidate
openharness rwp view <workflow>

# Tier 3: Execute only after confirming the plan
openharness rwp run <workflow> <script.py>
```

The agent never loads every workflow specification into context at once. It pulls on demand.

### 4. Undiscoverable = Nonexistent → Agent Legibility

**Principle**: If the agent can't read it from the repository, it doesn't exist.

This principle is harsh but true: information invisible to the agent is functionally absent. This means:

- Key decisions **must move from chat threads to versioned documents**
- Directory structure **must be intuitively navigable by an agent**
- Naming **must follow predictable conventions**, not rely on human background knowledge

`AGENTS.md` is not a README for humans. It is the **agent's entry router**. It answers: what lives where, which workflow to follow, what to write back when done.

### 5. Constraints Reduce Decision Cost → Skills Library

**Principle**: Don't give the agent more options. Give it fewer, clearer choices.

The `skills/` directory doesn't teach the agent "how to code" — it already knows how. Skills teach: "at this stage, what should you focus on, what must you produce, and what must you not do."

Each stage skill has explicit boundaries:
- Entry conditions (when to enter this stage)
- Output criteria (what must be delivered before exiting)
- Forbidden actions (what to avoid at this stage)
- Exit conditions (prerequisites for the next stage)

This eliminates "what next?" decision fatigue at every node.

---

## The Feedback Loop

Combine all the principles, and what emerges is a **feedback loop in the cybernetic sense**:

```text
Requirements → Overview Design → Detailed Design → Implementation → Verification
     │                                                            │
     │              ←── Evidence-driven correction ←─────────────┘
     │
     └──→ Archive (knowledge accumulation, feeds future tasks)
```

- **Forward**: each stage uses only the previous stage's artifact as input
- **Backward**: verification matches evidence against requirements; mismatch triggers retreat
- **Accumulate**: archived task packages become the project's structured memory; new tasks can query historical decisions

This is not a linear waterfall. It is a **closed loop with feedback**. Verification failure triggers correction, not silent pass-through.

---

## Command Reference

| Command | Cybernetic Semantics |
|---------|---------------------|
| `openharness task-package new <name>` | Create a new feedback loop |
| `openharness task-package list` | List all active loops |
| `openharness task-package view <task>` | Inspect a loop's current state |
| `openharness task-package transition <task> <state>` | Gate check and advance |
| `openharness rwp list` | Progressive disclosure: tier 1 |
| `openharness rwp view <workflow>` | Progressive disclosure: tier 2 |
| `openharness rwp run <workflow> <script>` | Execute runtime verification |
| `openharness init --agent <claude\|codex\|all>` | Deploy the cybernetic skeleton |
| `openharness update` | Update to latest |

---

## Project Structure

```text
AGENTS.md                           # Agent entry router
skills/using-openharness/
  ├── SKILL.md                      # Session entry: decide if task package is needed
  ├── states/                       # Stage skills (loaded by state)
  │   ├── proposing/                 # Requirements convergence
  │   ├── exploring-solution-space/ # Solution exploration
  │   ├── detailed-design/          # Detailed design
  │   ├── implementing/             # Implementation
  │   ├── verification-designing/   # Verification planning
  │   └── verifying/                # Verification execution
  └── references/                   # Templates & protocol docs
docs/
  ├── task-packages/<task>/         # Active task packages
  └── archived/task-packages/       # Archived (structured memory)
openharness_cli/                    # CLI tooling
tests/                              # Tests
install.sh / install.ps1            # Cross-platform install scripts
```

---

## Intellectual Origins

OpenHarness draws from several intellectual traditions:

- **Man-Computer Symbiosis** (J.C.R. Licklider, 1960) — tight coupling of human and computer as collaborative partners
- **Augmenting Human Intellect** (Douglas Engelbart, 1962) — computing that amplifies rather than replaces human cognition
- **Joint Cognitive Systems** (David Woods & Erik Hollnagel, 2006) — human and machine as a unified cognitive unit
- **Cybernetics** (Norbert Wiener, 1948) — theoretical foundation of feedback and self-correcting systems
- **Engineering Cybernetics** (Qian Xuesen, 1954) — translating cybernetic theory into engineering discipline
- **Progressive Disclosure** (Jakob Nielsen, 1995) — information revealed on demand
- **Information Theory** (Claude Shannon, 1948) — entropy reduction as structured engineering
- **OpenAI Harness Engineering** (2025) — attention economics in the age of agents

In code, OpenHarness is a derivative work that reuses and adapts source from [`obra/superpowers`](https://github.com/obra/superpowers). The skills library was incubated through [`openrelay`](https://github.com/Krual-T/OpenRelay).

Please preserve upstream attribution when redistributing substantial portions of this repository.

---

## License

[MIT](LICENSE), with upstream MIT attribution for `obra/superpowers`.

---

<p align="center">
  <strong>An agent is not a servant to command.<br>Give it a map, a feedback loop, a peer-collaboration protocol.<br>Then, work together.</strong>
</p>
