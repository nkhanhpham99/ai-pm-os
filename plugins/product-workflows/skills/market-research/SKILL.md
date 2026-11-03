---
name: market-research
description: Use when the user wants outside evidence gathered before a product or go-to-market decision - market size, competitors and their pricing or positioning, what real people say in communities or reviews, scientific or official evidence for a claim, news, or what is trending in the market. Triggers include "research X", "look into competitors", "what are people saying about", "is there evidence that", "size the opportunity", "competitive teardown", or a bare "look into X" that needs verifiable outside facts. Not for explaining a concept (knowledge-base), writing a requirements doc (prd), or logging a decision (decision-ledger). Not for a recurring social/competitor sweep (use market-sweep).
license: MIT
---

# Market research: facts you can trust, in a brief people will read

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **Research folder:** `./research/` (setting name: `research folder`). Reports are written as `YYYY-MM-DD-<slug>.md`. Create the folder if it does not exist. Quote paths, since they may contain spaces.
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess.
- **Product context:** read it from the user's CLAUDE.md or project docs (what the product is, who it is for, any regulated or sensitive area). If none is available, ask once before gathering. Never assume a product.
- **Depth:** Lean unless the user picks otherwise. Verified for anything that will drive a decision or go to an investor.
- If the settings rename the folder, treat every mention of the research folder below as that path.
- Storage is markdown. If the user wants the brief in Notion, read [using Notion](references/using-notion.md) (untested).

## Why this skill exists
Research only helps a decision if the reader can tell what was observed from what was inferred. When a real survey figure sits next to a plausible guess, both unmarked, the team builds on something that merely felt like evidence. So the work rests on one firewall:
- **Extracted data** is only what sources actually said: verbatim, never adjusted or invented.
- **Analysis** is where judgment applies (calculations, patterns, "so what for this product"), and every claim traces to an extracted source.
- **Verification** is a pass you run on yourself before delivering, because the costliest error is a confident number nobody checked.

The firewall is how you work, not how you present. The deliverable is a short brief a team reads in two minutes. All the rigor (ledger, raw figures, conflicts, verification) is still produced in full, but lives in a collapsed appendix. Hidden is not optional.

## Workflow
Keep a todo list so no step is skipped.

### 1. Lock the question and scope
Restate the question in one sentence and confirm what is in and out. A specific question answered well beats a broad one answered shallowly.

If the request covers several distinct topics, do not cover them in one shallow pass. Decompose into an ordered list of focused sub-topics with a one-line rationale each, ask the user to approve, reorder or cut, then run each as its own deep-dive and finish with a short cross-topic synthesis.

### 2. Present the cost and depth menu, then wait
Research costs tokens, mostly from raw material piling into context (comment trees, whole articles), not from the report. Before gathering, show the user the options and let them choose. Do not choose silently. Skip the menu only if they already named a depth or said "your call".

| Depth | What it means | Use for |
|---|---|---|
| **Lean** | About 5-8 sources, many from search snippets, secondary figures flagged, only the 3-5 figures you will quote are fetched | A quick lay of the land |
| **Verified** | About 10 sources, every load-bearing figure fetched and confirmed on its primary page | Decision-facing or investor-facing work |
| **Thorough** | About 12-15 sources plus heavy community or comment reading | Only when the user asks or the stakes demand it |

For each option give a rough token estimate, labelled as an estimate and based on how many pages you expect to fetch and read. State no precise cost as fact. For a multi-topic plan, give an estimate per sub-topic and a total. Recommend one option with a one-line reason, and agree a soft ceiling: if the run nears it, stop gathering, write with what you have, and note the gap.

Cost levers that keep rigor cheap:
- Fetching a page to confirm one figure is cheap, because it returns a distilled answer. Prefer more fetches and fewer raw dumps.
- Capture the figure and its date, not the page. Never keep whole articles in context.
- Community comment trees are the biggest sink. Read titles and post text first, and open comments only on the few highest-signal threads. If lived sentiment is the deliverable, a deep read is legitimate: price it as its own line in the menu and let the user approve it.

### 3. Map the question to sources
Read [the source playbook](references/source-playbook.md) only for the platforms in scope.

