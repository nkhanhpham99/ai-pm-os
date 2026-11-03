# Decisions

One entry per decision, experiment, idea or hypothesis, newest at the bottom. Each entry is a `## <id> · <title>` heading followed by `- Label: value` bullets. Unknown fields hold the literal `needs input`. Where there is deliberately no bet, the four bet fields hold `none set`. Edit entries in place and never reuse an id.

<!-- Everything above this line is the header to copy into a new decisions.md. Do not copy the reference section below. -->

---

## Reference (do not copy into decisions.md)

Field values:
- `Type`: decision | experiment | idea | hypothesis
- `Status`: open | needs input | closed | superseded
- `Owner`: who is accountable, or `needs input`
- `Logged`: YYYY-MM-DD
- `Topic`, `Priority` (P0 push hard | P1 normal | P2 easy-iterate, a fixed enum)
- `Metric`, `Baseline`, `Target`, `Review by` (YYYY-MM-DD): the bet, or `needs input`, or `none set`. `Baseline` and `Target` hold the value only (for example `12% weekly retention`). The source goes in `Provenance`.
- Every value is a single line. Write line breaks inside a quoted answer as ` / `.
- When one entry replaces another, the old entry's `Outcome` starts with `Superseded by D-NNN` and the new entry's `Provenance` starts with `Supersedes D-NNN`.
- `Reasoning`, `Provenance`: the user's words, and sourced / assumed / needs input per number
- `Outcome`, `Lesson`: filled at review, until then `needs input`

One example entry, with placeholder content only. Every value is fictional and shows the format, not a real result:

```markdown
## D-000 · Example: shorten the sign-up form
- Type: experiment
- Status: needs input
- Owner: needs input
- Logged: 2026-01-15
- Topic: Onboarding
- Priority: P1 normal
- Metric: sign-up completion rate
- Baseline: example value
- Target: needs input
- Review by: 2026-02-15
- Reasoning: "People seem to drop off at the long form, so a shorter one should help."
- Provenance: Baseline assumed (no source yet). Target needs input. Review by given by the user.
- Outcome: needs input
- Lesson: needs input
```

How to read it: the experiment has a bet (a metric, a starting value, a review date), but the target is unknown and the owner is unnamed, so Status is `needs input` rather than `open`. At review, the user is asked for the missing fields one at a time.
