# 004: Guardrails that match on text misfire

- **Date:** 2026-11-02
- **Hypothesis:** A guard hook that blocks dangerous git commands by searching the raw command text for dangerous phrases will block what it should and nothing else.
- **Change:** None yet. This entry records a failure of a local git guard hook. The guard is not part of this repo.
- **Measure:** Observed in normal use. No count, so this entry has no number.
- **Result:** The hypothesis is wrong. The guard blocked a harmless script. The script did not run anything dangerous. It only contained the text of a dangerous command (a hard reset). The guard saw the phrase and blocked the whole command.

  The guard was answering "does this text contain a scary phrase?" when the question that matters is "will this run a scary command?". Those are different questions. Text matching can get both directions wrong:
  - observed: it blocks safe commands that only mention a dangerous one, such as a script, a commit message or documentation;
  - not observed, but follows from the design: it can miss a dangerous command spelled in a way the pattern does not expect.

  It also shaped how this repo was built: some files were written with a file tool instead of a shell command, because a local guard would have blocked a shell command that merely contained such a phrase.

- **Lesson:** Match parsed commands, not raw strings. Split the command line the way the shell would, find the program and its arguments, and decide on those.
- **Decision:** Iterate. Status: open, fix not yet built.
- **Next:** Build a parser-based guard, with regression tests for both directions: a harmless command that mentions a dangerous phrase must pass, and a real dangerous command must be blocked. It gets a dated update here when it exists.
