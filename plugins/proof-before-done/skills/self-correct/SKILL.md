---
name: self-correct
description: Use when a stale, wrong, or overlooked claim is caught, whether the agent's own or one that the user, a teammate, a PR review, or fresh evidence just contradicted. Triggers on the situation, not a keyword, such as "wait, that's out of date", "I assumed X but it is actually Y", a recorded note that conflicts with what was just observed, or a review finding a bug in an earlier assumption. Not for capturing a brand-new lesson or for batch memory cleanup.
license: MIT
---

# Self-correct: fix a stale claim everywhere, now

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Knowledge locations to sweep:** the project `CLAUDE.md`, `~/.claude/CLAUDE.md`, the Claude memory directory, `~/.claude/agents/`, `~/.claude/skills/`, and an optional notes folder if the settings name one (setting name: `notes folder`).
- **Validity tiers:** V1 canon (deployed or team-approved fact), V2 provisional (in-progress local knowledge), V3 working (experiments, timelines). Definitions live in `templates/CLAUDE.md`. Latest wins within a tier.

## 1. Pin the correction
State the **wrong claim** (verbatim), the **correct claim**, and the **evidence** (source and date). If the correction is not clearly sourced, ask the user and stop. Never guess.

## 2. Classify
Clear technical correction: apply it (steps 3 to 7). Ambiguous or strategic: surface it with the evidence, do not decide silently.

## 3. Sweep for every copy
The failure mode is fixing one copy while stale twins survive. Before editing, search every location above with several phrasings of the claim. Agent and skill files restate facts too. Build the full list first.

## 4. Correct or supersede each copy
In every file found: fix the claim, tag it `(tier, date)`, and keep the old claim under a short "Conflicts" note with the date. Never silently rewrite history. Check anything that depends on the fact.

## 5. Flag wrong canon loudly
If the wrong claim was V1 canon, tell the user explicitly, not just in a log line.

## 6. Note the systemic cause
If the claim lived in more than one place, add one line on why it was missed.

## 7. Verify the sweep (required)
Re-run the exact step 3 searches after editing. The report must include:
- `copies: <N found> -> <0 stale remaining>` (only the preserved Conflicts notes may still match)
- the list of files changed

If any stale copy survives, fix it and re-run. If a location could not be searched, report `not verified: <location>`, never "clean".

## 8. Log and hand off
If your knowledge base keeps a log, append `correct | <claim> fixed everywhere, copies N -> 0, evidence`. Record any new reusable lesson separately.

## 9. Large sweeps
If the sweep spans many files, hand the edits to a background agent. Small corrections stay inline.

## Boundaries
- Never auto-edit shared or team-facing documents. Surface a "push this correction" note.
- If a location is unreachable, correct what you can, say what was not swept, and never fabricate.
