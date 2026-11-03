# Market sweep brief

- Status: draft
- Approved on:
- review_by (REQUIRED):

The sweep reads this file before every run. Fields marked REQUIRED must be filled before a run starts; a blank, a `<placeholder>` or `needs input` stops the run with a question. `none` is a deliberate answer and counts as filled. Change this file through the `tune` mode or by hand, never during a run.

## Product
- Product one-liner (REQUIRED):
- Category (REQUIRED):
- Goals, ranked (REQUIRED):
  1.
  2.
  3.
  4.

## Competitors (REQUIRED, at least 1)
| Name | URL | Why they matter |
|---|---|---|
| | | |

Social handles, ad-library pages and communities live in `WATCHLIST.md`.

## Audience
- Audience (REQUIRED):
- Regions and languages (REQUIRED):

## Platforms (REQUIRED)
| Platform | Reached through | Known limits |
|---|---|---|
| Web search and fetch | built-in | baseline, always on |

## Relevance tiers (REQUIRED)
- Core:
- Adjacent:
- Craft-only:

## Exclusions (REQUIRED)
Gates that drop a candidate before it counts toward anything.
1.
2.

Red lines (optional): claims, words or topics adaptations must never use.
-

## Running
- Cadence (REQUIRED):
- Budget per run (REQUIRED):
- Output destination (REQUIRED):
- Tune every: 4 runs
- Inbox source (optional): none
- Summary channel (optional): none

<!-- Everything above this line is the brief to copy into LANDSCAPE.md. Do not copy the example below. -->

---

## Example (do not copy into LANDSCAPE.md)

Every value below is fictional and shows the format, not a real product or market.

```markdown
# Market sweep brief

- Status: approved
- Approved on: 2026-01-10
- review_by (REQUIRED): 2026-04-10

## Product
- Product one-liner (REQUIRED): Pantry Pal plans a week of dinners from what is already in your cupboard, for people who cook for one.
- Category (REQUIRED): meal-planning app
- Goals, ranked (REQUIRED):
  1. content hooks
  2. competitor moves
  3. feature demand
  4. pricing and positioning

## Competitors (REQUIRED, at least 1)
| Name | URL | Why they matter |
|---|---|---|
| Example Meals | https://meals.example.com | the category leader most users compare against |
| Sample Plate | https://plate.example.com | targets the same solo cooks |

## Audience
- Audience (REQUIRED): people who cook for themselves after work and hate wasting food
- Regions and languages (REQUIRED): English, for the UK and Ireland

## Platforms (REQUIRED)
| Platform | Reached through | Known limits |
|---|---|---|
| Web search and fetch | built-in | baseline, always on |
| Reddit | Reddit MCP server | comment trees are expensive; titles first |
| Instagram | browser tool, signed in | skipped when signed out |
| Meta Ad Library | ads tool | search by page id only |

## Relevance tiers (REQUIRED)
- Core: cooking for one, leftovers, using up what is in the cupboard, weeknight dinner fatigue
- Adjacent: budgeting, batch cooking, living alone
- Craft-only: any food content whose hook or format is worth borrowing

## Exclusions (REQUIRED)
1. Language and region: English, for a UK or Irish audience. Check the post itself, not the query.
2. Parasocial test: would it have worked from an account nobody knows? Brand accounts are exempt.

Red lines (optional): no health or weight-loss claims; never use a competitor's trademark in our copy.

## Running
- Cadence (REQUIRED): weekly
- Budget per run (REQUIRED): the coverage floor plus one rotation source
- Output destination (REQUIRED): ./market-sweep/sweeps/
- Tune every: 4 runs
- Inbox source (optional): ./market-sweep/INBOX.md
- Summary channel (optional): none
```
