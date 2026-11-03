---
name: weekly-metrics-review
description: Use when the user wants the weekly metrics or KR review compiled ("weekly metrics review", "compile the weekly scoreboard", "how did our KRs move last week", "weekly KPI update", "did we do last week's top 3", "what's red in the metrics review", "the week so far"), when a scheduled weekly-metrics-review run starts, when they want to set up or change the metrics brief (north star, KRs, sources, owners, targets, status-color rules), record that a metric definition or target was wrong, or tune the review. Not for a one-off deep dive into a single metric, outside market evidence (market-research), or logging a decision (decision-ledger).
license: MIT
---

# Weekly metrics review: the scoreboard, plus who did what they said

Once a week: pull every key result live from its real source, compare it with last week, color the week by rules the user wrote in advance, check last week's top-3 commitments, and copy in the decisions still waiting on someone. Anything that cannot be read is left blank and marked as waiting on a named owner or source. It is never estimated.

This is a routine, not a one-shot prompt. It interviews the user first, runs from a brief it re-reads every time, records corrections, and every few runs proposes edits to itself.

## When to use

- **A weekly run**: by hand ("compile the weekly review", which reviews the week just ended) or from a schedule (see `SCHEDULING.md` at the plugin root).
- **Setting up or changing the brief**: first use, a new KR, a changed query, a new owner.
- **Recording a correction** with `learn`: "that query double-counts", "the target moved".
- **Tuning**: "tune the metrics review", or automatically every N runs.

Not for exploring why one metric moved. Investigate that separately, then record what was learned here.

## Defaults

Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Data folder:** `./metrics-review/` (setting name: `metrics review folder`). Holds `METRICS.md` (the brief), `LEARNINGS.md`, `RUN-LOG.md` and one file per review week, `YYYY-Www.md`. Create it at setup. Quote paths. If the settings rename the folder, treat every mention of `./metrics-review/` below as that path.
- **Decisions file:** `./decisions.md` (setting name: `decisions file`, shared with the decision-ledger skill). **Precedence:** the `Decisions file` field in `METRICS.md` wins when it is filled, because it is the approved path a scheduled run sees; at setup that field defaults to the `decisions file` setting, else `./decisions.md`. Read only, never written by this routine. If it does not exist, the review says so and carries on.
- **Templates:** [METRICS](assets/METRICS.template.md) for the brief, [the week template](assets/week-template.md) for each week's file.
- **Dates:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess.
- **Review week:** the ISO week (`YYYY-Www`, Monday to Sunday) the review covers. It is always the ISO week just ended: on the brief's run day (default Monday) and on any other day, the week before the current one. Get it with `date -v-7d +%G-W%V` (macOS) or `date -d '7 days ago' +%G-W%V` (GNU). The week file is named after the review week. **Last week** means the review week minus one (`date -v-14d +%G-W%V` or `date -d '14 days ago' +%G-W%V`). So "this week's review" always means the review week. Only an explicit request for the week in progress ("the week so far", "a partial review") covers the current week: then write it as `YYYY-Www-partial.md` for the current week; a partial file never counts as that week's review, so the scheduled run still writes the full one.
- **Tune cadence:** every 4 runs, or on request. The brief's `Tune every` field overrides it.
- **Storage:** markdown. If the brief's destination is Notion, read [using Notion](references/using-notion.md) (untested); the markdown week file is still written first.

## Modes (`setup` / `run` / `learn` / `tune`)

Pick the mode from the request. If the brief is missing, the mode is `setup` whatever was asked.

### `setup`: interview, foundation pass, approved brief
Follow [the intake](references/intake.md): one question at a time with a recommended default, in the order of the brief's REQUIRED fields; then a foundation pass where the agent finds the data sources and tests each query read-only, showing the value it got; then `METRICS.md` drafted with `Status: draft` and shown for approval. **Nothing runs until the user approves.** Create `LEARNINGS.md` and `RUN-LOG.md` (formats under Run), read all three back, report the paths.

### `run`: one weekly review
The Run section below. Readiness check first, every time.

