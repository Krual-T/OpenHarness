---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# Brainstorming Ideas Into Designs

## Skill Role

- Protocol status: core protocol skill
- Primary stage: requirements convergence
- Trigger: use when the task needs requirement clarity, scope convergence, or explicit design before execution

In this repository, `brainstorming` is a child skill of `using-openharness`.
It does not define task roots, stage flow, or archive rules. Its job is narrower: turn an under-specified task into requirements that are explicit enough to write into the active task package and hand off to exploration.

<HARD-GATE>
Do NOT invoke implementation work until the requirements are explicit enough to be written into the package and survive challenge. User approval is required only when the user explicitly asks for a review gate or when unresolved ambiguity makes autonomous continuation risky.
</HARD-GATE>

continue automatically by default once the requirements are concrete enough to keep moving safely.
Only stop for user review if one of these is true:
- the user explicitly asked for a review checkpoint
- a high-impact ambiguity remains and autonomous continuation would be risky
- repository evidence is missing badly enough that the requirements would be guesswork

do not create unnecessary approval pauses.

## Checklist

1. Explore project context: check the active task package, related files, docs, and recent commits.
2. Offer the visual companion only if upcoming questions are genuinely visual.
3. Ask clarifying questions only when the repository and user request still leave a high-impact ambiguity.
4. Propose 2-3 viable approaches with trade-offs and a clear recommendation.
5. Write the converged requirements into `01-requirements.md`.
6. Self-check the result against the requirements gate defined in `using-openharness`.
7. Hand off to `exploring-solution-space` once the requirements are concrete enough to challenge.

Brainstorming ends when `01-requirements.md` is strong enough for exploration, not when the prose becomes longer.

## The Process

**Understanding the idea:**

- Read the current project state first.
- If the request actually contains multiple independent efforts, decompose it before refining details.
- Ask one question at a time only when it removes real risk.

**Exploring approaches:**

- Compare at least one viable alternative to the recommended direction.
- Explain why the recommended path fits the current repository and task boundary better than the alternatives.

**Challenging the requirements:**

- Use the product perspective to challenge target user, core scenario, success definition, and non-goals.
- Use the CEO perspective to challenge timing, cost cap, strategic fit, and worst acceptable downside.
- Record substantive challenge closure in the task package instead of leaving it only in chat.

**Requirements gate before leaving brainstorming:**

- The repository-level requirements gate lives in `using-openharness`.
- The requirements gate must include target user, core scenario, single success metric, non-goals, cost cap, acceptance criteria, and at least one counterexample.
- If target user, core scenario, success metric, non-goals, effort boundary, acceptance criteria, or counterexample are still missing, keep converging requirements instead of pretending exploration will fix it later.

## After Brainstorming

- Write the validated requirements into the active task package under `docs/task-packages/<task>/`.
- Update `02-overview-design.md` or `03-detailed-design.md` only when the requirement discussion already proved a design constraint that belongs there.
- Continue into `exploring-solution-space` by default unless the user explicitly asked for a review checkpoint or the remaining ambiguity is too risky to carry forward.
- If no package exists yet, do not scaffold one at the first vague idea.
- When brainstorming is complete and you are about to enter exploration, scaffold the task package before invoking `exploring-solution-space`.

## Key Principles

- One question at a time.
- Requirements should be executable, not decorative.
- Keep YAGNI pressure on the scope.
- Do not skip alternatives just because one path feels obvious.
- Do not bypass the repository stage gate defined by `using-openharness`.

## Visual Companion

A browser-based companion for mockups, diagrams, and side-by-side visual comparisons. Offer it only when upcoming questions are genuinely easier to answer visually than in text.

**Offering the companion:** When visual treatment would materially help, send this message by itself:
> "Some of what we're working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? (Requires opening a local URL)"

If the user accepts, read `references/visual-companion.md` before using it.
