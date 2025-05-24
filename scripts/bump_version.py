#!/usr/bin/env python
"""Bump package version and prepend changelog entry."""
import sys
from pathlib import Path
from datetime import date
import re

if len(sys.argv) != 2:
    print("Usage: bump_version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1]
files = [Path('pyproject.toml'), Path('backend/pyproject.toml')]
for path in files:
    text = path.read_text()
    text = re.sub(r'version = "\d+\.\d+\.\d+"', f'version = "{new_version}"', text)
    path.write_text(text)

changelog = Path('CHANGELOG.md')
lines = changelog.read_text().splitlines()
today = date.today().isoformat()
header = f"## [{new_version}] – {today}"
entry = [header, "### Changed", f"* Backend package version bumped to {new_version}.", ""]
changelog.write_text("\n".join(entry + lines))
