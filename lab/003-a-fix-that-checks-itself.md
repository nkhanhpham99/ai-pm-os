# 003: A fix that checks itself

- **Date:** 2026-11-02
- **Hypothesis:** When a fact goes stale, the correction fails in a predictable way: one copy gets fixed and the others survive, so a later session reads a surviving copy and repeats the old claim. A correction skill that searches once and edits once will miss copies. Making it search again after editing, and report what is left, should catch them.
- **Change:** Added a required verify step to the `self-correct` skill: step 7 in [`SKILL.md`](../plugins/proof-before-done/skills/self-correct/SKILL.md). After editing, it re-runs the exact searches from the sweep and must report `copies: N found -> 0 stale remaining`, plus the list of files changed. If a copy survives, it fixes it and searches again. If a location could not be searched, it reports `not verified: <location>` instead of "clean".
- **Measure:** The skill's own report on its first real run: the stale claims found by the sweep, and what the re-run searches found after the edits.
- **Result:** 12 locations, 15 stale claims, down to 0. Source: the skill's report from that run, 2026-11-02.

  The verify step earned its place on that first run. The re-run searches caught a stale copy that the first pass had missed. Without step 7, the report would have said "fixed" with a stale copy still in place.

- **Decision:** Keep. The verify step is required, not optional.
- **Next:** An automated eval that plants one stale claim in several files and checks the skill fixes every copy and reports `N -> 0`. It will get its own entry when it has run.
