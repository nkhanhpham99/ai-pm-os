---
name: prd
description: Use when the user wants a PRD, feature spec or requirements write-up - "write me a PRD", "spec this feature", "turn this idea into requirements", "document how this flow works", "draft the requirements doc" - or wants to update an existing PRD (new sections, changed plans, priority tiers, backlog), or wants a shareable copy of one for teammates. Covers both new-feature PRDs and standardization PRDs for flows that already shipped. Not for gathering outside evidence (market-research) or logging a decision or bet (decision-ledger).
license: MIT
---

# PRD: grounded, honest about its own state, decision-ready

## Defaults
Read overrides from an `## ai-pm-os settings` section in the user's CLAUDE.md before using these.
- **PRD folder:** `./docs/prd/` (setting name: `PRD folder`). The working copy is `<slug>.md`; the shareable copy is `<slug>.shareable.md` in the same folder. Create the folder if it does not exist. Quote paths.
- **Decisions file:** `./decisions.md` (setting name: `decisions file`). Read it in the pre-flight when it exists.
- **Priority tiers:** P0 = the one or few broad goals the project must deliver, not granular. P1 = next after the minimum viable work. P2 = circle back later. The tiers are fixed in this version. They are a different scale from the decision ledger's `Priority` field (P0 push hard, P1 normal, P2 easy-iterate), so never mix the two.
- **Date format:** `YYYY-MM-DD`. Use the date from the environment or conversation; if neither gives one, run `date +%F`. Never guess.
- If the settings rename a folder or file, treat every mention below as that path.
- Storage is markdown. If the user wants the PRD in Notion, read [using Notion](references/using-notion.md) (untested).

## The one discipline
An unskilled agent asked for a PRD writes a confident, polished document after zero lookups: invented targets, invented product facts, invented dates, and the critical questions buried as "open questions". Plausible is not true.

**Nothing goes in the PRD that is not gathered, verified, tagged or asked.**
- Every number carries a source and a reason.
- Every claim about what the product does is verified (code, data, a real session) or tagged **Assumption**.
- Every unknown that would change the document's shape becomes a question to the user before drafting, not a footnote after.

**Latest wins.** When sources conflict (an old deck, a newer conversation, the code), the most recent information is authoritative. Say what changed.

## Pre-flight: check the decision ledger
Before proposing or gathering anything, see what has already been tried or decided in this area.
- If the `decision-ledger` skill is installed, or the decisions file exists, read it and find entries whose title, type or metric matches this work.
- Show a short "what we already tried or decided here, and how it turned out" summary first. Cite each entry's id, status, outcome and lesson. This grounds the PRD in accumulated evidence.
- If the file does not exist or has nothing on this topic, say so plainly and continue. Never invent prior entries.

## Step 0: classify and scope (with the user)
1. **Which kind?** (a) **New feature**: not built, so the PRD proposes and gates on validation. (b) **Standardization**: designed or shipped, so the PRD documents canonical reality, and the code, not anyone's memory of it, is the source of truth. State the kind in the Status line.
2. **Has the idea been validated?** If a new feature has no validation behind it, say so in the document, put validation gates in Next steps, and suggest gathering outside evidence with `market-research` if it is installed. If validation exists, summarize its verdict from the real source.
3. **Source materials.** Ask for decks, flow diagrams, design files and meeting outcomes, and where they live. Do not guess paths.

## Step 1: gather ground truth, before writing a section
Sweep in order of authority for "current state":

