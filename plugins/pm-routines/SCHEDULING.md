# Scheduling the routines

The routines in this plugin run by hand ("run the market sweep") or on a schedule. This page gives three ways to schedule them, a prompt for each routine, and the guardrails every scheduled run needs. It is instructions for you: nothing here creates a schedule by itself, and the skills never create, edit or delete a schedule.

**Before you schedule anything:** run the routine's `setup` by hand and approve its brief. For `market-sweep`, also run the first (calibration) sweep by hand and rate its findings. A schedule pointed at a missing or unapproved brief only produces "not ready" runs.

## Run guardrails (every recipe)

These come from running routines unattended for a long time.

1. **A hard time limit per run.** `watch-until` runs get 3 minutes. Give the other routines a limit that fits their brief's budget, and enforce it from outside the run where the recipe allows (see the `timeout` wrapper in the cron recipe).
2. **A timeout on every shell call inside the run.** The skills tell the agent to do this, and the prompts below repeat it, because a watcher once hung for 5 days on its first shell call. Use the shell tool's own timeout parameter, `--max-time` on `curl`, and `timeout` (or `gtimeout` from GNU coreutils on macOS) around anything else.
3. **One retry, then move on.** A failing source is retried once, then named as unreachable in the summary. Never a retry loop.
4. **Unattended means no questions.** A scheduled run cannot ask you anything. Wherever a skill says "ask", the question goes at the top of the run's summary and the run stops or skips that part. The prompts below say so explicitly.
5. **Absolute paths.** A schedule may start in a different folder from the one you set up in. Every prompt names the data folder (and, for `watch-until`, the brief and marker) by absolute path.
6. **Least privilege.** Allow only the tools a routine needs. Never schedule a routine with permission checks turned off.
7. **Read-only everywhere else.** The routines write only to their own data folder, plus the alert or summary channel their brief names.
8. **Retire what is done.** When `watch-until` fires or expires, it tells you to delete its schedule. Do it; the marker file keeps it silent until you do, but a dead schedule still costs a run each time.

## Recipe 1: Claude Code desktop scheduled tasks

Runs on your machine, with your local files, tools and connectors.

1. In the Claude Code desktop app, create a new scheduled task. (You can also ask Claude in a desktop session to "create a scheduled task" with the prompt below.)
2. Give it a name (for example `weekly-metrics-review`), the prompt for the routine from "Prompts" below with your absolute paths filled in, and a schedule.
3. Run it once with "run now" and read the summary before trusting the schedule.

