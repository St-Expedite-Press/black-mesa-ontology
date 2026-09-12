"""Design tokens — the single source of truth for the visual system.

These values also appear in templates/*.css, because CSS cannot import Python.
`tests/test_tokens.py` parses the stylesheets and asserts they agree, so the
duplication cannot drift silently. Change a value here and the test will tell
you which stylesheet to update.

Documented in templates/STYLE.md section 4 and the figure-design skill.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """One register's colour tokens."""

    ink: str            # primary text, strong strokes
    sub: str            # secondary text
    faint: str          # supplementary only - never load-bearing text
    rule: str           # hairlines, grids
    accent: str         # structure: section rules, subheads, running head
    accent_deep: str    # titles and top-level headings
    tint: str           # block fills, alternating table rows
    head_bg: str        # table header ground
    paper: str = "#ffffff"


#: Academic register. Used by paper.css and by every generated figure.
PAPER = Palette(
    ink="#16202a",
    sub="#445159",
    faint="#7d8890",
    rule="#c9d3d7",
    accent="#17646e",
    accent_deep="#0e3d47",
    tint="#eef3f4",
    head_bg="#16303c",
)

#: Internal register. Used by report.css.
REPORT = Palette(
    ink="#1c1a15",
    sub="#5c5748",
    faint="#8a8578",
    rule="#d8d3c4",
    accent="#2f6f4f",
    accent_deep="#2f6f4f",
    tint="#f4f2ea",
    head_bg="#1c1a15",
)

#: Ecological-press register (GUIS). Aged paper, warm ink, ember and bruise.
#: Documented in templates/EXPEDITE-GUIDE.md.
EXPEDITE = Palette(
    ink="#181410",
    sub="#4a4038",
    faint="#8a7d6b",
    rule="#c9bda4",
    accent="#c66f3a",
    accent_deep="#8f4a22",
    tint="#e6dcc2",
    head_bg="#181410",
    paper="#efe6cf",
)

#: The `mesa` register: defense-technical. Bone ground, cold near-black,
#: one institutional green. Documented in templates/MESA-GUIDE.md.
#: Named for the register, not for a project - this module is vendored into a
#: published repository that must name no programme.
MESA = Palette(
    ink="#14161a",
    sub="#4a4f57",
    faint="#8b8d87",
    rule="#cdcec8",
    accent="#2f6f4f",
    accent_deep="#14161a",
    tint="#e7e6de",
    head_bg="#14161a",
    paper="#f0eee7",
)

#: Reserved, and used only for genuine hazards in the Mesa register.
MESA_ALERT = "#a8432b"
#: Quotation rule in the Expedite register, and nowhere else.
EXPEDITE_BRUISE = "#a55b83"

#: Figures and charts use the academic palette in both registers, so a figure
#: is visually consistent wherever it is embedded.
FIGURE = PAPER

# Categorical series order for charts. Hue is never the only difference: each
# colour is paired with a marker and a dash pattern so a chart survives
# greyscale printing and colour-vision deficiency.
SERIES_COLORS = [
    FIGURE.accent,   # teal
    "#9a5b2e",       # burnt orange
    FIGURE.accent_deep,
    "#6b7d3a",       # olive
    "#7a4b6b",       # plum
    FIGURE.faint,
]
SERIES_MARKERS = ["o", "s", "^", "D", "v", "P"]
SERIES_DASHES = [(None, None), (5, 2), (1, 1.5), (7, 2, 1, 2), (3, 1), (9, 3)]

FONT_SANS = ["Segoe UI", "Inter", "DejaVu Sans", "Arial"]
FONT_SERIF = ["Source Serif 4", "Georgia", "Times New Roman"]
FONT_MONO = ["Cascadia Code", "Consolas", "DejaVu Sans Mono"]

#: Full-width figure canvas. Height varies; width is fixed so figures share a scale.
FIGURE_WIDTH = 760


def css_variable_map(palette: Palette) -> dict[str, str]:
    """Token name as it appears in CSS (--ink) mapped to its value."""
    return {
        "--ink": palette.ink,
        "--sub": palette.sub,
        "--faint": palette.faint,
        "--rule": palette.rule,
        "--accent": palette.accent,
        "--accent-deep": palette.accent_deep,
        "--tint": palette.tint,
        "--head-bg": palette.head_bg,
    }