| The user wants to know | Go to |
|---|---|
| What real people feel, complain about, ask for | Community discussions, app-store reviews, forums |
| Market size, growth, funding, news, trends | Web search, then reputable reports and journalism; trace to the primary source |
| Whether a claim is true | Scientific literature, official statistics |
| Competitor positioning, features, pricing | Competitor sites, app stores, public ad libraries, news |
| Professional or B2B signal | Public company pages and posts (read-only) |

Check whether a connected tool serves the question better than generic web search (a Reddit tool, an ads-library tool, a browser tool). Use what is installed, and never assume a tool exists.

### 4. Gather, and log each source the moment you use it
Record every source in the appendix ledger as you collect it, not from memory afterward: source or author, platform, type, **publish date, access date, URL, sample size (N) or "not stated", and the verbatim figure or quote**. **Never paraphrase at the gathering stage.** Capture exact wording and exact numbers.

Give every source a credibility tier (A to D, defined in the playbook). One rule protects the whole report: never generalize from Tier C or D. Forums, social posts and reviews tell you what to investigate. They do not establish what is true or how many.

### 5. Extract, with zero interpretation
Fill the ledger and the key-figures list using only what sources said. No estimates, no rounding beyond the source, no "this probably means". If a number is absent, write "not stated". Record every conflict and counter-argument. Hiding disagreement to tell a cleaner story is the opposite of the job.

### 6. Analyze
Apply judgment to the extracted data: compute derived metrics (show formula and inputs), find patterns across named sources, translate into "so what for this product". While working, tag each statement so you keep its status straight: **[calc]**, **[pattern]**, **[inference]** (state the assumption) or **[hypothesis]**. These tags are scaffolding. In the brief, translate them to plain words ("shows up repeatedly across user communities"). Give each major finding a High / Medium / Low confidence with a plain-word reason. Flag landmines: regulatory, sensitive-population, privacy or competitive issues that touch the product's context.

### 7. Verify before anyone sees it
Run the verification table in [the report format](references/report-format.md). Re-fetch the load-bearing figures, recompute every calculation independently, and confirm every claim traces to a ledger entry. Fix failures first. Rows 2, 3, 5 and 6 (claims trace to sources, numbers re-fetched and matched, calculations recomputed, no "not stated" turned into a number) must pass before delivery. Summarize the outcome in the appendix.

### 8. Write the brief, then read it back
Build the report from [the report format](references/report-format.md): a one-line takeaway, a TL;DR, findings as tables with sources linked inline, an honest counterpoint, what it means for the product, plain-word confidence, a bottom line, then the collapsed appendix.

Write it to `<research folder>/YYYY-MM-DD-<slug>.md`. **Then re-read the file from disk** and confirm the TL;DR, the findings and the appendix are all present and the ledger is non-empty. If the read-back fails or does not match, fix it and read again. If you still cannot confirm, say "not verified: <reason>". Put the TL;DR and the file path in chat.

## Hard rules
- **Never invent or adjust a number.** Not to round nicely, not to fill a gap. "Not stated" is a correct answer.
- **The brief never claims more than the ledger supports.** Every visible finding traces to a ledger entry.
- **Every external claim carries a source and a date**, linked inline in the brief and cited in full in the ledger. No source, no claim.
- **Capture N** for any quantitative or generalizing claim, or mark it missing.
- **Always surface conflicts**, including one in the visible counterpoint.
- **Flag landmines** that touch the product's regulated or sensitive context, in the visible brief.
- **Keep the visible layer plain.** Tier letters and working tags belong only in the appendix.
- **Stay neutral about the product's prospects.** Describe potential and constraints, never destiny, and end on the bottleneck or what to watch.
- **Read-only on third-party accounts.** Research never posts, comments, reacts, or changes anything on any account.
- **Estimate before spending.** Never launch a large multi-topic dig without the menu.

## Anti-patterns
- Laundering a forum figure into an analysis claim as if it were an official statistic.
- Citing a news article's number without finding the report it re-cites.
- Writing the brief before the ledger is filled.
- A "Verified" label on figures that were not re-fetched.
- Delivering without the read-back.
