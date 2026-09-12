"""Markdown to HTML, and HTML to PDF.

The Markdown extension set and the task-list rewrite live here rather than in
the renderer, so the linter can reason about exactly the HTML the renderer will
produce.
"""
from __future__ import annotations

import re
from pathlib import Path

import markdown as md
from jinja2 import Environment, FileSystemLoader

from . import mathtext
from .paths import TEMPLATES_DIR, stylesheets

MD_EXTENSIONS = ["extra", "sane_lists", "toc", "admonition", "tables"]

# python-markdown has no task-list support, so GFM checkboxes arrive as literal
# "[x]" text. Rewrite them into list items the stylesheets can draw.
TASK_RE = re.compile(r"<li>\s*\[([ xX])\]\s*")

TEMPLATE_NAME = "document.html.jinja"


class StyleNotFound(ValueError):
    pass


def to_html(body_md: str) -> str:
    """Render Markdown body text to HTML, with maths and task lists handled."""
    # Maths first: converting before Markdown stops underscores inside
    # expressions from being read as emphasis.
    body_md = mathtext.render(body_md)
    html = md.markdown(body_md, extensions=MD_EXTENSIONS)
    return TASK_RE.sub(
        lambda m: '<li class="task done">' if m.group(1).lower() == "x"
        else '<li class="task todo">',
        html,
    )


def load_stylesheet(style: str) -> str:
    path = TEMPLATES_DIR / f"{style}.css"
    if not path.exists():
        raise StyleNotFound(
            f"no stylesheet {style!r} in templates/ (have: {', '.join(stylesheets())})")
    return path.read_text(encoding="utf-8")


def build_page(meta: dict, body_html: str, style: str, fallback_title: str) -> str:
    """Assemble the full HTML document from metadata and rendered body."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(TEMPLATE_NAME)
    return template.render(
        title=meta.get("title") or fallback_title,
        subtitle=meta.get("subtitle"),
        doc_id=meta.get("doc_id"),
        # No default kicker. An organisation name baked in here would appear on
        # every document that omits one, including projects required to carry
        # no affiliation at all.
        kicker=meta.get("kicker", ""),
        authors=meta.get("authors"),
        meta=meta.get("meta"),
        footer=meta.get("footer"),
        body=body_html,
        css=load_stylesheet(style),
    )


def write_pdf(html: str, out_path: Path) -> None:
    """Render HTML to PDF with Chromium."""
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        page.pdf(path=str(out_path), format="Letter",
                 print_background=True, display_header_footer=False)
        browser.close()
