"""Tests for scripts/check_skills.py (stdlib unittest, fixtures in a temp dir)."""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "check_skills.py")

GOOD_DESC = "Use when the user wants to wrap up a session."


def write_skill(root, folder, frontmatter, plugin="demo"):
    d = os.path.join(root, "plugins", plugin, "skills", folder)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "SKILL.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n" + frontmatter + "\n---\n\n# Body\n")
    return path


def run_checker(root):
    proc = subprocess.run(
        [sys.executable, "-I", SCRIPT, root],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


class CheckSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def test_valid_skill_passes(self):
        write_skill(self.root, "demo-skill", f"name: demo-skill\ndescription: {GOOD_DESC}")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_no_skills_passes(self):
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_valid_skill_with_all_allowed_keys_passes(self):
        fm = (
            "name: demo-skill\n"
            "description: >\n"
            "  Use when the user wants a thing,\n"
            "  or another thing.\n"
            "license: MIT\n"
            "compatibility: Claude Code\n"
            "metadata:\n"
            "  version: 0.1.0\n"
            "  author: someone\n"
            "allowed-tools:\n"
            "  - Read\n"
            "  - Bash"
        )
        write_skill(self.root, "demo-skill", fm)
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_quoted_description_passes(self):
        write_skill(self.root, "demo-skill", 'name: "demo-skill"\ndescription: "Use when: quoted, with a colon."')
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_name_mismatch_fails(self):
        path = write_skill(self.root, "demo-skill", f"name: other-name\ndescription: {GOOD_DESC}")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)
        self.assertIn("name", out)

    def test_description_must_start_use_when(self):
        path = write_skill(self.root, "demo-skill", "name: demo-skill\ndescription: Helps you wrap up sessions.")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)
        self.assertIn("Use when", out)

    def test_description_too_long_fails(self):
        desc = "Use when " + "x" * (1537 - len("Use when "))
        self.assertEqual(len(desc), 1537)
        path = write_skill(self.root, "demo-skill", f"name: demo-skill\ndescription: {desc}")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)
        self.assertIn("1536", out)

    def test_description_at_limit_passes(self):
        desc = "Use when " + "x" * (1536 - len("Use when "))
        self.assertEqual(len(desc), 1536)
        write_skill(self.root, "demo-skill", f"name: demo-skill\ndescription: {desc}")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_nonportable_key_fails(self):
        path = write_skill(
            self.root,
            "demo-skill",
            f"name: demo-skill\ndescription: {GOOD_DESC}\nwhen_to_use: whenever",
        )
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)
        self.assertIn("when_to_use", out)

    def test_missing_frontmatter_fails(self):
        d = os.path.join(self.root, "plugins", "demo", "skills", "demo-skill")
        os.makedirs(d)
        path = os.path.join(d, "SKILL.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# No frontmatter here\n")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)

    def test_missing_description_fails(self):
        path = write_skill(self.root, "demo-skill", "name: demo-skill")
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(path, out)
        self.assertIn("description", out)

    def test_reports_every_failing_skill(self):
        bad1 = write_skill(self.root, "one", "name: one\ndescription: nope")
        bad2 = write_skill(self.root, "two", "name: wrong\ndescription: " + GOOD_DESC)
        write_skill(self.root, "three", "name: three\ndescription: " + GOOD_DESC)
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1)
        self.assertIn(bad1, out)
        self.assertIn(bad2, out)


if __name__ == "__main__":
    unittest.main()
