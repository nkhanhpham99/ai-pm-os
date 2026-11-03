# Using Notion as the storage backend (untested)

**Untested.** The markdown files in the PRD folder are the only tested backend. These notes were not run end to end against a real Notion workspace. Treat every step as a draft and say so to the user before relying on it.

Use this only when the user explicitly asks for the PRD in Notion. A Notion-capable tool must be connected. If none is available, keep the markdown files and tell the user why.

## Rules

1. **Only push the shareable copy.** The working copy, with local paths and session references, never goes to Notion. Make the shareable copy and pass its grep check first (see the PRD skill, step 6).
2. **Ask before pushing.** Never push unprompted.
3. **Published-reference rule.** The Notion page may only reference material that is itself published and reachable by the readers. If the PRD leans on a deck, a research note or an analysis, publish that to Notion first (as its own page or attachment) and link it, or drop the reference.
4. **Self-contained.** Every line must carry its full context in plain language. No local paths, no session identifiers, no unlabeled shorthand.
5. **Do not clobber.** If the user points at an existing page that has content (an overview, action items, attachments), merge into it: fill existing sections, append the PRD below, leave other blocks alone.
6. **Ask for the parent.** Get the parent page or database from the user. Do not guess a location. Read the database schema before setting properties, since schemas vary by workspace. Some properties (tags, owner) may not be settable through the API; tell the user which ones to set by hand.

## Steps

1. Create the page under the agreed parent. If the title does not apply on create, update it in a follow-up call.
2. **Read it back.** Fetch the page and confirm the title, the metrics table with its reasons, the open questions, and that tables and callouts rendered. Fix rendering quirks (bold text butted against inline code can leave stray asterisks, so rephrase those spans) and fetch again.
3. If you cannot fetch it, report "created, not verified: <reason>".
4. Report the page link and a one-line "what changed".
5. **Keep both copies in sync.** On every later edit, update the working copy, regenerate the shareable copy, re-run the grep check, then update the Notion page and read it back again.
