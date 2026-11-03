# 001: Auditing my own agent setup

- **Date:** 2026-11-02
- **Hypothesis:** My Claude Code setup does what its rules say it does. If that is true, the rules I wrote down should be backed by something that enforces them, and the tools I built should be in use.
- **Change:** None. This entry is the baseline audit that the later entries respond to.
- **Measure:** Two passes over the setup as it stood that day.
  1. **File review.** Read every instruction file, hook, custom subagent definition and the permissions file. For each hook, asked one question: can it stop the agent, or can it only print a message?
  2. **Transcript scan.** Searched past session transcripts for each custom subagent, to see which ones had ever been invoked.
- **Result:** Rules strong, enforcement thin.

  | Finding | Number | Source |
  |---|---|---|
  | Hooks that could block anything | 1 of 4 | file review, 2026-11-02 |
  | Custom subagents never invoked | 5 of 8 | transcript scan, 2026-11-02 |
  | Permissions file size | 1,613 one-off entries | file review, 2026-11-02 |

  The rules were clear and specific. Almost nothing checked whether they were followed. The other three hooks could not stop anything. The permissions file had grown one approval at a time until it was too long to review.

- **Decision:** Iterate.
  - **Rebuilt the permissions file** as 224 entries, with an ask-first list for risky actions. [`templates/settings.example.json`](../templates/settings.example.json) shows the shape of an ask-first list.
  - **Enforce proof before done first**, with a hook that can block a turn. That became [lab 002](002-does-my-agent-verify.md) and the [`proof-before-done`](../plugins/proof-before-done/) plugin.
  - The unused subagents were not acted on in this entry.
- **Next:** Re-run the same two passes once the lab 002 follow-up is measured, and compare against this baseline.
