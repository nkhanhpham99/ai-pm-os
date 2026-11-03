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


ROUTINE_HEADINGS = [
    "When to use",
    "Defaults",
    "Modes",
    "Readiness check",
    "Run",
    "Honest summary",
    "Guardrails",
]


def write_routine(root, folder, headings, plugin="pm-routines", extra=""):
    """Write a frontmatter-valid SKILL.md whose body has the given ## headings."""
    d = os.path.join(root, "plugins", plugin, "skills", folder)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "SKILL.md")
    body = "".join(f"## {h}\nText.\n\n" for h in headings)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"---\nname: {folder}\ndescription: {GOOD_DESC}\n---\n\n# Title\n\n" + body + extra)
    return path


def run_checker(root, *flags):
    proc = subprocess.run(
        [sys.executable, "-I", SCRIPT, *flags, root],
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


class RoutineCheckTest(unittest.TestCase):
    """--routine: skills under plugins/pm-routines/ must have the 7 routine sections, in order."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def test_routine_valid_passes(self):
        write_routine(self.root, "demo-routine", ROUTINE_HEADINGS)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 0, out)
        self.assertIn("routine", out)

    def test_routine_missing_heading_fails(self):
        headings = [h for h in ROUTINE_HEADINGS if h != "Readiness check"]
        path = write_routine(self.root, "demo-routine", headings)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("Readiness check", out)

    def test_routine_out_of_order_fails(self):
        headings = list(ROUTINE_HEADINGS)
        headings[4], headings[5] = headings[5], headings[4]
        path = write_routine(self.root, "demo-routine", headings)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("order", out)

    def test_routine_extra_section_fails(self):
        headings = ROUTINE_HEADINGS[:3] + ["Workflow"] + ROUTINE_HEADINGS[3:]
        path = write_routine(self.root, "demo-routine", headings)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("Workflow", out)

    def test_routine_heading_suffix_and_subsections_pass(self):
        headings = list(ROUTINE_HEADINGS)
        headings[2] = "Modes (`setup` / `run` / `learn` / `tune`)"
        extra = "### A subsection is fine\n\n```markdown\n## Not a real heading\n```\n"
        write_routine(self.root, "demo-routine", headings, extra=extra)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 0, out)

    def test_routine_duplicate_section_fails(self):
        headings = ROUTINE_HEADINGS + ["Guardrails"]
        path = write_routine(self.root, "demo-routine", headings)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("duplicate", out)

    def test_routine_mixed_fences_do_not_close_each_other(self):
        # a ``` line inside a ~~~ fence must not end the fence, so the
        # "## Workflow" inside it stays hidden; the real "## Extra" after it counts
        extra = "~~~markdown\n```\n## Workflow\n```\n~~~\n\n## Extra\n"
        path = write_routine(self.root, "demo-routine", ROUTINE_HEADINGS, extra=extra)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("Extra", out)
        self.assertNotIn("Workflow", out)

    def test_routine_check_runs_in_default_mode(self):
        path = write_routine(self.root, "demo-routine", ROUTINE_HEADINGS[:-1])
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 1, out)
        self.assertIn(path, out)
        self.assertIn("Guardrails", out)

    def test_non_routine_plugin_is_not_held_to_routine_sections(self):
        write_routine(self.root, "demo-skill", ["Workflow"], plugin="demo")
        rc, out = run_checker(self.root, "--routine")
        # the only skill is outside pm-routines, so --routine has nothing to check
        self.assertEqual(rc, 1, out)
        self.assertIn("no routine skills", out)
        rc, out = run_checker(self.root)
        self.assertEqual(rc, 0, out)

    def test_routine_flag_also_checks_frontmatter(self):
        d = os.path.join(self.root, "plugins", "pm-routines", "skills", "demo-routine")
        os.makedirs(d)
        path = os.path.join(d, "SKILL.md")
        body = "".join(f"## {h}\nText.\n\n" for h in ROUTINE_HEADINGS)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("---\nname: demo-routine\ndescription: Runs a thing.\n---\n\n" + body)
        rc, out = run_checker(self.root, "--routine")
        self.assertEqual(rc, 1, out)
        self.assertIn("Use when", out)


if __name__ == "__main__":
    unittest.main()
