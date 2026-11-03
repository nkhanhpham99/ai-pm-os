# Source playbook

How to get trustworthy material out of each kind of source, and how to grade it. Read only the sections that match the question. The goal everywhere is the same: capture **exact wording, exact numbers, the URL, the publish date and the sample size** at the moment you find them.

## Credibility tiers (assign one to every source)

| Tier | What it is | How to use it |
|---|---|---|
| **A** | Peer-reviewed studies, official statistics (government, intergovernmental bodies), regulatory filings, census | Establishes fact. Safe to generalize within the study's stated population. |
| **B** | Reputable journalism, industry or analyst reports with a stated methodology, official company data (filings, press releases) | Strong signal. Trace numbers to the primary source when you can, because reports often re-cite each other. |
| **C** | Forums, social posts, app-store reviews, individual anecdotes, marketing blogs, vendor-sponsored "studies" | Signal, not proof. Tells you what to investigate and adds qualitative voice. Do not generalize it or quote it as a population statistic. |
| **D** | Undated, unattributed, AI-generated or content-farm pages | Avoid. If unavoidable, flag loudly and treat it as a lead to verify, never as evidence. |

The most common research error is laundering a Tier C figure ("a commenter said 70% of people...") into an analysis claim as if it were Tier A. Do not.

## Community discussions (Reddit and similar)

Best for: what real people feel, complain about, ask for and recommend. This is raw voice-of-customer.

- If a Reddit tool is installed (for example a Reddit MCP server), use it. Otherwise use web search restricted to the site, and read the pages you find.
- Start by discovering which communities discuss the topic. If a tool gives relevance scores, follow high-scoring communities directly, combine several for medium scores, and refine the search terms for low ones.
- **Read titles and post text first.** They are cheap and carry most of the signal. A listing of 12-15 posts often reveals the recurring themes without opening a single comment tree.
- **Pull comments deliberately.** For a normal run, open comments on the one to three highest-signal threads. Each full tree is large. Theme frequency comes from how many independent posts raise a point, not from exhaustive reading.
- **When lived sentiment is the deliverable**, go deeper: more threads, fuller trees. Price it as a separate line in the cost menu and let the user approve the spend.
- **Always capture** the URL, the community, the post date, the score, and the verbatim quote. Report it as "users in <community> expressed...", never as a statistic. Note how many independent threads a theme appeared in. That is a frequency seen, not a percentage.

## Web, news and trends

Best for: market size, growth, funding, competitor news, regulation, what is trending now. Add the current year to recency-sensitive queries.

- Search to find candidates, then fetch the actual page and extract the exact figure and its date.
- **Chase the primary source.** An article that says a market "will reach X by year Y" is re-citing a report. Find that report and capture its name, date and methodology. Cite the primary, and note the secondary as where you found it.
- Record both **publish date** and **access date**. A projection from several years ago is a different fact from a current one.
- Restrict a search to primary domains (government, established analysts) when you need Tier A or B.
- If a page is script-heavy or blocks automated reads and a plain fetch returns little, say so under Gaps. Use a browser tool only if one is installed and the user is fine with it, and read only what is visible.

## Scientific and evidence questions

Best for: "is it actually true that...", "does X correlate with Y" - anything needing a defensible claim.

- Search Google Scholar, PubMed and journal sites. Prefer systematic reviews and meta-analyses over single studies.
- **Always capture** the study design (RCT, observational, meta-analysis), sample size N, population, effect size, publication date and journal. Design and sample size are the difference between "evidence" and "a study once suggested".
- Note funding or conflicts of interest when stated.
- Flag contested evidence in the Conflicts list.

## App-store reviews and competitor products

Best for: competitor strengths and weaknesses in users' own words, feature gaps, pricing, positioning.

- Fetch store listing and review pages. Capture rating, rating count, review date and verbatim review text.
- For each competitor capture: a positioning one-liner, core features, pricing tiers as published, platform, a rough size signal (ratings count, not downloads unless stated), and what reviewers praise versus criticize. Reviews are Tier C: report themes and counts, not percentages.
- Pricing and features change. Record the access date next to every price.

## Professional and B2B signal (read-only)

Best for: competitor company facts (description, website, follower size, official posts), partnership-channel intelligence, and how professionals talk about the topic.

- Use only public pages and public search. If a LinkedIn-capable tool is installed, use **read-only** operations only (company lookups, follower counts, reading a specific post). Its posting and ad-management operations are never part of research.
- **Hard rule:** never post, comment, react, reshare, delete, or touch ad campaigns on a real account while researching.
- If a page needs a logged-in session, read only what is already visible. Never log in on the user's behalf, scrape at scale, or take actions on the account.
- Capture author (with role and company), the post text verbatim, publish date, reaction and comment counts if shown, and URL.
- Tier: **B** for verifiable company facts pulled from an official company page, **C** for opinion. Much professional content is marketing, so treat vendor claims as Tier C until traced to a primary source.

## Competitor advertising (public ad libraries)

Best for: how competitors talk to customers: live ad creative, messaging angles and audience framing.

- Use a public ad library (for example the Meta Ad Library, through an ads tool if installed or through the library's own search page). Capture the advertiser, the ad copy verbatim, a description of the creative, and the dates the ad ran.
- Useful for positioning work: what claims do competitors make, which emotions do they target, and do they make claims the user's product must avoid for legal or regulatory reasons?
- An ad running is not proof it works. Report what is said and shown, not how well it performed.

## When sources disagree

This is normal and valuable. Do not resolve it by picking the convenient source. Record both in the Conflicts list with their tiers, and in the analysis explain the likely reason (different populations, dates, definitions, methods or incentives). A surfaced conflict is a finding. A hidden one is a liability.
