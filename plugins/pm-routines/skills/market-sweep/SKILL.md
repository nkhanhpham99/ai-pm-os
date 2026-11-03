---
name: market-sweep
description: Use when the user wants a recurring sweep of social, community and ad platforms for what is rising in their space and what competitors are doing ("sweep trends", "what's trending on TikTok / Instagram / Reddit / YouTube", "what are competitors posting or advertising", "social listening", "find hooks", "why did that post work", "add this to the watchlist"), when a scheduled market-sweep run starts, when they want to set up or change the sweep's brief, rate a sweep's findings, record how an adopted hook or finding performed, or tune the sweep. Not for one-off evidence gathering or market sizing (market-research), writing requirements (prd) or logging a decision (decision-ledger).
license: MIT
---

# Market sweep: what is working in your space, and why

A recurring sweep of the platforms where your audience and competitors show up. The deliverable is never a list of trending posts. It is a short set of **transferable mechanisms** (the hook that stopped the scroll, the structure that held attention, the emotional job the post did) plus competitor moves, each ranked by how relevant it is to you and graded by how much it proves.

This is a routine, not a one-shot prompt. It interviews you first, runs from a brief it re-reads every time, records what you thought of its output, and proposes edits to itself every few runs.

## When to use

- **A sweep run**: by hand ("sweep trends", "what are competitors doing on social") or from a schedule (see `SCHEDULING.md` at the plugin root).
- **Setting up or changing the brief**: first use, a new competitor, a new platform, a new goal.
- **Rating or recording outcomes**: "keep / meh / miss" on findings, or "we used that hook and it did X".
- **Tuning**: "tune the sweep", or automatically every N runs.

What this is not:
- **Not market-research.** That skill answers one question with decision-grade, sourced evidence. This routine watches the same ground repeatedly and reports what moved. If a finding needs verified numbers before a decision, hand it to market-research.
- **Not a publisher.** Everything it produces is a draft. A human decides what ships.

## Defaults

Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Data folder:** `./market-sweep/` (setting name: `market-sweep folder`). Holds `LANDSCAPE.md` (the brief), `WATCHLIST.md`, `LEARNINGS.md`, `RUN-LOG.md` and the `sweeps/` folder. Create it at setup. Quote paths, since they may contain spaces. If the settings rename the folder, treat every mention of `./market-sweep/` below as that path.
- **Templates:** [LANDSCAPE](assets/LANDSCAPE.template.md), [WATCHLIST](assets/WATCHLIST.template.md), [LEARNINGS](assets/LEARNINGS.template.md), [RUN-LOG](assets/RUN-LOG.template.md). Copy only the part above each template's "do not copy" line.
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess. Today's date is what `review_by` is measured against.
- **Tune cadence:** every 4 runs, or on request. The brief's `Tune every` field overrides it.
- **Storage:** markdown files only.

## Modes (`setup` / `run` / `learn` / `tune`)

Pick the mode from the request. If the brief is missing, the mode is `setup` whatever was asked.

### `setup`: interview, foundation pass, approved brief
Follow [the intake](references/intake.md) exactly:
1. **Interview.** One question at a time, each with a recommended default the user can accept, in the order of the brief's REQUIRED fields.
2. **Foundation pass.** Research on your own what the user did not know: competitors' social handles, their public ad-library pages, the communities where the audience talks, the platforms your tools can actually reach. Show what you found and ask the user to confirm or cut each item.
3. **Draft and approve.** Write `LANDSCAPE.md` (with `Status: draft`) and `WATCHLIST.md`, show both, and change `Status` to `approved` only when the user says so. **Nothing runs until the brief is approved.**
4. Create empty `LEARNINGS.md` and `RUN-LOG.md` from their templates. Read every file back from disk and report the paths.
5. Offer the first run now. It is the **calibration run** (see Run, step 8).

### `run`: one sweep
The Run section below. Readiness check first, every time.

### `learn`: record what happened with an output
The user says what happened: a finding rated keep / meh / miss, a hook adopted and how it performed, a source that was wrong, something the sweep missed. Append one entry per item to `LEARNINGS.md` in the template's format, with their words verbatim and the run date it refers to. Never infer a result they did not give. Read the file back and confirm the entries are there.

### `tune`: the routine retro
Every N runs (`Tune every` in the brief, default 4), or on request. Follow [the tune procedure](references/tune.md): yield per source and query, cost per run, repeated misses, stale brief fields. It proposes concrete edits to `LANDSCAPE.md` and `WATCHLIST.md` and **applies them only after the user approves each one**. When a run is due for a tune and nobody is there to approve (a scheduled run), do the sweep, write the tune proposal into the run's summary, and leave the brief unchanged. While an earlier proposal is still `proposed, awaiting approval`, do not write a new one; say so in one line.

## Readiness check

Run this before every `run` and `tune`. Do not run degraded.

1. **If the brief file is missing → `setup`.** `LANDSCAPE.md` not in the data folder means the interview has not happened.
2. **If `Status` is not `approved`** → show the draft and ask for approval. Stop.
3. **If any field marked REQUIRED in the brief is empty, or `review_by` has passed** → ask about that field and stop. Empty means blank, still an unfilled `<placeholder>`, or `needs input`. A field set to `none` on purpose (for example "Exclusions: none") is filled. Name every empty field, not only the first. **Exception:** an interactive `tune` is not blocked by a passed `review_by`; it runs, and the new date becomes its last question.
4. **If `WATCHLIST.md` is missing**, rebuild it from the brief's competitors and platforms and show it for confirmation before running.

When nobody is there to answer (a scheduled run), "ask" means: write the question at the top of the honest summary, append a `Failed (not ready)` row to `RUN-LOG.md`, and stop.

