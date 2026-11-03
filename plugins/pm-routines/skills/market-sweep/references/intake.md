# Intake: the setup interview

The sweep is only as good as its brief. This interview gathers the foundational facts a sweep needs, then the agent does its own research to fill what the user did not know, then the user approves a written brief. Nothing runs before that approval.

## How to ask

- **One question at a time.** Wait for the answer before the next question.
- **Every question carries a recommended default** the user can accept with "yes" or "default". Say where the default came from ("from your README", "the usual choice for a first sweep").
- **Prefer multiple choice** where the options are known.
- **Read before asking.** If the user's CLAUDE.md, README or project docs already describe the product, draft the answer from them and ask the user to confirm it, instead of asking cold.
- **"I don't know" is a fine answer.** Record `needs input` for that field, carry on, and try to fill it in the foundation pass. A REQUIRED field still `needs input` at the end blocks approval, so ask again then.
- **Never invent an answer for the user.** A default is a suggestion they accept, not a value you write on their behalf.

## The questions, in this order

This is the order of the REQUIRED fields in `LANDSCAPE.md`. Fill each field with the user's answer as you go.

| # | Field | Question | Recommended default |
|---|---|---|---|
| 1 | Product one-liner | "In one sentence: what do you make, and for whom?" | Drafted from the project's CLAUDE.md, README or docs if they describe it. Otherwise no default: this one needs the user. |
| 2 | Category | "What category would a stranger put it in?" | The category the one-liner implies (for example "habit tracker", "B2B invoicing"). |
| 3 | Goals (ranked) | "Rank what the sweep is for: content hooks, competitor moves, feature demand, pricing and positioning." | Competitor moves, then content hooks, then feature demand, then pricing and positioning. |
| 4 | Competitors (at least 1) | "Name the competitors or adjacent products to watch, with a URL each." | Two or three names from a quick web search of the category, shown for the user to accept or cut. At least one is required. |
| 5 | Audience | "Who should a finding speak to? Describe the people, not a demographic box." | The "for whom" part of the one-liner. |
| 6 | Regions and languages | "Which regions and languages count? Content outside them is dropped." | The regions and languages the product ships in, if the docs say so. Otherwise ask. |
| 7 | Platforms | "Here is what I can reach with the tools installed. Which should every run cover?" | Every platform detected (see "Detecting platforms" below). |
| 8 | Relevance tiers | "Here is my draft of core, adjacent and craft-only for you. Change anything?" | Drafted by the agent from answers 1 to 5 (see "Drafting the relevance tiers"). |
| 9 | Exclusions | "Which gates should drop a candidate before it counts?" | The two default gates below, with the regions and languages from question 6. |
| 10 | Cadence | "How often should it run?" | Weekly. |
| 11 | Budget per run | "How much should one run spend? A token ceiling, a time limit, or 'the floor plus one extra source'." | The coverage floor plus one rotation source, stopping when they are done. Before the first run, state an estimate of what that costs, labelled as an estimate. |
| 12 | Output destination | "Where should sweep files go?" | `sweeps/` inside the data folder. |
| 13 | `review_by` | "When should we revisit the whole brief?" | Three months from today. |

Then the optional fields, one question each, all skippable:
- **Inbox source**: a chat channel or a file (for example `INBOX.md` in the data folder) where people drop links for the next run. Default: none.
- **Summary channel**: where the short run summary is posted, if anywhere besides the chat. Default: none (the summary stays in the session).
- **Red lines**: claims, words or topics the user's own content must never use (for example medical claims, a competitor's trademark). Adaptations that would break one are logged as off-brand, never proposed. Default: none.
- **Tune every**: default 4 runs.

### Detecting platforms (question 7)

Check which tools this session actually has before asking. Never assume a tool exists.
- **Baseline, always:** web search and web fetch. They reach news, trend roundups, competitor sites, public ad-library pages and app-store listings.
- **Optional, if installed:** a Reddit tool (for example a Reddit MCP server), the YouTube Data API (a key in the environment), a Meta Ad Library or ads tool, a browser tool (for platforms that need a rendered page, such as TikTok and Instagram).
- For each platform, say how it will be reached and what it cannot do ("Instagram: browser only, and only if you are signed in in that browser; otherwise it is skipped"). [The platform notes](platform-notes.md) list the usual blocks.

### Drafting the relevance tiers (question 8)

Three tiers, applied to every finding:
- **Core**: speaks to the audience about the problem the product solves.
- **Adjacent**: the same people or the same emotional territory, but not the product's problem.
- **Craft-only**: off-topic, but the mechanism is worth borrowing anyway.

Write each tier as a short list of concrete themes, drawn from the user's own words in answers 1 to 5. Be strict about core: inflating it destroys the ranking's only purpose.

### The default exclusion gates (question 9)

Gates are blocking. A candidate that fails one is dropped or demoted before analysis, whatever its numbers.
1. **Language and region gate.** The post itself (title, caption, on-screen text, spoken audio) must be in a listed language for a listed region. Check the post, not the query you typed or an auto-translated title.
2. **The parasocial test.** "Would this have worked from an account nobody knows?" A large creator's personal-life post performs on the audience's existing attachment to them, not on the format. Such a post is vocabulary or theme signal only: never a transferable mechanism, never counted toward a pattern. Brand and company accounts are exempt, which is why they are strong evidence.

The user can add gates (for example "drop AI-generated content farms") or remove these.

## The foundation pass

After the questions, research on your own to fill what the user did not know. Keep it cheap: search results and profile pages, not deep reads.

For each competitor:
- Official social handles on each platform in the brief (from the competitor's own site footer, then platform search).
- Their public ad-library page, if they advertise.
- App-store or product listing, if relevant.

For the audience and category:
- Communities where they talk (subreddits, forums, groups), with a one-line reason each.
- A starting set of search queries per platform, written in the audience's words rather than the category's jargon.
- Theme accounts: accounts that post consistently about the category's topics without being about one person's life.

Then show it as a list, grouped by competitor and by platform, each line marked **found** (with the URL where you saw it) or **not found**. Ask the user to confirm, cut or correct, one group at a time. Write only confirmed items into `WATCHLIST.md`. Unconfirmed items go in as `candidate - confirm?`.

## Draft, show, approve

1. Create the data folder (default `./market-sweep/`, or the `market-sweep folder` setting). Confirm the path with the user.
2. Write `LANDSCAPE.md` from [the template](../assets/LANDSCAPE.template.md) with `Status: draft`, and `WATCHLIST.md` from [its template](../assets/WATCHLIST.template.md).
3. Show both files. Point out every field still `needs input`.
4. On the user's yes, set `Status: approved` and `Approved on: <today>`. Create `LEARNINGS.md` and `RUN-LOG.md` from their templates.
5. Read all four files back from disk. Report the paths and what is in each, in one line apiece, or "not verified: <reason>".
6. Offer the calibration run.
