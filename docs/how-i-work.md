# How I work with AI agents

This is the long version of the introduction in the [README](../README.md). It explains the principles behind the plugins, the structure every routine shares, and why I put my effort into enforcement and measurement rather than into better-worded rules.

I built this setup while shipping a consumer app. Nothing here depends on that product. Everything specific to it was taken out, so the plugins work for any product, team or workflow.

## The problem

AI agents are good enough now that I hand them real work: market research, PRDs, metrics reviews, scheduled checks, code. They fail in three ways that are consistent enough to design around.

1. **They are confidently wrong.** An agent treats a plan as a fact, a draft as the deployed system, and a guess as a number. It says all three in the same sure voice.
2. **They forget.** Each session starts empty. What was decided, ruled out or half-finished in the last one is gone unless it was written down somewhere the next session will read.
3. **They say "done" before it is done.** A write call that returns without an error gets reported as success. Nobody checked what actually landed.

My first answer was the usual one: write rules. My instruction file grew clear, specific rules for each failure. Then I measured whether they were followed.

## What the measurement showed

Two lab entries changed how I think about this.

- **[Lab 001](../lab/001-auditing-my-agent-setup.md)**, an audit of my own setup on 2026-11-02, found the rules strong and the enforcement thin. Only 1 of 4 hooks could block anything. 5 of 8 custom subagents had never been invoked. The permissions file had grown to 1,613 one-off entries.
- **[Lab 002](../lab/002-does-my-agent-verify.md)** replayed my past sessions through a check for one rule: after writing to an external tool, read it back before saying "done". Of 3,731 turns, 538 wrote to an external tool. Only 45 of those (8%) read the result back. In 425, the agent claimed completion without a read-back.

The rule had been in my instructions the whole time. It was followed in 8% of the turns it applied to. That is the number that reorganized this repo.

## Principles

**1. Rules are cheap. Enforcement is the work.** A rule in a file is a request. I now sort every rule by how strongly it is enforced:

| Level | Example | What it guarantees |
|---|---|---|
| Written | A line in `CLAUDE.md` | Nothing. It may be skimmed or trimmed out of context. |
| Injected | The `operating-rules` SessionStart hook | The agent has seen it this session. |
| Reminded | The `proof-before-done` PostToolUse hook | The agent is told at the moment it matters. |
| Blocking | The `proof-before-done` Stop hook | The turn cannot end on an unverified "done" without being asked once for proof. |
| Measured | `scripts/backtest.py` | I know how often the rule held, and whether a change moved it. |

A rule I care about should sit as far down this table as it can.

**2. Measure before and after.** A change ships with a way to tell whether it worked. Lab 002 has its baseline from before the hook. The follow-up runs the same script after two weeks with the hook on. That result is pending, and I will not predict it.

**3. Every number has a source.** Unknowns are written as `needs input`. A claim I cannot source carries no number at all. The skills follow the same rule: `market-research` logs every source with its date and the figure word for word, `prd` gives every target a reason, and `weekly-metrics-review` leaves an unreadable metric blank and names who it is waiting on, rather than estimating it.

**4. Fix every copy, then check.** A stale fact rarely lives in one place. Fixing one copy leaves the others to contradict it later. The `self-correct` skill sweeps for every copy, fixes them, then re-runs its own searches and reports `copies: N -> 0`. That re-run is required because on its first real run it caught a copy the first pass missed ([lab 003](../lab/003-a-fix-that-checks-itself.md)).

**5. A guardrail must understand what it guards.** A guard that searches raw text for a dangerous phrase blocks harmless commands that only mention it ([lab 004](../lab/004-guardrails-that-match-text-misfire.md)). Guards should parse the command and decide on what will actually run. That fix is not built yet, and the entry says so.

**6. State lives in files.** A session's memory is not a record. `session-handoff` keeps one lean `STATUS.md` per project, current state only, and reads it back before it reports. `decision-ledger` keeps bets in `decisions.md` so they can be reviewed against what happened. `knowledge-base` turns explanations into entries that are still there next month.

