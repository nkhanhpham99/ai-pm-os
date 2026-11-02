"""Tests for scripts/backtest.py. Run: python3 -m unittest discover -s plugins/proof-before-done/tests -v"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "backtest.py")
WRITE = "mcp__abc__notion-create-pages"
READ = "mcp__abc__notion-fetch"
SECRET = "SECRET-TRANSCRIPT-TEXT"


def load():
    spec = importlib.util.spec_from_file_location("backtest_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def user(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def tool_result():
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}


def tool_use(name):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": name, "input": {}}]}}


def say(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def write_transcript(directory, name, entries, extra_lines=()):
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
        for line in extra_lines:
            f.write(line + "\n")
    return path


def make_fixture(directory):
    # Transcript A: turn 1 writes and reads back; turn 2 never writes.
    write_transcript(directory, "a.jsonl", [
        user("log it"), tool_use(WRITE), tool_result(), tool_use(READ), tool_result(), say("Done, published."),
        user("thanks"), say("You're welcome."),
    ])
    # Transcript B: one turn writes, never reads back, claims completion.
    write_transcript(directory, "b.jsonl", [
        user("log it"), tool_use(WRITE), tool_result(), say(SECRET + " Done, it is live."),
    ])


class Backtest(unittest.TestCase):
    def test_backtest_counts(self):
        with tempfile.TemporaryDirectory() as d:
            make_fixture(d)
            mod = load()
            paths = sorted(os.path.join(d, n) for n in os.listdir(d))
            self.assertEqual(mod.backtest(paths), {"turns": 3, "write_turns": 2, "read_back": 1, "would_block": 1})

    def test_backtest_empty_dir(self):
        with tempfile.TemporaryDirectory() as d:
            mod = load()
            self.assertEqual(mod.backtest(mod.find_transcripts(d)),
                             {"turns": 0, "write_turns": 0, "read_back": 0, "would_block": 0})

    def test_backtest_skips_corrupt_lines(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_transcript(d, "c.jsonl", [
                user("log it"), tool_use(WRITE), tool_result(), say("Done."),
            ], extra_lines=["{not json", "", "\x00\x01 garbage"])
            mod = load()
            self.assertEqual(mod.backtest([path]), {"turns": 1, "write_turns": 1, "read_back": 0, "would_block": 1})

    def test_backtest_ignores_sidechain_and_unreadable(self):
        with tempfile.TemporaryDirectory() as d:
            side = dict(tool_use(WRITE), isSidechain=True)
            path = write_transcript(d, "s.jsonl", [user("x"), side, say("Done.")])
            mod = load()
            self.assertEqual(mod.backtest([path, os.path.join(d, "missing.jsonl")]),
                             {"turns": 1, "write_turns": 0, "read_back": 0, "would_block": 0})


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True, timeout=30)

    def test_json_output_and_no_transcript_text(self):
        with tempfile.TemporaryDirectory() as d:
            make_fixture(d)
            p = self.run_cli(d, "--json")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout), {"turns": 3, "write_turns": 2, "read_back": 1, "would_block": 1})
            self.assertNotIn(SECRET, p.stdout + p.stderr)

    def test_default_output_never_prints_transcript_text(self):
        with tempfile.TemporaryDirectory() as d:
            make_fixture(d)
            p = self.run_cli(d)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertNotIn(SECRET, p.stdout + p.stderr)

    def test_examples_flag_prints_text(self):
        with tempfile.TemporaryDirectory() as d:
            make_fixture(d)
            p = self.run_cli(d, "--examples", "1")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(SECRET, p.stdout)

    def test_missing_directory_is_an_error(self):
        p = self.run_cli(os.path.join(HERE, "no-such-dir"))
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
