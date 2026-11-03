# PRD - [Feature name] ([one-word framing, for example "standardization"])

| | |
|---|---|
| **Author / DRI (Product)** | [name or role] |
| **Reviewer** | [name or role, or `needs input`] |
| **Status** | [New feature, pending validation / Standardizing a shipped flow / Build-ready] |
| **Last updated** | [YYYY-MM-DD] |
| **Surface** | [web / iOS / Android / API / which user tier] |
| **Strategic context** | [the bigger move this serves] |
| **Sources** | [decks, flow diagrams, sessions, code branches - the real ones, verified] |

> **One line.** [What the feature is, the loop or mechanic, and what it is meant to change. One tight paragraph.]

> **Where this is.** [Honest state: drafted? prototyped? implemented? shipped? What has NOT happened yet. Point to Next steps.]

> **Origin** *(if it came from a meeting or diagram)*: [date, who presented, link]. Label any inspiration diagram or prototype as **inspiration only, not source of truth**, against what is actually implemented.

---

## 1. Problem and context (the why)

- The user pain or business gap, **with evidence** (funnel numbers, quotes, research files).
- **The reality it lands in.** The live internal data, tagged Verified, Estimate or Assumption, including inconvenient facts and confounds (for example "low adoption, but never promoted: that is low awareness, not proven low demand").
- Economics context if the feature touches monetization: cost, revenue lever, constraints. Cite where each was verified.

## 2. Goals and success metrics

**Objective:** [one sentence.]

> Metrics are behavioral and instrument-measurable first. Qualitative signals are optional later reads, not launch gates.

| Metric | Why it matters | Baseline (source, date) | Target and the reason for that number |
|---|---|---|---|
| [primary metric] | [why] | [value, or `needs input`] | [value, and one line: internal baseline first, outside benchmark second] |
| [loop or retention metric] | | | |
| [conversion metric] | | | must not reduce [existing healthy rate] |
| **Guardrail:** [what must not regress] | | | no regression |

**Definition of done:** [what confirmed success looks like - measurable, and honest about reads with no control group.]

## 3. Non-goals

- **Not** [the tempting adjacent thing that was cut, and why].
- **Not** [scope creep item].
- (Be aggressive here. This section saves the most pain.)

## 4. Users and user stories

**Primary persona:** [one line: who, their state of mind, their constraint.]

- *As a [user], I want [X] so that [Y].* (Cover the primary actor, the receiving side if two-sided, the not-yet-user if there is an invite loop, and one "as the business" story.)

## 5. The feature: flow (definitive source: [file, diagram or code path])

[Entry points. Then the canonical step-by-step flow with **(step N)** numbers, branches, and where any paid or gated step sits. Mark platform differences explicitly. Mark where generated or metered cost sits.]

## 6. Functional requirements

| # | Requirement | Priority |
|---|---|---|
| FR1 | ... | Must |
| FR2 | ... | Must / Should / Won't (this PRD) |

### Priority tiers (P0, P1, P2)

Broad tiers above the granular requirements. Default definitions, which the user may override:
- **P0:** the main goal the project must directly deliver. Not granular: one or a few major goals.
- **P1:** what to do next once the minimum viable work is complete.
- **P2:** should-have, to circle back to later.

## 7. Gating and pricing *(if monetization-relevant)*

[What is free versus gated, and the ladder the feature climbs. Cite the current gating decision and confirm it is the latest. Write `needs input` rather than a price you did not verify.]

## 8. UX states and edge cases

[Empty, error, no-connection or cold start, rate limits, consent or mute, decline paths, offline, localization. The missing-state list is the number one source of mid-sprint surprises.]

## 9. Analytics and instrumentation

[Event list with properties and variant tagging. **Name known instrumentation gaps** (check the event catalog): they block the metrics in section 2 and must be fixed first.]

## 10. Cost and economics *(if relevant)*

[Where marginal cost sits, what is free by design, what is gated to cover cost. Cite verified cost facts, not stale deck numbers.]

## 11. Validation status, risks and open questions

- **Validation verdict** (summarize from the real source, or state that none has been run for a new feature and recommend it).
- **Riskiest assumption**, named explicitly.
- Other risks, each with a mitigation.
- **Open questions:** numbered, each one a decision the user or team must make.
- **Assumptions:** beliefs with no data yet.

## 12. Next steps and phasing

- **A. Immediate path:** numbered, with a check mark on what is done. Include validation gates with pre-committed stop and scale thresholds where applicable. Mark every suggestion as a suggestion until the user confirms it.
- **B. Build sequencing** (Phase 1 now, Phase 2 next, Phase 3 later), only if a roadmap exists.

## 13. Backlog: ideas to revisit (no current plan)

Parked ideas worth a look later: not scheduled, not committed. Only items the user endorses.

## 14. Appendix: sources and provenance

- **Decks and files (primary):** [paths. In the shareable copy, link only what the reader can open.]
- **Sessions:** [which sessions, dates, what each contributed. Working copy only.]
- **Code (verified):** [file paths and what they proved. In the shareable copy, use repository URLs on the deployed branch.]
- **Data:** [source, figures pulled, date.]
- **Research:** [files or links.]
- **Competitor and market:** [scan results.]
