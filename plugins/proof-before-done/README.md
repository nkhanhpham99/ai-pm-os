# proof-before-done

Stops your agent from saying "done" about a write it never checked.

## The problem

An agent writes to an external tool (a chat message, a doc, a spreadsheet, a draft) and then reports success. The write call returning without an error is not proof that the content landed correctly. The only proof is reading it back.

In my own sessions, measured 2026-11-02: 3,731 turns, 538 of them wrote to an external tool, and only 45 (8%) read the result back after the last write. In 425 turns the agent claimed completion with no read-back. The method and the caveats are in [lab 002](../../lab/002-does-my-agent-verify.md).

## What is included

| Part | What it does |
|---|---|
| `hooks/proof_before_done.py post` | PostToolUse. After a write to an external tool, reminds the agent to read it back and report a link plus a one-line "what changed". |
| `hooks/proof_before_done.py stop` | Stop. If the turn wrote externally, never read it back after the last write, and the final message claims completion, it blocks the stop once and asks for the read-back or an explicit "not verified". |
| `scripts/backtest.py` | Replays the Stop check over your own past transcripts so you can see your own number before you trust mine. |
| `skills/self-correct` | When a stale or wrong claim is caught, finds every copy across your instruction files and memory, fixes them all, and reports `copies: N -> 0`. Its eval scored 1.00 in one run after a grader fix; the full run with a no-plugin baseline is pending ([lab 006](../../lab/006-does-self-correct-pass-its-own-eval.md)). |

The hooks fail open. Any parse problem, missing transcript, empty or non-JSON input exits 0 with no output, so a bug here can never block your session. They need `python3` and nothing else.

## Install

```
/plugin marketplace add nkhanhpham99/ai-pm-os
/plugin install proof-before-done@ai-pm-os
```

From a local clone, use the clone's path in place of `nkhanhpham99/ai-pm-os`. Check it loaded with `/hooks`.

## Extend the tool list

This edits your own copy: clone or fork the repo, make the change there, and install the plugin from that local path (`/plugin marketplace add <path>`). Edits inside an installed plugin's cache are lost on update.

Two places must agree:

1. `hooks/hooks.json`: the PostToolUse `matcher` decides which tool calls invoke the hook. Add a word for your tool to the alternation.
2. `hooks/proof_before_done.py`: `WRITE` lists the tool names that count as an external write, `READ_BACK` the ones that count as reading it back. Both match the end of the MCP tool name, so add the part after the last double underscore.

Run the tests after any change:

```
python3 -m unittest discover -s plugins/proof-before-done/tests
```

Without a matching `READ_BACK` entry, a write you added will keep blocking because nothing can satisfy it.

## Backtest on your own sessions

```
python3 plugins/proof-before-done/scripts/backtest.py PATH/TO/TRANSCRIPTS
python3 plugins/proof-before-done/scripts/backtest.py PATH/TO/TRANSCRIPTS --json
```

`PATH/TO/TRANSCRIPTS` is a folder of Claude Code session `.jsonl` files, searched recursively. The output is counts only: `turns`, `write_turns`, `read_back`, `would_block`. It never prints transcript text unless you pass `--examples N`, which prints N short snippets of final messages, so do not paste that output anywhere public.

The result is a heuristic. A turn counts as claiming completion when the final message contains a word like "done", "sent" or "published", so treat `would_block` as an estimate of the Stop check, not a verdict on any single turn.
