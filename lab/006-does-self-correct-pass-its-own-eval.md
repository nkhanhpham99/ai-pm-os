# 006: Does self-correct pass its own eval?

- **Date:** 2026-11-03
- **Hypothesis:** `self-correct` fixes every copy of a stale claim and says so in a checkable line. An automated eval that plants one stale fact in three files, worded differently, should score 1.0 with the plugin and clearly lower without it.
- **Change:** Ran the eval, read one run's trace, then tightened two steps of [`SKILL.md`](../plugins/proof-before-done/skills/self-correct/SKILL.md) once:
  - **Step 4:** every edited file gets its own one-line Conflicts note, including a passing mention in a how-to. A note in one file does not cover the others.
  - **Step 7:** the `copies: <N found> -> <M stale remaining>` line is written literally, even when the rest of the report is plain prose, and each changed file is listed with whether it got its note.
- **Measure:** The eval case [`self-correct-three-copies`](../plugins/proof-before-done/evals/self-correct-three-copies/case.yaml): a fictional project, one stale rate limit in three files. Three graders: the copies line (regex), every copy fixed with a dated Conflicts note and nothing else damaged (LLM judge), and the report naming the changed files (LLM judge). Three runs with the plugin and three without.

  ```bash
  claude plugin eval plugins/proof-before-done --trust-plugin --scaffold \
    --allow-tools Edit Write --judge-model sonnet --threshold 1.0 --no-publish
  ```

- **Result:** It does not pass yet.

  | Run | With plugin | Without | Difference | Cost |
  |---|---|---|---|---|
  | First run | 0.25 | 0.00 | +0.25 | $0.85 |
  | After one tightening | 0.50 | 0.00 | +0.50 | $0.83 |

  Source: the eval's own reports, 2026-11-03.

  The trace from a diagnostic run showed the skill firing, finding all three copies and fixing every value. It lost points in two places: one of the three files got no history note, and the report said "3 found, 0 still wrong" instead of the literal copies line. After tightening, the copies line passed in all three runs. The "every copy fixed" grader still failed in all three, and that re-run did not keep its traces, so the remaining cause is not yet diagnosed.

  Without the plugin, every run scored 0.00. Those runs kept no traces either, so what they changed is not recorded here.

- **Decision:** Iterate. Keep the tightened steps, because the copies line went from 0 of 3 runs to 3 of 3. Do not claim "fixes every copy" as measured until the eval passes.
- **Next:** Re-run with `--keep-temp`, read why the judge fails "every copy fixed" (the skill, or a grader stricter than the skill), fix whichever is wrong, and record the new score here as a dated update.
