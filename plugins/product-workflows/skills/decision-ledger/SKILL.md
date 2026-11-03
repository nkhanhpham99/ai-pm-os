---
name: decision-ledger
description: Use when the user wants to log a product decision, experiment, idea or hypothesis ("log a decision", "track this experiment", "add this idea to the ledger", "record this bet"), or wants to review the open ones ("review the decisions", "what is overdue", "answer the needs-input questions", "close this decision", "finalize this experiment"). Not for explaining a tradeoff (knowledge-base), writing a requirements doc (prd) or gathering outside evidence (market-research).
license: MIT
---

# Decision ledger: log the bet, review it later, never invent the answer

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Decisions file:** `./decisions.md` (setting name: `decisions file`). One markdown file holds every entry. If it does not exist, create it from the header of [the decisions template](assets/decisions-template.md). Quote paths.
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess. Today's date is what "past Review by" is measured against.
- If the settings rename the file, treat every mention of `decisions.md` below as that path.
- Storage is markdown. If the user wants the ledger in Notion, read [using Notion](references/using-notion.md) (untested).

## What this does
Product work gets scattered across code, chat, docs and people's heads. The ledger is one file where each decision, experiment, idea or hypothesis is written down with the bet behind it (what metric should move, from what, to what, by when), so it can be reviewed later against what actually happened.

Two modes. Pick from the request: **log** for a new entry, **review** for walking the open ones. If it is unclear, ask which.

## Anti-fabrication (read before either mode)
Work is scattered across code, chat, docs and the user's head. Without this rule, a pass would be tempted to infer an outcome from whatever evidence is lying around and write it down as fact. Every open field is an explicit question put to the user, never an assumed answer.

