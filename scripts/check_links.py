#!/usr/bin/env python3
"""check_links.py - fail if a relative markdown link in a tracked *.md file points nowhere.

Usage: python3 scripts/check_links.py [ROOT]

Skips http(s), mailto and pure #anchor links, code fences and inline code.
Strips any #fragment before checking. Exit 1 lists "file: target" per broken link.
"""
import os
import re
import subprocess
import sys
from urllib.parse import unquote

LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,}).*?^\s{0,3}\1\s*$", re.M | re.S)
CODE = re.compile(r"`[^`\n]*`")


def main(argv):
    root = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    files = subprocess.run(["git", "-C", root, "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
    broken = []
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
            text = CODE.sub("", FENCE.sub("", fh.read()))
        for target in LINK.findall(text):
            if re.match(r"(https?:|mailto:|#)", target):
                continue
            path = unquote(target.split("#", 1)[0])
            base = root if path.startswith("/") else os.path.join(root, os.path.dirname(rel))
            if not os.path.exists(os.path.join(base, path.lstrip("/"))):
                broken.append(f"{rel}: {target}")
    for line in broken:
        print(line)
    print(f"check_links: {len(files)} file(s), {len(broken)} broken link(s)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
