# pm-routines

Three routines a product manager runs on a schedule: a sweep of what is happening in the market, a weekly metrics review, and a one-off watcher. Each one interviews you before its first run, so it works for your product rather than the author's, and each one gets sharper the longer it runs.

## The problem

A scheduled prompt is easy to write and quietly gets worse. It runs on assumptions nobody wrote down, pads a quiet week so it looks busy, skips a source that stopped working without saying so, and never learns which of its outputs were useful. A watcher written in a hurry alerts every day, or hangs on its first shell call and never alerts at all.

These routines treat a recurring job as a small system with a feedback loop, not a one-shot prompt.

## The routine structure

Every routine has the same four modes:

1. **`setup`: the intake interview.** It runs automatically the first time, or whenever the brief file is missing. One question at a time, each with a recommended default you can accept. Then a **foundation pass**: the agent researches what you did not know (competitor handles, ad-library pages, communities, which query returns your metric) and asks you to confirm it. It writes a **brief file** in a data folder you choose, shows it to you, and runs nothing until you approve it.
2. **`run`.** Reads the brief first, every time. A **readiness check** stops the run with a question if a required field is empty or the brief is past its `review_by` date, instead of running on guesswork. Every run ends with an **honest summary**: a quiet week is reported as quiet, an unreachable source is named, and every file written is read back from disk before the summary says it was written.
3. **`learn`.** You record what happened with an output: a finding was a keeper, a metric definition was wrong, an alert was noise. Stored in the routine's `LEARNINGS.md`, in your words.
4. **`tune`: the routine retro.** Every 4 runs by default, or on request, the routine reviews its own `RUN-LOG.md`: yield per source, cost per run, repeated misses, stale brief fields. It proposes concrete edits to its own brief and applies them only after you approve each one. Each tune is written up as question, evidence, what changed: the kind of entry you could paste into a lab notebook.

## What is included

| Skill | What it does |
|---|---|
| `market-sweep` | A recurring sweep of social, community and ad platforms for rising content and competitor moves. Detects which platforms your tools can reach (web search and fetch always; a Reddit tool, the YouTube Data API, an ad-library tool and a browser if installed). Covers every platform in the brief every run, applies your exclusion gates before counting anything, and delivers **transferable mechanisms** (hook, structure, emotional job), each with a relevance tier and an evidence tier. Engagement numbers are copied as displayed. The first run is a calibration run: you rate each finding keep, meh or miss, and the first tune uses those ratings. |
| `weekly-metrics-review` | A weekly scoreboard. Pulls each key result live from the exact source and query in the brief, compares week over week as "A -> B", colors the week by rules you wrote in advance, audits last week's top-3 commitments (done or slipped, with evidence), and copies in open decisions from `decisions.md`. An unreadable metric is left blank and marked "awaiting <owner or source>", never estimated. Writes `./metrics-review/YYYY-Www.md`. Its tune flags metrics unreadable two weeks running and definitions that changed mid-stream. |
| `watch-until` | "Tell me once when X becomes true, then retire." Each run performs one read-only check (an HTTP call, a CLI command or an analytics query) under a 3-minute limit with a timeout on every shell call. When the condition is true it alerts once through your channel (push notification, chat message or an email draft), writes a marker file so it never repeats, and tells you to delete the schedule. If the expiry date comes first, it says so once and retires the same way. |

Plus [`SCHEDULING.md`](SCHEDULING.md): recipes for Claude Code desktop scheduled tasks, cloud routines (`/schedule`) and plain `cron` with `claude -p`, a prompt for each routine, the guardrails every scheduled run needs, and one recipe for a weekly `decision-ledger` review digest.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install pm-routines@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`.

`weekly-metrics-review` reads the `decisions.md` file that the `decision-ledger` skill (in `product-workflows`) writes. It works without it, and says so.

## Use it

- Market sweep: "set up a market sweep", "sweep trends", "what are competitors posting", "rate the last sweep", "tune the sweep".
- Metrics review: "set up the weekly metrics review", "compile this week's review", "that metric's query was wrong", "tune the metrics review".
- Watch: "tell me when version 2 is live in the store", "let me know once the fix shows up in production", "that alert was noise".

Then schedule it with a recipe from [`SCHEDULING.md`](SCHEDULING.md). Run `setup` by hand first: a schedule cannot answer interview questions.

To change where files go, add an `## ai-pm-os settings` section to your CLAUDE.md:

```markdown
## ai-pm-os settings
- market-sweep folder: ./market-sweep/
- metrics review folder: ./metrics-review/
- watch-until folder: ./watch-until/
- decisions file: ./decisions.md
```

The defaults are the values shown. Each skill reads the setting before using its default. `decisions file` is the same setting the `decision-ledger` skill uses.

## Storage

Markdown files in the data folder are the only tested backend. `weekly-metrics-review` has a `references/using-notion.md` for anyone who wants each week as a Notion page. It is marked untested.

## Known tradeoff

The routines stop and ask rather than run on a guess. A brief with an empty required field produces a question, not a report. An unattended run that hits a question puts it at the top of its summary and stops. That means a few "not ready" runs while a brief settles in, and it is deliberate: a weekly report built on an invented number does more damage than a missing one.
