"""Shared library for the black_mesa repository toolchain.

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
