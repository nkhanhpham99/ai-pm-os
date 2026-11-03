# Weekly metrics brief

- Status: draft
- Approved on:
- review_by (REQUIRED):

The review reads this file before every run. Fields marked REQUIRED must be filled before a run starts; a blank, a `<placeholder>` or `needs input` stops the run with a question. Change this file through the `tune` mode or by hand, never during a run.

## North star (REQUIRED)
- Name:
- Source (tool + exact query):
- Owner:
- Target:

## Key results (REQUIRED, 3 to 6)
One block per KR. Every line is REQUIRED. The number of KRs must sit inside `KR range` below.

### KR1 ·
- Name:
- Source (tool + exact query):
- Owner:
- Target:

### KR2 ·
- Name:
- Source (tool + exact query):
- Owner:
- Target:

### KR3 ·
- Name:
- Source (tool + exact query):
- Owner:
- Target:

## Status-color rules (REQUIRED)
- Green:
- Yellow:
- Red:

## Running
- Destination (REQUIRED):
- Decisions file (optional): ./decisions.md (wins over the CLAUDE.md `decisions file` setting for this routine; write an absolute path for scheduled runs)
- Run day (optional): Monday (every run reviews the ISO week just ended)
- Known-broken metrics (optional): none
- KR range: 3 to 6 (adjustable default)
- Tune every: 4 runs

<!-- Everything above this line is the brief to copy into METRICS.md. Do not copy the example below. -->

---

## Example (do not copy into METRICS.md)

Every value below is fictional and shows the format, not a real product. The targets are left as `<placeholders>` on purpose, so this example is still a draft: the readiness check would stop on each of them and ask the user for their real number.

```markdown
# Weekly metrics brief

- Status: draft
- Approved on:
- review_by (REQUIRED): 2026-03-31

## North star (REQUIRED)
- Name: weekly active planners (people who planned at least one dinner this week)
- Source (tool + exact query): product analytics tool, saved insight "Weekly active planners" (id example-insight-01), unique people, internal accounts excluded
- Owner: product lead (fictional role)
- Target: <target value> by 2026-03-31

## Key results (REQUIRED, 3 to 6)

### KR1 · New sign-ups per week
- Name: New sign-ups per week
- Source (tool + exact query): product analytics tool, saved insight "Sign-ups weekly" (id example-insight-02)
- Owner: growth lead (fictional role)
- Target: <target value> per week by 2026-03-31

### KR2 · Week-2 retention
- Name: Week-2 retention
- Source (tool + exact query): product analytics tool, retention insight "Week-2 retention" (id example-insight-03), cohort = sign-up week
- Owner: product lead (fictional role)
- Target: <target value> by 2026-03-31

### KR3 · Paid conversions per week
- Name: Paid conversions per week
- Source (tool + exact query): billing tool, overview metrics, "new paid customers, last 7 days"
- Owner: revenue lead (fictional role)
- Target: <target value> per week by 2026-03-31

## Status-color rules (REQUIRED)
- Green: the north star and every KR moved toward target this week.
- Yellow: the north star moved toward target, but at least one KR did not.
- Red: the north star fell week over week, or two or more KRs fell.

## Running
- Destination (REQUIRED): markdown, ./metrics-review/YYYY-Www.md
- Decisions file (optional): ./decisions.md
- Run day (optional): Monday
- Known-broken metrics (optional): KR2 reads 0 until the retention event is fixed; report it as "blocked: retention event fix pending"
- KR range: 3 to 6
- Tune every: 4 runs
```