| Source | Use for |
|---|---|
| **The code**, on the branch that deploys the service, freshly fetched (a local clone may lag, and the default branch may not be the deployed one) | Verifying any claim about what the product does: flows, fields, gating, costs. Cite file paths. |
| **Past sessions and notes** (the user's own words) | Ideation, decisions, constraints, earlier validation verdicts. The latest wins conflicts. |
| **The user's decks and docs** | Approved flows, pricing or gating specs, competitor scans. Look for sibling files. |
| **Saved memory or notes** | Durable context. A pointer, not verification: re-check anything load-bearing. |
| **Live data** from whatever analytics the user has connected | Baselines, denominators, funnel reality. If a source is not connected or does not answer, say so and tag the number Estimate or Assumption. |
| **Outside evidence** | `market-research`, with its costed menu. Never ad-hoc scraping. |

**Denominator check.** Before proposing any percentage metric, pull the real base. "Percent of connected users" is meaningless if almost nobody ever connected. A small or confounded base reshapes the PRD, so surface it in section 1 rather than hiding it.

## Step 2: ask, do not invent
Collect everything still unknown that would change the document's shape (user tier, platform, entry surface, what is gated, who reviews) and ask in one batch. Proceed on defaults only for genuinely cosmetic gaps, and say which defaults you took.

**Never invent** metric targets, rollout dates or week plans, "users currently do X" claims, team commitments, or competitor numbers. If it cannot be sourced this run, tag it, ask, or leave a named open question.

## Step 3: set targets with stated reasoning
For each metric target, in this order:
1. **Internal data first.** Pull the live baseline and state the target as an explicit change from it ("from <baseline> to at least <target>" with both values sourced).
2. **An outside benchmark second**, only when no internal baseline exists. Cite it.
3. **Always one line on why that number.**
4. Prefer behavioral, instrument-measurable metrics over ones that depend on recruiting interviewees.
5. **Check the instrumentation exists.** A metric nobody tracks is a wish. Name broken or missing events as prerequisites.

If there is no baseline and no benchmark, write the target as `needs input` and say what would supply it.

## Step 4: draft from the template
Copy [the PRD template](assets/prd-template.md) and fill it. House rules:
- **Status honesty.** The "Where this is" callout states what has not happened (not prototyped, not validated, not on every platform).
- **Origin labeling.** Inspiration diagrams and prototypes are labelled "inspiration only, not source of truth".
- **Priority tiers sit above the granular requirements**, and the two must not contradict.
- **The backlog holds only ideas the user endorsed.** Do not pad it with your own brainstorm.
- **Platform differences are explicit** (step counts, platform-only beats).
- **Review user-facing copy for harm.** Check tone, alarming one-tap actions, and anywhere generated text is wrong for the moment.

## Step 5: review loop with the user
Present the draft together with: (a) the open questions as numbered decisions, (b) conflicts you resolved by latest-wins, so they can veto, and (c) suggested next steps, clearly marked as suggestions, never baked into the plan. Iterate until confirmed. When a later edit lands, sweep the whole document for statements it now contradicts, because one plan change usually invalidates framing in several sections.

## Step 6: write both copies, then read them back
**Two copies, always.** The working copy is full. The shareable copy is clean.
- **Working copy** (`<PRD folder>/<slug>.md`): everything, including local paths, raw findings, data-pull mechanics and session references. This is the file the agent picks up later.
- **Shareable copy** (`<PRD folder>/<slug>.shareable.md`): self-contained and readable by a teammate with no access to the user's machine or sessions. Make it only when the user asks to share. Never share unprompted.

Making the shareable copy:
1. Start from the working copy and rewrite, do not just delete. Summarize detail as the bigger picture ("two candidate approaches are documented in the engineering plan").
2. Replace unlabeled shorthands ("Option A", "the plan, item 3") with what they mean.
3. Reference only material the reader can open. If the PRD leans on a deck, a research note or an analysis, publish that first and link it, or drop the reference. For code, link to a repository URL on the deployed branch, never a local path.
4. **Run the grep check on the shareable file. It must return nothing:**

```bash
grep -nEi '/Use[r]s/|/hom[e]/|(^|[^[:alnum:]])~/|\$HOME|/private/|/Volumes/|/tmp/|\.claude/|[A-Za-z]:\\|\.jsonl|session[ _-]?(id|[0-9a-f]{6,})|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' "<PRD folder>/<slug>.shareable.md"
```

   It catches local paths (including `~/` after punctuation, `$HOME`, `/private/`, `/Volumes/`, `/tmp/`, `.claude/`), transcript files, session ids (including short and hyphenated ones) and raw UUIDs. Fix every hit and run it again until it prints nothing. Then read the file once for shorthand and private context a pattern cannot catch. If you cannot run the check, say "not verified: <reason>" and do not call the copy shareable.

**Read each file back from disk** after writing and confirm the sections you wrote are present: the Status line, the metrics table with a reason for every target, the open questions, and the date. If a read-back does not match, fix it and read again. If you still cannot confirm, report "not verified: <reason>".

**Keep both copies in sync** on every later edit, and re-run the grep check on each shareable update.

## Red flags: stop and gather or ask
- A target number with no source-and-reason line
- "Users currently..." with no pull or verification behind it
- Zero lookups before drafting
- A week-by-week rollout the team never committed to
- A shape-changing unknown sitting in "Open questions" instead of asked up front
- Sharing a copy that was not asked for

| Excuse | Reality |
|---|---|
| "The user is in a hurry, just draft it" | A confident wrong PRD costs a rewrite and lost trust. The sweep takes minutes, and you can batch questions while gathering. |
| "These targets are industry standard" | Bases are small and specific. A generic percentage can be meaningless. Pull the real denominator. |
| "I flagged it as an open question" | If the answer changes the document's shape, ask before drafting. Open questions are for real unknowns. |
| "Memory gave me the context" | Memory is a pointer, not verification. It goes stale. Re-check load-bearing facts. |
| "The deck says so" | Decks go stale. The latest source wins, so verify in code or a recent conversation. |
