# Using Notion as the storage backend (untested)

**Untested.** The markdown file in the research folder is the only tested backend. These notes were not run end to end against a real Notion workspace. Treat every step as a draft, and say so to the user before relying on it.

Use this only when the user explicitly asks for the brief in Notion. A Notion-capable tool must be connected. If none is available, write the markdown file as usual and tell the user why.

## Steps

1. **Write the markdown file first.** The local file stays the working copy. Notion gets the clean brief.
2. **Ask where it goes.** Get the parent page or database from the user. Do not guess a location.
3. **Create the page** with the Notion tool, using the brief's content. Do not paste a raw HTML `<details>` block: it does not reliably convert. Render the appendix as a real toggle block, so the brief stays clean and the audit trail is one click away.
4. **Make it self-contained.** The page should be readable by someone with no access to the user's machine. Remove local file paths and session references, and link only to material that is itself published or reachable.
5. **Read it back.** Fetch the created page and confirm the title, the TL;DR, at least one findings table, and that the appendix rendered as a toggle with a non-empty ledger. Fix rendering quirks and fetch again. If you cannot fetch it, report "created, not verified: <reason>".
6. **Report** the page link and a one-line "what changed".

## Known risks

- Table and callout rendering may differ from the markdown. Check after creation.
- Property names and database schemas vary by workspace. Read the schema before writing properties.
- A page created without a stated parent may land somewhere unexpected.
