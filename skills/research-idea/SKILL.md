---
name: research-idea
description: "Research the ways an idea could be built before planning it: challenge the premise, generate different approaches, research and verify each against primary sources, present them as a visual HTML report with a recommendation, then grill the approach the user picks and record the decision for /plan or /idea-to-pr. Use for /research-idea or 'research ways to do X'."
disable-model-invocation: true
---

# Research Idea

The user has an idea and wants to know the ways to achieve it before committing to one. Produce a researched set of approaches, a recommendation the user can attack, and, once they pick, a recorded decision that `/plan` or `/idea-to-pr` builds from.

The deliverable is the decision, not code. Never start implementing inside this skill, even when the pick looks obvious.

## Route first

| Situation | Where it goes |
|---|---|
| An idea with more than one plausible way to build it | this skill |
| A question of fact (does library X support Y, what does API Z return) | the **research** skill |
| The approach is already clear, the shape needs working out | the **plan** skill |
| The idea spans many sessions and the questions themselves are unclear | `/wayfinder` |
| How or why the existing code works | the **how** or **why** skill |

## Start

Open a todolist with one entry per phase below, plus a first entry to read the Principles section of the **axo-mode** skill. A phase you skip stays on the list with a one-line reason.

## Phase A: Frame

Restate the idea in one sentence. Then settle three things in one round of the **grilling** skill's format, each question numbered with your recommended answer:

- **Done when.** The outcome the idea is for, as something observable. "Users stop losing drafts when the tab closes" is checkable. "Better drafts" is not.
- **Requirements.** Split them into **hard gates** (an approach that fails one is out) and **preferences** (weighed against each other). They come from the repo and the user, never from what web research happens to find.
- **Premise.** Is this the right problem? What happens if we do nothing? What already solves part of it? An answer here can end the skill early, and that is a good outcome.

Facts are your job. Look up anything the repo or a quick search can answer before asking, and ask only what the user decides. Wait for answers before Phase C.

## Phase B: Ground

