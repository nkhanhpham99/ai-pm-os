#!/usr/bin/env python3
"""Replay the proof-before-done stop check over every past turn in a folder of transcripts.

Usage: backtest.py TRANSCRIPT_DIR [--json] [--examples N]

Counts, per turn: how many wrote to an external tool, how many read it back after the last
write, and how many would have been blocked by the Stop hook. It never prints transcript
text unless you pass --examples N (which prints N short snippets of final messages).
"""
import argparse
import glob
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_hook():
    spec = importlib.util.spec_from_file_location("proof_before_done", os.path.join(HERE, "..", "hooks", "proof_before_done.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pbd = load_hook()


def find_transcripts(directory):
    return sorted(glob.glob(os.path.join(directory, "**", "*.jsonl"), recursive=True))


def read_entries(path):
    entries = []
    try:
        with open(path, errors="ignore") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if isinstance(e, dict) and e.get("type") in ("user", "assistant") and not e.get("isSidechain"):
                    entries.append(e)
    except OSError:
        pass
    return entries


def backtest(paths, examples=None):
    """Return {"turns", "write_turns", "read_back", "would_block"} over the given transcript files.

    If `examples` is a list, a (file, tool, text) tuple is appended for each would-be block.
    """
    turns = write_turns = read_back = would_block = 0
    for path in paths:
        entries = read_entries(path)
        starts = [i for i, e in enumerate(entries) if pbd.is_prompt(e)] + [len(entries)]
        for a, b in zip(starts, starts[1:]):
            turns += 1
            tools, text = [], ""
            for e in entries[a + 1:b]:
                if e.get("type") != "assistant":
                    continue
                for c in (e.get("message") or {}).get("content") or []:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") == "tool_use":
                        tools.append(c.get("name", ""))
                    elif c.get("type") == "text":
                        text = c.get("text", "")
            writes = [i for i, t in enumerate(tools) if pbd.WRITE.search(t)]
            if not writes:
                continue
            write_turns += 1
            if any(pbd.READ_BACK.search(t) for t in tools[writes[-1] + 1:]):
                read_back += 1
                continue
            if pbd.CLAIM.search(text) and not pbd.UNVERIFIED.search(text):
                would_block += 1
                if examples is not None:
                    examples.append((os.path.basename(path)[:8], tools[writes[-1]].split("__")[-1], text[:160].replace("\n", " ")))
    return {"turns": turns, "write_turns": write_turns, "read_back": read_back, "would_block": would_block}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Replay the proof-before-done stop check over past transcripts.")
    ap.add_argument("transcript_dir", help="folder containing .jsonl session transcripts (searched recursively)")
    ap.add_argument("--json", action="store_true", help="print the counts as JSON")
    ap.add_argument("--examples", type=int, default=0, metavar="N",
                    help="also print N sample would-be blocks, including a snippet of the final message")
    args = ap.parse_args(argv)
    if not os.path.isdir(args.transcript_dir):
        print(f"error: not a directory: {args.transcript_dir}", file=sys.stderr)
        return 2
    examples = [] if args.examples > 0 else None
    result = backtest(find_transcripts(args.transcript_dir), examples)
    if args.json:
        print(json.dumps(result))
    else:
        w = result["write_turns"]
        pct = lambda n: f" ({100 * n / w:.0f}% of write turns)" if w else ""
        print(f"turns: {result['turns']}")
        print(f"turns with an external write: {w}")
        print(f"read back after the last write: {result['read_back']}{pct(result['read_back'])}")
        print(f"would be blocked (claimed done, no read-back): {result['would_block']}{pct(result['would_block'])}")
    if examples:
        random.seed(1)
        print("examples (transcript text):")
        for ex in random.sample(examples, min(args.examples, len(examples))):
            print(" ", ex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
