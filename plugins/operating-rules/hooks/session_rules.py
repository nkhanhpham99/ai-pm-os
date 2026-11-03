#!/usr/bin/env python3
"""SessionStart hook: inject the compact operating rules (rules.md, next to this file).

Prints {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": <rules.md>}}.
Fails open: if rules.md is missing or unreadable, print nothing and exit 0.
Tests: ../tests/.
"""
import json
import os
import sys


def main():
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            return
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": text,
        }}))
    except Exception:
        return


if __name__ == "__main__":
    main()
    sys.exit(0)
