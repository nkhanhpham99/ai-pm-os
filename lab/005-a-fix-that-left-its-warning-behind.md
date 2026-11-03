# 005: Does logging every update keep my docs true?

- **Date:** 2026-11-03
- **Hypothesis:** If every change gets logged, my working docs stay true. A stale task should appear only when an update was missed, so the fix would be "log more".
- **Change:** Three rules, added to [`self-correct`](../plugins/proof-before-done/skills/self-correct/SKILL.md) (step 4), [`session-handoff`](../plugins/session-handoff/skills/session-handoff/SKILL.md) (hard rules 2 and 14), the review mode of [`decision-ledger`](../plugins/product-workflows/skills/decision-ledger/SKILL.md), and the [operating rules](../templates/CLAUDE.md) (rules 1 and 3):
  - **Rewrite, don't add.** A fix rewrites the old problem line. It never adds a "fixed" line beside it.
  - **Compact.** A closed item shrinks to one line: the outcome, the date, the reason that matters. An open item keeps its dated history until it closes.
  - **Check the premise.** A line in an old doc is the thing being checked, not the evidence. Before it becomes a task or is carried forward, it is checked against the real source (the config that runs, the latest run, the live record), or marked "not verified".
- **Measure:** What happened, reconstructed from the history the docs already kept, and the correction sweep's own report (`self-correct` step 7) on 2026-11-03.
- **Result:** The hypothesis was wrong. The update had been logged, twice.

  A note in my project knowledge base said a scheduled CI job would stop when a spending cap ran out, and that moving it to our own runners was an option. A teammate made that move the same day. The move was in git, and a later fix was in the knowledge base. But the old line was never rewritten. Later updates added new lines saying the job was green, so the old warning and the new status sat side by side. Days later, a sync routine read the old line and created a "waiting on a teammate" task. It never opened the job's config, which would have shown the job already running on our own runners.

  The correction sweep found the stale claim in 5 places and left 0. Source: the sweep's report, 2026-11-03.

  So the failure was not missing updates. It was additions without rewrites, and a routine that trusted a doc line without checking the real thing.

- **Decision:** Iterate. The three rules above are in the packaged skills. In my own setup I also added two pieces that are not packaged here, because they depend on my own task board and alert channel: a daily check that re-tests any "waiting" or "blocked" row idle for 3 or more days, and an alert when a scheduled run has been stuck in the queue for more than 2 hours.
- **Next:** Over the next two weeks, count how many "waiting" or "blocked" rows the daily check flags as no longer true. Result pending. The stuck-run alert has not yet been tested against a real stuck run.