Run in parallel with Phase A's questions, as subagents per axo-mode's [Subagents](../axo-mode/SKILL.md#subagents) section.

- When the idea touches this repo, run the **how** skill over the area it touches. Read `GLOSSARY.md` and the ADRs under `docs/adr/` for that area. An approach that contradicts an ADR is allowed only with a reason to reopen it.
- Walk the reuse ladder and record what exists at each rung: a helper already in the repo, the standard library, a platform feature, an installed dependency (read the lockfile), a maintained library or managed service. The cheapest rung that meets the hard gates is a candidate whether or not anyone proposes it.

## Phase C: Diverge

Size the run to the idea before spawning anything:

| Size | Signal | Generators | Researchers |
|---|---|---|---|
| Small | One module, a local choice | none, list the candidates yourself | one per finalist |
| Medium | A feature, a new dependency, or a service choice | Minimal, Ideal, Adopt | one per finalist |
| Large | Crosses subsystems or changes how the product works | all four lenses | one per finalist |

Spawn the generators in one message, each with the prompt in [references/generator-prompt.md](references/generator-prompt.md) and one lens:

- **Minimal.** The smallest change that meets the hard gates with what the repo and its installed dependencies already provide.
- **Ideal.** As if the requirement had been there from day one, per [end-state](../axo-mode/principles/end-state.md). Name the migration cost but don't let it veto the design.
- **Adopt.** A library, managed service, or platform feature does most of the work, and repo code becomes glue.
- **Lateral.** Remove the need, invert the problem, or drop one preference and see what opens.

Use `subagent_type: "general-purpose"` and `model: "opus"`. The prompt keeps them read-only.

Then converge:

1. Add **Keep what we have** as the baseline. It is exempt from screening and gets no researcher or card. Its comparison row comes from Phase B. It stays even when nobody would pick it, because every other approach has to beat it.
2. Collapse variants. Two candidates with the same mechanism are one candidate, per the **architect** skill's design-it-twice rule: a second flavor of the first shape does not count.
3. Drop any candidate without a basis: a `direct:` repo fact, an `external:` named prior art, or a `reasoned:` written argument.
4. Screen the rest against the hard gates. Keep 3 to 5 finalists and one line on why each cut lost.

If the finalists are all one mechanism, the framing was too narrow. Return to Phase A with what that shows rather than researching three copies of one idea.

## Phase D: Research

Spawn the researchers in one message, each with the prompt in [references/researcher-prompt.md](references/researcher-prompt.md), one finalist with its basis (from its generator, or the one you recorded when you listed it yourself), and the contents of the **research** skill's [SOURCES.md](../research/SOURCES.md) pasted in. That file lives in the research skill's directory, `../research/` relative to this skill's directory. Resolve the absolute path and confirm it exists before spawning. Use `subagent_type: "general-purpose"` and `model: "sonnet"`.

You do not research yourself while they run. Read their notes when they return. At most one gap round: respawn a researcher only for a gap that could change the ranking, then move on.

## Phase E: Verify

Rank the finalists from the notes. Then, in parallel:

- **Verifier.** A fresh subagent gets the claims the ranking rests on, with their cited sources, and the prompt in [references/verifier-prompt.md](references/verifier-prompt.md). Use `model: "sonnet"`.
- **Skeptic.** A fresh subagent gets only the idea, its done-when line, the requirements, the recommended approach in one sentence, and the other approaches' names, with the prompt in [references/skeptic-prompt.md](references/skeptic-prompt.md). It never sees the supporting evidence. Run it on a different model from this session's, so it does not share your reasoning.

Apply the results:

- An overturned claim comes out of the report, and the ranking is redone without it. If that changes the pick, verify the new pick's claims and rerun the skeptic on it, once.
- A disputed or unverified claim stays in the report with its status pill. It cannot carry the recommendation on its own.
- The recommendation needs two floors: a verified repo fact (or a stated reason the repo is irrelevant) and at least one verified external source. Missing either, its badge is **Hold** and the report says what evidence would settle it. A confident verdict on thin evidence is the failure this skill exists to prevent.
- The skeptic's strongest argument goes into the report next to the recommendation, whether or not it changed your mind.

## Phase F: Report

Write the self-contained HTML report described in [HTML-REPORT.md](HTML-REPORT.md) to the OS temp directory, so nothing lands in the repo yet. Resolve it from `$TMPDIR`, falling back to `/tmp` (`%TEMP%` on Windows), as `<tmpdir>/research-idea-<slug>-<timestamp>.html`. Open it (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and give the user the absolute path.

The approaches appear before the recommendation, so the reader forms a view before seeing yours. Use the `GLOSSARY.md` vocabulary for anything in the domain.

Then ask: "Which would you like to explore?" Stop until the user answers. Picking is the user's decision, including picking against the recommendation.

## Phase G: Grill the pick

Once the user picks, run the **grilling** skill over the chosen approach, plus the **domain-modeling** skill when the repo has domain docs. Grill only the decisions that change what gets planned: scope edges, the gates the approach only partly passed, the risks the skeptic raised, and anything that decides the slicing.

- A question whose answer is observable (behavior, timing, output, how a library reacts) goes to the **prototype** skill, not to the user.
- A fact the grilling needs goes to a subagent given SOURCES.md, and its findings go into the record's Evidence section rather than a separate note.
- A new domain term goes into `GLOSSARY.md` as it settles.

## Phase H: Record and hand off

Write the decision record where `docs/agents/artifacts.md` says research notes go. No such file → `docs/research/<slug>.md`, and tell the user they can settle the convention with `/setup-axostack`. Re-entering the same idea updates the existing file.

```markdown
---
status: chosen  # chosen | superseded
date: <YYYY-MM-DD>
superseded-by:  # path to the record or plan that replaced this one
---

# <Idea, in the domain's words>

## Idea

<one sentence>. Done when <observable outcome>.

## Requirements

Hard gates:
- <gate>

Preferences, in order:
- <preference>

## Decision

<The chosen approach and its mechanism in two or three sentences. Who picked it, and whether it was the recommendation.>

## Approaches considered

| Approach | Origin | Effort | Verdict | Why not |
|---|---|---|---|---|
| <chosen> | reuse / extend / adopt / build | S-XL | chosen | |
| <runner-up> | | | runner-up | <and the condition under which it would win> |
| Keep what we have | | | baseline | |

## Evidence

<The cited findings the decision rests on, each with source, date, and verification status. Inferences marked as such.>

## Risks

<The skeptic's strongest argument and the cheapest way to reverse the decision.>

## Open questions

<Numbered, each with a recommended answer, in the grilling skill's format, for /plan to pick up.>
```

Run the **technical-writing** and **unslop** skills over the record before it lands.

When the user rejected a candidate for a reason a future reader would need (a constraint, not "not now"), offer an ADR through the **domain-modeling** skill so the next exploration does not propose it again.

**Reply:** the record's path, the chosen approach, the runner-up and when it wins, what stayed unverified, and the next step: `/plan <path>` when the change needs shaping and slicing, or `/idea-to-pr <path>` when it is small enough to go straight to a PR.
