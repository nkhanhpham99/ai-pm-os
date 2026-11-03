# session-handoff

Keeps one lean STATUS.md current, so you can `/clear` and the next session resumes by reading a single file.

## The problem

A long session holds a lot of state: what is done, what is in flight, what was decided and why, what was ruled out, what is waiting on someone else. When the context is cleared or the session ends, that state is gone. The usual fix is a long summary pasted into chat, which nobody keeps and which duplicates whatever the project already records.

## What is included

| Part | What it does |
|---|---|
| `skills/session-handoff` | Updates the project's `STATUS.md` in place, re-reads it from disk to confirm the write landed, then gives a three-line chat receipt and a copy-paste primer for the next session. |

It works for any kind of work: a build, a brainstorm, a prototype, a campaign, research, scheduling, tracking. The skeleton is the same and only the content changes.

## How it works

1. **STATUS.md is the artifact, chat is the receipt.** The full state goes into the file. Chat only confirms what changed.
2. **Lean, not an append-log.** Current state only. Finished items shrink to one-liners, and deep detail stays in a notes, research, or plan doc that STATUS.md links by absolute path. Git history keeps the rest.
3. **Fixed sections:** Standing gotchas (including "Tried & rejected"), Quick start, CURRENT, NEXT, BLOCKED, CHECK / ASK, DONE. An empty section says "none".
4. **Merge, don't clobber.** If a STATUS.md already exists, the skill matches its headings.
5. **Read-back before the receipt.** After writing, the skill re-reads the file from disk and confirms the changed sections are there. If it cannot, the receipt says "not verified".
6. **Copy-paste primer.** Every handoff ends with a block to paste into a fresh session. It names the absolute path and tells the agent to read the linked docs too.
7. **Teammate ask-docs only when needed.** If the work is blocked on a person, their asks go in a separate `<NAME>-ASKS.md`. Solo work gets none.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install session-handoff@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`.

## Use it

Say "session handoff", "wrap up session", "update STATUS", or "record where we are". The skill also applies when you are about to `/clear`, and it should be used at milestones during a session rather than only at the end.

To change the defaults (the status file name or the ask-doc name), add an `## ai-pm-os settings` section to your CLAUDE.md. The skill reads it before using its own defaults.
