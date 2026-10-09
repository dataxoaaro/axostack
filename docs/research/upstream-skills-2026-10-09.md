# Upstream skill update, October 9, 2026

This record covers upstream changes since the [October 6 audit](upstream-skills-2026-10-06.md), applied while the library was pruned from 66 to 36 skills. It is the first audit that includes ponytail, whose base was not recorded before. Cloudflare's security-audit-skill is unchanged.

| Source | Previous audited head | Audited head | Commits |
|---|---|---|---:|
| Matt Pocock | `6fd947921b935b7e1e69293a200400f0fdd5c15f` | `b0618bc436ad893b3c5e84e55fba86586d34a404` | 16 |
| pstack | `23e4138daa01c42d4969f7a5465f82704e64f798` | `ccb5507cec1546dc88135c1139c811e6c59115ba` | 44 |
| ponytail | `c982cd411abb53323c4baa1baa3c2f020b8d0b08` (first recorded base) | `9cc65d03aa2da1db7121b912d03596409ee340b8` (v5.1.0) | 58 |
| Cloudflare security-audit-skill | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` | 0 |

Upstream diffs: [Matt](https://github.com/mattpocock/skills/compare/6fd947921b935b7e1e69293a200400f0fdd5c15f...b0618bc436ad893b3c5e84e55fba86586d34a404), [pstack](https://github.com/cursor/plugins/compare/23e4138daa01c42d4969f7a5465f82704e64f798...ccb5507cec1546dc88135c1139c811e6c59115ba), [ponytail](https://github.com/DietrichGebert/ponytail/compare/c982cd411abb53323c4baa1baa3c2f020b8d0b08...9cc65d03aa2da1db7121b912d03596409ee340b8). Regenerate the file-level inventory with:

```
python3 docs/research/compare-upstream-skills.py <matt-clone> <cursor-plugins-clone> --matt-base 6fd9479 --cursor-base 23e4138 --pony <ponytail-clone> --pony-base c982cd4 --cloudflare <cloudflare-clone> --cloudflare-base c1c8a8c
```

The base options now default to the audited heads above. All three `--*-ref` options default to `HEAD`, so check out the audited heads in the clones first.

## Applied

| Local skill | Source | Change |
|---|---|---|
| grilling | Matt `95249b0` | Each question is worded so "yes" accepts the recommended answer. |
| wayfinder | Matt `8295b8e` | Maps and tickets carry only `wayfinder:` labels, never a triage label. Cross-references use real ids, because a placeholder `#<n>` auto-links to an unrelated issue. Research branches are pushed but open no PR. A ticket resolves as the type its label names. The setup skill keeps the local name `setup-axostack`. |
| architect | pstack `a586282` | Four new red flags in `references/design-red-flags.md`: split ownership, two ways to do one task, importable internals, hand-synced list. The SKILL.md screening sentence now assumes the next contributor sees only the files it opened and copies the nearest example. Local model lists and skill names are unchanged. |
| tdd | Matt `3f59913` | Each proposed seam says what it catches and what it misses. |
| diagnosing-bugs | Matt `f3fc563` | A forced mutation must be shown to have landed before the red result is trusted. |
| implement | Matt `6d6a5b9` | A passed ticket reference is fetched and its title stated. |
| code-review | Matt `3da8c01` | Standards files are searched for, and sub-agents run in the foreground. |
| setup-axostack | Matt `5b7cade` | Triage-label creation and tracker command fixes. |
| code-review | ponytail v5.1.0 | Scale checks in the Correctness brief, and an exception for house components. |
| retro | pstack `9511e60` | The `/correct` skill is folded into retro rather than added as a skill. |
| why | Local | The discovery step listed MCPs from a Cursor `mcps/` directory. It now lists the servers and tools in the current session and notes each evidence category with no connected source. |
| recall | Local | Removed routes to `session-pickup` and `automate-me`, which do not exist here. Resuming one prior chat points to `claude --resume`. |
| figure-it-out | Local | Names only axo-mode's real playbooks: Investigation, Feature, Bug fix, Refactoring, Prototype. Perf, Visual parity, Eval, and Multi-phase plan do not exist. |
| blast-radius | Local | Replaced the leftover "Solid versus React" example with a neutral timing example. |
| codebase-design | Local | The ban on "boundary" covers module design vocabulary only, where **seam** is the word. "Trust boundary" in security contexts stays valid, which matches code-review's Security axis and the type-system-discipline principle. |

## Not applied

- **code-review tracker doc path** (Matt `3da8c01`). The `issue-tracker.md` path does not exist here, so only the standards search and foreground sub-agents were taken.
- **Cursor model defaults** (pstack `df58112`). It drops Sol and defaults to Opus xhigh and Grok. The local model lists name Claude models.
- **poteto-help** (pstack `4e5b1cf` and follow-ups). A typed-only guide to pstack's own skills and `/setup-pstack`. It does not map onto this library.
- **Benchmark wording** (pstack `e43c7ee`). Bare performance mantras in pstack's perf-issue step. This library has no perf-issue playbook, and benchmark-checklist covers the topic.
- **Merged axes reviewer** (ponytail v5, `01cbf81`). Ponytail merged all review axes into one reviewer. code-review keeps separate axes run in parallel.
- **Matt `in-progress/`**. `chief-of-staff` and `claude-handoff` are experimental and not graduated.

## Verification

- `python3 scripts/check-skill-refs.py`: 36 skills checked, no problems.
- `git diff --check` passed.
- Every SHA in this record was resolved with `git log -1` in the local upstream clones.
