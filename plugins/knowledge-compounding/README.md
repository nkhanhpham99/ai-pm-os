# knowledge-compounding

Turns explanations from your sessions into a cross-linked, diagrammed markdown knowledge base, so what you learn today is still there next month.

## The problem

You meet new concepts constantly: a piece of infrastructure, a buzzword, a business idea, a system-design pattern. Someone explains it well in a session, you nod, and when the session ends the understanding goes with it. Next time it comes up, you ask again.

## What is included

| Part | What it does |
|---|---|
| `skills/knowledge-base` | After an explanation-style answer, hands the full explanation to one background agent, which writes a beginner-first entry with a diagram, links it to related entries in both directions, and updates three meta pages. It then re-reads what it wrote from disk before it reports done. |

The entry is not a dictionary definition. It starts from zero, zooms out to the bigger picture, draws the concept inside its system, and anchors it to your current projects (taken from your CLAUDE.md and the working directory).

## How it works

1. **Answer first, undisturbed.** The skill never changes how a question is answered, and never makes you wait.
2. **Capture in the background.** One background agent writes the entry, so the working session keeps its flow. Without an agent tool, the capture runs inline at the end of the turn.
3. **One page per concept**, plus comparison pages for tradeoffs you asked to save. A comparison entry stores case verdicts ("A, for this project, because...") rather than a universal winner, and new cases are appended, never overwritten.
4. **Three meta pages** sort to the top of the folder: `0 INDEX.md` (table of every entry), `1 GLOSSARY.md` (every abbreviation and term of art), `2 MAP.md` (mermaid mind map).
5. **Links travel both ways.** A new entry links to related ones, and each related entry gets a back-link.
6. **Proof before done.** The capture re-reads the entry and the updated meta pages from disk and reports "not verified" when it cannot confirm a write.

Output is plain markdown with `[[wiki-links]]`, YAML frontmatter, and mermaid. It renders in any markdown tool and works unchanged in Obsidian, which is compatible but not required.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install knowledge-compounding@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`.

## Use it

Ask for an explanation: "explain X in plain English", "what is X", "I don't understand why Y", or "explain with full context". Say "add this to my knowledge base" or "save this explanation" to capture something that was not a question. Ask "what do I already have on X" to read from the knowledge base, or "rebuild the index" to regenerate the meta pages after hand edits.

To change where entries are written, add an `## ai-pm-os settings` section to your CLAUDE.md:

```markdown
## ai-pm-os settings
- knowledge-base folder: <PATH-TO-YOUR-KNOWLEDGE-BASE>
```

The default is `~/knowledge/`. The skill reads the setting before using the default.

## Known tradeoff

The trigger is deliberately narrow. Comparison and tradeoff questions ("X vs Y", "pros and cons", "which should I use") no longer auto-capture. They are captured only when you ask to save them, or ask for the tradeoff "with full context". The upside is fewer surprise background writes. The cost is that some comparisons worth keeping will be missed unless you ask.
