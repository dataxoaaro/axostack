# Skill update application record

The user approved the September 9 proposal. This update changes ten existing skill directories and adds `principle-attack-the-premise`, bringing this branch's library to 58 skills and 22 principles. Plugin version is 0.4.0. The original comparison snapshot remains in [the audit](upstream-skills-2026-09-09.md).

These are selective integrations. An inspected upstream revision is not a claim that every change in that revision was imported.

| Local skill | Source revision | Applied changes and retained differences |
|---|---|---|
| grilling | Matt `3cca18b368ae95cdbdebbff572ccafa662551015` | Adopted the round example. Other files unchanged. |
| unslop | pstack `f8abeddd1862dc73704e3d719dd73df0d51b8c71` | Removed Adding soul, added stable rule IDs and rules 32 and 33. Retained all earlier rules and automatic invocation. |
| technical-writing | Same pstack revision | Added authorization-aware vocabulary changes and concise PR descriptions with evidence links. Other editorial changes deferred. |
| how | Same pstack revision | Adopted the explanation-only workflow and reference updates, removed the two critique references. Fixed the simple-path prompt to work without explorer findings. Retained invocation settings and existing model defaults. |
| architect | Same pstack revision | Adopted prose/reference cleanup and removed the critique-mode dependency. Added codebase-design for interface assessment. Retained automatic grilling, local principle names, invocation settings, and existing model defaults. |
| why | Same pstack revision | Adopted deduplication and reference cleanup. Retained seven-category coverage, uncertainty, non-mutating investigator instructions, invocation settings, and existing model defaults. |
| axo-mode | Same pstack revision, adapted | Added evidence/uncertainty guidance and the premise principle index. Narrowed how routing to explanation. Retained local workflows and permissions. |
| principle-attack-the-premise | Same pstack revision, adapted | Added assumption testing after repeated failed fixes. Scoped actor measurements to imbalance problems and corrected the conclusion an even census supports. Automatic invocation. |
| tdd | Same pstack revision, adapted into Matt-derived guidance | Added observable-outcome and assertion guidance to tests.md. Preserved valid absence, exception, and property tests. Did not add the separate upstream testing principle. |
| plan, implement | Same pstack revision, selected planning concepts | Added slice evidence links, exact tested-state tracking, conditional performance baselines, and verification-gap handling on resume. Retained local slice statuses and workflow. |

The audit described architect's local route as `grill-me`, following older provenance. Inspection of the actual pre-update contents showed that later local work had already changed it to automatically invocable `grilling`. This update preserves that behavior.

The broader editorial sweep, experimental `implement-spec`, `retro`, `make-bot-ui`, the full multi-phase execution framework, its checker, and upstream model changes remain deferred. No new tracker or remote operations were introduced.

## Verification

- All 11 updated or added skill directories passed skill-creator's frontmatter and naming validator. It ran with `uv run --with pyyaml` because the system interpreter lacks PyYAML.
- The repository reference checker passed against an isolated copy containing exactly this update: 58 skills, no problems. It also ran from an unrelated working directory.
- Invocation flags for all updated existing skills match the pre-update revision.
- Standards review found no actionable regressions. Spec review found one simple-path prompt contradiction in how; it was corrected and the reviewer confirmed resolution.
- A read-only exercise used how to explain the real sync script. A premise-checking scenario correctly treated an even worker census as insufficient to reject the stale-cache hypothesis.
- Comment review found no actionable comments. The added TDD material is instructional guidance, not application code requiring a new test suite.
- `git diff --check` passed.

The exercised how path was the simple explanation path. Complex multi-explorer orchestration, full seven-source why investigations, and project-specific performance runs were not exercised here. Their external tool availability remains environment-dependent; this update does not claim to resolve pre-existing Cursor-specific configuration instructions.

[SHA-256 hashes](applied-skill-hashes-2026-09-09.json) identify all 40 files in the updated directories after validation. The scoped installation sync completed for all 11 directories. All 40 installed file hashes matched, and both deleted critique files were absent.

An unrelated `idea-to-pr` skill and its README additions appeared concurrently. They are excluded from this update's commit and installation scope.

## Combined publication

The user subsequently authorized including `idea-to-pr` and its README additions in the same 0.4.0 publication. The combined library contains 59 skills. Review clarified that an existing matching issue must be reused, preserving its destination and assignee unless a change was requested. The earlier exclusion describes the upstream-update commit only.
