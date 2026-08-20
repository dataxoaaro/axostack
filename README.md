# axostack

Dataxo's agentic development stack. It combines two upstream systems into one library: the principle hierarchy from [pstack](https://github.com/cursor/plugins/tree/main/pstack) and the workflow pipeline from [mattpocock/skills](https://github.com/mattpocock/skills), routed by an entry-point skill written for Claude Code.

## Architecture

Three layers.

1. **axo-mode** is the router. Its trigger table maps situations to skills, its principles index points at the 21 leaf principles, and its playbooks (feature, bug-fix, investigation, refactoring, prototype, committing) are step lists the agent copies verbatim into its todo list.
2. **Workflow skills** are the verbs. The tracked-work loop is axostack's own, built on Pocock's pipeline: `to-linear-issue` researches an idea into an evidenced Linear issue, `to-tickets` breaks plans into dependency-ordered tickets, `triage` runs the queue, and `work-linear-issue` picks a ready issue up and drives it through `implement` → `tdd` → `code-review` to reviewed local commits. Alignment is `grill-me`/`grill-with-docs`, design is `codebase-design`/`improve-codebase-architecture`/`wayfinder`. Investigation and design rigor are pstack's: `how`, `why`, `architect`, `blast-radius`, `swarm`, `arena`, `figure-it-out`. Contested designs resolve through grilling the user, not multi-model debate. Quality gates: `unslop`, `no-comments`, `technical-writing`.
3. **Principles** are the judgment. 21 `principle-*` leaf skills from pstack, loaded only when applied, cited in the reply with the decision they changed.

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

Manual: copy folders from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project), and `agents/axo-agent.md` into `~/.claude/agents/`.

## Usage

Run `/setup-axostack` once per repo. It configures the issue tracker (Linear, GitHub, GitLab, or local markdown), triage labels, and domain doc locations that the tracker-facing skills read.

The core loop for tracked work:

1. `/to-linear-issue <idea or question>` researches it and publishes an evidenced issue.
2. `/triage` moves the queue; `/to-tickets` breaks an agreed plan into blocking-ordered tickets.
3. `/work-linear-issue ABC-123` (or bare, to take the next ready issue) claims it, branches with the key prefix, builds under axo-mode's playbooks, and closes out with commits and a tracker update.

Either invoke `/axo-mode` explicitly or let the agent reach for it on multi-step tasks. Individual skills also work standalone: `/grill-me` before a plan, `/tdd` for a feature slice, `/diagnosing-bugs` on a hard bug, `/code-review` before a commit, `/bro` when a reply needs restating in plain language.

## Provenance

Every vendored skill's source repo, commit, and modification status is recorded in [UPSTREAM.md](./UPSTREAM.md). Licenses and attribution are in [LICENSE](./LICENSE).
