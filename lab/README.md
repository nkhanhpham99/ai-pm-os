# The lab

This folder is a notebook of dated experiments on my own AI agent setup. Each entry starts with a hypothesis, makes one change, measures it, and records what I decided. Some plugins in this repo exist because an entry here showed a problem worth fixing. The rest carry no impact claim until an entry measures one.

Rules for every entry:

- Every number has a source: a command anyone can re-run, or a named measurement with its date.
- If a number cannot be sourced, the sentence has no number.
- A result that has not been measured yet is written as "pending". It is never predicted.
- Entries are not rewritten after the fact. A later measurement gets its own entry, or a dated update at the bottom.

## Entries

| # | Entry | Status |
|---|---|---|
| 001 | [Auditing my own agent setup](001-auditing-my-agent-setup.md) | Done. Baseline for 002. |
| 002 | [Does my agent actually verify before saying "done"?](002-does-my-agent-verify.md) | Hook shipped. Follow-up measurement pending. |
| 003 | [A fix that checks itself](003-a-fix-that-checks-itself.md) | Kept. |
| 004 | [Guardrails that match on text misfire](004-guardrails-that-match-text-misfire.md) | Open. Fix not built. |
| 005 | [Does logging every update keep my docs true?](005-a-fix-that-left-its-warning-behind.md) | Iterating. Two-week count pending. |
| 006 | [Does self-correct pass its own eval?](006-does-self-correct-pass-its-own-eval.md) | Passing in one run (1.00) after a grader fix. Full run pending. |

## Entry template

Copy this into `lab/NNN-short-title.md`.

```markdown
# NNN: Title as a question or a claim

- **Date:** YYYY-MM-DD
- **Hypothesis:** what I expect, stated so it can be wrong.
- **Change:** what I changed, with a link to the commit or the files.
- **Measure:** how it was measured. Give the command when it can be re-run.
- **Result:** the numbers, each with its source.
- **Decision:** keep, revert, or iterate, and why.
- **Next:** the follow-up, and when.
```

## Suggest an experiment

Open an issue with the [experiment idea template](../.github/ISSUE_TEMPLATE/experiment-idea.md). It asks for the same fields as an entry. A good suggestion names something you could measure today, even roughly.
