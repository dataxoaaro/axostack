# Upstream skill update proposal

Checked September 9, 2026. This document records the original audit and proposal. The user subsequently approved the proposed changes. See the [application record](skill-update-record-2026-09-09.md) for what was applied and verified. Counts and comparisons below describe the pre-update snapshot.

The comparison covers all 57 local skill directories and their supporting files. Of 53 inherited directories, 32 have upstream changes and 21 have none. Most changed directories contain prose edits. Four locally authored skills need a comparison of related workflows rather than a direct sync.

| Source | Recorded baseline | Audited head | Inherited directories | Changed upstream |
|---|---|---|---:|---:|
| Matt Pocock | `885e2ca4d842d139e9aef4e48d366c63cb1b8013` | `3cca18b368ae95cdbdebbff572ccafa662551015` | 16 | 1 |
| pstack | `fd6dd6f7276956a532bb78a748a8d2818b6eb5f4` | `f8abeddd1862dc73704e3d719dd73df0d51b8c71` | 37 | 31 |

The source revisions come from the last version of the deleted provenance file, recovered with `git show 127120a^:UPSTREAM.md`. Local HEAD was `cf0e582`; the worktree was clean before this audit. The four local skills are `axo-mode`, `plan`, `to-linear-issue`, and `work-linear-issue`. Their origins and related workflows do not make them direct copies. The exact directory mappings and file deltas are in [the generated inventory](upstream-skills-2026-09-09.json). Upstream comparisons are pinned to [Matt's audited revisions](https://github.com/mattpocock/skills/compare/885e2ca4d842d139e9aef4e48d366c63cb1b8013...3cca18b368ae95cdbdebbff572ccafa662551015) and [pstack's audited revisions](https://github.com/cursor/plugins/compare/fd6dd6f7276956a532bb78a748a8d2818b6eb5f4...f8abeddd1862dc73704e3d719dd73df0d51b8c71).

## Changes I recommend first

### Update grilling's example

Matt's only update to an inherited skill is a clearer example of a question round. It now shows two numbered questions, each with a recommendation, separated by a horizontal rule. The question process itself is unchanged. Local `grilling` still matches the baseline, so this is a small conflict-free port. The other 15 Matt-derived directories have no upstream changes. [Upstream change](https://github.com/mattpocock/skills/commit/85f83d3fde1d3a90d5c9a657f6998c79a6c37308).

Proposed edit to `skills/grilling/SKILL.md`: replace "Each question should be formatted like so" with "Format a round like so", then extend the existing example with the recommendation for Q1, a horizontal separator, and Q2 before its recommendation. Preserve the existing frontmatter and supporting agent metadata.

### Strengthen evidence wording in axo-mode

On September 9, pstack added a reply rule requiring evidence or an uncertainty label beside each claim, and requiring agents to run checks they can perform themselves. This belongs in axostack's reply instructions even though `axo-mode` is locally authored. [Upstream commit](https://github.com/cursor/plugins/commit/f8abeddd1862dc73704e3d719dd73df0d51b8c71).

Proposed wording:

> Support factual claims with evidence you inspected. Mark inferences, predictions, and unresolved hypotheses explicitly. Run available checks before handing verification back to the user.

This is an adaptation. It preserves the distinction between an evidence-backed inference and an unsupported guess without forcing a mechanical label onto every sentence.

### Update unslop and technical-writing together

Pstack removed `unslop`'s "Adding soul" section and added rules 32 and 33 for mannered prose and excessive compression. It also declares rule numbers stable, so removed rules leave gaps. I recommend those changes. Your current "Let some mess in" advice conflicts with the more useful goal of clear, literal prose. Keep existing useful rules 1, 2, 4, 6, and 21 unless there is a separate reason to remove them. Their upstream deletion is editorial, not a correctness fix. [Current upstream unslop](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/unslop/SKILL.md).

`technical-writing` now tells agents to propose vocabulary-rule changes instead of modifying `unslop` while doing ordinary writing. It also asks for brief PR descriptions with links to large verification artifacts. Adopt both. [Current upstream technical-writing](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/technical-writing/SKILL.md).

Proposed wording for the vocabulary instruction:

> Propose additions to unslop with the offending phrase, its replacement, and a diff. Apply them when the user has authorized skill changes.

Keep `unslop` automatically invocable. Upstream added `disable-model-invocation: true`, which conflicts with your router and README. This setting must not be imported with the prose.

## Changes that need integration decisions

### Simplify how and move architecture criticism to the existing design workflow

Pstack removed `how`'s critique mode, deleted `references/critic-prompt.md` and `references/critique-rubric.md`, and shortened the explanation workflow. It also removed `architect`'s instruction to use that mode. These are coordinated changes across five files in `how` and three in `architect`, not a one-file refresh. [Upstream how](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/how/SKILL.md), [upstream architect](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/architect/SKILL.md).

I recommend adopting the simpler explanation workflow because axostack already has `codebase-design`, `architect`, and the user-invoked `improve-codebase-architecture`. For a change's design, `architect` can use `codebase-design`. A broad architecture survey remains the purpose of `/improve-codebase-architecture`.

The proposed change includes updating `how`'s description, both remaining prompt templates, `architect`'s grounding instruction, and the README row that promises critic agents. Only then remove the two obsolete references. Preserve `architect`'s local routing to `grill-me`; upstream still names the intentionally excluded `interrogate` skill.

### Add premise checking, with a narrower claim

The new `principle-attack-the-premise` says to reconsider a shared assumption after repeated fixes fail. It calls for a reproducible per-actor measurement before another fix. That is useful for repeated load-distribution, ownership, and concurrency failures. However, its final rule says an even actor distribution means the premise is not the cause. That conclusion does not follow for every premise. Its actor-specific procedure also does not fit every debugging problem. [Upstream principle](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/principle-attack-the-premise/SKILL.md).

I recommend adding the principle with this core wording:

> When repeated fixes rely on the same assumption and fail the same check, write down that assumption and design a measurement that could disprove it. For an imbalance, measure the distribution by actor before changing the mechanism. An even distribution rules out the measured skew; it does not establish that every shared assumption is correct.

Keep the trigger focused on repeated failed fixes. Add it to `axo-mode`'s principles index and the README, with automatic invocation consistent with the existing principles.

### Reuse the useful testing advice without importing a faulty rule

The new `principle-test-behavior-not-implementation` promotes observable outcomes and independent expected values. Matt's TDD skill already covers much of that. I recommend adding any missing examples to `tdd/tests.md` rather than immediately creating a second owner for the same guidance. [New pstack principle](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/principle-test-behavior-not-implementation/SKILL.md), [existing local tests guidance](../../skills/tdd/tests.md).

Do not copy its claim that all listed assertion shapes pass when imported functions return `undefined`. `expect(subject()).toBeDefined()` fails in that case, as does `expect(subject()).toEqual([])`. Valid absence, exception, and property tests also need more judgment than a requirement for literal expected values permits. These are logical counterexamples to the upstream wording, not findings from running a particular project's test suite.

Proposed wording:

> Test the subject through its public boundary and assert the result or effect its caller observes. Choose an expected result independently of the implementation. Ask which realistic defect the assertion would catch. Keep absence, exception, and property assertions when they express the contract; strengthen tests that could pass without exercising the subject.

### Borrow selected planning checks

Pstack replaced its multi-phase plan reference with an extensive checklist and added `scripts/check-plan.mjs`. Useful ideas include linking completed items to actual evidence, recording the verified commit, and measuring a baseline before comparing performance. [Upstream plan playbook](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md), [upstream checker](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/poteto-mode/scripts/check-plan.mjs).

For axostack, extend the existing `plan` slice table and `implement` completion rule with evidence links and the verified revision. Require performance baselines when performance is part of the acceptance criteria. A later checker should validate axostack's format, not the upstream skeleton.

Defer the full playbook. It assumes ten live verification lanes, named Cursor control skills, cloud VMs, autonomous execution playbooks, periodic wake mechanisms, and interaction review gates for each relevant PR. Those dependencies are outside the current library. Copying its checker alone would enforce a document format your plans do not use.

## Lower-priority refreshes

`why` changed across 12 files. Most edits shorten repeated instructions and defer the output structure to its existing synthesizer template. Its seven-source investigation and evidence framework remain. Adopt the deduplication when convenient, keeping explicit source coverage, uncertainty, and read-only reviewer constraints. This is maintenance, not a new investigation capability. [Upstream why](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/why/SKILL.md).

The remaining changed pstack directories mostly remove repetition, metaphors, and punctuation or update model defaults. `reflect` also limits its trigger text to an explicit user request, which agrees with axostack's current frontmatter. `show-me-your-work` retains its existing TSV format and logger; the logger did not change. The boundary and type-system principles received editorial changes, not new validation mechanisms. These can wait for an editorial pass. [Prose changes](https://github.com/cursor/plugins/commit/e8d856f), [punctuation changes](https://github.com/cursor/plugins/commit/d7cde2b), [invocation changes](https://github.com/cursor/plugins/commit/73f8be4).

The source audit found no upstream changes in `agents/comment-sicko.md`. Preserve its local Claude agent naming.

## New capabilities to defer

These are additions after the recorded baselines, not missing updates to installed skills:

| Addition | Assessment |
|---|---|
| Matt `in-progress/implement-spec` | Experimental scheduling of a ticket graph in isolated worktrees into one PR. Consider the dependency scheduling later. It overlaps local `implement` and introduces PR lifecycle and concurrency assumptions. |
| Matt `in-progress/retro` | Experimental environment review. Consider its diagnostic categories for `reflect`'s tooling reviewer. A direct import overlaps `reflect` and references the excluded `writing-for-agents` skill. |
| pstack `make-bot-ui` | New durable chat-control UI capability. Useful only if you want that workflow; it is not a maintenance requirement for this library. |

Sources: [implement-spec](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/implement-spec/SKILL.md), [retro](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/retro/SKILL.md), [make-bot-ui](https://github.com/cursor/plugins/blob/f8abeddd1862dc73704e3d719dd73df0d51b8c71/pstack/skills/make-bot-ui/SKILL.md).

## Local choices to preserve

- Keep Matt's TDD implementation and Dataxo's behavior-change trigger. Pstack's separate TDD skill is not its successor.
- Keep the expanded local `implement`, plan slice status, verification and resume behavior. Matt's short `engineering/implement` has not changed.
- Keep Linear integration, `setup-axostack` naming, `docs/agents/artifacts.md` handling, and local tracker templates.
- Keep the current model-invocation policy. Several pstack skills are deliberately user-only upstream but are callable workflow steps here.
- Preserve Claude transcript paths and agent adaptations. Do not import Cursor `Task` arguments, configuration paths, or model names as though they were portable APIs.
- Preserve your remote-action policy and the local committing workflow. Pstack's ready-only PR policy, forge selection, and autonomous shipping playbooks are separate workflow choices.

Some old Cursor-specific instructions already remain in local `how` and `why`. Resolving them against the actual runtime would be worthwhile, but that is pre-existing portability work. The newer upstream model names do not resolve it.

The full-copy update commands for either original repository are therefore inappropriate for this combined library. Apply selected upstream deltas against the recorded baseline, preserving the local side of the comparison.

## Verification and repeatability

The audit read full Git histories and compared Git blob identities for every file beneath each mapped directory. It compares baseline to upstream head separately from baseline to local contents, so local renames and customizations do not count as upstream updates. The generated inventory records 53 changed upstream files across 32 inherited directories, including the two deleted critique references. Changed-file counts do not imply that every change is worth adopting.

Checks on the actual local installation:

- `scripts/sync-skills.sh --check`: 57 skills, install matches the checkout.
- `python3 scripts/check-skill-refs.py`: 57 skills checked, no problems.

The read-only [comparison script](compare-upstream-skills.py) takes full-history clones of the two upstream repositories. To reproduce the audited revisions:

```sh
python3 docs/research/compare-upstream-skills.py /path/to/matt-skills /path/to/cursor-plugins \
  --matt-ref 3cca18b368ae95cdbdebbff572ccafa662551015 \
  --cursor-ref f8abeddd1862dc73704e3d719dd73df0d51b8c71
```

Without the revision flags, it compares the clones' current HEADs. It does not fetch or modify either clone or any skill. Its name mapping is specific to this library and the recovered baseline; future renames require review. The four locally authored skills, related unvendored workflows, and new capabilities were reviewed manually above.

For future updates, keep an audit record of the upstream revision actually merged per skill, plus the local adaptations to preserve. The snapshot accompanying this proposal records what was inspected, not a claim that those revisions have been installed. After accepted edits, run the reference checker and review the changed directory contents before syncing the installation.

## Complete inherited-skill coverage

In the table below, "changed" means that at least one file changed upstream since its recorded baseline. It does not mean the local difference is a defect. "Unchanged" requires no upstream refresh, even where axostack has local customizations.

| Local skill | Source | Upstream status | Changed files |
|---|---|---|---:|
| `architect` | pstack | Changed | 3 |
| `arena` | pstack | Changed | 1 |
| `blast-radius` | pstack | Changed | 1 |
| `bro` | pstack | Unchanged | 0 |
| `code-review` | matt | Unchanged | 0 |
| `codebase-design` | matt | Unchanged | 0 |
| `create-verification-skill` | pstack | Unchanged | 0 |
| `diagnosing-bugs` | matt | Unchanged | 0 |
| `domain-modeling` | matt | Unchanged | 0 |
| `figure-it-out` | pstack | Changed | 1 |
| `grill-me` | matt | Unchanged | 0 |
| `grill-with-docs` | matt | Unchanged | 0 |
| `grilling` | matt | Changed | 1 |
| `how` | pstack | Changed | 5 |
| `implement` | matt | Unchanged | 0 |
| `improve-codebase-architecture` | matt | Unchanged | 0 |
| `maintain-verification-skill` | pstack | Unchanged | 0 |
| `no-comments` | pstack | Changed | 1 |
| `principle-boundary-discipline` | pstack | Changed | 1 |
| `principle-build-the-lever` | pstack | Changed | 1 |
| `principle-encode-lessons-in-structure` | pstack | Changed | 1 |
| `principle-exhaust-the-design-space` | pstack | Unchanged | 0 |
| `principle-experience-first` | pstack | Changed | 1 |
| `principle-fix-root-causes` | pstack | Changed | 1 |
| `principle-foundational-thinking` | pstack | Changed | 1 |
| `principle-guard-the-context-window` | pstack | Changed | 1 |
| `principle-laziness-protocol` | pstack | Changed | 1 |
| `principle-make-operations-idempotent` | pstack | Unchanged | 0 |
| `principle-migrate-callers-then-delete-legacy-apis` | pstack | Changed | 1 |
| `principle-minimize-reader-load` | pstack | Changed | 1 |
| `principle-model-the-domain` | pstack | Changed | 1 |
| `principle-never-block-on-the-human` | pstack | Changed | 1 |
| `principle-outcome-oriented-execution` | pstack | Unchanged | 0 |
| `principle-prove-it-works` | pstack | Changed | 1 |
| `principle-redesign-from-first-principles` | pstack | Changed | 1 |
| `principle-separate-before-serializing-shared-state` | pstack | Changed | 1 |
| `principle-sequence-verifiable-units` | pstack | Changed | 1 |
| `principle-subtract-before-you-add` | pstack | Changed | 1 |
| `principle-type-system-discipline` | pstack | Changed | 1 |
| `prototype` | matt | Unchanged | 0 |
| `recall` | pstack | Changed | 1 |
| `reflect` | pstack | Changed | 5 |
| `research` | matt | Unchanged | 0 |
| `setup-axostack` | matt | Unchanged | 0 |
| `show-me-your-work` | pstack | Changed | 1 |
| `swarm` | pstack | Changed | 1 |
| `tdd` | matt | Unchanged | 0 |
| `technical-writing` | pstack | Changed | 1 |
| `to-tickets` | matt | Unchanged | 0 |
| `triage` | matt | Unchanged | 0 |
| `unslop` | pstack | Changed | 1 |
| `wayfinder` | matt | Unchanged | 0 |
| `why` | pstack | Changed | 12 |
