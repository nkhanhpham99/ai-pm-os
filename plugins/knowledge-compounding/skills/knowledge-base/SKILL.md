---
name: knowledge-base
description: Use when the user asks an explanation-style question that teaches a concept, term, workflow, buzzword, business idea, or piece of infrastructure ("explain", "explain in plain English", "what is X", "I don't understand", "why does X work this way", "explain with full context", "explain with the broader picture"), or says "add this to my knowledge base", "save this explanation", or "what do I already have on X". Also use for a comparison or tradeoff question ("X vs Y", "pros and cons", "which should I use") only when the user asks to save it, or asks for the tradeoff "with full context". Also use when the user asks to rebuild the knowledge base index, glossary, or map.
license: MIT
---

# Knowledge base: explanations that compound

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Knowledge-base folder:** `~/knowledge/` (setting name: `knowledge-base folder`; the template's `knowledge-base-path` key means the same thing). Expand `~` to the real home path before running shell commands, and quote the path, since it may contain spaces. Create the folder if it does not exist.
- **Entry format:** plain markdown with YAML frontmatter, `[[wiki-links]]`, and mermaid diagrams. It also works unchanged in Obsidian, which is compatible but not required.
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess.
- If the settings rename the folder, treat every mention of the folder below as that path.

## What this does
Things the user learns in a session usually evaporate when the session ends. This skill makes them compound. Each explanation becomes a permanent, beginner-friendly, cross-linked entry in the knowledge-base folder: one page per concept, a diagram of where it sits in the larger system, and an anchor to what the user is working on now.

The result is a mind map, not a dictionary. Every entry zooms out from the specific answer to the bigger picture and connects to the entries around it.

## Layout of the folder
- **One page per concept:** `<Concept Name>.md` in natural title casing. However long the explanation grows, it lives on that concept's own page, never in a shared file.
- **Comparison pages:** `X vs Y.md`, for tradeoffs that were asked to be saved.
- **Three meta pages** with a numeric prefix, so they sort to the top of any file list (digits sort before letters): `0 INDEX.md` (table of every entry), `1 GLOSSARY.md` (every abbreviation and term of art), `2 MAP.md` (mermaid mind map). Keep these exact filenames, with the number and the space. Never write a bare `INDEX.md`, `GLOSSARY.md`, or `MAP.md`, which would create a duplicate that no longer sorts to the top.
- Formats for the entries and the meta pages: [entry templates](references/entry-templates.md) and [meta pages](references/meta-pages.md).

## The two-phase flow

### Phase 1: answer in the session, undisturbed
Answer the question exactly as the session naturally would. Do not restructure the answer around this skill, do not announce capturing mid-answer, and do not make the user wait. If they asked for plain English, lead with the beginner-level framing before any jargon.

### Phase 2: capture in the background
After the answer is delivered, dispatch ONE background agent (Agent tool, `run_in_background: true`, general-purpose) to write the entry. Say so in one short line ("Adding this to your knowledge base in the background") and carry on with whatever the session was doing. Capturing never interrupts the work.

Build the agent's prompt from [the capture prompt](references/capture-prompt.md). It must be self-contained, because the agent cannot see the session. Fill in:
1. **The concept name(s).** Usually one. If the answer taught several distinct concepts, list each, and the agent writes one file per concept, cross-linked.
2. **The full explanation just given.** Paste it. Do not summarize it away.
3. **Session context.** What project or task was active when the question came up. Anchor to the user's current projects (from CLAUDE.md / cwd). Only you can supply this, and it becomes the entry's "In my world" section. For a saved comparison, pass the full case: the project, the scale, the constraints, which option won and why.
4. **The folder path** (resolved from the settings), and the path of this plugin's reference files so the agent reads the templates.

If the Agent tool is unavailable, do the capture inline at the end of your turn using the same steps. It is fine to be brief on polish, but never skip the index update, the relationship linking, or the read-back.

## What the capture does
1. **Check what exists.** List the folder. Read `0 INDEX.md` and `1 GLOSSARY.md`. The glossary catches alias collisions the file list misses (the question says "RLS" but the page is `Row-Level Security.md`). If the concept already exists, update that entry: merge the new explanation, add the new session context to "In my world", refresh `updated:`. Never create a duplicate or a "-2" file.
2. **Write or update the entry** from the right template: a concept entry for "what is X", a comparison entry for a saved tradeoff. If one question does both, write both and link them both ways.
3. **Connect the relationships in both directions.** Scan existing entry titles for related concepts, add them to the new entry's Related section, then open each related entry and add the new one to its Related section with a one-line relationship. A link only creates structure when the reader can travel both ways.
4. **Update all three meta pages.** A page that is not in the index, glossary, and map does not exist as far as navigation is concerned. Harvest every abbreviation and term of art from the entry into the glossary, including terms with no page yet.
5. **Read back, then report.** Re-read the written entry and each updated meta page from disk, and confirm the content is there. Report the files written and updated, back-links added, glossary terms added, and the entry count. If any read-back could not be done or did not match, say "not verified" and why. Never imply the write landed.

## Writing rules
- **Never invent.** The "In my world" section uses only what you were given: the session context or notes the agent actually read. If nothing connects yet, say which future work would likely touch the concept.
- **Beginner-first, always.** The user may reread an entry months later with zero context, so the "Plain English" section must stand alone.
- **Every jargon term is a link or a definition.** A term that deserves its own entry but has none is still written as `[[Term]]`, which shows up as a visible gap. Do not recursively create entries for every linked term. Only the concepts actually explained in the session get pages.
- **A comparison verdict is only true for a specific case.** Comparison entries accumulate case verdicts over time. When the same tradeoff resurfaces in another project, append a new case verdict. Never overwrite or "correct" an old one.
- **Tags are the third connection dimension.** One domain tag plus a few topical tags per entry. Reuse existing tags rather than minting near-synonyms.
- **The knowledge-base folder is the only place this writes.** Do not edit other notes, memory files, or project docs.

## Explicit commands
- **"What do I have on X?" / "check my knowledge base":** read the entry and its related entries, answer from them, and say when each was last updated. Read-only, so no capture follows.
- **"Add this to my knowledge base":** capture whatever was just discussed, even if it was not a question. Same Phase 2 flow.
- **"Rebuild the index / glossary / map":** regenerate the three meta pages from the entry files on disk, useful after hand edits. Read the pages back before reporting.

## Anti-patterns
- Changing how the answer is written, or announcing the capture before the answer is delivered.
- Capturing a one-line factual lookup. Only answers that teach something are worth an entry.
- Writing a long explanation into a shared file instead of the concept's own page.
- Adding an entry without updating the index, glossary, and map.
- Forward links with no back-links.
- Product, project, or stack details that nobody supplied. Anchor only to what the session context says.
- Reporting "added" without re-reading the files from disk.
