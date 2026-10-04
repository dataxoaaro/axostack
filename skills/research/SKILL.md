---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. For comparing the ways an idea could be built, recommend `/research-idea` instead.
---

Spin up a **background agent** to do the research, so you keep working while it reads. Include the contents of [SOURCES.md](SOURCES.md) in its prompt.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it, under the tiers, freshness, and untrusted-input rules in SOURCES.md.
2. Write the findings to a single Markdown file in SOURCES.md's note layout: Takeaway, Cited findings, Inferences, Gaps.
3. Save it where `docs/agents/artifacts.md` says research notes go. No such file → match whatever convention the repo already uses, and failing that write it to `docs/research/` and say where.