**7. Ask before assuming or spending.** The skills stop and ask when a question would change the result: `market-research` offers a depth menu before it spends anything, `prd` asks its shape-changing questions before it drafts, and the routines refuse to run on an incomplete brief.

## The loop

The plugins sit on one loop.

- **Capture.** What I learned and what I decided gets written down, with its source. Plugins: `knowledge-compounding` (`knowledge-base`) and `product-workflows` (`market-research`, `prd`, `decision-ledger`).
- **Verify.** Every external write is read back, and every correction reaches every copy. Plugin: `proof-before-done` (hooks and `self-correct`).
- **Hand off.** The state of the work goes into a file a fresh session can read. Plugin: `session-handoff`.
- **Compound.** What a change did gets measured and written up, and the next change is chosen from that. The [lab](../lab/) is where this happens, and the `learn` and `tune` modes of `pm-routines` do the same for each routine.

`operating-rules` sits under the whole loop: the eight rules from [`templates/CLAUDE.md`](../templates/CLAUDE.md), injected at the start of every session.

## The routine structure

A scheduled prompt is easy to write and quietly gets worse. It runs on assumptions nobody wrote down, pads a quiet week to look busy, skips a source that stopped working, and never learns which outputs were useful. So every routine in `pm-routines` (`market-sweep`, `weekly-metrics-review`, `watch-until`) is a small system with a feedback loop, built from the same four modes.

1. **Setup.** An interview, one question at a time, each with a recommended default. Then a foundation pass, where the agent researches what I did not know and asks me to confirm it. The result is a brief file, shown to me, and nothing runs until I approve it.
2. **Run.** Reads the brief first, every time. A readiness check stops the run with a question if a required field is empty or the brief is past its review date. Every run ends with an honest summary: a quiet week is reported as quiet, an unreachable source is named, and every file written is read back before the summary says it was written.
3. **Learn.** I record what happened with an output, in my own words: this finding was a keeper, that metric definition was wrong, that alert was noise.
4. **Tune.** Every 4 runs by default, the routine reviews its own run log (yield per source, cost per run, repeated misses, stale brief fields), proposes concrete edits to its own brief, and applies each one only after I approve it. A tune is written up as question, evidence and change, the same shape as a lab entry.

The approval step is the point. A routine that edits itself without asking drifts in ways nobody notices. A routine that proposes, shows evidence and waits gets better in ways I can follow.

## Why enforcement beats rules

The short answer is the 8% in lab 002. The longer answer is about where the cost lands.

A written rule costs nothing to add and nothing to break. The agent pays no price for skipping it, and I only find out later, when something I was told was done turns out not to be. Enforcement moves the cost to the moment of the mistake, where it is cheapest to fix: the agent is asked for the read-back while the page is still open.

Enforcement has its own failure modes, and the design has to account for them.

- **False positives.** The Stop hook decides that a message "claims completion" by matching words like "done" or "sent". That is a heuristic. It blocks once per turn, and an explicit "not verified" always satisfies it, so a wrong call costs one extra sentence, not a stuck session.
- **Bugs.** A hook that crashes must not trap the session it runs in. Every hook here fails open: on any parse problem or unexpected input it exits silently. The risk of failing open is a hook that is broken and quiet, which is why each one ships with regression tests and the backtest can replay it over real transcripts.
- **Matching the wrong thing.** Lab 004 is a guard that enforced, but on text instead of meaning. Enforcement is only as good as what it inspects.

The order I now work in is: write the rule, measure how often it holds, enforce the ones that matter, and measure again.

## What I left out

- **Other people's skills.** I use several skills written by others. None are included here, because they are not mine to package. The credits in the README name the projects that shaped this one.
- **Untested backends.** Markdown is the only tested storage. Where a skill could publish to Notion, the reference file describes how and is marked untested.
- **A framework.** This is markdown skills, a few small hook scripts and templates. Nothing to run except the hooks and the checks.
