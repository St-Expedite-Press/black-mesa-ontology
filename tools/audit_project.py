#!/usr/bin/env python
"""Check a project's content for terms it is required not to name.

The GUIS ecosystem-typology project is independent research and must not name
the Black Mesa programme, its funder, or any platform or company. A bare grep
cannot express this, because the rule has to be *stated* somewhere - the
project's own CLAUDE.md necessarily names what it forbids, as does this script.

So governance files are excluded from the check and content files are not, and
the distinction lives here rather than in a command people have to remember to
scope correctly.

Usage:
    python tools/audit_project.py                     # audit all configured projects
    python tools/audit_project.py --project guis-ecosystem-typology
    python tools/audit_project.py --list              # show what is configured
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import _bootstrap  # noqa: F401
from blackmesa.paths import PROJECTS_DIR as PROJECTS, REPO_ROOT

# Files that define or explain the rule, and therefore must be allowed to state
# the terms it forbids. Everything else in the project is content and is checked.
GOVERNANCE = {"CLAUDE.md"}

AUDITS: dict[str, dict] = {
    "guis-ecosystem-typology": {
        "reason": "Independent research: must carry no programme or platform affiliation.",
        "forbidden": r"black[\s_-]?mesa|darpa|ag[\s_x×-]?bto",
        "extensions": {".md", ".ttl", ".py", ".json", ".csv", ".txt", ".svg", ".html"},
    },
}


def audit(project: str, cfg: dict, root: Path | None = None) -> list[tuple[Path, int, str]]:
    """Scan a project's content for the terms it must not name.

    `root` overrides the project directory so that an ASSEMBLED PUBLICATION
    TREE can be audited rather than only the project source. That distinction
    turned out to matter: auditing projects/guis-ecosystem-typology/ passes,
    because the offending text is not in the project - it is in the shared
    toolchain the publication vendors alongside it. The package is named
    `blackmesa`, and audit_project.py, tokens.py and test_shacl.py all name the
    programme. Auditing the project only is auditing the wrong tree at the one
    moment the rule binds hardest.
    """
    root = root or (PROJECTS / project)
    if not root.is_dir():
        print(f"error: no directory {root}", file=sys.stderr)
        return []
    pattern = re.compile(cfg["forbidden"], re.IGNORECASE)
    base = REPO_ROOT if REPO_ROOT in root.parents or root == REPO_ROOT else root
    hits: list[tuple[Path, int, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in cfg["extensions"]:
            continue
        if path.name in GOVERNANCE:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                try:
                    shown = path.relative_to(base)
                except ValueError:
                    shown = path
                hits.append((shown, i, line.strip()[:120]))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=None)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for name, cfg in AUDITS.items():
            print(f"{name}\n  reason: {cfg['reason']}\n  forbids: {cfg['forbidden']}")
        return 0

    targets = {args.project: AUDITS[args.project]} if args.project and args.project in AUDITS \
        else AUDITS
    if args.project and args.project not in AUDITS:
        print(f"no audit configured for {args.project!r}; nothing to check")
        return 0

    failed = False
    for name, cfg in targets.items():
        hits = audit(name, cfg)
        if hits:
            failed = True
            print(f"FAIL  {name}: {len(hits)} occurrence(s) of forbidden terms")
            print(f"      {cfg['reason']}")
            for path, line_no, text in hits:
                print(f"      {path}:{line_no}: {text}")
        else:
            print(f"PASS  {name}: no forbidden terms in content files")
            print(f"      ({cfg['reason']})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
