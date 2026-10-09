# axostack

Agentic development stack for Claude Code: an entry-point router, a Linear-first workflow pipeline, and a set of engineering principles, packaged as one skills library.

## Architecture

Three layers, and one split inside the middle layer that explains most of the library.

1. **axo-mode** routes. Its trigger table maps a situation to a skill, its principles index points at the 13 principle files in `skills/axo-mode/principles/`, and its playbooks are step lists the agent copies into its todo list verbatim.

2. **Skills** do the work, on two axes that do not compete. A **playbook** is the sequence for a kind of work: feature, bug fix, refactoring, investigation, prototype, committing. A **phase verb** is the depth on one part of any of them. `plan` writes the change down, `implement` builds it, and `code-review` checks it. A playbook names the verb and stops. The verb owns what happens inside. That is why the feature playbook is six steps instead of a second description of the build loop.

   The rest serve those two. Alignment is `grilling`. Design is `architect` and `codebase-design`. Investigation is `how`, `why`, `research`, and `research-idea`. The tracker pipeline is `to-issue`, `triage`, `to-tickets`, and `idea-to-pr`. Prose gates are `unslop`, `no-comments`, and `technical-writing`.

3. **Principles** carry the judgment. 13 reference files under axo-mode, not skills, each read only when it applies and cited with the decision it changed.

## Skills

Invoke: **slash** means you type it (`/skill-name`) and the agent cannot start it on its own, **auto** means the agent may also reach for it when the task fits. The difference is the `disable-model-invocation` flag in each skill's frontmatter, so a skill another skill has to call mid-workflow must be **auto**.

Slash is a deliberate list, not a leftover. A skill is slash-only when starting it should be a person's decision: it runs for a long time unattended, it spends real money, it writes to a tracker or a remote, or its whole job is a conversation the agent must not hold with itself. Everything else is auto, because a router that names a skill the agent cannot reach is a router that dead-ends. The current members:

<!-- user-only:start -->
`figure-it-out`, `idea-to-pr`, `implement-spec`, `improve-codebase-architecture`, `research-idea`, `retro`, `setup-axostack`, `to-issue`, `to-tickets`, `triage`, `verification-skill`, `wayfinder`
<!-- user-only:end -->

`scripts/check-skill-refs.py` fails when that list and the frontmatter flags disagree, so adding a skill to one without the other is caught rather than inferred later.

### Router and setup

| Skill | Invoke | What it does |
|-------|--------|--------------|
| axo-mode | auto | The entry point. Routes situations to skills, indexes the principles, and holds the playbooks (feature, bug-fix, investigation, refactoring, prototype, committing) copied verbatim into the todo list. |
| setup-axostack | slash | Once per repo: configures the issue tracker (Linear first-class), triage labels, domain doc locations, and where plans and research notes land. |

### Linear workflow

| Skill | Invoke | What it does |
|-------|--------|--------------|
| idea-to-pr | slash | Take an idea, a fix, or an existing issue through a plan, a Linear issue, a dedicated worktree, a PR, and independent reviews with repairs. Run bare, it takes the next unblocked `ready-for-agent` issue. Local mode stops at commits on the branch. Prefixes the branch and PR title with the issue key. |
| to-issue | slash | Research a question, idea, or problem and publish it as one evidenced issue with approach and acceptance criteria. |
| to-tickets | slash | Break an agreed plan into tracer-bullet tickets with blocking edges, published in dependency order. |
| triage | slash | Move incoming issues through triage roles: categorise, verify, grill if needed, write agent-ready briefs. |
| wayfinder | slash | Plan work too large for one session as a shared map of decision tickets, resolved one at a time until the path is clear. |

### Align and design

