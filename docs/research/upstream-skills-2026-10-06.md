# Upstream skill update, October 6, 2026

This record covers Matt Pocock's skills since the [October 3 audit](upstream-skills-2026-10-03.md). The user asked for `pr` and `implement-spec` in particular. The library now has 65 skills, 23 of them principles. Plugin version is 0.8.0. pstack and Cloudflare were not re-audited.

| Source | Previous audited head | Audited head | Commits |
|---|---|---|---:|
| Matt Pocock | `d81f3a183412e71a5b1e84ca21bc1a35eea03a60` | `6fd947921b935b7e1e69293a200400f0fdd5c15f` | 34 |

Upstream diff: [Matt](https://github.com/mattpocock/skills/compare/d81f3a183412e71a5b1e84ca21bc1a35eea03a60...6fd947921b935b7e1e69293a200400f0fdd5c15f). The file-level inventory is in [upstream-skills-2026-10-06.json](upstream-skills-2026-10-06.json), generated after the changes below. Regenerate it with:

```
python3 docs/research/compare-upstream-skills.py <matt-clone> <cursor-plugins-clone> --matt-base d81f3a1 --cursor-base 23e4138 --cursor-ref 23e4138
```

`--matt-base` now defaults to `6fd9479`.

`pr` and `implement-spec` did not change upstream in this window. Both graduated on September 24, and the October 3 audit deferred them. They are new to this library, not new upstream.

## Applied

| Local skill | Source | Change |
|---|---|---|
| pr | Matt `a7d038f`, adapted | New, automatically invocable. The template (visual Summary, before-and-after Evidence, Merge Danger with door and blast radius) and the visual menu are copied with `CREDITS.md`. Local additions: a repo PR template wins on the headings it defines, the body ends with the tracker issue URL, a list of changes that are one-way even after a revert, a pointer to **blast-radius** when the change reaches outside the diff, `before → after` for performance per **benchmark-checklist**, and a rewrite after a large change under review. The last three come from the failure modes in upstream's `docs/engineering/pr.md`. |
| implement-spec | Matt `24f41cc`, adapted | New, slash only. Same core: tickets as a task graph, background implementers in their own worktrees, one integration branch, one code-review after every ticket lands, one fix pass. Local changes follow. Input may be a plan's Slices table, so it runs without a tracker. Implementers are `axo-agent` with `isolation: "worktree"`, and the orchestrator merges with `--ff-only`. When a branch is behind the tip, a merger brings the tip into that ticket's branch first. A run record in the git common directory makes resume idempotent, and the frontier is computed from it because tracker blocked-by counts go stale mid-run. Seams named in the tickets count as agreed, because background implementers cannot confirm them with the user. Tickets are assigned and move to In Progress and In Review, never Done. Pushing and the PR need the user's request. Failed tickets get one retry. The upstream docs' known failures are encoded: shared-file collisions, review-fix runaway, and tests that skip in a worktree because fixtures are untracked. |
| to-tickets | Matt `cffab50`, `9e2abf8` | Tickets become sub-issues of their source issue, and `## Blocked by` is omitted when blockers are native edges. |
| setup-axostack/issue-tracker-github.md | Matt `cffab50`, `e0efb6e` | The sub-issue operation, and external PRs listed through the REST pulls endpoint. Now matches upstream byte for byte. |
| setup-axostack/issue-tracker-linear.md | Local | The sub-issue operation that to-tickets now names. |
| axo-mode, technical-writing, idea-to-pr, README | Local | Route PR bodies to `pr` and parallel ticket graphs to `/implement-spec`. technical-writing's PR sentence and idea-to-pr's PR body row now point to `pr`. |

## Not applied

- **implement wording** (`e48341a`, `04320ee`). Upstream changed "use /tdd" to "call the Skill tool with tdd". The local body already uses bold skill names, which axo-mode defines as Skill tool calls.
- **ask-matt** routes post-bug reflection to `/retro`. ask-matt and retro are not in this library. `/reflect` covers the same ground.
- **handoff and claude-handoff** temp-dir and quoting fixes. Not in this library.
- **chief-of-staff**. New and experimental in upstream's `in-progress/`. It describes a long-running coordinator that improves the agents' environment as it goes. Worth another look once it graduates.
- **Repo metadata.** `SCOPE.md`, `.out-of-scope/` records, issue forms, triage workflows, and the unslop pass over upstream's docs. None ships as a skill.

## Verification

- `python3 scripts/check-skill-refs.py`: 65 skills checked, no problems. This includes the user-only list in the README against `implement-spec`'s `disable-model-invocation` flag.
- skill-creator's `quick_validate.py`, run with `uv run --with pyyaml`, passed pr, to-tickets, technical-writing, idea-to-pr, and axo-mode. implement-spec and setup-axostack fail only on `disable-model-invocation`, the known gap in that validator.
- `git diff --check` passed.
- An independent review subagent read the diff against the upstream clone and the local skills it touches. It found 12 defects, 10 of them in implement-spec: tdd's seam confirmation unreachable from background implementers, untracked fixtures missing in the integration worktree too, the merger's direction and worktree unstated, code-review and no-comments running against the user's checkout, plan Status writes moving the integration tip mid-run, tickets claimed without an assignee, the plugin namespace for `axo-agent`, the description contradicting the three-ticket threshold, a draft PR step that did nothing, and a plan's gating tables ignored. The other two were a pr description naming the Committing playbook, which writes no PR body, and a hedge. All 12 are fixed in this change.
- `implement-spec` has not run against a real spec yet. Its first run is the test of the worktree, merge, and resume steps.
