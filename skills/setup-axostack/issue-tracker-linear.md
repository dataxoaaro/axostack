# Issue tracker: Linear

Issues and specs for this repo live in Linear, accessed through the Linear MCP server. Tool names vary between Linear MCP versions, so discover the exact names from the available tools (or ToolSearch) before the first call. The operations below name the capability; bind each to whichever tool provides it.

**Team**: _(fill in the Linear team name or key for this repo)_
**Project**: _(optional: the Linear project new issues default to)_

## Conventions

- **Create an issue**: the issue-create/save tool, with team, title, and markdown description. Record the returned issue key (e.g. `ABC-123`).
- **Read an issue**: the issue-get tool by key, plus the comment-list tool for discussion.
- **List issues**: the issue-list tool filtered by team, state, and label.
- **Comment on an issue**: the comment-create/save tool with markdown body.
- **Apply / remove labels**: the label tools; create a missing label before applying it.
- **Close**: set the issue's state to the team's Done state via the issue-update tool.

## Branch and commit conventions

The issue key prefixes the branch name (`abc-123-short-description`), which lets Linear link the branch automatically. The key also goes in the commit message body and PR title. Never write the key in code comments, docstrings, or identifiers.

## When a skill says "publish to the issue tracker"

Create a Linear issue in this repo's team and report its key and URL.

## When a skill says "fetch the relevant ticket"

Read the issue by key, including comments.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a parent issue with **child** sub-issues as tickets.

- **Map**: one issue labelled `wayfinder-map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: a sub-issue of the map (set parent on create). Label `wayfinder-<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, assign the driving dev.
- **Blocking**: Linear's native "blocked by" relation between issues. A ticket is unblocked when every blocker is Done.
- **Frontier query**: list the map's open children, drop any with an open blocker or an assignee; first in map order wins.
- **Claim**: assign the issue to yourself, the session's first write.
- **Resolve**: comment the answer, set state to Done, then append a context pointer to the map's Decisions-so-far.