| Skill | Invoke | What it does |
|-------|--------|--------------|
| grilling | auto | Question the user until every branch of the design tree is resolved, one round of numbered questions at a time. Also runs domain-modeling when the repo has GLOSSARY.md or ADRs. Backs triage, wayfinder, and plan review. |
| architect | auto | Sketch types, signatures, and module structure through parallel design exploration before code, for a specific change. Requires at least two structurally distinct designs. |
| codebase-design | auto | The deep-module vocabulary: a lot of behavior behind a small interface, at a clean seam, testable through it. Used by architect and improve-codebase-architecture. |
| improve-codebase-architecture | slash | Survey a whole codebase for deepening opportunities, report them, grill through the one you pick. |
| plan | auto | Work a feature or fix into one plan document: grounded, risk-graded, sliced into tickets, with every unsettled question numbered for the next grilling session. |
| prototype | auto | A throwaway sketch that answers a design question by observation instead of asking. |

### Build and verify

| Skill | Invoke | What it does |
|-------|--------|--------------|
| implement | auto | Build the work a spec or tickets describe, driving tdd at the agreed seams and closing with code-review. |
| implement-spec | slash | Land a whole spec in one run: background implementers build every unblocked ticket in its own worktree, each merges into one integration branch, then one code-review and one fix pass. |
| tdd | auto | Red-green-refactor, one vertical slice at a time. The default build loop for behavior changes. |
| code-review | auto | Four-axis review of the diff since a fixed point, including uncommitted work: repo standards, spec fidelity, correctness, and complexity (what the change could do without), plus security when the diff touches a trust boundary. Runs as parallel subagents and verifies each finding against the code before reporting. |
| security-audit | auto | Cloudflare's source-first security review. Guidance mode answers security questions and backs code-review's Security axis. A full audit, with a coverage ledger, independent verifiers, and schema-checked findings, runs only on an explicit audit or pen-test request. |
| diagnosing-bugs | auto | Gated diagnosis loop for hard bugs: feedback loop that goes red on the bug, minimise, hypothesise, instrument, fix, regression-test. |
| blast-radius | auto | Find what a change could break beyond the diff, and prove the one safety-critical fact by running real code. |
| benchmark-checklist | auto | Vet a measured number before reporting or acting on it: limiter, tuning, physical limits, errors, repeatability, end-to-end share, and whether the work ran. Covers eval results too. |
| no-comments | auto | Strip narrating and workaround comments via the comment-sicko agent, then fix what the deletions expose. |
| verification-skill | slash | `create` generates a project-local `verify-<app>` skill that drives the real app the way a user does and captures evidence. `maintain` audits it and its feature map against the source. |

### Investigate

| Skill | Invoke | What it does |
|-------|--------|--------------|
| how | auto | How a subsystem works: architecture walkthroughs, runtime flow, placement and layering questions. Architecture assessment belongs to the design skills. |
| why | auto | Why it is this way: design rationale and regression history mined from source control, tracker, docs, and observability in parallel. |
| research | auto | Investigate an external question against primary sources and land a cited Markdown file in the repo. Source tiers, freshness, and citation rules live in its `SOURCES.md`. |
| research-idea | slash | Research the ways to build an idea: premise check, approaches with different mechanisms, parallel research and verification, an HTML report with a recommendation and its strongest counter-argument, then a grilled decision record that `/plan` or `/idea-to-pr` builds from. |

### Parallelism and long runs

| Skill | Invoke | What it does |
|-------|--------|--------------|
| arena | auto | Race mode: N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Partition mode: one worker per slice of the work, drained into one report. |
| figure-it-out | slash | Design a bespoke, auditable playbook when no bundled one fits a large or multi-part task. |
| show-me-your-work | auto | A reviewable decision trail (one row per decision: what, why, evidence, result) for long or unattended runs. |
| recall | auto | Reconstruct working context from your own transcripts and live state when resuming ("where did I leave off"). |
| retro | slash | Retrospective on a session that went harder than it should have. The library target runs three transcript reviewers and applies approved edits to these skills. The repo target proposes environment fixes (navigation pointers, automated checks, coding standards, slimmer steering files, information access), fixes recurring mistakes at the highest level that works, and keeps a rule-to-enforcement table. Every finding is traced to a moment in the session. Builds only what you pick. |

