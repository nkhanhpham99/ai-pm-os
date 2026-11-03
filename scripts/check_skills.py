#!/usr/bin/env python3
"""check_skills.py - validate every plugins/*/skills/*/SKILL.md.

Usage: python3 scripts/check_skills.py [--routine] [ROOT]

Exit 0 if every skill passes; otherwise exit 1 and print "path: reason" for each
problem. Frontmatter is read with a minimal YAML-subset reader (stdlib only):
scalars (plain, quoted, folded ">" and literal "|"), one-level mappings, and
lists (block "- x" or inline "[a, b]").

Rules (portable Agent Skills subset):
  - frontmatter keys limited to name, description, license, compatibility,
    metadata, allowed-tools
  - name equals the folder name (lowercase letters, digits, hyphens)
  - description present, starts with "Use when", at most 1536 characters

Routine rule (skills under plugins/pm-routines/skills/):
  - the body's level-2 ("## ") sections are exactly, in order: When to use,
    Defaults, Modes, Readiness check, Run, Honest summary, Guardrails.
    A heading may carry a suffix after the name, e.g. "## Modes (`setup` / ...)".
    "###" subsections are free; headings inside ``` or ~~~ fences are ignored
    (a fence closes only on the same character, at least as long).
  - Applied in the default mode too, so CI catches drift. --routine checks only
    the routine skills (frontmatter + sections) and fails if none are found.
"""
import glob
import os
import re
import sys

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MAX_DESCRIPTION = 1536
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s+(.*)|\s*)$")
ROUTINE_PLUGIN = "pm-routines"
ROUTINE_SECTIONS = [
    "When to use",
    "Defaults",
    "Modes",
    "Readiness check",
    "Run",
    "Honest summary",
    "Guardrails",
]
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
H2_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$")


class FrontmatterError(Exception):
    pass


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        body = s[1:-1]
        return re.sub(r'\\(["\\nt])', lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), body)
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")
    return s


def _is_quoted_open(s):
    return s[:1] in ("'", '"') and not (len(s) >= 2 and s[-1] == s[0])


def _plain(s):
    # strip a trailing YAML comment from plain scalars
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def _scalar(first, cont):
    first = first.strip()
    parts = [first] + [c.strip() for c in cont if c.strip()]
    joined = " ".join(p for p in parts if p)
    if first[:1] in ("'", '"'):
        return _unquote(joined)
    return _plain(joined)


def _block_scalar(indicator, cont):
    lines = [c[min(len(c) - len(c.lstrip()), _indent(cont)):] if c.strip() else "" for c in cont]
    while lines and not lines[-1].strip():
        lines.pop()
    if indicator.startswith("|"):
        return "\n".join(lines).strip()
    # folded: blank line = paragraph break, otherwise join with a space
    out, buf = [], []
    for ln in lines:
        if ln.strip():
            buf.append(ln.strip())
        else:
            out.append(" ".join(buf))
            buf = []
    out.append(" ".join(buf))
    return "\n".join(o for o in out if o).strip()


def _indent(lines):
    ind = [len(c) - len(c.lstrip()) for c in lines if c.strip()]
    return min(ind) if ind else 0


def _inline_list(s):
    inner = s.strip()[1:-1]
    return [_unquote(x) for x in inner.split(",") if x.strip()]


def _nested(cont):
    body = [c for c in cont if c.strip() and not c.lstrip().startswith("#")]
    if not body:
        return ""
    first = body[0].lstrip()
    if first.startswith("- ") or first == "-":
        items = []
        for c in body:
            s = c.lstrip()
            if s.startswith("- "):
                items.append(_unquote(_plain(s[2:])))
            else:
                raise FrontmatterError(f"unparseable list line: {c.strip()!r}")
        return items
    mapping = {}
    for c in body:
        m = KEY_RE.match(c.strip())
        if not m:
            raise FrontmatterError(f"unparseable mapping line: {c.strip()!r}")
        mapping[m.group(1)] = _unquote(_plain(m.group(2) or ""))
    return mapping


