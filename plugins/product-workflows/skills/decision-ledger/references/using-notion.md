# Using Notion as the storage backend (untested)

**Untested.** The `decisions.md` file is the only tested backend, and other tools in this marketplace read that file. These notes were not run end to end against a real Notion workspace. Treat every step as a draft and say so to the user before relying on it.

Use this only when the user explicitly asks for the ledger in a Notion database. A Notion-capable tool must be connected. If none is available, keep using `decisions.md` and tell the user why. Anything that reads `decisions.md` will not see Notion entries, so say that too.

## Mapping

Use one database row per entry. Read the database schema first, since property names and types vary by workspace, and map these fields to the closest properties. Do not create a database or add properties without asking.

| Entry field | Suggested property |
|---|---|
| id and title | Title (`<id> · <title>`) |
| Type, Status, Priority, Topic | Select properties |
| Owner | Person or text |
| Logged, Review by | Date |
| Metric, Baseline, Target | Text (so `needs input` and `none set` fit). Baseline and Target hold the value only |
| Reasoning, Outcome, Lesson | Text or page body |
| Provenance | Text (the source of each number goes here, not in Baseline or Target) |

## Rules (same as the markdown version)

- Ask for the database or parent page. Never guess a location.
- Never write a value the user did not give. Unknown fields hold the literal `needs input`. A deliberate "no bet" holds `none set`.
- Log mode asks one question at a time, and review mode walks the open entries one at a time, exactly as in the skill.
- Record the user's Reasoning, Outcome and Lesson verbatim.

## Read-back

After creating or updating a row, fetch it and confirm the title, Type, Status and every bet field match what the user gave. Report the link and a one-line "what is on the entry". If the fetch fails, report "created, not verified: <reason>". In review mode, fetch every row you updated before the recap.
