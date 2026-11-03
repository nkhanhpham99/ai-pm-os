---
name: session-handoff
description: Use when the user says "wrap up", "write a handoff", "session handoff", "update STATUS.md", "record where we are", or "save progress before I clear context", or is about to /clear, compact, or end a long session. Also use proactively at a milestone, a new pending item, or a new open question. Applies to any kind of work (build, brainstorm, prototype, campaign, research, schedule, tracking, summary).
license: MIT
---

# Session handoff: keep one lean STATUS.md current

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Status file:** `STATUS.md` at the root of the project or work folder.
- **Teammate ask-doc name:** `<NAME>-ASKS.md` at the same root, named for the person. Created only when needed (see below).
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F` or ask. Never guess.
- If the settings rename the status file, treat every mention of STATUS.md below as that name.

## What this does
Keep a lean, always-current STATUS.md for whatever the user is working on, so they can `/clear` and the next agent resumes by reading that one file. It applies to every kind of work: building, brainstorming, prototyping, running a campaign, research, scheduling, tracking. It is not just for code.

**STATUS.md is the durable artifact. Chat is only a receipt.** Never dump a long handoff into chat, because that duplicates the file. Write the current state into STATUS.md and give a short confirmation in chat.

**STATUS.md stays lean.** It is current state, not an append-log. Deep detail lives elsewhere (a notes file, a research or spec doc, a plan) and STATUS.md points to it. Finished items compress to one-liners. Where the file is git-tracked, `git log -p STATUS.md` preserves the full history.

## When to invoke
The user asks for a handoff, a wrap-up, a status update, or to record where things stand, or is about to `/clear`. Also invoke it side-by-side: at each milestone, new pending item, or new thing to check or ask, not only at the end of a session.

## Workflow
1. **Review the full conversation**, not just the last few turns.
2. **Gather session state.** You already know it, so do not audit the filesystem or run broad searches. Collect what got done, what is in flight, what is queued, decisions made, open questions, teammate asks, and any deep-detail docs written. For live work, also collect background processes started with `run_in_background` (the shell IDs matter) and any dev server, URL, or artifact the work runs at.
3. **Locate STATUS.md** at the root of the project or work folder. If none exists, create one using the structure below. If one exists, **merge into it**: match its headings, and do not restructure or overwrite it.
4. **Update it lean and side-by-side.** Move finished items into DONE as one-liners. Refresh CURRENT, NEXT, and CHECK / ASK. Keep Standing gotchas and Quick start accurate. Stamp "Last updated" with today's date. Use the date from the environment or conversation; if neither gives one, run `date +%F` or ask. Never guess. Edit the file directly, since it is the user's own status doc.
5. **Route teammate asks to a separate doc, only when needed** (see below).
6. **Read it back (required).** Re-read STATUS.md from disk after writing and confirm the sections you changed are actually there: the new "Last updated" date, the items you moved or added, and the deep-doc paths. If the file was not written or the read-back does not match, fix it and re-read. If you still cannot confirm it, say "not verified" in the receipt and say why. Never imply the file landed.
7. **Give a short chat receipt and a copy-paste primer**, not the full handoff (see below).

## STATUS.md structure (lean)
Order and meaning, adapted to the work type. When a STATUS.md already exists, follow its shape instead.

```
# <Project / work> — STATUS

_Last updated: <YYYY-MM-DD> · <one line: what this is>_

## Standing gotchas
- <constraint, warning, or thing that bit us that stays true across sessions> — or "none yet"
- Tried & rejected: <approach ruled out + why, so the next session does not redo it> — or "none"
  (build: shared code, secrets, risk to other environments. campaign: brand red lines, things not to
   mention. research: source caveats. tool or API: burns credits.)

## Quick start
<how a fresh agent resumes fast, in a few lines: what to read for deep detail (notes file,
 research or spec doc, plan, as absolute paths), and how to run or open the work: dev server,
 background shell IDs and the kill command, OR the artifact / doc / dashboard URL, OR the output
 file path.>

## 🔁 CURRENT
- <in flight right now + what is left> → deep detail: `<absolute path to notes / research / plan>`

## ⏭️ NEXT
- <queued, roughly ordered> (link its deep doc if the item needs more than a line)

## ⏸️ BLOCKED
- <item> — waiting on <who / what> → see `<NAME>-ASKS.md` — or "none"

## ❓ CHECK / ASK
- <open question or decision for the user to confirm> — or "none"

