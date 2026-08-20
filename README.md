# axostack

Dataxo's agentic development stack for Claude Code: an entry-point router, a Linear-first workflow pipeline, and a set of engineering principles, packaged as one skills library.

## Architecture

Three layers.

1. **axo-mode** is the router. Its trigger table maps situations to skills, its principles index points at the 21 leaf principles, and its playbooks (feature, bug-fix, investigation, refactoring, prototype, committing) are step lists the agent copies verbatim into its todo list.
2. **Workflow skills** are the verbs. `to-linear-issue` researches an idea into an evidenced Linear issue, `to-tickets` breaks plans into dependency-ordered tickets, `triage` runs the queue, and `work-linear-issue` picks a ready issue up and drives it through `implement` → `tdd` → `code-review` to reviewed local commits. Alignment is `grill-me`/`grill-with-docs`, design is `codebase-design`/`improve-codebase-architecture`/`wayfinder`, investigation is `how`/`why`/`research`. Contested designs resolve through grilling the user. Quality gates: `unslop`, `no-comments`, `technical-writing`.
3. **Principles** are the judgment. 21 `principle-*` leaf skills, loaded only when applied, cited in the reply with the decision they changed.

## Skills

Invoke: **slash** means you type it (`/skill-name`) and the agent cannot start it on its own, **auto** means the agent may also reach for it when the task fits. The difference is the `disable-model-invocation` flag in each skill's frontmatter, so a skill another skill has to call mid-workflow must be **auto**.

### Router and setup

| Skill | Invoke | What it does |
|-------|--------|--------------|
| axo-mode | auto | The entry point. Routes situations to skills, indexes the principles, and holds the playbooks (feature, bug-fix, investigation, refactoring, prototype, committing) copied verbatim into the todo list. |
| setup-axostack | slash | Once per repo: configures the issue tracker (Linear first-class), triage labels, and domain doc locations the tracker-facing skills read. |

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

Easily confused pairs: `domain-modeling` builds the project's vocabulary docs, while `principle-model-the-domain` structures code around the domain. `figure-it-out` designs a playbook for one session-sized task, while `wayfinder` maps work spanning many sessions. `research` reads external sources, while `how` and `why` read your own codebase and history.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add <owner>/axostack
/plugin install axostack
```

Any agent, as editable files via [skills.sh](https://skills.sh):

```
npx skills@latest add <owner>/axostack
```

Manual: copy folders from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project), and the files in `agents/` into `~/.claude/agents/`.

## Usage

Run `/setup-axostack` once per repo. It configures the issue tracker (Linear, GitHub, GitLab, or local markdown), triage labels, and domain doc locations that the tracker-facing skills read.

The core loop for tracked work:

1. `/to-linear-issue <idea or question>` researches it and publishes an evidenced issue.
2. `/triage` moves the queue; `/to-tickets` breaks an agreed plan into blocking-ordered tickets.
3. `/work-linear-issue ABC-123` (or bare, to take the next ready issue) claims it, branches with the key prefix, builds under axo-mode's playbooks, and closes out with commits and a tracker update.

Either invoke `/axo-mode` explicitly or let the agent reach for it on multi-step tasks. Individual skills also work standalone: `/grill-me` before a plan, `/tdd` for a feature slice, `/diagnosing-bugs` on a hard bug, `/code-review` before a commit, `/bro` when a reply needs restating in plain language.

## License

MIT. Portions are adapted from other MIT-licensed projects; their required copyright notices are in [LICENSE](./LICENSE).
