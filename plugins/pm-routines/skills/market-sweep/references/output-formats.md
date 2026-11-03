# Output formats

Every run writes, in this order: the sweep file, the run-log row, the watchlist updates, and (only if the brief names a summary channel) a short summary post. Each has a different reader. The sweep file is the full record; the run log is what `tune` reads; the summary is the notification.

## 1. The sweep file: `<output destination>/YYYY-MM-DD.md`

The output destination defaults to `sweeps/` inside the data folder; the file goes directly in it.

The complete record, including everything that failed or was skipped. If two runs land on one date, add `-2` to the second.

```markdown
# Market sweep · YYYY-MM-DD

- Run health: Full | Partial (<what was skipped>) | Quiet week | Failed
- Calibration run: yes | no
- Covered: <platform>, <platform>, ...
- Skipped: <platform> (<reason>), ... | none
- Findings: <n> total · <n> core · <n> adjacent · <n> craft-only · <n> new to the brief
- Inbox: <n> drops triaged | no inbox

## Headline
One sentence. The single thing worth knowing from this run.

## Patterns (three or more independent examples each)
### <named mechanism>
- Evidence: <link> (<engagement as displayed>), <link> (...), <link> (...)
- Why it works now: <the mechanism, not the topic>
- What you could do with it: <concrete, this cycle>
- Confidence: High | Medium | Low (<plain-word reason>)

## Possible, watch it (two examples, not yet a pattern)

## Competitor moves
Per competitor: what changed since the last sweep, live ad count as displayed, notable claims, with links and dates.

## Findings
One block per finding, ordered core, then adjacent, then craft-only:
### F<n> · <short label naming the mechanism>
- Platform · format · author: ...
- URL: ...
- Posted: YYYY-MM-DD | not shown
- Hook (verbatim): "..."
- Beat map: hook -> ... -> landing
- Emotional job: ...
- Travels as: Save | Share | Comment-bait | Watch-through (inferred from <basis>, if inferred)
- Engagement: <as displayed>
- Relevance: core | adjacent | craft-only
- Evidence tier: A | B | C | D
- Transferable: Yes | Yes with changes (<change>) | No (<red line>)
- Adaptation: ...

## Feature demand (core tier only; logged signal, not a roadmap)
## Pricing and positioning
## Seeds
## What did not travel
## What changed since the last sweep
## Off-brand but notable
## Skipped and why
## Query health
Queries that returned nothing, with the platform. A dead query silently returning zero looks the same as "no trend".
```

Include only the sections the brief's goals call for; keep "Skipped and why" and "Query health" always. In a quiet week, the file may be four lines long. Do not pad it.

On a calibration run, number every finding (`F1`, `F2`, ...) so the user can rate them by number.

## 2. The run-log row

Append one row to `RUN-LOG.md` per run, in [the template](../assets/RUN-LOG.template.md)'s columns. Count honestly:
- **Candidates** are items you captured. **Kept** are items that became findings after the gates. Record both per source, because yield (kept out of candidates) is what `tune` prunes on.
- **Cost** is whatever this environment actually reports (tokens, tool calls, run time). If nothing is reported, write `not measured`. Never estimate cost as fact.

## 3. Watchlist updates

In `WATCHLIST.md`: set `Last run`, update `Inbox last processed`, and record query health (queries that returned nothing this run). Add newly spotted accounts, communities and competitors as `candidate - confirm?` with the date found. A candidate seen in two runs is flagged for promotion at the next tune; it is never promoted without the user's yes.

## 4. The summary post (optional)

Only if the brief names a summary channel. Short enough to read on a phone, no preamble, under about two hundred words:

```
Market sweep · <date> · <run health>
Coverage: <platform> ok · <platform> ok · <platform> skipped (<reason>) · explore: <n> new
Headline: <one sentence>
Patterns: <mechanism> (<n> examples, <confidence>) -> <what to do>
Best core finding: "<verbatim hook>" (<platform>, <engagement as displayed>)
Competitor moves: <one line, or "none notable">
Needs you: <candidates to confirm, ratings, a sign-in, a tune proposal, or "nothing">
```

Lead with run health, so a partial run is never mistaken for a full one. Never post invented findings to cover a quiet week: post the quiet week. After posting, read the message back from the channel where the tool allows it; otherwise say "posted, not verified: <reason>".

Every finding keeps its source link on every surface. Every claim is one click from its evidence.