## ✅ DONE
- <one-liner, newest first. When it settled a decision, keep the why inline: `did X (chose over Y, because Z)`.>
```

**Adapt by work type.** The skeleton stays the same and the content changes. Build: DONE lists shipped changes and paths, Quick start says how to run it and which branches matter. Brainstorm: CURRENT holds the directions being explored, NEXT holds what to pressure-test. Campaign: DONE lists assets sent, Quick start gives the tracker or analytics URL. Research: DONE lists questions answered, Quick start gives the output doc path. Schedule or tracking: CURRENT holds live items, NEXT holds what is upcoming.

## Teammate ask-docs, only when you need them
If the work needs a teammate (a question only they can answer, a handoff, a blocker on their access, secrets, or deploys), collect those asks in a **separate `<NAME>-ASKS.md`** at the project root, named for the person. Write it so that person's agent can act on it, and mark each ask as new, sent, or done. Point to it from the CHECK / ASK or BLOCKED line in STATUS.md.

Do **not** create a teammate doc for solo work. If no teammate is involved, there is no ASKS file, and CHECK / ASK just holds the user's own open questions (or "none").

## Chat receipt and copy-paste primer
Keep it to this, every time. First the short receipt:

```
STATUS.md updated → `<absolute path>` (read back: verified)
Changed: <e.g. moved 3 items to DONE, added X to CURRENT, new BLOCKED item on a teammate>
Needs you / teammate: <blocking question + who> — or "nothing"
```

If the read-back failed or was skipped, write `(read back: not verified, <reason>)` instead.

Then always add a ready-to-copy block the user can paste into a brand-new session so it orients itself with full context. It is a fenced block of one or two lines that names the STATUS.md path and the current thread:

````
Paste into the next fresh session:
```
Read `<absolute path to STATUS.md>` and every deep doc it links, top to bottom, then continue from CURRENT. We're mid-stream on <one-line what CURRENT is>; next up is <NEXT in about 6 words>.
```
````

The primer must name the **absolute STATUS.md path** and tell the agent to read the docs STATUS.md points to. That is what makes "full context" real, rather than just the board.

## Hard rules
1. **File first, not chat first.** Full state goes in STATUS.md. Chat is the short receipt. Never paste the whole board into chat.
2. **Keep it lean, never re-sprawl.** DONE items are one-liners. Deep detail lives in notes, research, or plan docs, not STATUS.md. Do not append raw logs.
3. **Side-by-side updates.** Update at every milestone, new pending item, or new ask, not only at wrap-up.
4. **Every deep thread links its doc.** Any CURRENT, NEXT, or BLOCKED item with more than a line of real context must name its deep doc by absolute path. "Read STATUS.md and continue" only delivers full context if every thread links to its depth.
5. **Record the why on decisions.** When an item settles a choice, keep the rationale inline (`chose X over Y, because Z`) so the next session does not reopen it. Capture ruled-out approaches under Standing gotchas, in "Tried & rejected".
6. **Read back before the receipt.** Never say STATUS.md is updated until you have re-read it from disk. Otherwise say "not verified".
7. **Always end with the copy-paste primer.** Every handoff produces the fenced primer block naming the absolute STATUS.md path.
8. **One STATUS.md per project, merged not duplicated.** Match an existing file's headings. Never spawn a second status file.
9. **Teammate docs only when needed.** Create `<NAME>-ASKS.md` only when actually collaborating with, or blocked on, that person.
10. **Never invent state.** For an empty section, write "none" and do not omit it.
11. **Absolute paths always** inside STATUS.md, never `~` or relative paths.
12. **Background and live state is load-bearing.** Background shell IDs plus the kill command, dev ports, and live URLs go in Quick start, or the next agent cannot find them.
13. **Stay in scope.** This skill writes only STATUS.md (and an ask-doc when needed); it does not touch other notes or memory unless the user asks.

## Anti-patterns
- Dumping the full board into chat alongside the file.
- Letting STATUS.md grow into an append-log, or keeping DONE verbose instead of one-liners.
- Putting deep reasoning or history in STATUS.md instead of pointing to the notes, research, or plan doc.
- Creating a teammate ASKS file for solo work, or a second STATUS.md when one exists.
- Leaving CURRENT or Quick start vague. They are what the next session reads first.
- Relative paths or `~` inside STATUS.md.
- Making up the "Last updated" date. Use the date from the environment or conversation, or `date +%F`.
- Reporting "updated" without having re-read the file.
