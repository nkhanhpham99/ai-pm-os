"""Tests for scripts/check_links.py (stdlib unittest, fixtures in a temp git repo)."""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "check_links.py")


def git(root, *args):
    subprocess.run(["git", "-C", root, *args], check=True, capture_output=True)


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def run_checker(root):
    proc = subprocess.run([sys.executable, "-I", SCRIPT, root], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


class CheckLinksTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        git(self.root, "init", "-q")

    def track(self):
        git(self.root, "add", "-A")

    def test_good_links_pass(self):
        write(self.root, "docs/guide.md", "# Guide\n")
        write(
            self.root,
            "README.md",
            "[guide](docs/guide.md) [section](docs/guide.md#guide) [top](#top)\n"
            "[web](https://example.com/x.md) [mail](mailto:someone@example.com)\n"
            "`[not a link](inline-code.md)`\n\n```\n[fenced](fenced.md)\n```\n",
        )
        write(self.root, "docs/back.md", "[up](../README.md)\n")
        self.track()
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_broken_link_fails_and_is_named(self):
        write(self.root, "docs/guide.md", "# Guide\n")
        write(self.root, "README.md", "[guide](docs/guide.md)\n[gone](docs/missing.md#part)\n")
        self.track()
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1, out)
        self.assertIn("README.md", out)
        self.assertIn("docs/missing.md", out)
        self.assertNotIn("docs/guide.md", out)

    def test_linked_image_target_is_checked(self):
        write(self.root, "README.md", "[![b](https://x/y.svg)](missing.md)\n")
        self.track()
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1, out)
        self.assertIn("missing.md", out)

    def test_filename_with_space_is_scanned(self):
        write(self.root, "my notes.md", "[gone](nowhere.md)\n")
        write(self.root, "README.md", "[notes](my%20notes.md)\n")
        self.track()
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1, out)
        self.assertIn("my notes.md: nowhere.md", out)
        self.assertNotIn("my%20notes.md", out)

    def test_untracked_markdown_is_not_scanned(self):
        write(self.root, "README.md", "fine\n")
        self.track()
        write(self.root, "scratch.md", "[gone](nowhere.md)\n")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
