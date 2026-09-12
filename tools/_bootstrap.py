"""Put src/ on the import path, and make the console able to print the output.

The tools are run as scripts rather than installed, so `import blackmesa` needs
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

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass  # a redirected or wrapped stream that cannot be reconfigured
