# Background capture prompt

Use this as the prompt for the single background agent in Phase 2. Fill every `<...>` slot. The agent cannot see the session, so the prompt must be self-contained. Dispatch it with `run_in_background: true`.

```
You are capturing one explanation into the user's knowledge base. Work only inside the
knowledge-base folder below. Do not edit any other file.

KNOWLEDGE-BASE FOLDER: <resolved absolute path; create it if missing; quote it in shell commands>
TODAY: <YYYY-MM-DD>
CONCEPT(S): <name, or a list if the answer taught several distinct concepts; one file each>
ENTRY TYPE: <concept | comparison | both>

THE FULL EXPLANATION GIVEN IN THE SESSION (verbatim, do not shorten):
<paste it>

SESSION CONTEXT (what the user was working on when this came up; this becomes the
"In my world" anchor, and for a comparison the case verdict: project, scale,
constraints, which option won and why):
<paste it. Anchor to the user's current projects (from CLAUDE.md / cwd).>

READ FIRST: <absolute path of this plugin's skills/knowledge-base/SKILL.md>, and the
templates it links in references/entry-templates.md and references/meta-pages.md.
Follow "What the capture does" in SKILL.md exactly.

STEPS
1. List the folder. Read `0 INDEX.md` and `1 GLOSSARY.md` if they exist. If an entry for
   this concept already exists (check aliases through the glossary), UPDATE it: merge the
   new explanation, add the new session context to "In my world", refresh `updated:`.
   Never create a duplicate or a "-2" file.
2. Write or update the entry from the right template. Beginner-first. Every jargon term
   is defined inline or written as a [[link]]. Include a small mermaid diagram that shows
   the concept in its system. Use only the session context above for "In my world".
   Never invent project details.
3. Add back-links: for each related existing entry, open it and add this one to ITS
   Related section with a one-line relationship.
4. Update all three meta pages, `0 INDEX.md`, `1 GLOSSARY.md`, `2 MAP.md`, with these
   exact filenames. Create any that are missing. Add every abbreviation and term of
   art from the entry to the glossary, including terms that have no page yet.
5. PROOF BEFORE DONE. Do not report success from memory of what you wrote. Re-read from
   disk (a fresh read, not your earlier text):
   - the entry file you wrote or updated,
   - each back-linked entry you edited,
   - `0 INDEX.md`, `1 GLOSSARY.md`, and `2 MAP.md`.
   For each one, confirm the new content is actually there: the entry's title and
   `updated:` date, the new row in the index, the new terms in the glossary, the new
   node and edges in the map, the back-link lines. If a file is missing, empty, or does
   not contain what you wrote, fix it and re-read. If you still cannot confirm something,
   or could not re-read it, say "not verified" for that file and give the reason. Never
   imply a write landed.

FINAL REPORT (one line each): files written, files updated, back-links added, glossary
terms added, current entry count, and for every file either "read back: verified" or
"not verified: <reason>".
```

## Notes for the dispatcher
- Pass the explanation verbatim. A summary loses the exact analogies and examples that make the entry good.
- If the session context is thin, say so in the prompt rather than padding it. The agent will then write "In my world" as future-work pointers instead of inventing a connection.
- When the background agent finishes, relay its report only if it says "not verified" or reports a problem. Otherwise a verified capture needs no further message to the user.
