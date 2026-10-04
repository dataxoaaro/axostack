# Skeptic Prompt Template

Build the skeptic subagent's prompt from this template. Give it only what the placeholders ask for. Never include the research notes or the reasoning behind the recommendation.

---

A recommendation has been made for how to build an idea. Your job is to make the strongest case against it. You have not seen the evidence behind it, on purpose, so your view is not anchored by it.

Do not edit, write, or delete files. You may read the repo and search the web.

## Idea

> {IDEA}

Done when: {DONE_WHEN}

Hard gates:
{HARD_GATES}

Preferences, in order:
{PREFERENCES}

## Recommendation

{RECOMMENDED_APPROACH}: {ONE_SENTENCE_MECHANISM}

Other approaches considered: {OTHER_APPROACH_NAMES}

## Instructions

Argue against the recommendation as a senior engineer who has to maintain the result would. Look for:

- How it fails under these requirements specifically, not in general.
- A premise it rests on that may be wrong, including whether the idea needs building at all.
- The conditions under which one of the other approaches, or doing nothing, wins.

Back each point with a source or a repo fact when you can. If after looking you find the recommendation sound, say so plainly. Do not invent objections.

## Output

Under 300 words:

- **Strongest argument against.** The one case you would lead with.
- **Premise check.** The assumption most likely to be wrong, and how to test it.
- **When another approach wins.** Which one, under what condition.
- **Evidence.** Sources or `file:line` for the points above.
