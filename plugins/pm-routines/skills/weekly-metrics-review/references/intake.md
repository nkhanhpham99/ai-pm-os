# Intake: the setup interview

A weekly review is only as honest as its definitions. This interview pins down what is measured, where each number comes from, who owns it and what counts as a good week, before any week is compiled. Then the agent tests every source itself. Nothing runs until the user approves the written brief.

## How to ask

- **One question at a time.** Wait for the answer before the next one.
- **Every question carries a recommended default** the user can accept. Say where it came from.
- **Read before asking.** If the project already has OKRs, a metrics doc, a dashboard or a decisions file, draft answers from it and ask the user to confirm.
- **"I don't know" is fine.** Record `needs input`, carry on, and try to fill it in the foundation pass. A REQUIRED field still `needs input` at the end blocks approval.
- **Never invent a target, an owner or a query.** A default is a suggestion the user accepts, not a value written on their behalf.

## The questions, in this order

This is the order of the REQUIRED fields in `METRICS.md`.

| # | Field | Question | Recommended default |
|---|---|---|---|
| 1 | North star | "Which one number best says the product is working?" | Drafted from the project's docs or existing OKRs, if any. Otherwise no default. |
| 2 | Key results (3 to 6, an adjustable default) | "Which 3 to 6 key results do you want on the scoreboard every week?" | The KRs in the project's docs, if any. |
| 3 | Per KR: source | For each KR, one at a time: "Where does this number live? Name the tool and the exact query, saved insight or dashboard tile." | The best match found in the foundation pass, shown with the value it returned. |
| 4 | Per KR: owner | "Who is accountable for this number?" | `needs input` until the user names someone. Never assume it is the user. |
| 5 | Per KR: target | "What value, by when, counts as hitting it?" | The target in the project's docs, if any. Otherwise `needs input`. |
| 6 | Status-color rules | "What makes a week green, yellow or red?" | Green: every KR on track for its target. Yellow: any KR off track but moving the right way. Red: any KR moving the wrong way, or the north star down week over week. The user should reword these in their own terms. |
| 7 | Destination | "Where should each week's review go?" | A markdown file per week, `./metrics-review/YYYY-Www.md`. Notion only if asked (untested). |
| 8 | `review_by` | "When should we revisit the whole brief?" | The end of the current quarter. |

Then the optional fields, one question each, all skippable:
- **Where open decisions live**: default the `decisions file` setting if the user's CLAUDE.md has one, else `./decisions.md` (the decision-ledger skill's file, if installed). Write it into the brief's `Decisions file` field as an absolute path; that field then wins over the setting for this routine.
- **Run day**: default Monday. Every run reviews the ISO week just ended (the review week), whatever day it runs.
- **Known-broken metrics**: any metric that reads wrong until something ships ("reads 0 until the tracking fix lands"). It is reported with that flag, never as a real value.
- **Tune every**: default 4 runs.

## The foundation pass

After the questions, do the research the user should not have to.
1. **Detect the data tools** this session actually has: analytics or product-data tools, billing or subscription tools, a database client, a spreadsheet tool, a browser. Never assume a tool exists.
2. **For each KR, find the source.** Look for a saved insight, dashboard tile or existing query that matches the user's definition. Prefer an existing saved object (by id) over a query you write, so the number matches what the team already sees.
3. **Test each source once, read-only.** Run the exact query and show the user the value it returned and the time window it covered. Ask: "Is this the number you mean?" A query that cannot be run is written down as `awaiting <owner or source>` with the reason.
4. **Check the definition for traps**: internal or test accounts included, a time window that does not match a week, a metric counting events rather than people, a filter on one platform only. Ask about each one you find.
5. **Note which numbers are manual** (someone's spreadsheet, a figure a person reports). Their source is that person, and they are `awaiting <owner>` whenever not supplied.

## Draft, show, approve

1. Create the data folder (default `./metrics-review/`, or the `metrics review folder` setting). Confirm the path.
2. Write `METRICS.md` from [the template](../assets/METRICS.template.md) with `Status: draft`. Every KR row carries name, source (tool plus exact query or id), owner and target.
3. Show it. Point out every field still `needs input`.
4. On the user's yes, set `Status: approved` and `Approved on: <today>`. Create `LEARNINGS.md` and `RUN-LOG.md` in the formats given in the skill.
5. Read all three files back from disk. Report the paths, the number of KRs, and any metric already known to be awaiting, or "not verified: <reason>".
6. Offer the first run now. It has no prior week, so every comparison will say so.
