---
status: accepted
---

# Factory behavior lives in a separate pack, not in the developer skills

axostack's skills are for a developer who runs them by hand and answers their questions. An AI software factory needs the same stations to run with no human attached. Skills in that mode have to research facts, record the decisions they assumed, stop with an outcome a machine can read, and work under enforced permissions. We decided to keep axostack as the developer pack. The factory versions go into a separate pack, provisionally called axo-factory, that reuses axostack's artifacts and skill content. We did not add autonomy flags or an unattended mode to each developer skill. A flag in every skill would branch every station on whether a human is present. It would make the bodies longer to read and widen the gap from the upstream skills they are ported from. It would also put factory risk into the tools developers use every day.

## Considered options

- **An autonomy argument or unattended rule in every axostack skill.** Rejected for the reasons above. It looks cheaper at first, and it is the option a later contributor is most likely to propose again.
- **One orchestrator skill that runs forked stations.** Rejected. Forked subagents cannot ask the user, and Claude Code ignores hooks and permission fields on plugin agents.
- **Adopting an external factory runtime, such as the eve template or Cyrus.** Rejected for now. Each adds an app or a daemon that one maintainer has to run.

## Consequences

- axostack skills keep their questions. A question that blocks a factory run is an axo-factory problem, not a reason to remove the question from the developer skill.
- axostack keeps the section headings of the documents its skills write stable: plan, tickets, review report, PR body, and run records. axo-factory relies on those headings.
- `docs/research/axo-factory-direction.md` describes the target.
- `docs/research/lean-developer-skills-for-a-future-factory.md` records the developer-side decision.
