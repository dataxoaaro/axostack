# Upstream skill update, October 3, 2026

This record covers the audit of both upstream sources since the [September 9 update](skill-update-record-2026-09-09.md) and the changes applied from it. The user approved the recommendations, chose a full switch to `GLOSSARY.md`, and asked for the stale model IDs to be fixed in the same change. The library now has 61 skills and 23 principles. Plugin version is 0.5.0.

| Source | Previous audited head | Audited head | Inherited directories changed |
|---|---|---|---:|
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | `d81f3a183412e71a5b1e84ca21bc1a35eea03a60` | 7 |
| pstack | `f8abeddd1862dc73704e3d719dd73df0d51b8c71` | `23e4138daa01c42d4969f7a5465f82704e64f798` | 16 |

Upstream diffs: [Matt](https://github.com/mattpocock/skills/compare/3cca18b368ae95cdbdebbff572ccafa662551015...d81f3a183412e71a5b1e84ca21bc1a35eea03a60), [pstack](https://github.com/cursor/plugins/compare/f8abeddd1862dc73704e3d719dd73df0d51b8c71...23e4138daa01c42d4969f7a5465f82704e64f798). The file-level inventory is in [upstream-skills-2026-10-03.json](upstream-skills-2026-10-03.json). It was generated after the changes below, so `local_differs_from_head` shows what remains different on purpose. Regenerate it with:

```
python3 docs/research/compare-upstream-skills.py <matt-clone> <cursor-plugins-clone> --matt-base 3cca18b --cursor-base f8abedd
```

The script's bases were hard-coded to the original import revisions. They are now `--matt-base` and `--cursor-base` options, defaulting to the heads audited here, so the next audit diffs from this one. `benchmark-checklist` is added to its pstack list.

## Applied

| Local skill | Source | Change |
|---|---|---|
| domain-modeling, setup-axostack, tdd, triage, diagnosing-bugs, improve-codebase-architecture, codebase-design | Matt [`d80fa0f`](https://github.com/mattpocock/skills/commit/d80fa0f) | `CONTEXT.md` renamed to `GLOSSARY.md`, `CONTEXT-MAP.md` to `GLOSSARY-MAP.md`, and `CONTEXT-FORMAT.md` to `GLOSSARY-FORMAT.md`. Six files now match upstream byte for byte. tdd and triage keep their earlier local description and setup-skill name. |
| plan, to-linear-issue, setup-axostack/artifacts.md, README | Same rename, local | The same rename in locally authored text, so no skill reads a file the others no longer write. |
| swarm | pstack | Measurement and verification briefs name exact SHAs and the method. A result missing them is respawned once, then recorded as a gap that does not count as a pass. A worker that proves a defect lists every defect it can prove. The local worktree hint and Agent tool spawn instruction are kept. The Cursor-only `cloud_base_branch` parameter is replaced with `isolation: "worktree"`. |
| show-me-your-work | pstack | Runs and `start` rows, so a log shared across runs or resumed later shows who wrote which rows. The end-of-run audit adds superseding rows instead of cutting rows, which removes the conflict with the append-only rule. `log.sh` writes the header with `>>` when the file is missing or empty. The local "this session's conversation" wording replaces upstream's Cursor transcript path. |
| principle-explain-the-number | pstack, adapted | New verification principle: name the limiter of a measured number and rule out errors, skipped work, untuned sides, and noise. Automatically invocable, unlike upstream, to match the other principles. Indexed in axo-mode and the README. |
| benchmark-checklist | pstack, adapted | New skill with the seven questions the principle points to. Automatically invocable so the principle can route to it. Upstream's Perf issue, Hillclimb, and Opening a PR playbook references are replaced with technical-writing and show-me-your-work, and `sysctl -n hw.ncpu` is added for macOS. Routed from axo-mode. |
| technical-writing | pstack Opening a PR playbook, adapted | One sentence: report a performance change as one primary number, `before → after`, with the runs linked. benchmark-checklist cites it. |
| how, why, architect | Local fix | Cursor model IDs (`grok-4.6-fast-xhigh`, `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`) replaced with Claude Code Agent tool values. how explorers use `general-purpose` on `sonnet` and the explainer uses `general-purpose` on `opus`. Both stay read-only through their prompts, which now forbid edits and name shell search as a fallback for Grep and Glob. why investigators use `general-purpose` on `sonnet` and the synthesizer uses `opus`. architect runs one runner each on `fable`, `opus`, and `sonnet`. The Cursor-only `readonly` parameter and `generalPurpose` type name are gone from these three skills. |

## Not applied

- **Model configuration in arena, architect, how, why, reflect, and swarm.** Upstream now reads model choices from `~/.cursor/rules/pstack-models.mdc` with new Cursor model IDs. Cursor-only. Local arena, reflect, and swarm already pick models without Cursor IDs.
- **Removed guidance.** Upstream [`b0b9c7a`](https://github.com/cursor/plugins/commit/b0b9c7a) cut instructions its newer models no longer need: technical-writing's sources and review checklist, unslop's self-audit step, parts of five principles, blast-radius's "mark unproven facts as unproven", and figure-it-out's instruction to audit delegates' artifacts. These guard against overclaiming. Kept.
- **how explorer prompt punctuation and reflect's "list each learning" wording.** Editorial, deferred.
- **New Matt skills.** `pr` (PR body template) is the candidate worth a later look as a technical-writing addition. `retro` and `implement-spec` moved out of in-progress, and `resolving-merge-conflicts` was deleted. None is part of this library.
- **Other new pstack skills.** `typescript-best-practices`, `interrogate`, `poteto-mode`, and `setup-pstack` changes are outside this library's scope.

## Migration note

Repos already configured with a `CONTEXT.md` or `CONTEXT-MAP.md` need it renamed to `GLOSSARY.md` or `GLOSSARY-MAP.md`. The skills no longer look for the old names.

## Verification

- `python3 scripts/check-skill-refs.py`: 61 skills checked, no problems.
- skill-creator's `quick_validate.py`, run with `uv run --with pyyaml`, passed 14 of the 18 changed or added directories. The other four (improve-codebase-architecture, setup-axostack, to-linear-issue, triage) fail only on `disable-model-invocation`, a Claude Code key this validator copy does not know. Those flags were already on main and are intentional.
- No skill's `disable-model-invocation` flag changed against main.
- Six Matt-derived files match upstream at `d81f3a1` byte for byte after the rename. No `CONTEXT` reference remains in `skills/` or the README.
- `log.sh` exercised on a new log (header once, rows appended), an existing empty log (header added), and a cell starting with `=` (quoted).
- `git diff --check` passed.
- An independent review subagent read the full diff against both upstream clones. It found no blocking defects and seven smaller ones: an unbacked technical-writing citation, prompts naming Grep and Glob without a fallback, a stale MCP rationale in why, the one-row rule conflicting with `start` rows, Cursor-only `cloud_base_branch` in swarm, a miscount here, and `Explore` being too shallow for how's explorers. All seven are fixed in this change.