**Never write a value, date, number or outcome the user did not actually give you.** If they do not know, write the literal `needs input` and keep Status as `needs input`. An honest gap beats a confident guess every time. Judge each number honestly: *sourced* (a cited source or real data), *assumed* (the user's belief with no data behind it), or *needs input* (unknown). Do not upgrade assumed to sourced because it sounds plausible.

## The entry format
Each entry in `decisions.md` is a `## <id> · <title>` heading followed by these bullets, one per line, in this form: `- Label: value`. Other tools read this file by label, so keep the labels exact.

| Label | Value |
|---|---|
| `Type` | `decision`, `experiment`, `idea` or `hypothesis` |
| `Status` | `open`, `needs input`, `closed` or `superseded` |
| `Owner` | who is accountable, or `needs input` |
| `Logged` | `YYYY-MM-DD` |
| `Topic` | a short area label (reuse the labels already in the file) |
| `Priority` | `P0 push hard`, `P1 normal` or `P2 easy-iterate`. This enum is fixed |
| `Metric` | the measure the bet is judged on, or `needs input`, or `none set` |
| `Baseline` | the starting value only (for example `12% weekly retention`), or `needs input`, or `none set`. The source goes in `Provenance` |
| `Target` | the value to reach, value only, or `needs input`, or `none set` |
| `Review by` | `YYYY-MM-DD`, or `needs input`, or `none set` |
| `Reasoning` | the user's own words on why |
| `Provenance` | per number: sourced (with the source), assumed, or needs input |
| `Outcome` | what actually happened, or `needs input` |
| `Lesson` | the one-line takeaway, or `needs input` |

- **Ids** are `D-001`, `D-002`, and so on. Read the file, take the highest number, add one. When the file has no entries yet, the first id is `D-001`. Never reuse an id, even after `superseded`.
- **Each value is a single line.** If a quoted answer has line breaks, write them as ` / `.
- **`Priority` here is a different scale** from the P0/P1/P2 tiers in a PRD. Do not mix the two.
- **Unknown fields hold the literal `needs input`.** A deliberate "there is no bet" is different: write `none set` in the four bet fields. Never leave a bet field blank.
- **Status rules.** `needs input` when `Owner` is unknown, or a bet exists and any bet field is `needs input`. `open` when the entry is trackable (an owner, and a complete bet or no bet). `closed` when the outcome is known and confirmed by the user. `superseded` when a later entry replaces it.
- A worked example is at the bottom of [the template](assets/decisions-template.md).

## Mode: log
Ask one question at a time. Prefer a multiple-choice question when options exist.

1. **Read the decisions file first** (create it if missing) so you can reuse topic labels and assign the next id.
2. **Type** (required): decision, experiment, idea or hypothesis.
3. **Topic** (required): offer the topics already in the file, or let the user name a new one.
4. **Priority** (required, always set): P0 push hard, P1 normal or P2 easy-iterate.
5. **Title and reasoning** (required): the thinking behind it, in the user's own words. Do not paraphrase it away.
6. **Owner:** who is accountable. `needs input` if they do not say.
7. **Is there a falsifiable bet?** Ask yes or no.
   - **Yes:** capture Metric, Baseline, Target and Review by. Write the Baseline and Target as values only and put where each came from in `Provenance`. A number with no source is recorded as assumed. A number the user does not know stays `needs input`.
   - **No:** write `none set` in the four bet fields and do not push the user to invent one. That is a valid entry for an early idea.
8. **Does this replace an earlier entry?** If yes, set the old entry's Status to `superseded` and start its Outcome with `Superseded by D-NNN` (the new id). Start the new entry's Provenance with `Supersedes D-NNN` (the old id), so the link runs both ways. These two agent-written link phrases are exempt from the verbatim rule, which applies to the user's own statements.

Then:
- Set `Logged` to today's date, `Status` per the status rules, and `Provenance` per number.
- **Append the entry** to the end of the file using the Edit tool (or write the file if it was just created). Never rewrite or reorder other entries.
- Leave `Outcome` and `Lesson` as `needs input`. They are filled at review.

**Read it back.** Re-read `decisions.md` from disk and find the new entry by id. Confirm the title, Type, Status, Owner, Priority and every bet field match what the user gave. Report the id, the file path and a one-line "what is on the entry". If the read-back does not match, fix it and read again. If you cannot confirm, say "logged, not verified: <reason>".

## Mode: review
Walks the entries that need attention, one question at a time, and records the answers as sourced truth.

1. **Read the decisions file.** If it does not exist or has no entries, say so and stop.
2. **Find what needs attention:**
   - Status is `open` or `needs input`, or
   - `Review by` is a real date earlier than today and Status is not `closed` or `superseded`.
   Entries with Review by set to `needs input` or `none set` are included only through the Status rule.
3. **Show a short list** first: id, title, and why it is up (which field is missing, or "review date passed on <date>"). Then walk them one at a time. Ask the user which to start with if there are many.
4. **Resolve each open question.** For each entry, ask the user directly what the open field should be: Outcome, Baseline, Target, Metric, Review by, Owner, or whatever is missing. Then:
   - Write **only** what the user confirmed, **verbatim** where it is a statement (Reasoning, Outcome, Lesson). Do not tidy it.
   - Once they confirm a number, record where it came from in `Provenance`. A number they could not source is recorded as assumed.
   - If they do not know, leave the field as `needs input` and keep Status `needs input`.
   - Move Status forward: `open` once it has what it needs to be tracked, `closed` once the outcome is known.
   - If the review date passed and the outcome is not known, ask whether to set a new Review by date or leave it. Never move a date without being told.
5. **Offer to close** any entry the user considers done. On close:
   1. Ask for the **Outcome**: whether the bet held, did not hold, or partly held, in their words, with the final figure if there is one.
   2. Ask the user to confirm the exact one-line **Lesson** wording before writing it. Do not paraphrase it for them.
   3. Set Status to `closed`.
   4. If a lesson changes a standing rule, offer to add it to the project's CLAUDE.md or notes, and only do so if they say yes.
6. **Edit in place.** Change only the labelled lines of the entries being reviewed, using the Edit tool. Never rewrite the whole file.

**Read it back (after each write, and again before the recap).** Re-read `decisions.md` from disk and confirm each field you wrote now shows the user's answer. Anything that did not land is reported as "not verified: <reason>". End with a short recap: which entries were updated (and which fields), which were closed, and which still need input (and exactly what is missing on each).

## Anti-patterns
- Inferring an outcome from evidence lying around and writing it down as the user's answer.
- Filling `Baseline` or `Target` with a plausible number to avoid leaving a gap.
- Forcing a bet onto an idea that has none.
- Paraphrasing the user's Reasoning, Outcome or Lesson.
- Rewriting the whole file, or reordering entries, instead of editing the labelled lines.
- Reusing an id.
- Reporting "logged" or "closed" without re-reading the file.
