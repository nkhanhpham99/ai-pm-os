# Using Notion as the destination (untested)

**Untested.** The markdown week file is the only tested destination. These notes were not run end to end against a real Notion workspace. Treat every step as a draft, and say so to the user before relying on it.

Use this only when the brief's destination says Notion. A Notion-capable tool must be connected. If none is available (or it needs re-authorization in an unattended run), write the markdown file as usual and say in the summary which connector to reconnect.

## Steps

1. **Write the markdown week file first.** It stays the record the next run compares against.
2. **Know where it goes.** The brief names the parent page or database. Never guess a location.
3. **Create one page per week** with the week file's content: status, scoreboard table, audit, open decisions, what fell short, next week's top 3, sources. If the parent is a database, read its schema first and fill only properties that exist.
4. **Make it self-contained.** A teammate with no access to the user's machine must be able to read it. No local file paths, no private links. Name the decisions file rather than linking to a local path.
5. **Read it back.** Fetch the created page and confirm the status line, every scoreboard row, the audit and the top 3. Fix rendering problems and fetch again. If you cannot fetch it, report "created, not verified: <reason>".
6. **Report** the page link and a one-line "what changed".

## Known risks

- Tables and colored callouts may render differently from the markdown. Check after creating.
- Never edit last week's page except to tick last week's top-3 checkboxes, and only if the brief says to.
- A page created without a stated parent may land somewhere unexpected.
