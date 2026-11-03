# Entry templates

Two entry types. Both are plain markdown with YAML frontmatter. `[[wiki-links]]` and mermaid work in any markdown renderer that supports them, and in Obsidian.

- **Concept:** "what is X" explanations.
- **Comparison:** "X vs Y", pros and cons, "which should I use" tradeoffs the user asked to save. File name: `X vs Y.md`.

If one question does both (explains a concept and weighs options), write the concept entry, put the tradeoff in a comparison entry, and link them both ways.

## Concept template

The section order is deliberate. It walks from "I know nothing" to "I see the whole system" to "this is why it matters to me".

````markdown
---
title: <Concept Name>
aliases: [<abbreviations, alternate names>]
domain: <one of: tech, infrastructure, system-design, business, product, data, security, workflow, buzzword>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
context: "<one line: where and why this came up>"
tags: [knowledge-base, <domain>]
---

# <Concept Name>

> **In one sentence:** <plain-English definition a non-technical person would get>

## Plain English

<The beginner-level explanation. Start from zero. Use an everyday analogy if one fits
naturally. No unexplained jargon: every technical term used here is either defined
inline or is a [[link]] to another entry.>

## The bigger picture

<Zoom out. What problem does this exist to solve? What category of things does it
belong to? What are the neighboring or competing concepts? If the session's answer was
niche ("this specific flag does X"), expand it to the general concept here.>

## How it fits together

<A mermaid diagram. Pick the shape that matches the concept:
- `flowchart` for processes, workflows, data flows
- `graph` for concept maps and system positioning
- `sequenceDiagram` for interactions between parties or services
Keep it small and legible, roughly 5 to 12 nodes. Show the concept IN ITS SYSTEM,
not a restatement of the definition.>

## In my world

<The anchor. How this connects to the user's actual work. Anchor to the user's current
projects (from CLAUDE.md / cwd) and to the session context you were given. Be specific:
"the nightly export job is exactly this pattern" beats "this is used in databases".
Use only what was supplied. If nothing connects yet, say what future work would likely
touch it.>

## Related

- [[Other Entry]] — <one line on the relationship>
- [[Another Entry]] — <...>
````

## Comparison template

The critical rule: **a verdict is only true for a specific case.** "A beats B" means nothing. "A beat B for the reporting job because it needed relational joins at small scale" is knowledge. Comparison entries therefore accumulate case verdicts. When the same tradeoff resurfaces in a different project, append a new case verdict and never overwrite an old one. Both were right, for their case.

````markdown
---
title: <X vs Y>
aliases: []
type: comparison
domain: <same domain list as concepts>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [knowledge-base, comparison, <domain>]
---

# <X> vs <Y>

> **The tradeoff in one sentence:** <what is actually being chosen between, in plain
> English, e.g. "paying with money vs paying with complexity">

## What each one is

<One plain-English paragraph per option. Link each to its concept entry, [[X]] and
[[Y]], even if the entry does not exist yet.>

## Head to head

| | <X> | <Y> |
|---|---|---|
| <criterion: cost, speed, complexity, scale ceiling, lock-in...> | ... | ... |

<Only criteria that actually discriminate, a handful of rows. After the table, a short
paragraph on WHEN the balance tips: "X wins when...; Y wins when...". This is the
level and scale scoping the verdicts depend on.>

## Case verdicts

### <YYYY-MM-DD> — <the specific case>
- **Context:** <project, scale, constraints at the time>
- **Verdict:** <which option, at which level. "X, but only for the first version" is valid>
- **Why:** <the deciding factor(s) for THIS case>
- **Would flip if:** <what change in circumstances would reverse it>

## Related

- [[X]] / [[Y]] — the concept entries
````
