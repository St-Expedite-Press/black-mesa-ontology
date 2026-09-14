"""Put src/ on the import path, and make the console able to print the output.

The tools are run as scripts rather than installed, so `import workbench` needs
src/ on sys.path. Each tool does `import _bootstrap  # noqa: F401` before
importing the package. Installing the project would remove the need for this;
the explicit import is preferred over an install step that must be remembered.

The encoding fix is here for the same reason `paths.py` exists: every tool needs
it and none should have to remember it. A Windows console defaults to cp1252,
which cannot encode the em dashes and arrows the tools print in their reports —
so lint findings arrived as mojibake, which is a poor way to read a finding.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# A project may carry its own package - analysis code that belongs to one
# project rather than to the shared workbench. In this repository those live at
# projects/<name>/src; in a published repository the single project has been
# flattened and its package is already in the src/ above, so this loop finds
# nothing and needs no special case.
#
# Discovered rather than named: this module is vendored into a repository that
# must name no project, so it cannot contain a list of project directories.
_projects = ROOT / "projects"
if _projects.is_dir():
    for _p in sorted(_projects.iterdir()):
        _src = _p / "src"
        if _src.is_dir() and str(_src) not in sys.path:
            sys.path.insert(0, str(_src))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass  # a redirected or wrapped stream that cannot be reconfigured
