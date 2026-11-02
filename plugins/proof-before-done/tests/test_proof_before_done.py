"""Regression tests for hooks/proof_before_done.py.

Run: python3 -m unittest discover -s plugins/proof-before-done/tests -v
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks", "proof_before_done.py")
NOTION_WRITE = "mcp__abc__notion-create-pages"
NOTION_READ = "mcp__abc__notion-fetch"


def user(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def tool_result():
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}


def tool_use(name):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": name, "input": {}}]}}


def say(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def run(mode, payload):
    p = subprocess.run([sys.executable, "-I", HOOK, mode], input=json.dumps(payload), capture_output=True, text=True, timeout=10)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout) if p.stdout.strip() else None


def stop(entries, active=False):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
    try:
        return run("stop", {"transcript_path": f.name, "stop_hook_active": active})
    finally:
        os.unlink(f.name)


class StopHook(unittest.TestCase):
    def test_blocks_done_claim_after_unverified_write(self):
        out = stop([user("log my day"), tool_use(NOTION_WRITE), tool_result(), say("Done, the entry is published.")])
        self.assertEqual(out["decision"], "block")
        self.assertIn("notion-create-pages", out["reason"])

    def test_allows_when_read_back_follows_write(self):
        out = stop([user("log my day"), tool_use(NOTION_WRITE), tool_result(), tool_use(NOTION_READ), tool_result(), say("Done, published.")])
        self.assertIsNone(out)

    def test_read_before_write_does_not_count(self):
        out = stop([user("x"), tool_use(NOTION_READ), tool_result(), tool_use(NOTION_WRITE), tool_result(), say("Updated.")])
        self.assertEqual(out["decision"], "block")

    def test_allows_explicit_not_verified(self):
        out = stop([user("x"), tool_use(NOTION_WRITE), tool_result(), say("Created the page (not verified: fetch failed).")])
        self.assertIsNone(out)

    def test_allows_turn_without_external_write(self):
        out = stop([user("x"), tool_use("Edit"), tool_result(), say("Done.")])
        self.assertIsNone(out)

    def test_only_looks_at_current_turn(self):
        out = stop([user("a"), tool_use(NOTION_WRITE), tool_result(), say("Wrote it."), user("b"), say("Done.")])
        self.assertIsNone(out)

    def test_no_loop_when_stop_hook_active(self):
        out = stop([user("x"), tool_use(NOTION_WRITE), tool_result(), say("Done.")], active=True)
        self.assertIsNone(out)

    def test_missing_transcript_fails_open(self):
        self.assertIsNone(run("stop", {"transcript_path": "/nonexistent.jsonl"}))

    def test_missing_transcript_path_fails_open(self):
        self.assertIsNone(run("stop", {}))

    def test_empty_stdin_fails_open(self):
        for mode in ("post", "stop"):
            p = subprocess.run([sys.executable, "-I", HOOK, mode], input="", capture_output=True, text=True, timeout=10)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout.strip(), "")

    def test_non_json_fails_open(self):
        for mode in ("post", "stop"):
            p = subprocess.run([sys.executable, "-I", HOOK, mode], input="this is not json {", capture_output=True, text=True, timeout=10)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout.strip(), "")

    def test_unknown_mode_fails_open(self):
        p = subprocess.run([sys.executable, "-I", HOOK, "bogus"], input="{}", capture_output=True, text=True, timeout=10)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "")


class PostHook(unittest.TestCase):
    def test_reminds_after_external_write(self):
        out = run("post", {"tool_name": "mcp__x__slack_send_message"})
        ctx = out["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("slack_send_message", ctx)

    def test_silent_for_reads(self):
        self.assertIsNone(run("post", {"tool_name": NOTION_READ}))


class HooksJson(unittest.TestCase):
    """Pins the README claim that the hooks.json matcher and the WRITE pattern must agree."""

    def test_matcher_covers_every_write_alternative(self):
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "..", "hooks", "hooks.json")) as f:
            matcher = json.load(f)["hooks"]["PostToolUse"][0]["matcher"]
        spec = importlib.util.spec_from_file_location("pbd_under_test", HOOK)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        m = re.fullmatch(r"__\((.*)\)\$", mod.WRITE.pattern)
        self.assertIsNotNone(m, mod.WRITE.pattern)
        names = m.group(1).split("|")
        self.assertGreater(len(names), 10)
        for name in names:
            tool = "mcp__x__" + name
            self.assertTrue(mod.WRITE.search(tool), tool)
            self.assertTrue(re.fullmatch(matcher, tool), f"matcher does not cover {tool}")


if __name__ == "__main__":
    unittest.main()