def parse_frontmatter(text):
    """Return (dict, None) or (None, error message)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter (file must start with ---)"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "unterminated frontmatter (no closing ---)"
    block = lines[1:end]

    # group into (key, rest, continuation lines)
    entries = []
    for ln in block:
        if not ln.strip() or ln.lstrip().startswith("#"):
            if entries:
                entries[-1][2].append(ln)
            continue
        if ln[0] in (" ", "\t"):
            if not entries:
                return None, f"unparseable frontmatter line: {ln.strip()!r}"
            entries[-1][2].append(ln)
            continue
        m = KEY_RE.match(ln)
        if not m:
            return None, f"unparseable frontmatter line: {ln.strip()!r}"
        entries.append([m.group(1), (m.group(2) or "").strip(), []])

    data = {}
    try:
        for key, rest, cont in entries:
            if key in data:
                return None, f"duplicate frontmatter key: {key}"
            if rest[:1] in (">", "|"):
                data[key] = _block_scalar(rest, cont)
            elif rest == "":
                data[key] = _nested(cont)
            elif rest.startswith("[") and rest.endswith("]"):
                data[key] = _inline_list(rest)
            elif _is_quoted_open(rest) or rest[:1] not in ("'", '"'):
                data[key] = _scalar(rest, cont)
            else:
                data[key] = _unquote(rest)
    except FrontmatterError as exc:
        return None, str(exc)
    return data, None


def check_skill(path):
    """Return a list of problem strings for one SKILL.md."""
    problems = []
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return [f"cannot read file: {exc}"]
    data, err = parse_frontmatter(text)
    if err:
        return [err]

    for key in data:
        if key not in ALLOWED_KEYS:
            problems.append(
                f"non-portable frontmatter key '{key}' (allowed: {', '.join(sorted(ALLOWED_KEYS))})"
            )

    folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
    name = data.get("name")
    if not isinstance(name, str) or not name:
        problems.append("missing 'name'")
    else:
        if name != folder:
            problems.append(f"name '{name}' does not match folder '{folder}'")
        if not NAME_RE.match(name):
            problems.append(f"name '{name}' must be lowercase letters, digits and hyphens")

    desc = data.get("description")
    if not isinstance(desc, str) or not desc:
        problems.append("missing 'description'")
    else:
        if not desc.startswith("Use when"):
            problems.append("description must start with 'Use when'")
        if len(desc) > MAX_DESCRIPTION:
            problems.append(f"description is {len(desc)} characters (max {MAX_DESCRIPTION})")
    return problems


def _h2_headings(text):
    """Level-2 heading texts in the body (after frontmatter), outside code fences."""
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    out, fence = [], None  # fence = the opening run, e.g. "```" or "~~~~"
    for ln in lines[start:]:
        m = FENCE_RE.match(ln)
        if fence is None:
            if m:
                fence = m.group(1)
                continue
        else:
            # only the same character, at least as long, with no info string, closes it
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
            continue
        m = H2_RE.match(ln)
        if m and not ln.startswith("###"):
            out.append(m.group(1))
    return out


def _section_name(heading):
    """Map a heading to its routine section name, or None if it is not one."""
    h = heading.strip().lower()
    for name in ROUTINE_SECTIONS:
        n = name.lower()
        if h == n or (h.startswith(n) and not h[len(n)].isalnum()):
            return name
    return None


def check_routine(path):
    """Return problems with a routine SKILL.md's section structure."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return [f"cannot read file: {exc}"]
    problems = []
    found = []
    for heading in _h2_headings(text):
        name = _section_name(heading)
        if name is None:
            problems.append(
                f"unexpected routine section '## {heading}' (allowed, in order: {', '.join(ROUTINE_SECTIONS)})"
            )
        elif name in found:
            problems.append(f"duplicate routine section '## {name}'")
        else:
            found.append(name)
    for name in ROUTINE_SECTIONS:
        if name not in found:
            problems.append(f"missing routine section '## {name}'")
    present = [n for n in ROUTINE_SECTIONS if n in found]
    if found != present:
        problems.append(
            f"routine sections out of order: found {', '.join(found)}; expected order {', '.join(ROUTINE_SECTIONS)}"
        )
    return problems


def is_routine(path, root):
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root))
    parts = rel.split(os.sep)
    return len(parts) >= 2 and parts[0] == "plugins" and parts[1] == ROUTINE_PLUGIN


def main(argv):
    args = argv[1:]
    routine_only = "--routine" in args
    args = [a for a in args if a != "--routine"]
    root = args[0] if args else "."
    pattern = os.path.join(root, "plugins", "*", "skills", "*", "SKILL.md")
    paths = sorted(glob.glob(pattern))
    if routine_only:
        paths = [p for p in paths if is_routine(p, root)]
        if not paths:
            print(f"check_skills: no routine skills found under plugins/{ROUTINE_PLUGIN}/skills/")
            return 1
    failed = False
    routines = 0
    for path in paths:
        problems = check_skill(path)
        if is_routine(path, root):
            routines += 1
            problems += check_routine(path)
        for problem in problems:
            print(f"{path}: {problem}")
            failed = True
    if not failed:
        if routine_only:
            print(f"check_skills: {routines} routine skill(s) OK")
        else:
            print(f"check_skills: {len(paths)} skill(s) OK ({routines} routine)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