Notes:
- A local scheduled task runs only while the machine is awake and the app can run it. Check how your version handles a missed run before relying on a schedule for anything time-critical.
- Tasks are stored per user (on current versions, each task's prompt lives in a `SKILL.md` under `~/.claude/scheduled-tasks/<task-id>/`). To retire one, delete or disable it in the app.

## Recipe 2: cloud routines with `/schedule`

Runs in the cloud on a cron schedule, without your machine being on.

1. In Claude Code, run `/schedule` and describe the routine, or paste the routine's prompt from below.
2. Choose the schedule, and the repository the routine works in.

Notes:
- **A cloud run does not see your machine.** Local files, a local browser and local-only MCP servers are not available. Keep the routine's data folder inside the repository the routine checks out, and make sure the run can save its outputs (commit them, or deliver the summary to a connected channel).
- Only connectors available to cloud runs can be used. A `market-sweep` that depends on a local browser for some platforms will report those platforms as skipped.
- To retire a cloud routine, use `/schedule` to list your routines, then disable or remove it.

## Recipe 3: plain `cron` with `claude -p`

Runs on your machine through `cron`, headless. `claude -p "<prompt>"` runs one non-interactive session and exits.

1. Find the full path to `claude` with `command -v claude`. Cron starts with a minimal `PATH`, so use the full path.
2. Save the routine's prompt to a file, for example `/absolute/path/to/project/.routines/weekly-metrics-review.prompt`.
3. Add a line with `crontab -e`:

```cron
# Mondays at 08:00: weekly metrics review
0 8 * * 1 cd "/absolute/path/to/project" && timeout <seconds> /absolute/path/to/claude -p "$(cat .routines/weekly-metrics-review.prompt)" --allowedTools "Read,Write,Edit,Glob,Grep,Bash(date:*)" >> metrics-review/cron.log 2>&1

# Daily at 09:00: a watch (3-minute hard limit)
0 9 * * * cd "/absolute/path/to/project" && timeout 180 /absolute/path/to/claude -p "$(cat .routines/watch-new-version.prompt)" --allowedTools "Read,Write,Edit,Bash(curl:*),Bash(date:*)" >> watch-until/new-version/cron.log 2>&1
```

Notes:
- **`timeout` is the outer hard limit.** On macOS it is not installed by default: install GNU coreutils and use `gtimeout`, or the run has no outer limit.
- **Headless runs cannot answer permission prompts.** List the tools the routine needs in `--allowedTools`, and scope the shell to the commands the routine actually runs (`Bash(curl:*)` for a watch whose check is a `curl` call, `Bash(date:*)` for working out dates) rather than allowing plain `Bash`. Add `WebSearch,WebFetch` for `market-sweep`, and the MCP tools for your data sources and alert channel. Anything not allowed is refused, and the run reports it. Do not use a permission mode that skips checks.
- `--max-budget-usd <amount>` caps what one run can spend.
- The run uses your existing Claude Code login. If it expires, runs fail; check the log file.
- On macOS, `cron` may need permission to read some folders. `launchd` is the native alternative with the same command.
- To retire a routine, delete its line with `crontab -e`.

## Prompts

Fill in the angle-bracket parts. Every prompt says the run is unattended, names absolute paths, and repeats the time-limit guardrail.

### market-sweep

```text
Use the market-sweep skill in run mode. The data folder is <absolute path>/market-sweep/.
This is an unattended scheduled run: nobody can answer questions. Wherever the skill says to ask,
put the question at the top of your summary and stop or skip that part. Do not change the brief;
if a tune is due, write the proposal into the summary and LEARNINGS.md only.
Put a timeout on every shell call, retry a failing source once, then name it as skipped.
Read back every file you write before the summary. End with the honest summary.
```

### weekly-metrics-review

```text
Use the weekly-metrics-review skill in run mode for the review week (the ISO week just ended).
The data folder is <absolute path>/metrics-review/. Read open decisions from the file named in METRICS.md's Decisions file field (or, if that is blank, the decisions file setting).
This is an unattended scheduled run: nobody can answer questions. Wherever the skill says to ask,
put the question at the top of your summary. Leave next week's top 3 as needs input with labelled suggestions.
Never estimate an unreadable metric: mark it awaiting its owner or source.
Put a timeout on every shell call, retry a failing source once. Read back the week file before the summary.
```

### watch-until

```text
Use the watch-until skill in run mode for the watch at <absolute path>/watch-until/<watch-slug>/WATCH.md.
This is an unattended scheduled run: nobody can answer questions.
The whole run must finish in under 3 minutes. Put a timeout on every shell call (60000 ms on the shell tool,
--max-time on curl). If a call hangs or errors, retry once, then write "could not check today" and stop.
Alert at most once, using the marker file. Never delete or edit this schedule; tell me to.
```

### decision-ledger weekly review (from the product-workflows plugin)

The `decision-ledger` skill's review mode asks you questions one at a time, which a scheduled run cannot do. So the scheduled version only builds the digest; you answer it later by saying "review the open decisions" in a normal session.

```text
Use the decision-ledger skill to prepare a weekly review digest of the decisions file (<absolute path from your decisions file setting>).
This is an unattended scheduled run: nobody can answer questions, so do not write anything into the decisions file.
List every entry that needs attention: Status open or needs input, or a real Review by date before today
with Status not closed or superseded. For each give the id, title, owner, and exactly which fields are
still needs input or that the review date passed. Parse entries by label; treat "none set" as a deliberate no-bet,
not a gap. End with the digest and a reminder to run "review the open decisions" in a normal session.
```

Schedule it weekly, the day before the weekly metrics review if you run both, so the review copies in a fresh list.