### `learn`: record a correction or an outcome
The user says what happened: a definition was wrong, a target changed, a source moved, a commitment's status was misread. Append one entry to `LEARNINGS.md` with the date, the metric or item, the kind (`definition`, `target`, `source`, `audit`, `other`), and the user's words verbatim. A change to the brief itself goes through `tune` or an explicit "change the brief": never silently. Read the file back.

### `tune`: the routine retro
Every N runs (`Tune every` in the brief, default 4), or on request. Read `RUN-LOG.md`, `LEARNINGS.md`, the brief and the week files in the window, then report:
- **Metrics unreadable 2 or more weeks running**, with the owner or source each was awaiting. Propose a fix per metric: a new query, a new owner, or dropping it.
- **Definitions that changed mid-stream**: a source or query in a week file that differs from an earlier week's, so the "A -> B" comparison crossed a definition change. Propose a note on the affected weeks or a restated baseline.
- Targets already passed or plainly out of reach, owners missing, status-color rules that could not be applied, and `review_by` passed or near.
- Top-3 commitments that slipped two weeks running.

Propose concrete edits to `METRICS.md`, walk them one at a time, and apply **only the ones the user approves**, using the Edit tool on the labelled lines. If `review_by` has passed, the new date is the last question. Record the tune (question, evidence, edits applied or rejected) in `LEARNINGS.md`, add a `tune` row to `RUN-LOG.md`, read both back. In an unattended run, write the proposal into the summary and `LEARNINGS.md` as `proposed, awaiting approval`, and change nothing else. While such a proposal is still pending, an unattended run does not write a new one; its summary says one line: "a tune proposal from <date> is awaiting approval".

## Readiness check

Run this before every `run` and `tune`. Do not run degraded.

1. **If the brief file is missing → `setup`.** No `METRICS.md` in the data folder means the interview has not happened.
2. **If `Status` is not `approved`** → show the draft and ask for approval. Stop.
3. **If any field marked REQUIRED in the brief is empty, or `review_by` has passed** → ask about that field and stop. Empty means blank, an unfilled `<placeholder>`, or `needs input`. Name every empty field. The number of KRs must sit inside the brief's `KR range` (an adjustable default of 3 to 6); outside it, ask. A metric that cannot be *read* this week is not an empty field; that is handled in the run as "awaiting". **Exception:** an interactive `tune` is not blocked by a passed `review_by`; it runs, and the new date becomes its last question.
4. **`run` only (not `tune`): if the review week's file already exists**, this run would duplicate that review week. Interactive: show the existing file and ask whether to update it or stop. Unattended: append a `not ready (duplicate of <review week>)` row and stop. Never overwrite a week silently.

When nobody is there to answer (a scheduled run), "ask" means: put the question at the top of the honest summary, append a `not ready` row to `RUN-LOG.md`, and stop.

## Run

Keep a todo list so no step is skipped.

1. **Read state.** Work out the review week and last week (see Defaults). Read `METRICS.md` in full, `LEARNINGS.md` entries since the last tune, the last rows of `RUN-LOG.md`, and last week's file (review week minus one; ignore `-partial` files). If last week's file is missing, every comparison is "no prior week". Metric values cover the review week's Monday to Sunday.
2. **Pull every metric live**, exactly as the brief defines it: the named tool and the exact query, dashboard or insight id. Read-only calls only. Record the value exactly as the source returns it, the time you read it, and the query you actually ran.
   - **Unreadable** (tool missing, auth expired, query errors, source not yet built): leave the value blank and write `awaiting <owner or source>: <reason>`. Never estimate it, never reuse last week's number, never write 0 for "could not read".
   - A value the brief flags as known-broken (for example "reads 0 until the tracking fix ships") is reported with that flag, not as a real number.
