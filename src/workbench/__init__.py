"""Shared library for this repository's toolchain.

Named for what it is - the shared bench both projects work on - and
deliberately after neither of them. One project is independent research that
must carry no programme, platform, funder or company name, and it is published
as its own repository with a vendored copy of this package. A package named
after the sibling project would have made that publication advertise the thing
its separation rule forbids, which is precisely what happened before the
rename. Keep every module here project-neutral; `tools/audit_project.py`,
run over an assembled publication tree, is what catches a regression.


The command-line tools in tools/ are thin wrappers over this package. Anything
used by more than one tool belongs here, so that the linter and the renderer
cannot disagree about what a document is.

    paths      repository layout, project discovery
    frontmatter  YAML frontmatter parsing and the Document type
    tokens     design tokens - the single source of truth for the visual system
    mathtext   a practical LaTeX subset rendered to Unicode HTML
    rendering  Markdown to HTML to PDF
"""

from . import frontmatter, mathtext, paths, rendering, tokens

__all__ = ["frontmatter", "mathtext", "paths", "rendering", "tokens"]
