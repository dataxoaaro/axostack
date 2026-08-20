# Vendored skills

Provenance for every skill copied from an upstream repo. When upstream improves a skill, diff against the recorded commit: an unmodified skill can be overwritten, a modified one needs a merge. Update the commit here after syncing.

## From pstack (cursor/plugins, commit fd6dd6f)

Source: https://github.com/cursor/plugins/tree/main/pstack

| Skill | Modified |
|-------|----------|
| architect | yes, design pressure routes to grill-me instead of the removed interrogate skill |
| arena | yes, Cursor model-pool config replaced with model-tier guidance |
| blast-radius | no |
| bro | no |
| figure-it-out | yes, reads axo-mode's principles instead of poteto-mode's |
| how | yes, dropped a reference to the removed interrogate skill |
| no-comments | yes, spawns the comment-sicko agent via the Agent tool instead of Cursor's Task API |
| show-me-your-work | yes, end-of-run audit checks the session instead of Cursor transcript paths |
| swarm | yes, Cursor Task API and model config replaced with the Agent tool |
| technical-writing | no |
| unslop | no |
| why | no |
| principle-* (all 21) | no |
| agents/comment-sicko.md | yes, agent name kebab-cased for the Claude Code Agent tool |

Not vendored: poteto-mode (replaced by our own axo-mode), interrogate (replaced by grill-me and grill-with-docs for contested designs), tdd (Pocock's taken instead), reflect, recall, teach, automate-me, setup-pstack, create/maintain-verification-skill, typescript-best-practices.

## From mattpocock/skills (commit 885e2ca)

Source: https://github.com/mattpocock/skills

| Skill | Modified |
|-------|----------|
| code-review | yes, setup skill renamed to setup-axostack |
| codebase-design | no |
| diagnosing-bugs | no |
| domain-modeling | no |
| grill-me | no |
| grill-with-docs | no |
| grilling | no |
| implement | no |
| improve-codebase-architecture | no |
| prototype | no |
| research | no |
| setup-axostack | yes, renamed from setup-matt-pocock-skills, Linear added as a first-class tracker with a new issue-tracker-linear.md template |
| tdd | yes, description strengthened: TDD is the default build loop in Dataxo repos, not opt-in |
| to-tickets | yes, setup skill renamed to setup-axostack |
| triage | yes, setup skill renamed to setup-axostack |
| wayfinder | yes, setup skill renamed to setup-axostack |

Dependency notes: grill-with-docs needs grilling and domain-modeling. improve-codebase-architecture needs codebase-design, grilling, and domain-modeling. wayfinder needs grilling, prototype, research, and the setup config. implement needs tdd and code-review. to-tickets and triage need the setup config. diagnosing-bugs is kept for axo-mode's bug-fix playbook.

Not vendored: ask-matt (replaced by axo-mode's routing table), to-spec (folded into to-linear-issue), handoff, wizard, resolving-merge-conflicts, to-questionnaire, wait-what, teach, writing-for-agents, everything under in-progress/ and misc/.

## Own skills

Original to this repo, written in the vendored stacks' shape and adapted for Claude Code:

- **axo-mode** and its playbooks: the router, replacing poteto-mode.
- **to-linear-issue**: research an idea or question and publish it as an evidenced Linear issue. Composes how/why, research, and grilling.
- **work-linear-issue**: claim a ready Linear issue, branch with the key prefix, build under axo-mode's playbooks via implement/tdd/code-review, close out with commits and a tracker update.
- **setup-axostack**'s Linear parts and **agents/axo-agent.md**.