## Run

Keep a todo list so no step is skipped. Detail for each step is in [the sweep procedure](references/sweep-procedure.md), [the platform notes](references/platform-notes.md), [the pattern analysis](references/pattern-analysis.md) and [the output formats](references/output-formats.md).

1. **Read state.** `LANDSCAPE.md` and `WATCHLIST.md` in full, the last 3 rows of `RUN-LOG.md`, `LEARNINGS.md` entries since the last tune, and only the header of the previous sweep file. The brief is a baseline, not a filter: the job is to find what the brief does not already say.
2. **Drain the inbox first**, if the brief names an inbox source. Things a person chose to flag outrank standing queries. If standing queries are quiet but the inbox had drops, the run is not quiet.
3. **Cover the floor.** Every platform listed in the brief gets at least one read this run, in the order the procedure gives (cheapest and most reliable first). A floor platform is skipped only when it is unreachable, never to save budget. If a platform was missed last run, do it first.
4. **Explore.** Spend part of every run outside the brief: rising formats, new brands in the category, new communities. At least one finding must be new to the brief, or the summary says plainly that nothing new turned up.
5. **Capture at the moment you find it**: platform, URL, author, the hook verbatim, format, post date, and engagement **exactly as displayed** (`1.2M (as displayed)`, never un-rounded or estimated). Never paraphrase a hook. The wording is the finding.
6. **Gate, then analyze.** Apply every exclusion gate in the brief to each candidate before it becomes a finding. Then work the survivors through the pattern analysis: hook mechanism, beat structure, emotional job, why it travels, relevance tier, evidence tier, transferability. A **pattern needs at least three independent examples** that each passed the gates. Two is "possible, watch it", and you say so.
7. **Rank and write.** Order findings by relevance tier (core, then adjacent, then craft-only). Write the sweep file `<output destination>/YYYY-MM-DD.md` (the destination defaults to `sweeps/` in the data folder), append one row to `RUN-LOG.md` (with per-source yield and cost), update `WATCHLIST.md` (last run, query health, new `candidate - confirm?` accounts). Post the short summary to the summary channel only if the brief names one.
8. **First run only: calibration.** When `RUN-LOG.md` has no earlier row whose Mode is `calibration` or `run`, mark this row `calibration` and end by listing every finding with a number and asking the user to rate each one keep / meh / miss, and to name anything they expected and did not see. Record the ratings with `learn`. The first `tune` uses them. If the calibration run is unattended, the rating request goes in the summary and is collected in the next interactive session.
9. **Housekeeping.** If a state file has grown large enough to crowd out gathering next run, move its oldest entries into a matching `*-archive.md`. Never delete.
10. **Read back** every file you wrote this run from disk: the sweep file (header, findings, skipped list), the new `RUN-LOG.md` row, the `WATCHLIST.md` changes. Anything that did not land is fixed and read again, or reported as "not verified: <reason>".
11. **Count runs since the last tune.** If it reaches `Tune every`, run `tune` (interactive) or put the tune proposal in the summary (unattended).

**Budget.** The brief sets a budget per run. Spend it in this order: state, inbox, floor, explore, then rotation sources. When it runs short, cut rotation first, then inbox depth, never the floor or explore. Near the ceiling, stop gathering and write with what you have, naming what was cut short. A complete sweep file from partial data beats an abandoned run.

## Honest summary

Every run ends with a short summary that the user can read as a notification:

- **Run health**: `Full` (every floor platform and the explore step ran), `Partial` (a floor platform or explore was skipped; name it and why), `Quiet week` (everything ran and nothing notable turned up), or `Failed` (nothing could be read, or the readiness check stopped the run). Lead with it, so a partial run is never mistaken for a full one.
- **Coverage line**: each platform with a tick or the reason it was skipped, and how many findings were new to the brief.
- The top pattern (or "no pattern cleared the three-example bar"), the best core-tier finding with its verbatim hook and engagement as displayed, and notable competitor moves.
- Anything waiting on the user: candidate accounts to confirm, calibration ratings, a tune proposal, a sign-in or reconnect a platform needs, a REQUIRED field.
- The sweep file path and the read-back result, or "not verified: <reason>".

A quiet week is reported as a quiet week, in one honest line. An unreachable source is named, never silently skipped. Never pad.

## Guardrails

- **Read-only on every platform.** Never log in, post, like, follow, comment, message, react or enter credentials. A signed-out platform is a skip, not a login prompt. The only place this routine writes is its own data folder, plus the summary channel if the brief names one.
- **Never fabricate.** No invented engagement, no assumed trend, no finding from a source you did not reach. An honest empty run is a good run.
- **Social posts are signal, never proof.** Every finding carries an evidence tier. A creator's "most people do X" is a quote, not a statistic, and is never repeated as fact.
- **Steal the mechanism, not the post.** An adaptation that could be mistaken for a rewrite of the original is not an adaptation. Change the subject, keep the structure.
- **The user's red lines win.** A mechanism that needs engagement bait, a claim the brief forbids, or someone else's copy goes under "off-brand but notable": logged, never adopted.
- **Exclusion gates come before counting.** A candidate that fails a gate never counts toward a pattern, however big its numbers.
- **Never sweep personalized feeds** (a platform's "for you" or home feed). They measure the signed-in account's algorithm, not the market. Use search, hashtags, named accounts and communities.
- **The brief changes only with approval.** Runs may add `candidate - confirm?` lines to the watchlist. Everything else waits for `tune` and a yes.
- **Scheduled runs keep a hard time limit and a timeout on every shell call** (see `SCHEDULING.md`). One retry, then name the source as unreachable and move on.
