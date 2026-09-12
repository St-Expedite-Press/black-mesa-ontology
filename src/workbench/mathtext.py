"""Render a practical subset of LaTeX math to styled HTML.

The document pipeline has no MathJax or KaTeX: the renderer has no network
guarantee, and embedding a full math engine to set a few dozen expressions
would be disproportionate. The maths actually used in these documents is
simple — single-letter variables, subscripts and superscripts, set notation, a
handful of operators and Greek letters — and all of it has Unicode equivalents.

So this translates that subset and leaves anything it does not recognise
visibly intact rather than silently mangled. `tools/lint_docs.py` reports any
expression containing unconverted LaTeX so it is caught before rendering
rather than discovered in the PDF.

Anything genuinely beyond this subset — integrals, matrices, aligned
multi-line derivations — is a signal to use the LaTeX route
(`pandoc --pdf-engine=xelatex`) for that document instead.
"""
from __future__ import annotations

import html
import re

DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
# Inline maths: avoid matching across a blank line, and require non-space at the edges.
INLINE_RE = re.compile(r"(?<!\$)\$(?!\s)([^$\n]{1,200}?)(?<!\s)\$(?!\$)")

SYMBOLS = {
    r"\Delta": "Δ", r"\delta": "δ", r"\Sigma": "Σ", r"\sigma": "σ",
    r"\Phi": "Φ", r"\phi": "φ", r"\Theta": "Θ", r"\theta": "θ",
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\lambda": "λ",
    r"\mu": "μ", r"\tau": "τ", r"\pi": "π", r"\rho": "ρ", r"\epsilon": "ε",
    r"\mid": " ∣ ", r"\in": " ∈ ", r"\notin": " ∉ ",
    r"\subseteq": " ⊆ ", r"\subset": " ⊂ ", r"\cup": " ∪ ", r"\cap": " ∩ ",
    r"\leq": " ≤ ", r"\geq": " ≥ ", r"\neq": " ≠ ", r"\approx": " ≈ ",
    r"\times": " × ", r"\cdot": " · ", r"\pm": " ± ",
    r"\rightarrow": " → ", r"\to": " → ", r"\leftarrow": " ← ",
    r"\Rightarrow": " ⇒ ", r"\mapsto": " ↦ ",
    r"\ldots": "…", r"\dots": "…", r"\cdots": "⋯",
    r"\infty": "∞", r"\forall": "∀", r"\exists": "∃", r"\emptyset": "∅",
    r"\sum": "∑", r"\prod": "∏", r"\propto": " ∝ ",
    r"\arg\max": "arg max", r"\arg\min": "arg min",
    r"\max": "max", r"\min": "min", r"\log": "log", r"\exp": "exp",
    r"\quad": "  ", r"\qquad": "    ", r"\,": " ", r"\;": " ", r"\!": "",
    r"\{": "{", r"\}": "}", r"\%": "%", r"\&": "&",
    # Delimiter sizing hints. Without a stacked layout there is nothing to
    # size, so they are dropped and the bare delimiter is kept.
    r"\left": "", r"\right": "",
    r"\bigl": "", r"\bigr": "", r"\Bigl": "", r"\Bigr": "",
    r"\big": "", r"\Big": "", r"\biggl": "", r"\biggr": "",
}

# \mathcal{P} and similar script capitals.
MATHCAL = {
    "A": "𝒜", "B": "ℬ", "C": "𝒞", "D": "𝒟", "E": "ℰ", "F": "ℱ", "G": "𝒢",
    "H": "ℋ", "I": "ℐ", "J": "𝒥", "K": "𝒦", "L": "ℒ", "M": "ℳ", "N": "𝒩",
    "O": "𝒪", "P": "𝒫", "Q": "𝒬", "R": "ℛ", "S": "𝒮", "T": "𝒯", "U": "𝒰",
    "V": "𝒱", "W": "𝒲", "X": "𝒳", "Y": "𝒴", "Z": "𝒵",
}

LATEX_LEFTOVER_RE = re.compile(r"\\[a-zA-Z]+")


def _script(body: str, tag: str) -> str:
    return f"<{tag}>{html.escape(body)}</{tag}>"


def to_html(expr: str) -> str:
    """Translate one expression. Unknown commands survive as visible text."""
    s = expr.strip()

    s = re.sub(r"\\mathcal\{([A-Z])\}", lambda m: MATHCAL.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\(?:mathrm|mathbf|text|mathit)\{([^}]*)\}", r"\1", s)

    # Longest first, so \arg\max wins over \max.
    for cmd in sorted(SYMBOLS, key=len, reverse=True):
        s = s.replace(cmd, SYMBOLS[cmd])

    s = s.replace("\\\\", " ")

    # Fractions become a/b: a stacked fraction is not worth the markup here.
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)

    parts, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch in "_^" and i + 1 < len(s):
            tag = "sub" if ch == "_" else "sup"
            if s[i + 1] == "{":
                close = s.find("}", i + 2)
                if close != -1:
                    parts.append(_script(s[i + 2:close], tag))
                    i = close + 1
                    continue
            parts.append(_script(s[i + 1], tag))
            i += 2
            continue
        parts.append(html.escape(ch))
        i += 1
    return "".join(parts)


def unconverted(expr: str) -> list[str]:
    """LaTeX commands this module does not handle, for the linter to report."""
    s = re.sub(r"\\mathcal\{[A-Z]\}", "", expr)
    s = re.sub(r"\\(?:mathrm|mathbf|text|mathit|frac)\b", "", s)
    for cmd in SYMBOLS:
        s = s.replace(cmd, "")
    return sorted(set(LATEX_LEFTOVER_RE.findall(s)))


def render(md_text: str) -> str:
    """Replace $$...$$ and $...$ in Markdown source with styled HTML.

    Run before Markdown processing: converting first stops Markdown from
    treating underscores inside expressions as emphasis.
    """
    md_text = DISPLAY_RE.sub(
        lambda m: f'\n\n<div class="equation">{to_html(m.group(1))}</div>\n\n', md_text)
    return INLINE_RE.sub(
        lambda m: f'<span class="math">{to_html(m.group(1))}</span>', md_text)


def find_expressions(md_text: str) -> list[str]:
    return ([m.group(1) for m in DISPLAY_RE.finditer(md_text)]
            + [m.group(1) for m in INLINE_RE.finditer(md_text)])
