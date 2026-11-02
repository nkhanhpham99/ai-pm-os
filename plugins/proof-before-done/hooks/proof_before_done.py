#!/usr/bin/env python3
"""Enforce "proof before done": never claim an external write landed without reading it back.

  post  (PostToolUse): after a write to an external surface (a docs/notes tool, chat, email,
        a spreadsheet, a file store), inject a reminder to re-fetch it and report the link.
  stop  (Stop): if this turn wrote to an external surface, never read it back after the
        last write, and the final message claims completion, block the stop once and ask
        for the read-back (or an explicit "not verified").

To cover another tool, add its name to WRITE (and its read counterpart to READ_BACK), and add
the tool to the PostToolUse matcher in hooks/hooks.json. Both patterns match the END of the
MCP tool name (the part after the last double underscore).

Fails open: any parse problem exits 0 with no output. Tests: ../tests/.
"""
import json
import re
import sys

WRITE = re.compile(r"__(notion-create-pages|notion-update-page|notion-create-database|notion-update-data-source"
                   r"|notion-move-pages|notion-duplicate-page|slack_send_message|slack_schedule_message"
                   r"|slack_create_canvas|slack_update_canvas|send_message|create_draft|update_draft|reply|forward"
                   r"|update_doc|create_file|update_file|update_values|append_values|update_spreadsheet"
                   r"|batch_clear_values)$")
READ_BACK = re.compile(r"__(notion-fetch|notion-search|notion-query-data-sources|slack_read_channel|slack_read_thread"
                       r"|slack_read_canvas|get_draft|get_message|get_thread|list_drafts|read_doc|read_file_content"
                       r"|get_file_metadata|get_values|get_spreadsheet|view_message)$")
CLAIM = re.compile(r"\b(done|sent|published|posted|pushed|updated|created|deployed|landed|live|shipped|saved|logged)\b", re.I)
UNVERIFIED = re.compile(r"\b(not verified|unverified|could not verify|couldn't verify)\b", re.I)


def post(payload):
    name = payload.get("tool_name", "")
    if not WRITE.search(name):
        return None
    return {"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": (f"PROOF-BEFORE-DONE: {name} wrote to an external surface. Before reporting it done, "
                              "read it back (fetch/get the same page, message or doc) and report the link plus a "
                              "one-line 'what changed'. If you cannot read it back, say 'not verified' and why."),
    }}


def is_prompt(entry):
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and not any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content)


def stop(payload):
    if payload.get("stop_hook_active"):
        return None
    entries = []
    with open(payload["transcript_path"]) as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") in ("user", "assistant") and not e.get("isSidechain"):
                entries.append(e)
    start = max((i for i, e in enumerate(entries) if is_prompt(e)), default=-1)
    tools, final_text = [], ""
    for e in entries[start + 1:]:
        if e.get("type") != "assistant":
            continue
        for c in (e.get("message") or {}).get("content") or []:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "tool_use":
                tools.append(c.get("name", ""))
            elif c.get("type") == "text":
                final_text = c.get("text", "")
    writes = [i for i, t in enumerate(tools) if WRITE.search(t)]
    if not writes:
        return None
    last = writes[-1]
    if any(READ_BACK.search(t) for t in tools[last + 1:]):
        return None
    if not CLAIM.search(final_text) or UNVERIFIED.search(final_text):
        return None
    return {"decision": "block", "reason": (
        f"Proof before done: this turn wrote with {tools[last]} but never read it back afterwards, and the reply "
        "claims completion. Re-fetch what you wrote and report the link + one-line 'what changed', "
        "or state 'not verified' and why.")}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        payload = json.load(sys.stdin)
        out = post(payload) if mode == "post" else stop(payload) if mode == "stop" else None
    except Exception:
        return
    if out:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
