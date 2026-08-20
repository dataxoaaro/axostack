# axostack

Agentic development stack for Claude Code: an entry-point router, a Linear-first workflow pipeline, and a set of engineering principles, packaged as one skills library.

## Architecture

Three layers, and one split inside the middle layer that explains most of the library.

1. **axo-mode** routes. Its trigger table maps a situation to a skill, its principles index points at the 21 leaf principles, and its playbooks are step lists the agent copies into its todo list verbatim.

2. **Skills** do the work, on two axes that do not compete. A **playbook** is the sequence for a kind of work: feature, bug fix, refactoring, investigation, prototype, committing. A **phase verb** is the depth on one part of any of them. `plan` writes the change down, `implement` builds it, and `code-review` checks it. A playbook names the verb and stops. The verb owns what happens inside. That is why the feature playbook is six steps instead of a second description of the build loop.

   The rest serve those two. Alignment is `grilling`. Design is `architect` and `codebase-design`. Investigation is `how`, `why`, and `research`. The tracker pipeline is `to-linear-issue`, `triage`, `to-tickets`, and `work-linear-issue`. Prose gates are `unslop`, `no-comments`, and `technical-writing`.

3. **Principles** carry the judgment. 21 `principle-*` leaf skills, each loaded only when it applies and cited with the decision it changed.

## Skills

Invoke: **slash** means you type it (`/skill-name`) and the agent cannot start it on its own, **auto** means the agent may also reach for it when the task fits. The difference is the `disable-model-invocation` flag in each skill's frontmatter, so a skill another skill has to call mid-workflow must be **auto**.

### Router and setup

| Skill | Invoke | What it does |
|-------|--------|--------------|
| axo-mode | auto | The entry point. Routes situations to skills, indexes the principles, and holds the playbooks (feature, bug-fix, investigation, refactoring, prototype, committing) copied verbatim into the todo list. |
| setup-axostack | slash | Once per repo: configures the issue tracker (Linear first-class), triage labels, domain doc locations, and where plans and research notes land. |

### Linear workflow

| Skill | Invoke | What it does |
|-------|--------|--------------|
| to-linear-issue | slash | Research a question, idea, or problem and publish it as one evidenced Linear issue with approach and acceptance criteria. |
| work-linear-issue | slash | Claim a ready issue by key (or take the next unblocked `ready-for-agent` one), branch with the key prefix, build under axo-mode's playbooks, close out with commits and a tracker update. |
| to-tickets | auto | Break an agreed plan into tracer-bullet tickets with blocking edges, published in dependency order. |
| triage | slash | Move incoming issues through triage roles: categorise, verify, grill if needed, write agent-ready briefs. |
| wayfinder | slash | Plan work too large for one session as a shared map of decision tickets, resolved one at a time until the path is clear. |

### Align and design

| Skill | Invoke | What it does |
|-------|--------|--------------|
| grilling | auto | The interview primitive: question the user until every branch of the design tree is resolved. Backs the two skills below plus triage and wayfinder. |
| grill-me | slash | A grilling session for any plan or design. Also the resolution path for contested designs. |
| grill-with-docs | slash | grill-me plus docs: sharpens terminology and updates CONTEXT.md and ADRs as it goes. |
| architect | auto | Sketch types, signatures, and module structure through parallel design exploration before code, for a specific change. |
| codebase-design | auto | The deep-module vocabulary: a lot of behavior behind a small interface, at a clean seam, testable through it. Used by architect and improve-codebase-architecture. |
| improve-codebase-architecture | slash | Survey a whole codebase for deepening opportunities, report them, grill through the one you pick. |
| plan | auto | Work a feature or fix into one plan document: grounded, risk-graded, sliced into tickets, with every unsettled question numbered for the next grilling session. |
| prototype | auto | A throwaway sketch that answers a design question by observation instead of asking. |

### Build and verify

