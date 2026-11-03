---
name: watch-until
description: Use when the user wants to be told once when something becomes true, then stop ("tell me when X is live", "watch until", "let me know once the fix reaches production", "alert me when the new version is in the store", "ping me when the certificate is renewed", "check daily whether the flag is on"), when a scheduled watch-until run starts, or when they want to set up, change, rate or retire a watch ("was that alert useful", "tune the watch", "stop watching"). Not for recurring reports (weekly-metrics-review) or trend sweeps (market-sweep).
license: MIT
---

# Watch until: tell me once, then retire

A small scheduled check for a one-off question: "has X happened yet?" Each run performs one read-only check. The first time the answer is yes, it alerts once, writes a marker file so it never alerts again, and tells the user to delete the schedule. If the expiry date comes first, it says so once and retires the same way.

This is a routine, not a one-shot prompt: it interviews the user first, runs from a brief it re-reads every time, records whether its alert was useful, and can tune its own check.

## When to use

- **Setting up a watch**: "tell me when the new version is live in the store", "let me know once the fix shows up in production traffic", "ping me when the certificate is renewed".
- **A scheduled run** of an existing watch (see `SCHEDULING.md` at the plugin root).
- **Rating or tuning**: "that alert was noise", "the check keeps timing out", "extend the watch".
- **Retiring**: "stop watching X".

Not for anything that should report every time it runs. That is a recurring report, not a watch.

## Defaults

Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Data folder:** `./watch-until/` (setting name: `watch-until folder`). Each watch has its own subfolder, `./watch-until/<watch-slug>/`, holding `WATCH.md` (the brief), `RUN-LOG.md` and `LEARNINGS.md`. Quote paths. If the settings rename the folder, treat every mention of `./watch-until/` below as that path.
- **Marker path:** `./watch-until/<watch-slug>/ALERTED` unless the brief says otherwise. For scheduled runs, write it in the brief as an absolute path, since a schedule may start in a different folder.
- **Template:** [WATCH](assets/WATCH.template.md). Copy only the part above its "do not copy" line.
- **Time limit:** 3 minutes per run, and a timeout on every shell call (see Guardrails).
- **Dates:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess. Today's date is what the expiry date is measured against.
- **Tune cadence:** every 4 runs, or on request.

## Modes (`setup` / `run` / `learn` / `tune`)

Pick the mode from the request. If the brief is missing, the mode is `setup` whatever was asked.

### `setup`: interview, test the check, approved brief
Ask **one question at a time**, each with a recommended default, in the order of the brief's REQUIRED fields:
1. **Condition**, in plain words. "What should become true?" Default: the user's own sentence, restated.
2. **Read-only check.** "How can I tell, without changing anything?" Propose one: an HTTP GET to a public endpoint, a CLI command that only reads, or an analytics query. Prefer the cheapest check that answers the question. Default: the one you propose after a quick look at what is reachable.
3. **True when.** "What exact output counts as yes?" Make it mechanical: a field value, a status code, a row count, a threshold. Also ask what counts as **unclear** (too little data, an empty response). Default: drafted from the check's actual output.
4. **Alert channel.** Push notification, a chat message to a named channel, or an email **draft** (never sent). Default: whichever notification tool this session has; ask if none. Then draft the alert message and get it approved.
5. **Expiry date.** "After what date should I give up and tell you?" Default: one month from today.
6. **Marker path.** Default: `./watch-until/<watch-slug>/ALERTED`, written as an absolute path.

Then:
- **Prove the check is read-only.** It must not write, post, deploy, delete or change state anywhere: HTTP GET or HEAD only, SQL `SELECT` only, CLI subcommands that only read. Refuse anything else and propose a read-only alternative.
- **Run it once now**, with the time limit and timeouts, and show the user the raw output and how "true when" evaluates on it. If it is already true, say so: there is nothing to watch.
- Write `WATCH.md` with `Status: draft`, show it, and set `Status: approved` only on the user's yes. **Nothing is scheduled or run until then.** Create `RUN-LOG.md` and `LEARNINGS.md` (formats under Run). Read all three back from disk and report the paths.
- Give the user the scheduling recipe from `SCHEDULING.md`, with the absolute path to `WATCH.md` filled in. This skill never creates the schedule itself.

### `run`: one check
The Run section below. Readiness check first, every time.

### `learn`: was the alert useful?
Record what the user says about an alert or a run: useful, noise, a false positive, too late, or a check that misread the output. Append to `LEARNINGS.md` with the date and their words verbatim. Read it back.

### `tune`: the routine retro
Every 4 runs, or on request. Read `RUN-LOG.md` and `LEARNINGS.md` and report: runs that errored or timed out, runs that were `unclear` and why, how close the check comes to the time limit, how far away the expiry date is, and any learnings about false positives. Propose concrete edits to `WATCH.md` (a faster check, a sharper "true when", a new expiry date) and apply **only the ones the user approves**. In an unattended run, put the proposal in the summary and change nothing.

