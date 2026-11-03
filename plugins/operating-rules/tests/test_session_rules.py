"""Tests for hooks/session_rules.py.

Run: python3 -m unittest discover -s plugins/operating-rules/tests -v
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "hooks")
HOOK = os.path.join(HOOKS, "session_rules.py")
RULES = os.path.join(HOOKS, "rules.md")


def run(hook):
    return subprocess.run([sys.executable, "-I", hook], input="{}", capture_output=True, text=True, timeout=10)


class SessionRulesTest(unittest.TestCase):
    def test_emits_session_start_context(self):
        p = run(HOOK)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        spec = out["hookSpecificOutput"]
        self.assertEqual(spec["hookEventName"], "SessionStart")
        with open(RULES, encoding="utf-8") as f:
            self.assertEqual(spec["additionalContext"], f.read())
        self.assertTrue(spec["additionalContext"].strip())

    def test_missing_rules_fails_open(self):
        with tempfile.TemporaryDirectory() as d:
            copy = os.path.join(d, "session_rules.py")
            shutil.copy(HOOK, copy)  # no rules.md next to it
            p = run(copy)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "")

    def test_blank_rules_prints_nothing(self):
        for blank in ("", "   \n\t\n  \n"):
            with tempfile.TemporaryDirectory() as d:
                copy = os.path.join(d, "session_rules.py")
                shutil.copy(HOOK, copy)
                with open(os.path.join(d, "rules.md"), "w", encoding="utf-8") as f:
                    f.write(blank)
                p = run(copy)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout.strip(), "", repr(blank))

    def test_rules_under_250_words(self):
        with open(RULES, encoding="utf-8") as f:
            words = len(f.read().split())
        self.assertLessEqual(words, 250, f"rules.md is {words} words")


if __name__ == "__main__":
    unittest.main()
