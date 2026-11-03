# product-workflows

Three skills for a product manager's core loop: find out what is true outside, write down what to build, and keep a record of the bets you made so you can check them later.

## The problem

Research reports blend what sources said with what the writer guessed. PRDs arrive polished and full of invented targets. Decisions get made in chat, forgotten, and never checked against what happened. An agent left alone makes all three worse, because it writes plausible text with great confidence.

These skills put one discipline under all three: **nothing goes in that is not sourced, verified, tagged or asked.** Unknowns are written as `needs input`, never filled in. Every skill re-reads what it wrote from disk before it reports done, and says "not verified" when it cannot.

## What is included

| Skill | What it does |
|---|---|
| `market-research` | Gathers outside evidence (market size, competitors, community voice, scientific evidence, trends). Offers a Lean / Verified / Thorough menu before spending anything. Logs every source with publish date, access date, URL, sample size and the verbatim figure. Never paraphrases at gathering. Delivers a TL;DR brief with the full audit trail collapsed in an appendix, written to a markdown file and read back. |
| `prd` | Writes or updates a PRD from verified ground truth, asks the questions that change the document's shape before drafting, and gives every target a reason. Keeps two copies: a full working copy and a clean shareable copy that must pass a grep check for local paths and session ids. Reads the decision ledger first when one exists. |
| `decision-ledger` | Two modes. `log` records a decision, experiment, idea or hypothesis (type, topic and priority always, a falsifiable bet only when one exists). `review` walks open, needs-input and overdue entries one question at a time and records the answers verbatim. Reads `decisions.md` back after every write. |

## The decisions.md format

Each entry is a `## <id> · <title>` heading followed by `- Label: value` bullets: `Type`, `Status`, `Owner`, `Logged`, `Topic`, `Priority`, `Metric`, `Baseline`, `Target`, `Review by`, `Reasoning`, `Provenance`, `Outcome`, `Lesson`. Unknown values are the literal `needs input`. A worked example is in `skills/decision-ledger/assets/decisions-template.md`. Other tools in this marketplace read this file by label, so the labels are fixed.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install product-workflows@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`.

## Use it

- Research: "research the market for X", "what are people saying about Y", "is there evidence that Z".
- PRD: "write a PRD for this feature", "spec this flow", "make a shareable copy of the PRD".
- Decisions: "log this decision", "track this experiment", "review the open decisions".

To change where files go, add an `## ai-pm-os settings` section to your CLAUDE.md:

```markdown
## ai-pm-os settings
- research folder: ./research/
- decisions file: ./decisions.md
- PRD folder: ./docs/prd/
```

The defaults are the values shown. Each skill reads the setting before using its default.

## Storage

Markdown files are the only tested backend. Each skill has a `references/using-notion.md` for anyone who wants Notion. It is marked untested, and the skills point to it only when you ask for Notion.

## Known tradeoff

The skills ask before they spend or assume. `market-research` waits for you to pick a depth. `prd` asks its shape-changing questions up front. `decision-ledger` asks one question at a time. That is slower than a one-shot draft, and it is deliberate: a fast PRD with invented targets costs more to unwind than a short interview. If you want a one-shot, say "your call" on depth and give the defaults for the questions.