## Readiness check

Run this before every `run`.

1. **If the brief file is missing → `setup`.**
2. **If the marker file exists** → the watch has already alerted (or expired). Do not check, do not alert. One line: "<watch> already alerted on <date from the marker>. Delete or disable its scheduled task." Stop.
3. **If `Status` is not `approved`** → ask for approval and stop.
4. **If any field marked REQUIRED in the brief is empty** → ask about that field and stop. Empty means blank, an unfilled `<placeholder>`, or `needs input`. Name every empty field.
5. **If the expiry date has passed** (the brief's `review_by` is its expiry date) → retire: send one expiry notice through the alert channel ("<condition> did not become true before <expiry>; this watch has stopped"), write the marker with `expired` and today's date, read the marker back, tell the user to delete the schedule, and stop.

When nobody is there to answer (a scheduled run), "ask" means: put the question in the honest summary, append a `not ready` row to `RUN-LOG.md`, and stop.

## Run

The whole run must finish inside the time limit. Keep it to the steps below.

1. **Read `WATCH.md`.** Only that file and the last row of `RUN-LOG.md`. Each run starts fresh; everything it needs is in the brief.
2. **Perform the check** exactly as written in the brief. Do not improvise a different check. Every shell call carries a timeout (see Guardrails). If the call hangs, errors or times out, retry **once**. If it fails again, record `error`, write "could not check today: <reason>" in the summary, and stop. An error never alerts.
3. **Evaluate "true when"** against the raw output, literally. The result is one of:
   - `true`: the output meets the brief's "true when".
   - `false`: it does not.
   - `unclear`: the output meets the brief's "unclear when", or cannot be parsed. Unclear never alerts.
4. **If `false` or `unclear`**: append a `RUN-LOG.md` row and stop. The summary is one line with what was observed.
5. **If `true`**:
   1. **Alert once** through the brief's channel, with the approved message. Fill its blanks only with values actually observed in this run's output.
   2. **Verify the alert landed** where the channel allows: read the chat message back, or fetch the email draft. A push notification cannot be read back: say "sent, not verified: push notifications cannot be read back".
   3. **Write the marker file** with the date, the observed value and the alert channel. If the alert call failed, do **not** write the marker; say "alert failed: <reason>; the next run will try again".
   4. **Read the marker back** from disk.
   5. **Retire**: tell the user the watch is done and how to delete or disable its scheduled task (see `SCHEDULING.md`). Never delete or edit the schedule yourself.
6. **Append one row to `RUN-LOG.md`** and read it back.

### RUN-LOG.md, LEARNINGS.md and marker formats
`RUN-LOG.md` is a table, newest at the bottom: `| Date | Result | Observed | Duration | Notes |`. Result is `true`, `false`, `unclear`, `error`, `not ready`, `already alerted`, `expired` or `tune`. Observed is a short excerpt of the raw output, never a paraphrase.
`LEARNINGS.md` entries are `## YYYY-MM-DD · <short label>` followed by `- Kind: useful | noise | false positive | late | misread | tune` and `- What happened: "<verbatim>"`.
The marker is a small text file: `alerted YYYY-MM-DD` (or `expired YYYY-MM-DD`), then `observed: <excerpt>` and `channel: <channel>`.

## Honest summary

Every run ends with a short summary:
- **Usually one line**: "<watch>: still false (observed <excerpt>), checked <date>", or "unclear (<why>)", or "could not check today: <reason>".
- **On true**: what became true, the observed value, where the alert went and whether it was verified, that the marker was written and read back, and how to delete the schedule.
- **On expiry**: that the watch gave up on its expiry date, that the notice went out, and how to delete the schedule.
- Anything that needs the user: a REQUIRED field, an approval, a check that keeps failing, a tune proposal.

Never report "alerted" without the alert call succeeding and the marker read back. Never report "still false" when the check did not actually run.

## Guardrails

- **Read-only apart from the alert.** The check never writes, posts, deploys, deletes or changes state. The only things this routine writes are the alert, the marker, `RUN-LOG.md` and `LEARNINGS.md`.
- **One alert, ever.** The marker file is the memory. If it exists, the routine never alerts again, even if the condition flips back and forth.
- **Hard time limit: 3 minutes per run.** Put a timeout on every shell call: the shell tool's own timeout parameter (for example 60000 ms), `--max-time` on `curl`, and `timeout` (on macOS, `gtimeout` from GNU coreutils, if installed) around anything else. This exists because a watcher once hung for 5 days on its first shell call. Retry at most once, then stop and say so.
- **Never fabricate the observation.** The summary quotes what the check returned. No check, no claim.
- **Never message anyone the brief did not name**, never send an email (drafts only), never change templates, code or settings because a watch fired. The alert tells a human; the human acts.
- **Never delete or edit the schedule.** Retiring means telling the user how to do it.