3. **Compare week over week** as `A -> B` with last week's recorded value. If either side is blank, say which (`awaiting -> B`, `A -> awaiting`). If the source or query changed since last week, mark the row `definition changed`.
4. **Color the week** using the brief's status-color rules, literally. Show which rule fired. If a rule needs a value that is awaiting, do not guess the color: write `not judged: <which input is awaiting>`.
5. **Audit last week's top 3.** Last week's file listed the commitments for the review week. For each one: `done`, `slipped` or `partly`, each with the evidence (where you saw it) and the owner. With no evidence either way, write `unconfirmed: ask <owner>`. Never mark an item done on inference.
6. **Copy in open decisions** from the decisions file, if it exists (see "Reading decisions.md" below). Copy them; never invent decision text. A decision the user mentions this week that has no entry is listed as `not yet logged`.
7. **Next week's top 3** (the commitments for the week after the review week, which the next review audits). Write the commitments the user gives, verbatim, with an owner each. If none are given (a scheduled run), write `needs input` and list up to three *suggestions* drawn from this week's red and awaiting rows, labelled as suggestions. Only confirmed commitments are audited next week.
8. **Write the week file** `./metrics-review/<review week>.md` (for example `2026-W45.md`) from [the week template](assets/week-template.md). Append one row to `RUN-LOG.md`.
9. **Read back** the week file from disk: every metric row present, the status line, the audit, the decisions section, the top 3. Read back the new `RUN-LOG.md` row. Fix anything that did not land and read again, or report "not verified: <reason>".
10. **Count runs since the last tune.** If it reaches `Tune every`, run `tune` (interactive) or put the proposal in the summary (unattended).

### Reading decisions.md
The decisions file is a list of entries. Each is a `## D-NNN · <title>` heading followed by `- Label: value` bullets, one per line.
- **Parse by label, never by position.** Entries may carry extra labels (`Topic`, `Priority`, `Reasoning`, `Provenance`) in any order. Ignore labels you do not need.
- **Status** is one of `open`, `needs input`, `closed`, `superseded`. Copy entries whose Status is `open` or `needs input`, plus any whose `Review by` is a real date before today and whose Status is not `closed` or `superseded` (mark those `overdue since <date>`).
- **`needs input`** in any field means unknown: list the field as what is missing. **`none set`** in the bet fields (`Metric`, `Baseline`, `Target`, `Review by`) means a deliberate "no bet": it is not missing and is not reported as a gap.
- `Baseline` and `Target` hold values only. A bet's verdict, if any, lives in the `Outcome` text. Do not restate it as a verdict of your own.
- Copy: id, title, Owner, Status, and either what is missing or the review date. Never edit the decisions file.

### RUN-LOG.md and LEARNINGS.md formats
`RUN-LOG.md` is a table, one row per run, newest at the bottom:
`| Review week | Date | Mode | Status color | Metrics read | Awaiting (metric: owner or source) | Definition changes | Top-3 audit (done/slipped/partly/unconfirmed) | Notes |`
Mode is `run`, `tune` or `not ready` (with the reason, for example `duplicate of 2026-W45`). `LEARNINGS.md` entries are `## YYYY-MM-DD · <metric or item>` followed by `- Kind:`, `- Week:`, `- What happened: "<verbatim>"`.

## Honest summary

End every run with a short summary the user can read as a notification:
- The status color and the rule that fired, or `not judged` and why.
- Each metric in one line: `<name>: A -> B` against its target, or `awaiting <owner or source>`.
- Last week's top-3 audit: done, slipped, partly, unconfirmed.
- Open decisions copied in, by id, and anything not yet logged.
- What needs the user: commitments for next week, a reconnect or permission a source needs, a REQUIRED field, a tune proposal.
- The week file path and the read-back result, or "not verified: <reason>".

A flat week is reported as flat. An unreadable metric is named with who or what it is waiting on, never quietly dropped or filled in.

## Guardrails

- **Never fabricate a number.** Blank and `awaiting` beats a plausible guess, every time. No estimates, no carried-forward values, no zero standing in for "could not read".
- **Read-only on every data source.** Queries and dashboard reads only. Never change a dashboard, an insight, a query, a metric definition or a filter in the tool.
- **The brief's definitions are the definitions.** Never swap in a "better" query during a run. Propose it in `tune`.
- **Colors come from the rules,** not from how the week feels. Never color away bad news.
- **Decisions are copied, not written.** Never invent decision text, never edit the decisions file.
- **Commitments are the user's words.** Suggestions are labelled as suggestions and never audited as commitments.
- **Shared copies are self-contained.** A week file or page meant for a team carries no local paths or private links in its body.
- **Scheduled runs keep a hard time limit and a timeout on every shell call** (see `SCHEDULING.md`). One retry on a failing source, then mark it awaiting and move on.
