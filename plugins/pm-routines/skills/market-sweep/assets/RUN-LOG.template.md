# Market sweep run log

One row per run, newest at the bottom. The `tune` mode reads this file to compute yield per source, cost per run and coverage health. Never edit past rows.

| Date | Mode | Run health | Covered | Skipped (reason) | Candidates -> kept, per source | New to brief | Cost | Notes |
|---|---|---|---|---|---|---|---|---|

<!-- Everything above this line is the run log to copy into RUN-LOG.md. Do not copy the reference section below. -->

---

## Reference (do not copy into RUN-LOG.md)

- **Mode:** `calibration` (the first run), `run`, `tune` (a tune happened; marks the start of the next window), or `not ready` (the readiness check stopped the run).
- **Run health:** `Full`, `Partial`, `Quiet week` or `Failed`.
- **Candidates -> kept, per source:** for each source, items captured and items that became findings after the gates, as `Reddit 12->3; Instagram 8->1`.
- **Cost:** what the environment reported (tokens, tool calls, minutes), or `not measured`. Never an estimate presented as a measurement.
- **Notes:** one line. A cut-short source, a timeout, a re-auth needed.

Fictional example rows:

```markdown
| 2026-01-17 | calibration | Partial | web, Reddit, Ad Library | Instagram (signed out) | web 6->2; Reddit 12->3; Ad Library 4->2 | 2 | not measured | ratings requested |
| 2026-01-24 | run | Full | web, Reddit, Ad Library, Instagram | none | web 5->1; Reddit 10->2; Ad Library 4->1; Instagram 9->2 | 1 | 41 tool calls | |
```
