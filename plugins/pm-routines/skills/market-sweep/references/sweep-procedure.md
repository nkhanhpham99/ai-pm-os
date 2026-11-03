# Sweep procedure

How one run gathers material. The order is fixed so the parts that matter most never fall off the end of the budget. Platform-specific blocks and workarounds are in [the platform notes](platform-notes.md).

## Run order

| Order | Step | Rule |
|---|---|---|
| 1 | Read state | Brief and watchlist in full. Only the recent run-log rows, recent learnings and the previous sweep's header. Never read `*-archive.md` files unless a question needs history. |
| 2 | Inbox | Only if the brief names an inbox source. Triage every drop, but cap the depth. A drop that needs more becomes "carried to next run". |
| 3 | Floor | Every platform in the brief, at least one read each. Within the floor, cheapest and most reliable first: APIs and MCP tools, then web search and fetch, then the browser last (it is the slowest and most fragile; a browser failure then costs nothing already gathered). |
| 4 | Explore | Open discovery outside the brief (Track C below, new brands, new communities). Every run. |
| 5 | Rotation | Extra depth on one platform per run, rotating, only if budget is left. |
| 6 | Write | Sweep file, run-log row, watchlist updates, optional summary post. |

A floor platform or the explore step is skipped only when unreachable, never to save budget. When budget runs short, cut rotation first, then inbox depth.

## Capture rules (everywhere)

- Capture **at the moment you find it**: platform, URL, author and their context, the hook verbatim (the opening line, the on-screen text, or the first seconds described literally), format, post date, engagement as displayed, recurring comment themes.
- **Engagement is text, not a number.** Write `471.9K (as displayed)`. Platforms round. Never un-round, convert or estimate.
- Prefer **many cheap reads** (titles, hooks, captions, search result cards) over **few expensive dumps** (whole comment trees, whole pages).
- If a platform is unreachable, record it under "skipped and why" and move on. Never produce findings for a platform you did not reach.

## The inbox (optional brief field)

An inbox is a place where people drop links for the next run: a chat channel, or a plain file such as `INBOX.md` in the data folder. A person chose to flag each drop, so drops outrank standing queries.

1. **Read new drops** since `Inbox last processed` in the watchlist. Skip the routine's own summary posts and earlier replies.
2. **Open each drop read-only** and capture what it actually is (creator, hook verbatim, format, engagement as displayed, date). Read the sender's note as their hypothesis ("the way they open this" points at the hook; "competitor?" points at positioning) and answer their question.
3. **Test whether it is isolated or rising.** Run two or three adjacent searches (the same mechanism from other creators, the same theme on another platform, the account's own recent posts). Then give one verdict:
   - **Rejected**: fails an exclusion gate. Say which gate.
   - **Rising**: at least three independent creators, each passing the gates, using the same mechanism (not merely the same topic), clustered recently. Promote to a pattern.
   - **Isolated**: a good post with no wave behind it. Log it as craft and say plainly it is not a trend. At two creators, "possible, watch it".
   - **Established**: already in the brief or earlier sweeps, or so common it is table stakes. Link the earlier finding and judge saturation.
   When evidence is thin, the honest default is **Isolated**, not Rising.
4. **If it is a brand**, check it against the competitor roster. A new name goes into the watchlist as `candidate - confirm?`.
5. **Reply** to the person who dropped it, if the inbox is a channel where replies are possible: what it is, the verdict with the evidence, and what to take from it or why not. Three or four lines. An honest "not much here, and here is why" teaches the target faster than silence.
6. **Advance `Inbox last processed`** to the newest drop handled. Never re-process an answered drop.

## The three tracks

Themed keyword searching alone tends to return content farms and creators trading on their own audience. These three tracks lead instead.

### Track A: competitor and category accounts
**The question: how do the products in this space perform on social, and what works for them?**

Work the competitor roster from the watchlist, the most important first. For each brand capture:
- The content mix they post (product demo, founder talking, customer story, meme, carousel, trend reuse).
- **Which posts beat that account's own baseline.** Compare against the account's typical numbers, not the platform's. A post far above a small account's usual reach is the finding; the same reach on a large account may be a flop.
- How they open: the first line or first seconds, verbatim.
- What they claim, and whether any claim crosses the user's red lines (defensive intelligence: claims a regulator or a platform could act on).
- Their ad-library activity: is the brand spending, how many ads are live (as displayed), and what angle the copy takes.

Brand accounts are exempt from the parasocial gate, which makes them strong evidence.

### Track B: theme accounts
**The question: who posts consistently about the category's topics without it being about one person's life?**

Accounts built around a topic, not a person. Their output is a template, which is what a small team can actually reuse. Capture the **repeatable production formula**: text placement, audio choice, edit rhythm, carousel structure, caption pattern. New finds go into the watchlist as `candidate - confirm?`.

### Track C: trend radar
**The question: what is rising on the internet right now, and can the user credibly join it?**

Not limited to the category. For each trend, answer:
1. What it is, in one line, with a linked example.
2. Where it is on the curve: emerging, peaking, saturated or dead. Joining a saturated trend reads as late.
3. Does it have a core that fits the user's audience and goals? Most trends do not, and forcing one is worse than skipping it.
4. Can the user join without breaking a red line or looking like a brand pretending to be someone it is not?

**Say no often and explicitly.** "We looked, and this one is not for us because X" is a useful output. Trends are craft-only unless they genuinely touch the core or adjacent tier.

## Per-platform notes

Use what is installed. [The platform notes](platform-notes.md) hold the known blocks and workarounds.

- **Communities (Reddit and similar).** Through a Reddit tool if installed, otherwise web search restricted to the site. Start from the watchlist's communities. Titles and post text first, sorted by top over the sweep window. Open comments only on the few richest threads. Capture community, date, score as displayed, verbatim title or quote, URL. Theme frequency is how many independent posts raise it, never a percentage. Communities are the best source for feature demand, because people explain their reasoning in text.
- **Video platforms with an API (YouTube).** Search for candidates in the sweep window, then fetch statistics for the ones worth keeping. API counts are exact; record them with the retrieval date. Region and language parameters are hints, not filters: apply the language gate to each result by hand.
- **Ad libraries (Meta Ad Library and similar).** Search by the competitor's page or brand name, never by generic category keywords (those return spam advertisers). Record the number of live ads as displayed. Fetch creative snapshots sparingly, and only for relevant advertisers. An ad running is not proof it works.
- **Web, news and roundups.** The substitute for platforms you cannot reach directly: weekly trend roundups, "why this went viral" analyses, competitor blogs and changelogs. These are reporting, not measurement: attribute their numbers and treat them as claims. Add the year to recency-sensitive queries.
- **Browser-only platforms (TikTok, Instagram and similar).** Read-only, through a browser tool, using search pages, hashtag pages and named accounts. Never the home or "for you" feed. If signed out, skip and say so.

## Stop at the ceiling

When the budget in the brief is nearly spent, stop gathering and write with what you have. The sweep file names what was cut short. A complete file from partial data beats an abandoned run.
