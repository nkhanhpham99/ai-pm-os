# Tune: the routine retro

Every N runs (the brief's `Tune every`, default 4), or whenever the user asks, the sweep reviews its own record and proposes edits to itself. The point is that the routine gets sharper with use instead of accumulating noise. Nothing in the brief or watchlist changes until the user approves.

## Inputs

- `RUN-LOG.md`: the rows since the last tune (or all rows, for the first tune).
- `LEARNINGS.md`: ratings (keep / meh / miss), outcomes of adopted findings, reported misses, corrections.
- `WATCHLIST.md`: query health, candidates, inbox marker.
- `LANDSCAPE.md`: every field, especially `review_by`.
- The headers of the sweep files in the window.

## What to compute

Show the numbers you computed and where they came from. If an input is missing (a run with `not measured` cost, a finding nobody rated), say so instead of filling it in.

1. **Yield per source and per query.** Candidates captured, findings kept, and, where ratings exist, how many kept findings were rated keep. A source with candidates but no kept findings across the window is a pruning candidate. A query that returned nothing in every run of the window is dead.
2. **Cost per run.** As recorded. Note which sources took the most and whether the floor fit inside the budget. If the floor did not fit, say whether to raise the budget or drop a platform.
3. **Repeated misses.** Things the user said the sweep should have caught (`miss` ratings and "you missed X" notes). Group them: a missing platform, a missing competitor, a query in the wrong words, a gate that is too strict.
4. **Rated noise.** Findings rated `meh` or `miss` that share a source, a tier or a mechanism. A tier that keeps producing meh findings may be drawn too wide.
5. **Stale brief fields.** `review_by` passed or near, competitors not seen in any run of the window, a goal that produced no findings, candidates seen twice and still unconfirmed, a summary channel or inbox that failed.
6. **Coverage health.** Floor platforms skipped in two runs running, and why.

## The proposal

Write a short, numbered list of concrete edits. Each edit says what changes, in which file, and why, citing the numbers above:

```markdown
## Tune · YYYY-MM-DD (runs <first date> to <last date>)

Question: is the sweep spending its budget where the keepers come from?
Evidence: <the computed table, short>
Proposed edits:
1. WATCHLIST: drop query "<query>" on <platform>. Zero candidates in every run of the window.
2. WATCHLIST: add community <name> (<url>). Two of the misses were discussed there.
3. LANDSCAPE: move "<theme>" from core to adjacent. Most of its findings were rated meh.
4. LANDSCAPE: add exclusion gate "<gate>". Three findings rated miss were <kind>.
5. LANDSCAPE: promote candidate <brand> to the competitor roster. Seen in two runs.
Not changing: <anything considered and rejected, with the reason>
```

Then walk the edits **one at a time** and ask yes, no or change. Apply only the approved ones, using the Edit tool on the labelled lines. Never rewrite the whole file. When `review_by` has passed, the last question is the new date. (The readiness check lets an interactive tune run with a passed `review_by` for exactly this reason.)

## Recording the tune

1. Append the tune block above to `LEARNINGS.md`, with each edit marked `applied`, `rejected` or `changed to <what>`. Written this way, each tune is an entry the user could paste into a lab notebook: the question, the evidence, what changed, what to watch next.
2. Append a `tune` row to `RUN-LOG.md`, so the next tune knows where its window starts.
3. Read back `LANDSCAPE.md`, `WATCHLIST.md`, `LEARNINGS.md` and `RUN-LOG.md` from disk and confirm each approved edit landed. Report what changed in one line per file, or "not verified: <reason>".

## Unattended runs

A scheduled run cannot ask for approval. When a tune is due in an unattended run, compute the numbers and write the proposal into the honest summary and into `LEARNINGS.md` marked `proposed, awaiting approval`. Change nothing else. The next interactive session walks the proposal.

While a `proposed, awaiting approval` entry is still pending in `LEARNINGS.md`, an unattended run does not propose again. Its summary says one line instead: "a tune proposal from <date> is awaiting approval". The window for the next tune still starts at the last `tune` row in `RUN-LOG.md`, so nothing is lost by waiting.
