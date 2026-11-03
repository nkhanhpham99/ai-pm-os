# operating-rules

Puts eight short operating rules in front of your agent at the start of every session.

## The problem

Rules in a `CLAUDE.md` only help if the agent has them in context. A long file gets skimmed, trimmed or forgotten. This plugin injects a compact version of the rules (under 250 words) through a SessionStart hook, so they are always the first thing the agent sees.

It is opt-in. Install it only if you want the rules applied in every project you open. The full reasoning behind each rule, with a one-line "why", lives in [`templates/CLAUDE.md`](../../templates/CLAUDE.md). Copy that file into your own `CLAUDE.md` and edit it to taste.

The eight rules: knowledge validity tiers, a same-tier conflict ladder, never fabricate and let corrections propagate, proof before done, self-check before escalating, two-layer explanations, debugging discipline, and a project router.

## What is included

| Part | What it does |
|---|---|
| `hooks/session_rules.py` | SessionStart. Prints `rules.md` as additional context. Prints nothing and exits 0 if `rules.md` is missing or unreadable. |
| `hooks/rules.md` | The compact rules. Edit it to change what your agent is told. Keep it under 250 words. |

The hook needs `python3` and nothing else.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install operating-rules@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`. Check it loaded with `/hooks`.

If you would rather not use plugins, wire the same hook by hand: [`templates/settings.example.json`](../../templates/settings.example.json) has the entry.

## Edit the rules

This edits your own copy: clone or fork the repo, make the change there, and install the plugin from that local path (`/plugin marketplace add <path>`). Edits inside an installed plugin's cache are lost on update.

Change `hooks/rules.md`, then run the tests:

```
python3 -m unittest discover -s plugins/operating-rules/tests
```

`test_rules_under_250_words` fails if the file grows past 250 words. The limit is deliberate: rules injected into every session cost context every time, so keep them short and put the detail in your `CLAUDE.md`.
