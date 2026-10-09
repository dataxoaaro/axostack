---
status: chosen  # chosen | superseded
date: 2026-10-09
superseded-by:
---

# A lean axostack whose developer skills cover every software factory station

## Idea

Cut axostack to a lean, current set of human-interactive developer skills that together cover every station of an AI software factory, so a later factory can be built from them. Done when every factory station maps to one axostack skill a developer runs by hand, the library has about 35 skills with no stale references or contradictions, the seven fact questions are researched instead of asked, and code-review's median wall time drops on real runs.

## Requirements

Hard gates:
- Interactive developer use keeps working: slash entry points, and grilling on decisions the user owns.
- Skills stay plain SKILL.md, installable through the Claude Code plugin and skills.sh, with no dependency on a hosted platform.
- One person can maintain the library alongside the upstream syncs from Matt Pocock's skills, pstack, Cloudflare's security-audit-skill, and ponytail.
- Every factory station has a developer skill. The stations are intake, specification, planning, build, verification, review, review feedback, and process improvement. Release and monitoring wait for the factory.

Preferences, in order:
- Lean: fewer skills, shorter always-loaded descriptions.
- Fewer questions about facts the skill could look up.
- Faster code-review.
- Low upstream-sync cost.
- Artifacts a later factory can reuse unchanged.

## Decision

axostack stays the developer pack. Every skill keeps its human interaction, and nothing runs unattended. Factory variants of the interactive skills go into a separate pack later, provisionally called axo-factory. That pack decides how a skill behaves with no human attached. This work does not build a runner, workflows, permission profiles, or an eval suite.

The user picked this over the report's recommendation, which was a headless station runner gated by an eval suite. The user's reason: the factory is the next step, and this one prepares the skills for it.

The scope, in delivery order:

1. **Fix and port.** Fix the eight stale references and five contradictions listed under Evidence. Port Matt's seven updates, architect's four red flags from pstack, and ponytail's scale line into code-review's Correctness brief. Record a ponytail base SHA in `docs/research/compare-upstream-skills.py`.
2. **Code-review speed.** One script precomputes the per-file diff, the commit list, the spec, the test results, and the callers of each changed symbol, and every axis reads that output. Bound the Correctness axis: no nested agents, a soft budget of about 25 tool calls, and a split by file cluster on large diffs. Spawn Correctness first, in the foreground. Verify each axis as it returns. Use Sonnet for the Spec, Standards, Complexity, and Security axes. idea-to-pr repair rounds review only the fix commits.
3. **Prune from 66 to about 35 skills.**
   - Move the 23 `principle-*` skills into `skills/axo-mode/principles/` and merge them to about 12.
   - Delete `bro`, `grill-me`, and `grill-with-docs`. grilling gains a rule to also run domain-modeling when domain docs exist.
   - Fold `work-linear-issue` into idea-to-pr, `swarm` into arena, and `reflect` plus pstack's `/correct` into retro.
   - Merge `create-verification-skill` and `maintain-verification-skill` into one skill.
   - Cut every auto-invoked description to 220 characters or fewer.
   - Make `idea-to-pr` and `to-tickets` slash-only, as README:21 requires.
   - Rename `to-linear-issue` to `to-issue`.
4. **Questions.** Add one rule in axo-mode's Autonomy section. The skill researches facts instead of asking. It asks about decisions once, batched, each with a recommended answer. It asks for approval of one-way doors, and the invocation can grant that approval up front. Every skill that stops cites the rule. Convert the seven fact questions listed under Evidence. Seams named in a plan or ticket count as agreed in tdd. Merge the two one-way-door lists in axo-mode and never-block-on-the-human.
5. **Add `address-pr-feedback`.** It handles review comments and red CI on an open PR, with at most two fix attempts. It is the review-feedback station and the only new skill.

## Station coverage after the change

| Station | Developer skill |
|---|---|
| Intake | `to-issue`, `triage` |
| Specification | `research`, `research-idea`, `grilling`, `domain-modeling` |
| Planning | `plan`, `to-tickets`, `wayfinder`, `architect` |
| Build | `idea-to-pr`, `implement`, `implement-spec`, `tdd`, `diagnosing-bugs` |
| Verification | `blast-radius`, `security-audit`, `benchmark-checklist`, the merged verification skill |
| Review | `code-review`, `no-comments` |
| Review feedback | `address-pr-feedback` (new) |
| PR | `pr` |
| Process improvement | `retro` |
| Release, monitoring | none, deferred to the factory |

## Approaches considered

| Approach | Origin | Effort | Verdict | Why not |
|---|---|---|---|---|
| Developer pack covering every station, with factory variants later in a separate pack | extend | L | chosen | |
| Headless station runner, gated by an eval suite | extend | M | runner-up | Wins once a real unattended consumer exists. It is the first job of the factory work. |
| Eval-gated autonomy with `claude plugin eval` | adopt | M | deferred | Wins when factory work starts, or when upstream ports begin to regress skills. |
| Station contracts in frontmatter | extend | M | partly kept | Claude Code ignores `metadata`, so only the acceptance-criteria thread is worth taking (see Q1). |
| One line skill orchestrating forked stations | extend | L | rejected | Forks cannot ask the user, and plugin agents drop their hooks. |
| Fork the eve template, Cyrus, Tessl | adopt | L-XL | cut | Too much infrastructure for one maintainer, or a hosted login. |
| Keep what we have | | | baseline | Stale references, 23 unused principle skills, and slow reviews remain. |

