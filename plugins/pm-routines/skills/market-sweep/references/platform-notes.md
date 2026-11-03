# Platform notes: known blocks and workarounds

Platforms change their defenses often, so treat each note as a likely cause to check, not a guarantee. When a workaround stops working, record it in the watchlist's query health and tell the user; do not keep retrying. When you find a new block, add a line to `LEARNINGS.md` so the next tune can fold it in here for this user.

## Rules that apply everywhere

- **Signed out means skipped.** Never log in, never enter credentials, never accept a sign-in prompt. Record the skip and ask the user to sign in themselves before the next run.
- **Do not retry a blocked route in a loop.** Repeated attempts are exactly what anti-bot systems escalate on. Try once, try the workaround once, then skip and name it.
- **Throttling is a stop sign.** If reads start failing after many page loads, pause once, then stop that platform and note how many items were read.
- **Read the page's own network traffic, not hand-made API calls.** Calls you construct yourself against a platform's internal API usually lack the signatures the page adds, and often come back as a success code with an empty body. That looks exactly like "nothing there" and is not a valid signal.
- **Check what a tool returns before trusting its name.** A tool called something like "trending music" may return a licensed music library for publishing, not trend data. A "virality predictor" may score content you supply, not discover anything.

## Personalized feeds

A platform's home feed or "for you" feed reflects the signed-in account's history and location, not the market. An account based in one country will be served that country's content. **Never sweep these feeds.** Use search, hashtag pages, named accounts and communities, which are keyword-driven and far less personalized. Search results still carry regional weighting, so the language and region gate still applies to each result. If a run's results look regionally skewed, say so in the sweep file.

## Region and language parameters

API parameters such as a region code or a relevance language are hints, not filters. Results in other languages routinely come back anyway. Apply the language and region gate per result, by checking the content itself (caption, on-screen text, audio), never the auto-translated title.

## Short-video platforms (TikTok and similar)

- **Profile pages are often blocked to automated browsing** while video pages and search stay open. Signs: a "please wait" screen, a near-empty page, script errors in the console. The errors are symptoms; the cause is the blocked request.
- **Workarounds, in order:** an embeddable profile page if the platform offers one (it usually lists recent posts); a single video page, whose embedded data often carries the author's account stats and exact counts; the user card on a search results page; the account's posts collected through search filtered to that handle.
- **Search through the page's own search box or results route**, not a bare query URL that lands on a tab that errors. The address bar may normalize back to the home page while the results still render; that is not a failed navigation.
- **Prefer the page structure over plain text extraction** when reading results. Text extraction can return leftover feed content instead of the results.
- Saves are often not shown on the web. A save-worthy verdict there is inferred.
- Public trend dashboards are frequently closed or gated. Weekly trend roundups found through web search are the usual substitute.

## Photo and reel platforms (Instagram and similar)

- Named account pages usually load when signed in. Signed out, skip.
- Never the home feed.
- The caption is often the hook, more than the visual. Capture it verbatim.
- Reels usually show views and likes; carousels usually show likes and comments only. Record what is shown.
- The most fragile source in a typical set. A skip here is normal and costs little.

## Social pages with localized or obfuscated text

- **Localized labels.** A signed-in account's locale may turn labels into another language. A locale parameter in the URL (for example `?locale=en_US`) often fixes it. If labels stay localized, translate them; do not guess.
- **Obfuscated post text.** Some platforms interleave invisible characters in post text to defeat scraping, so extracted text comes back as garbage. Prefer the page's accessibility structure over raw text. If a caption cannot be read cleanly, record it as unreadable. Never reconstruct it.
- If the brief covers a platform only through its ad library, do not browse its organic pages, and do not list organic as skipped: it is out of scope, not missing.

## Community platforms (Reddit and similar)

- Unauthenticated raw requests are commonly refused. Use an installed community tool, which carries its own access, or web search restricted to the site.
- Some tools enforce a discovery step before use (list the operations, read an operation's schema, then execute). Follow it.
- Comment trees are the biggest budget sink. Titles and post text first.

## Video platforms with an API (YouTube and similar)

- Search calls usually return ids and titles but not statistics. A second call fetches the counts. Search calls typically cost much more quota than statistics calls, so search a few times and batch the statistics call.
- Keep any API key in an environment file that is excluded from version control. Never print it in a command that gets echoed.
- On a quota error, skip the platform for this run and say so.

## Ad libraries (Meta Ad Library and similar)

- **Generic keyword searches return spam.** Advertisers with nonsense names and empty creative crowd the results. Search by the competitor's page id or brand name, kept in the watchlist.
- **Ad body copy is often missing from tool responses**, which may return only a link to a snapshot of the creative. Fetch snapshots sparingly, for relevant advertisers only.
- Some ad tools reject arguments that other tools in the same set require. If a call fails on an unknown argument, drop that argument and retry once.
- A connector that needs re-authorization cannot do it in an unattended run. Write the sweep file anyway and tell the user which connector to reconnect.

## Web pages that will not read

Script-heavy or protected pages may return little to a plain fetch. Say so in the sweep file. Use a browser tool or a paid scraping tool only if the brief allows it and its cost fits the run's budget. Never use a paid tool on platforms whose terms forbid scraping.
