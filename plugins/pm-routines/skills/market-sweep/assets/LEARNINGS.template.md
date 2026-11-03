# Market sweep learnings

What happened with the sweep's output, in the user's own words: ratings, outcomes of adopted findings, misses, corrections, and every tune. Newest at the bottom. The `tune` mode reads this file; runs never edit past entries.

<!-- Everything above this line is the header to copy into LEARNINGS.md. Do not copy the reference section below. -->

---

## Reference (do not copy into LEARNINGS.md)

One entry per item. Each value is a single line; write line breaks inside a quote as ` / `.

```markdown
## YYYY-MM-DD · <short label>
- Kind: rating | outcome | miss | correction | platform | tune
- Run: <date of the sweep it refers to>
- Finding: <F-number and label, or none>
- Rating: keep | meh | miss | none
- What happened: "<the user's words, verbatim>"
- Source: <where the outcome number came from, or "the user's report", or needs input>
```

Field notes:
- `rating` is a keep / meh / miss on one finding. The calibration run produces one per finding.
- `outcome` records what happened after a finding was used: "we tried the hook; it did X". Copy any number exactly as the user gave it, and say where it came from in `Source`. A number the user did not give is never written.
- `miss` is something the sweep should have caught and did not.
- `correction` is a finding that turned out wrong (a misread engagement count, a post that was an ad).
- `platform` is a new block or workaround found on a platform.
- `tune` entries hold the whole tune block (see `references/tune.md`), with each proposed edit marked applied, rejected or changed.

Fictional example:

```markdown
## 2026-01-17 · F3 rated keep
- Kind: rating
- Run: 2026-01-17
- Finding: F3 · "what I cooked with one onion" accumulation format
- Rating: keep
- What happened: "This is exactly the kind of format we can make every week."
- Source: the user's report
```