## Evidence

Repo facts, verified on 2026-10-09:
- 50 of 66 skills are auto-invoked. Their descriptions total 11,969 characters. The 23 principles account for 4,448 characters, or 37%.
- The principles were invoked about once in 60 days, across 1,679 transcripts. code-review had 105 calls, idea-to-pr 35, and pr 30.
- Stale references: `why/SKILL.md:61` (Cursor `mcps/`), `recall/SKILL.md:16` (`session-pickup`, `automate-me`), `figure-it-out/SKILL.md:11` (missing playbooks), `principle-type-system-discipline/SKILL.md:10`, `principle-encode-lessons-in-structure/SKILL.md:24`, `reflect/SKILL.md:59`, `swarm/SKILL.md:8`, `blast-radius/SKILL.md:34`.
- Contradictions:
  - `principle-outcome-oriented-execution/SKILL.md:14` allows breakage, and `principle-sequence-verifiable-units/SKILL.md:8` forbids it.
  - `tdd/SKILL.md:38` sends refactoring to code-review, which never refactors.
  - `setup-axostack/SKILL.md:11` names GitHub as the default tracker against Linear at `:44`.
  - `tdd/SKILL.md:22` requires seam confirmation, and `architect/SKILL.md:44` does not.
  - `codebase-design/SKILL.md:22` bans the word "boundary".
- The seven fact questions:
  - `tdd/SKILL.md:22-24`: seam confirmation.
  - `idea-to-pr/SKILL.md:15-17`: workspace, project, and assignee.
  - `to-tickets/SKILL.md:41-55`: the quiz after an approved plan.
  - `triage/SKILL.md:72,90`: waits before verifying, and confirms explicit commands.
  - `work-linear-issue/SKILL.md:18`: confirms the next issue.
  - `setup-axostack/SKILL.md:46,60`: team and labels.
  - `code-review/SKILL.md:40`: asks for the spec.
- code-review spawned all axes in one message in 6 of 6 measured runs, from 2026-10-06 to 2026-10-08. Correctness was the slowest axis in every run. The main thread waited on it alone for 148 s on average, 31% of the mean run of 478 s. Verified on one session by an independent check.

External sources, verified on 2026-10-09:
- Matt Pocock skills `6fd9479..b0618bc`: tdd `3f59913`, grilling `95249b0`, diagnosing-bugs `f3fc563`, wayfinder `8295b8e`, implement `6d6a5b9`, code-review `3da8c01` (foreground sub-agents, all standards files), setup `5b7cade`.
- pstack `23e4138..ccb5507`: architect red flags `a586282`, `/correct` `9511e60`.
- ponytail v5.1.0 `01cbf81`: the scale checks.
- Cloudflare security-audit-skill has not changed since `c1c8a8c`.
- `claude -p "/skill"` runs a slash-only plugin skill, and `--permission-prompts none` removes `AskUserQuestion`. Verified by a local run on Claude Code 2.1.295 and by https://code.claude.com/docs/en/headless. A later factory can therefore start the slash-only skills.

Inference, not measured: the code-review changes cut 25 to 45% of wall time. The user accepted a smaller gain without measuring it.

## Risks

The skeptic argued that no evidence shows a need for unattended runs, so building a factory runner would be premature. This decision accepts that argument and defers the runner.

Two risks remain:
- Principles moved out of the skill list are no longer offered for auto-invocation, so agents may apply them less. They were invoked about once in 60 days, so little is lost.
- Splitting the Correctness axis by file cluster can miss a bug that crosses clusters. The user accepted this risk without an eval suite.

Each step lands as its own PR, so `git revert` undoes any one of them.

## Open questions

All five were settled with the user on 2026-10-09:

1. Acceptance criteria carry from the plan to the review: yes. Plan slices carry acceptance criteria, `to-tickets` copies them verbatim, and code-review's Spec axis returns pass or fail with evidence for each one. This lands in step 2.
2. Checking the code-review speedup: no eval and no measured check. The transcript findings are enough, and a smaller gain than estimated is acceptable.
3. `address-pr-feedback` adapts pstack's `babysit` playbook and eve's two-attempt cap, credited in LICENSE.
4. The principle merges: `subtract-before-you-add` and `minimize-reader-load` fold into `laziness-protocol`, and `explain-the-number` folds into `benchmark-checklist`. `exhaust-the-design-space` folds into `architect`. `guard-the-context-window` and `never-block-on-the-human` become sections of axo-mode. `foundational-thinking` folds into `model-the-domain`, and `boundary-discipline` folds into `type-system-discipline`. `outcome-oriented-execution`, `redesign-from-first-principles`, and `migrate-callers-then-delete-legacy-apis` become one end-state principle, which resolves its contradiction with `sequence-verifiable-units`.
5. Where axo-factory lives is deferred to the factory work. The target is in [axo-factory-direction.md](axo-factory-direction.md), and the decision to keep factory behavior out of these skills is [ADR 0001](../adr/0001-factory-behavior-lives-in-a-separate-pack.md). Until the factory work starts, axostack keeps the headings of the documents its skills write stable.
