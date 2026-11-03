---
name: self-correct
description: Use when a stale, wrong, or overlooked claim is caught, whether the agent's own or one that the user, a teammate, a PR review, or fresh evidence just contradicted. Triggers on the situation, not a keyword, such as "wait, that's out of date", "I assumed X but it is actually Y", a recorded note that conflicts with what was just observed, or a review finding a bug in an earlier assumption. Not for capturing a brand-new lesson or for batch memory cleanup.
license: MIT
---

# Self-correct: fix a stale claim everywhere, now

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Knowledge locations to sweep:** the project `CLAUDE.md`, `~/.claude/CLAUDE.md`, the Claude memory directory, `~/.claude/agents/`, `~/.claude/skills/`, and an optional notes folder if the settings name one (setting name: `notes folder`).
- **Validity tiers:** Canon (deployed or official fact, or a team-approved decision), Provisional (in-progress local knowledge), Working (experiments, plans, timelines). These are rule 1 of the ai-pm-os operating rules (https://github.com/nkhanhpham99/ai-pm-os/blob/main/templates/CLAUDE.md). If the user's CLAUDE.md names its tiers differently, use the user's names. Latest wins within a tier.

## 1. Pin the correction
State the **wrong claim** (verbatim), the **correct claim**, and the **evidence** (source and date). If the correction is not clearly sourced, ask the user and stop. Never guess.

## 2. Classify
Clear technical correction: apply it (steps 3 to 7). Ambiguous or strategic: surface it with the evidence, do not decide silently.

## 3. Sweep for every copy
The failure mode is fixing one copy while stale twins survive. Before editing, search every location above with several phrasings of the claim, including the old wording of the problem itself ("waiting on", "not yet", "blocked by", "the cap stops it"). Agent and skill files restate facts too. Build the full list first.

## 4. Correct or supersede each copy
In every file found:
- **Rewrite the claim in place**, tagged `(tier, date)`. Do not add a "corrected" line next to the stale one: a fixed problem whose old warning still sits beside a new "fixed" line reads as broken to the next reader.
- **Keep the history as one line** under a short "Conflicts" note **in that same file**: the date, what the old claim said, and what replaced it. Every file you edit gets its own line, including a passing mention in a how-to or a table cell; a history note in one file does not cover the others. Never silently rewrite history, and never paste the old paragraph back in.
- **Compact as you go.** If the correction shows the item is closed, shrink it to one outcome line (what is true now, the date, the reason that matters). If it is still open, keep its dated context until it closes.
- Check anything that depends on the fact.

## 5. Flag wrong Canon loudly
If the wrong claim was Canon, tell the user explicitly, not just in a log line.

## 6. Note the systemic cause
If the claim lived in more than one place, add one line on why it was missed.

## 7. Verify the sweep (required)
Re-run the exact step 3 searches after editing. The report must include, even when the rest of it is plain prose:
- this line, written literally in this form with your numbers, so a person or a script can check it: `copies: <N found> -> <M stale remaining>` (for example `copies: 3 -> 0`; only the preserved Conflicts lines may still match)
- the list of files changed, each with whether it got its Conflicts line

If any stale copy survives, fix it and re-run. If a location could not be searched, report `not verified: <location>`, never "clean".

## 8. Log and hand off
If your knowledge base keeps a log, append `correct | <claim> fixed everywhere, copies N -> 0, evidence`. Record any new reusable lesson separately.

## 9. Large sweeps
If the sweep spans many files, hand the edits to a background agent. Small corrections stay inline.

## Boundaries
- Never auto-edit shared or team-facing documents. Surface a "push this correction" note.
- If a location is unreachable, correct what you can, say what was not swept, and never fabricate.