| Skill | Invoke | What it does |
|-------|--------|--------------|
| implement | auto | Build the work a spec or tickets describe, driving tdd at the agreed seams and closing with code-review. |
| tdd | auto | Red-green-refactor, one vertical slice at a time. The default build loop for behavior changes. |
| code-review | auto | Two-axis review of the diff since a fixed point: repo standards and spec fidelity, run as parallel subagents. |
| diagnosing-bugs | auto | Gated diagnosis loop for hard bugs: feedback loop that goes red on the bug, minimise, hypothesise, instrument, fix, regression-test. |
| blast-radius | auto | Find what a change could break beyond the diff, and prove the one safety-critical fact by running real code. |
| no-comments | auto | Strip narrating and workaround comments via the comment-sicko agent, then fix what the deletions expose. |
| create-verification-skill | slash | Generate a project-local `verify-<app>` skill that drives the real app the way a user does and captures evidence. |
| maintain-verification-skill | slash | Periodic audit that keeps the project's verify skill and feature map honest against the source. |

### Investigate

| Skill | Invoke | What it does |
|-------|--------|--------------|
| how | auto | How a subsystem works: architecture walkthroughs, runtime flow, placement and layering questions, with critic subagents. |
| why | auto | Why it is this way: design rationale and regression history mined from source control, tracker, docs, and observability in parallel. |
| research | auto | Investigate an external question against primary sources and land a cited Markdown file in the repo. |

### Parallelism and long runs

| Skill | Invoke | What it does |
|-------|--------|--------------|
| swarm | auto | Fan out N parallel workers over a partition of the work, drain them, return one report. |
| arena | auto | N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. |
| figure-it-out | slash | Design a bespoke, auditable playbook when no bundled one fits a large or multi-part task. |
| show-me-your-work | auto | A reviewable decision trail (one row per decision: what, why, evidence, result) for long or unattended runs. |
| recall | auto | Reconstruct working context from your own transcripts and live state when resuming ("where did I leave off"). |
| reflect | slash | Three parallel reviewers over the session transcript, synthesized into approved edits on existing skills. The improvement loop. |

### Docs and prose