### Docs and prose

| Skill | Invoke | What it does |
|-------|--------|--------------|
| unslop | auto | Cut AI tells from any writing. Applies to every prose surface, including replies. |
| technical-writing | auto | The layered docs standard (Diátaxis, Google style, STE, Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |
| pr | auto | The PR body template: a visual Summary, before-and-after Evidence, and a Merge Danger call naming the door (one-way or two-way) and the blast radius. |
| domain-modeling | auto | Build and sharpen the project's domain model: glossary terms, GLOSSARY.md, ADRs. |

### Agents

| Agent | What it does |
|-------|--------------|
| axo-agent | Code-writing delegate that reads axo-mode in full before working, so subagents carry the same discipline. |
| comment-sicko | Read-only comment-hunting reviewer spawned by no-comments. |

### Principles

13 reference files in `skills/axo-mode/principles/`, indexed in axo-mode, each read in full only when applied. They are not skills, so they add nothing to the always-loaded skill list. Grouped: **core** ([laziness-protocol](skills/axo-mode/principles/laziness-protocol.md), [end-state](skills/axo-mode/principles/end-state.md), [experience-first](skills/axo-mode/principles/experience-first.md), [build-the-lever](skills/axo-mode/principles/build-the-lever.md)), **architecture** ([model-the-domain](skills/axo-mode/principles/model-the-domain.md), [type-system-discipline](skills/axo-mode/principles/type-system-discipline.md), [make-operations-idempotent](skills/axo-mode/principles/make-operations-idempotent.md), [separate-before-serializing-shared-state](skills/axo-mode/principles/separate-before-serializing-shared-state.md)), **verification** ([attack-the-premise](skills/axo-mode/principles/attack-the-premise.md), [prove-it-works](skills/axo-mode/principles/prove-it-works.md), [fix-root-causes](skills/axo-mode/principles/fix-root-causes.md), [sequence-verifiable-units](skills/axo-mode/principles/sequence-verifiable-units.md)), **meta** ([encode-lessons-in-structure](skills/axo-mode/principles/encode-lessons-in-structure.md)). Each file's first paragraph states when it applies. Designing it twice is part of `architect`, explaining a measured number is part of `benchmark-checklist`, and guarding the context window and never blocking on the human are axo-mode's Subagents and Autonomy sections.

Easily confused pairs: `domain-modeling` builds the project's vocabulary docs, while the model-the-domain principle structures code around the domain. `figure-it-out` designs a playbook for one session-sized task, while `wayfinder` maps work spanning many sessions. `research` reads external sources, while `how` and `why` read your own codebase and history. `/retro` aimed at the library turns a session into edits on these skills, while aimed at the repo it turns the session into checks, pointers, and standards in the repo you worked on. `arena`'s race mode runs N attempts at one task, while its partition mode gives each worker its own slice. `research` answers a question of fact, while `research-idea` compares the ways to build something and records which one was chosen. `plan` writes down a change you can already state, `wayfinder` maps one you can't yet, and `architect` designs the types inside a plan rather than replacing it.

## Install

Claude Code, as a plugin. The marketplace is named `dataxo`, so the plugin is installed as `axostack@dataxo`:

```
/plugin marketplace add dataxoaaro/axostack
/plugin install axostack@dataxo
```

Update with `/plugin marketplace update dataxo`. Plugin installs are pinned to the `version` in `.claude-plugin/plugin.json`, so bump it when you want existing users to receive a change.

Any agent, as editable files via [skills.sh](https://skills.sh):

```
npx skills@latest add dataxoaaro/axostack
```

Update with `npx skills@latest update`. This path tracks the default branch and ignores the plugin version, so merging to `main` is enough.

From a clone, with the sync script:

```
scripts/sync-skills.sh
```

It installs each skill directory separately and links any that is missing. Editing the checkout changes nothing until it runs. Copy the files in `agents/` into `~/.claude/agents/` yourself.

Do not sync by hand with a single `rsync --delete` over the install directory. That deletes every installed skill that does not come from this repo.

## Usage

Run `/setup-axostack` once per repo. It records the issue tracker (Linear, GitHub, GitLab, or local markdown), the triage labels, the domain doc locations, and where plans land. The tracker-facing skills read that configuration.

Then pick the entry point that matches what you have.

**An idea, and several ways to build it.** `/research-idea <idea>` challenges the premise, researches the approaches against primary sources, and opens an HTML report with a recommendation. You pick one, it grills you on it, and it writes a decision record to `docs/research/`. Hand that file to `/plan` or `/idea-to-pr`.

**An idea or fix to carry through to a PR.** `/idea-to-pr <request>` investigates, plans, asks for the Linear workspace and assignee, and creates the issue in the appropriate project. It builds in a dedicated worktree, opens a draft PR such as `[AXO-123] Fix session expiry`, runs independent reviews, and repairs valid findings. The request authorizes issue and PR updates and pushing the task branch. Merging remains a separate action. An interrupted run resumes from its recorded issue, worktree, and PR.

**An idea, not a plan.** `/to-issue <idea>` researches it against the codebase and publishes one evidenced issue. Run `/triage` to move the queue when issues pile up.

**An agreed direction, not a design.** `/plan <feature>` writes `docs/plans/<NNNN>-slug.md`, grounded in the codebase, with alternatives recorded, assumptions graded on evidence, work sliced into tickets, and open questions numbered. Then `/grilling docs/plans/<NNNN>-slug.md` attacks each question and folds the answers back into the file.

**A plan.** `/to-tickets docs/plans/<NNNN>-slug.md` publishes the slices to your tracker in dependency order. To build the whole graph in one run, `/implement-spec <plan or parent issue>` runs every unblocked ticket in parallel and lands them on one integration branch.

**A ticket.** `/idea-to-pr ABC-123` claims it, branches with the key prefix, builds in a worktree, and carries it to a reviewed PR. Run it bare to take the next ready issue, or in local mode (`/idea-to-pr --local ABC-123`) to stop at commits on the branch. Without a tracker, `/implement` builds straight from the plan.

Both paths meet at `/to-tickets`. What differs is where you start. An unshaped idea goes to the tracker first, and an agreed direction goes to a plan first.

Either invoke `/axo-mode` explicitly or let the agent reach for it on a multi-step task. Skills also work standalone. Reach for `/grilling` to stress-test a design, `/tdd` for one feature slice, `/diagnosing-bugs` on a hard bug, and `/code-review` before a commit.

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

The open questions use `grilling`'s format, so `/grilling <plan>` starts from the plan's own frontier instead of re-deriving the design. Q1 came back against the plan's recommendation. `implement` re-entered the plan to record that, then built the slices against the revised version.

## Checks

```
python3 scripts/check-skill-refs.py
```

Fails when a skill body names a skill that does not exist, links a principle file that does not exist, leaves a principle file out of axo-mode's index, tells the agent to invoke a skill whose frontmatter marks it user-run, or carries frontmatter that would stop it registering. Stdlib only, no install step. Run it after editing any skill.

`.github/workflows/checks.yml` runs the same command on every push to `main` and every pull request, plus the security-audit skill's validator tests (`node --test skills/security-audit/*.test.cjs`).

```
scripts/sync-skills.sh --check
```

Reports skills whose installed copy differs from the checkout, and exits non-zero if any do. Writes nothing.

To be warned about that drift automatically:

```
git config core.hooksPath scripts/hooks
```

`scripts/hooks/pre-push` then warns when your install is stale. It never blocks, because drift means your local agent is running old skills and says nothing about whether the push is safe. This check cannot run in CI: a runner has no install directory, so every skill would report missing.

## License

MIT. Portions are adapted from other MIT-licensed projects. Their required copyright notices are in [LICENSE](./LICENSE).
