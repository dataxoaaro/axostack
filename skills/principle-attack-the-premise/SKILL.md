---
name: principle-attack-the-premise
description: "Apply when repeated fixes rely on the same assumption and fail the same check. Test the shared assumption before attempting another fix."
---

# Attack the premise

When repeated fixes rely on the same assumption and fail the same check, write down that assumption and design a measurement that could disprove it.

- Name what the failed fixes assumed and what observation would contradict it.
- Run the measurement before another fix. Keep the probe reproducible, per **principle-build-the-lever**.
- For an imbalance, measure the distribution by actor before changing the mechanism. If the same actors repeatedly hold the imbalance, investigate how work or ownership is assigned, per **principle-fix-root-causes**.
- An even distribution rules out the measured skew in that run. It does not establish that every shared assumption is correct.
- If the evidence contradicts the assumption, revise the explanation before changing the code. If it does not, record what the measurement leaves unresolved and choose the next discriminating check.

Use a measurement suited to the suspected cause. An actor census helps investigate an imbalance, but a parser defect or stale configuration needs a different probe.