| Skill | Invoke | What it does |
|-------|--------|--------------|
| unslop | auto | Cut AI tells from any writing. Applies to every prose surface, including replies. |
| technical-writing | auto | The layered docs standard (Diátaxis, Google style, STE, Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |
| domain-modeling | auto | Build and sharpen the project's domain model: glossary terms, CONTEXT.md, ADRs. |
| bro | slash | Restate the last message in plain human language, no jargon. |

### Agents

| Agent | What it does |
|-------|--------------|
| axo-agent | Code-writing delegate that reads axo-mode in full before working, so subagents carry the same discipline. |
| comment-sicko | Read-only comment-hunting reviewer spawned by no-comments. |

### Principles

21 leaf skills, indexed in axo-mode, each read in full only when applied. Grouped: **core** (laziness-protocol, foundational-thinking, redesign-from-first-principles, subtract-before-you-add, minimize-reader-load, outcome-oriented-execution, experience-first, exhaust-the-design-space, build-the-lever), **architecture** (model-the-domain, boundary-discipline, type-system-discipline, make-operations-idempotent, migrate-callers-then-delete-legacy-apis, separate-before-serializing-shared-state), **verification** (prove-it-works, fix-root-causes, sequence-verifiable-units), **delegation** (guard-the-context-window, never-block-on-the-human), **meta** (encode-lessons-in-structure). Each `principle-*` folder's description states exactly when it applies.

Easily confused pairs: `domain-modeling` builds the project's vocabulary docs, while `principle-model-the-domain` structures code around the domain. `figure-it-out` designs a playbook for one session-sized task, while `wayfinder` maps work spanning many sessions. `research` reads external sources, while `how` and `why` read your own codebase and history. `plan` writes down a change you can already state, `wayfinder` maps one you can't yet, and `architect` designs the types inside a plan rather than replacing it.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add dataxoaaro/axostack
/plugin install axostack
```

Any agent, as editable files via [skills.sh](https://skills.sh):

```
npx skills@latest add dataxoaaro/axostack
```

From a clone, with the sync script:

```
scripts/sync-skills.sh
```

It installs each skill directory separately and links any that is missing. Editing the checkout changes nothing until it runs. Copy the files in `agents/` into `~/.claude/agents/` yourself.

Do not sync by hand with a single `rsync --delete` over the install directory. That deletes every installed skill that does not come from this repo.

## Usage

Run `/setup-axostack` once per repo. It records the issue tracker (Linear, GitHub, GitLab, or local markdown), the triage labels, the domain doc locations, and where plans land. The tracker-facing skills read that configuration.

Then pick the entry point that matches what you have.

**An idea, not a plan.** `/to-linear-issue <idea>` researches it against the codebase and publishes one evidenced issue. Run `/triage` to move the queue when issues pile up.

**An agreed direction, not a design.** `/plan <feature>` writes `docs/plans/<NNNN>-slug.md`, grounded in the codebase, with alternatives recorded, assumptions graded on evidence, work sliced into tickets, and open questions numbered. Then `/grill-with-docs docs/plans/<NNNN>-slug.md` attacks each question and folds the answers back into the file.

**A plan.** `/to-tickets docs/plans/<NNNN>-slug.md` publishes the slices to your tracker in dependency order.

**A ticket.** `/work-linear-issue ABC-123` claims it, branches with the key prefix, builds under axo-mode's playbooks, and updates the tracker. Run it bare to take the next ready issue. Without a tracker, `/implement` builds straight from the plan.

Both paths meet at `/to-tickets`. What differs is where you start. An unshaped idea goes to the tracker first, and an agreed direction goes to a plan first.

Either invoke `/axo-mode` explicitly or let the agent reach for it on a multi-step task. Skills also work standalone. Reach for `/grill-me` to stress-test a design, `/tdd` for one feature slice, `/diagnosing-bugs` on a hard bug, `/code-review` before a commit, and `/bro` when a reply needs restating in plain language.

## A worked example

The plan flow above ran against a real defect in this repo and produced [docs/plans/0001-implement-skill-duplicates-the-feature-playbook.md](docs/plans/0001-implement-skill-duplicates-the-feature-playbook.md). Trimmed to the three sections that make a plan more than a design note:

```markdown
## Assumptions

| # | Assumption | Grade | Evidence |
|---|-----------|-------|----------|
| A1 | No file outside `skills/implement/` quotes its body | 4 | probe over 110 Markdown files: 0 quotes, 3 name references |
| A5 | The three playbook tails collapse into one verb | 3 | Partly false, found while building slice 2. See A6. |

## Slices

| # | Slice | Blocked by | Status | Delivers |
|---|-------|-----------|--------|----------|
| 1 | Write `implement` as the build-phase verb | none | landed bf87f10 | An agent following it commits on a branch, gated |
| 2 | Collapse the tail out of the three playbooks | 1 | landed 40065ab | The build sequence is stated once |

## Open decisions

Q1 - Delete `implement`, or reduce it to a three-line router?

Recommended: delete it. The routing entry already names the real sequence.
```

Every assumption carries a grade from `blast-radius`: 1 means you said so, 4 means you ran it. A1 reached 4 because a script proved it over every Markdown file in the repo. A5 stayed at 3, and building slice 2 falsified it, which is what grading it was for.

A slice's status points at the commit that landed it, so `implement` reconciles the table against `git log` when it resumes rather than inferring where the work stopped.

The open questions use `grilling`'s format, so `/grill-with-docs <plan>` starts from the plan's own frontier instead of re-deriving the design. Q1 came back against the plan's recommendation. `implement` re-entered the plan to record that, then built the slices against the revised version.

## Checks

```
python3 scripts/check-skill-refs.py
```

Fails when a skill body names a skill that does not exist, cites a principle without its `principle-` prefix, tells the agent to invoke a skill whose frontmatter marks it user-run, or carries frontmatter that would stop it registering. Stdlib only, no install step. Run it after editing any skill.

`.github/workflows/checks.yml` runs the same command on every push to `main` and every pull request.

```
scripts/sync-skills.sh --check
```

Reports skills whose installed copy differs from the checkout, and exits non-zero if any do. Writes nothing.

## License

MIT. Portions are adapted from other MIT-licensed projects. Their required copyright notices are in [LICENSE](./LICENSE).
