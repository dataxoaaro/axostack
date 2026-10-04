# HTML Report Format

The report is one self-contained HTML file in the OS temp directory. Tailwind and Mermaid come from CDNs. Mermaid draws flows and sequences. Hand-built divs and inline SVG draw the editorial visuals (where the work happens, what sits on whose side of a dependency). Mix the two so every diagram doesn't look the same.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Research: {{idea}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict" });
    </script>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="premise">...</section>
      <section id="approaches" class="space-y-10">...</section>
      <section id="comparison">...</section>
      <section id="cut">...</section>
      <section id="recommendation">...</section>
      <section id="open-questions">...</section>
    </main>
  </body>
</html>
```

## Header

The idea in one sentence, the "done when" line, and the date. Under it, the requirements as two rows of chips: hard gates (dark) and preferences (outlined, in order). A compact legend for the badges. No introduction paragraph.

## Premise

A small panel with three lines: is this the right problem, what happens if we do nothing, what already solves part of it. Each line is the answer, not the question restated.

## Approach card

One `<article>` per finalist. Order them by effort, smallest first, not by rank, so the reader forms a view before reaching the recommendation.

- **Title.** Names the approach by its mechanism: "Adopt a durable job queue", not "Option B".
- **Badge row.** Recommendation strength, then origin, then effort:
  - Strength: `Strong` emerald, `Worth exploring` amber, `Speculative` slate, `Hold` rose (a Hold badge carries a one-line "settled by" note).
  - Origin: `reuse`, `extend`, `adopt`, or `build`.
  - Effort: `S`, `M`, `L`, or `XL`.
- **Today / With this approach.** The centrepiece: two diagrams side by side. See the patterns below.
- **How it works.** One sentence, at the level of mechanism. No file paths or schemas.
- **Gates.** One pill per hard gate: `pass` emerald, `partial` amber, `unknown` slate. A `fail` never appears, because a failing approach was cut.
- **Wins** and **Costs.** Bullets of six words or fewer each.
- **Lock-in.** One line: what you depend on, and what leaving would take.
- **Evidence.** Two to four citations, each a link with its date and a status pill: `verified`, `disputed`, or `unverified`.

No paragraphs of explanation. If a diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that shows where the approaches actually differ.

### Flow (Mermaid flowchart)

When the approaches differ in what calls what. Today on the left, the approach on the right. Color new parts in the accent and removed parts struck through or faded.

```html
<div class="grid grid-cols-2 gap-4">
  <div class="rounded-lg border border-slate-200 bg-white p-4">
    <p class="text-xs uppercase tracking-wider text-slate-500">Today</p>
    <pre class="mermaid">
      flowchart LR
        Editor --> SaveButton --> API
    </pre>
  </div>
  <div class="rounded-lg border border-emerald-300 bg-white p-4">
    <p class="text-xs uppercase tracking-wider text-emerald-700">With this approach</p>
    <pre class="mermaid">
      flowchart LR
        Editor --> LocalDraft --> SyncWorker --> API
        classDef new fill:#d1fae5,stroke:#059669;
        class LocalDraft,SyncWorker new
    </pre>
  </div>
</div>
```

### Sequence (Mermaid sequenceDiagram)

When the approaches differ in round trips, ordering, or who waits on whom.

### Ownership split (hand-built)

When the question is build versus adopt. A horizontal bar divided into "our code" and "their code", sized by how much of the behavior each owns. Adopt approaches show a thin slice of ours. Build approaches show the reverse.

### Reach (hand-built)

When the approaches differ in how much of the system they touch. A row of boxes, one per module or service, with the touched ones filled.

## Comparison

One table. Rows are the finalists plus **Keep what we have**. Columns are each hard gate, each preference, effort, and lock-in. Cells hold `pass` / `partial` / `unknown` pills or a few words. The baseline row may also show `fail` (rose), since it usually misses the done-when line. No weighted total or overall score: a summed score hides the weighting the user should be making.

## Cut

One line per candidate cut in Phase C: its name and why it lost (failed a gate, a variant of another approach, no basis).

## Recommendation

One larger card, after everything above:

- **Pick.** The approach, linked to its card, and one sentence on why it wins under these requirements.
- **Runner-up.** The approach and the condition under which it would win instead.
- **Strongest argument against.** The skeptic's case, quoted or closely paraphrased, and your answer to it, or a plain statement that it stands.
- **Reversal.** What it would cost to back out of this choice later.

## Open questions

The decisions the grilling phase will take up, numbered, each with a recommended answer.

## Style

- Lean editorial, not corporate dashboard. Generous whitespace. `font-serif` headings work well with stone and slate.
- One accent (emerald) plus amber for partial and rose for Hold.
- Keep diagrams around 320px tall so Today and With this approach sit side by side without scrolling.
- `text-xs uppercase tracking-wider` for labels inside diagrams.
- The only scripts are the Tailwind CDN and the Mermaid import. No other interactivity.

## Tone

Plain words, concise. Name approaches and parts by what they do and by the `GLOSSARY.md` terms when the repo has them. No hedging and no throat-clearing. If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it.
