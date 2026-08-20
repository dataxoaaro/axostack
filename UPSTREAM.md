# Vendored skills

Provenance for every skill copied from an upstream repo. When upstream improves a skill, diff against the recorded commit: an unmodified skill can be overwritten, a modified one needs a merge. Update the commit here after syncing.

## From pstack (cursor/plugins, commit fd6dd6f)

Source: https://github.com/cursor/plugins/tree/main/pstack

| Skill | Modified |
|-------|----------|
| architect | yes, design pressure now routes to grill-me instead of the removed interrogate skill |
| blast-radius | no |
| how | yes, dropped a reference to the removed interrogate skill |
| no-comments | no |
| technical-writing | no |
| unslop | no |
| why | no |
| principle-* (all 21) | no |

Not vendored: poteto-mode (replaced by our own axo-mode), interrogate (replaced by grill-me and grill-with-docs for contested designs), swarm, arena, figure-it-out, reflect, recall, show-me-your-work, teach, tdd (Pocock's taken instead), bro, automate-me, setup-pstack, create/maintain-verification-skill, typescript-best-practices.

## From mattpocock/skills (commit 885e2ca)

Source: https://github.com/mattpocock/skills

| Skill | Modified |
|-------|----------|
| code-review | no |
| diagnosing-bugs | no |
| domain-modeling | no |
| grill-me | no |
| grill-with-docs | no |
| grilling | no |
| handoff | no |
| implement | no |
| prototype | no |
| research | no |
| setup-axostack | yes, renamed from setup-matt-pocock-skills, Linear added as a first-class tracker with a new issue-tracker-linear.md template |
| tdd | no |
| to-spec | no |
| to-tickets | no |
| triage | no |
| writing-for-agents | no |

Not vendored, candidates for later: ask-matt (replaced by axo-mode's routing table), wayfinder, wizard, codebase-design, improve-codebase-architecture, resolving-merge-conflicts, to-questionnaire, wait-what, teach, everything under in-progress/ and misc/.

## Own skills

axo-mode (and its playbooks), setup-axostack's Linear parts, and agents/axo-agent.md are original to this repo, written in poteto-mode's shape and adapted for Claude Code.
