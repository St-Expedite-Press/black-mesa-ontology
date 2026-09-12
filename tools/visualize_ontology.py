#!/usr/bin/env python
"""Visualize an RDF/OWL/TTL graph two ways:

1. An interactive pyvis HTML graph (drag, zoom, hover for full URIs) — good
   for exploration during ontology development.
2. A static Graphviz SVG/PDF class diagram (classes + object properties only,
   literals/datatype properties dropped) — good for embedding in PDF reports.

Usage:
    python tools/visualize_ontology.py path/to/schema.ttl [path2.ttl ...] \
        -o visualizations/schema

Produces <out>.html (interactive) and <out>.svg / <out>.pdf (class diagram),
provided the `dot` executable is on PATH (installed via winget/Graphviz).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import _bootstrap  # noqa: F401  (sys.path + console encoding)
import graphviz as gv
import rdflib
from pyvis.network import Network
from rdflib import RDF, RDFS, OWL
from rdflib.namespace import NamespaceManager


def load_graph(paths: list[Path]) -> rdflib.Graph:
    g = rdflib.Graph()
    for p in paths:
        fmt = rdflib.util.guess_format(str(p)) or "turtle"
        g.parse(str(p), format=fmt)
    return g


def short(ns_manager: NamespaceManager, term) -> str:
    if isinstance(term, rdflib.BNode):
        return f"_:{term}"
    try:
        return ns_manager.qname(term)
    except Exception:
        return str(term)


def build_pyvis(g: rdflib.Graph, out_html: Path) -> None:
    net = Network(height="900px", width="100%", directed=True, notebook=False,
                  bgcolor="#f4f2ea", font_color="#1c1a15", cdn_resources="in_line")
    net.barnes_hut(gravity=-6000, spring_length=180)
    seen = set()

    def add_node(term, color, shape):
        node_id = str(term)
        if node_id in seen:
            return
        seen.add(node_id)
        label = short(g.namespace_manager, term)
        net.add_node(node_id, label=label, title=str(term), color=color, shape=shape)

    for s, p, o in g:
        if p == RDF.type and o in (OWL.Class, RDFS.Class):
            add_node(s, "#2f6f4f", "box")
            continue
        if isinstance(o, rdflib.Literal):
            continue  # skip literal fan-out; keep the graph readable
        s_color = "#2f6f4f" if (s, RDF.type, OWL.Class) in g or (s, RDF.type, RDFS.Class) in g else "#7a6a4f"
        o_color = "#2f6f4f" if (o, RDF.type, OWL.Class) in g or (o, RDF.type, RDFS.Class) in g else "#7a6a4f"
        add_node(s, s_color, "box" if s_color == "#2f6f4f" else "ellipse")
        add_node(o, o_color, "box" if o_color == "#2f6f4f" else "ellipse")
        net.add_edge(str(s), str(o), label=short(g.namespace_manager, p), color="#8a8578")

    out_html.parent.mkdir(parents=True, exist_ok=True)
    # Write with explicit utf-8 rather than net.write_html(), which opens the
    # file with the platform default encoding (cp1252 on Windows) and chokes
    # on non-ASCII bytes inlined from the vis-network bundle.
    out_html.write_text(net.generate_html(notebook=False), encoding="utf-8")
    print(f"Wrote {out_html}")


def node_id(label: str) -> str:
    """Graphviz reads a colon as a node:port separator, so qnames cannot be used
    as node identifiers directly. Sanitise the id and keep the qname as label."""
    return label.replace(":", "__").replace(".", "_").replace("-", "_")


def build_class_diagram(g: rdflib.Graph, out_base: Path) -> None:
    dot = gv.Digraph("ontology", format="svg")
    dot.attr(rankdir="LR", bgcolor="#f4f2ea", fontname="Arial")
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="#ffffff",
             color="#2f6f4f", fontname="Arial", fontsize="11")
    dot.attr("edge", fontname="Arial", fontsize="9", color="#8a8578", fontcolor="#5c5748")

    # Skip blank nodes: anonymous class expressions have no useful label and
    # render as orphan boxes.
    classes = {c for c in (set(g.subjects(RDF.type, OWL.Class))
                           | set(g.subjects(RDF.type, RDFS.Class)))
               if not isinstance(c, rdflib.BNode)}
    for c in classes:
        lbl = short(g.namespace_manager, c)
        dot.node(node_id(lbl), label=lbl)

    # subclass edges
    for s, o in g.subject_objects(RDFS.subClassOf):
        if s in classes and o in classes:
            dot.edge(node_id(short(g.namespace_manager, s)),
                     node_id(short(g.namespace_manager, o)),
                     label="subClassOf", style="dashed")

    # object properties between classes (via domain/range where declared)
    for prop in set(g.subjects(RDF.type, OWL.ObjectProperty)):
        domains = list(g.objects(prop, RDFS.domain))
        ranges = list(g.objects(prop, RDFS.range))
        label = short(g.namespace_manager, prop)
        for d in domains:
            for r in ranges:
                if isinstance(d, rdflib.BNode) or isinstance(r, rdflib.BNode):
                    continue
                d_lbl = short(g.namespace_manager, d)
                r_lbl = short(g.namespace_manager, r)
                if d not in classes:
                    dot.node(node_id(d_lbl), label=d_lbl, style="rounded,filled,dashed", fillcolor="#f4f2ea")
                if r not in classes:
                    dot.node(node_id(r_lbl), label=r_lbl, style="rounded,filled,dashed", fillcolor="#f4f2ea")
                dot.edge(node_id(d_lbl), node_id(r_lbl), label=label)

    out_base.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("dot") is None:
        print("warning: `dot` not on PATH for this process — restart your terminal after the Graphviz "
              "winget install, or pass GRAPHVIZ_DOT explicitly. Skipping static diagram.", file=sys.stderr)
        return
    dot.render(str(out_base), format="svg", cleanup=True)
    dot.render(str(out_base), format="pdf", cleanup=True)
    print(f"Wrote {out_base}.svg and {out_base}.pdf")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ttl_files", nargs="+", type=Path)
    parser.add_argument("-o", "--out-base", type=Path, required=True,
                         help="Output path prefix, e.g. projects/x/visualizations/schema")
    args = parser.parse_args()

    for p in args.ttl_files:
        if not p.exists():
            print(f"error: {p} not found", file=sys.stderr)
            return 1

    g = load_graph(args.ttl_files)
    print(f"Loaded {len(g)} triples from {len(args.ttl_files)} file(s)")

    build_pyvis(g, args.out_base.with_suffix(".html"))
    build_class_diagram(g, args.out_base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
