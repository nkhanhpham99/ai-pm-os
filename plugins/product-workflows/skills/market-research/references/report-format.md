# Report format and verification

Two layers, produced every time: a **visible brief** a busy reader finishes in two minutes, and a **collapsed appendix** holding the full audit trail. The appendix is hidden, not skipped.

File name: `<research folder>/YYYY-MM-DD-<slug>.md`.

## The template

Copy this and fill it in. Replace every bracket. Delete this guidance when you fill a section.

````markdown
# [Topic] - [punchy subtitle of what was found]

*Research brief for [purpose] - [YYYY-MM-DD] - depth: [Lean | Verified | Thorough]*

> **In one line:** [the single most important takeaway, in plain language]

---

## TL;DR
- [5-7 bullets that are the report in miniature: key findings, the "so what", and one line on how solid the evidence is. A reader who stops here still has the gist.]

---

## 1. [First finding theme - a plain heading]
| [col] | [col] | [col] | Source |
|---|---|---|---|
| **[label]** | [plain finding] | [context] | [inline link](url) |

## 2. [Second theme]
| ... | ... | Source |
|---|---|---|

## The honest counterpoint
[The strongest conflict or counter-argument, in plain words, with the conflicting sources linked inline. Prose, not a table.]

## What this means for [the product]
> **Opportunities**
> - [Compact, decision-oriented bullets: what to build or how to position.]
>
> **Landmines**
> - [Regulatory, sensitive-population, privacy or competitive issues, each one line, linked to evidence. Write "none found" only if you looked.]

## How confident are we?
| Finding | Confidence | Why (plain) |
|---|---|---|
| [finding] | High / Medium / Low | [plain reason with an inline link, not tier codes] |

## Bottom line
> [One neutral closing read. Name the potential opening the research suggests (a possibility, never "this product will win"), then end on the bottleneck or what to watch.]

---

### Sources
[Cited sources as inline links, lightly labelled by reliability in plain words, for example "community discussions (real voices, directional signal)" and "research and reporting (higher reliability)".]

*Reliability in plain terms: [which claims rest on peer-reviewed or official sources and which are directional signal. State that missing numbers were left out, not estimated.]*

---

<details>
<summary><strong>Full research data, sources and verification (expand for the working detail)</strong></summary>

Tiers: A = peer-reviewed or official - B = reputable journalism or methodology-stated reports - C = forums, social, anecdote (signal, not proof) - D = undated or unattributed.

#### Source ledger
| # | Source / author | Platform | Tier | Published | Accessed | URL | N | Verbatim key figure or quote |
|---|---|---|---|---|---|---|---|---|
| S1 | | | | | | | | |

#### Key extracted figures
- [Metric - value as stated - N - source # - date. Verbatim, no rounding. "Not stated" where absent.]

#### Conflicts surfaced
- [Claim vs counter-claim - source # vs source # - nature of the conflict.]

#### Gaps (not stated)
- [Things looked for and not found. Include pages that could not be read.]

#### Verification
[Outcome of the table below. State that the anti-fabrication core passed, and any honest limitations. Outcome: PASS or PASS WITH NOTED LIMITATIONS - reason.]

#### Suggested next research
- [Adjacent topics this dig surfaced.]

</details>
````

Writing rules for the visible layer:
- Findings are tables, not loose prose. Lead each row with a **bold label**. Pick columns that fit: "group / figure / context / source", "common advice / what people actually say / source", "recurring conversation / what is said / source".
- Sources are linked inline on the claim, for example `[Trade body, 2026](url)`. No `S1 (C)` codes in the visible brief.
- Confidence is stated in words, not tier letters.
- The bottom line describes potential and constraints, never a promise.

## Verification table

Work through every row before delivering. Fill the last two columns, and summarize the outcome in the appendix. A row you cannot pass honestly is marked FAIL with a note, never quietly skipped.

How to verify, not just tick boxes:
- **Re-fetch, do not trust memory.** Re-open the source and compare the number or quote character for character with the ledger.
- **Recompute independently.** Redo each calculation from the stated inputs without looking at your earlier result. If the two differ, both are suspect until reconciled.
- **Trace, do not vibe.** For each claim, point at a specific source number.

| # | Check | How to verify | Pass criteria | Result | Notes |
|---|---|---|---|---|---|
| 1 | Source completeness | Scan the ledger | Every source has name, platform, type, publish date, access date and URL | | |
| 2 | No orphan claims | Go claim by claim through the brief | Every claim traces to a ledger source # | | |
| 3 | Numbers are real | Re-fetch the load-bearing sources (a few in Lean, all in Verified) | Every checked figure matches the source exactly | | |
| 4 | Sample size present | Scan every quantitative or generalizing claim | Each has N, or is marked "not stated" | | |
| 5 | Calculations recomputed | Redo each [calc] from stated inputs | Result matches; formula and inputs shown | | |
| 6 | No "not stated" became a number | Compare the brief with the Gaps list | Nothing marked "not stated" appears as a figure | | |
| 7 | Tier discipline | Check each generalization | No population claim rests on Tier C or D | | |
| 8 | Conflicts surfaced | Compare findings with the Conflicts list and the counterpoint | All disagreements are recorded, none smoothed away | | |
| 9 | Recency | Check publish dates against the question | Stale sources are labelled as such, especially fast-moving market data | | |
| 10 | Reasoning is honest | Check the working tags | Hunches are not dressed as conclusions; tags translated to plain words | | |
| 11 | Landmines flagged | Scan all findings | Any regulatory, sensitive-population or privacy issue is flagged in the visible brief | | |
| 12 | Confidence honest | Read the confidence table | Each rating matches its evidence strength | | |

**Pass bar.** Rows 2, 3, 5 and 6 (the anti-fabrication core) must all pass before delivery. A failure there means a number or claim is untrustworthy: fix it or remove it. Fix other failures where possible. If a limitation is genuine (the only data available is Tier C), keep the row as FAIL with a note so the reader sees the honest limitation. State plainly in chat if any row could not be passed, and why.

## Read-back check (after writing the file)

Re-read the written file from disk and confirm: the TL;DR is present, each finding table has at least one row with a link, the appendix ledger is non-empty, and the Verification block states an outcome. Report "not verified: <reason>" for anything you could not confirm.
