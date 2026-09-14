#!/usr/bin/env python
"""Check an RDF/OWL/TTL graph for structural quality and (optionally) SHACL conformance.

Runs four tiers of checks, cheapest first, and does not stop early — a full
report is always printed:

0. Imports — follows owl:imports transitively and parses each one from the
   repository, so the imported hierarchy is actually in the graph the later
   checks run over.
1. Lint — classes/properties missing rdfs:label or rdfs:comment, classes with
   no subClassOf anchor (orphans, excluding declared top-level roots),
   properties with no declared domain/range.
2. OWL-RL reasoning (owlrl) — expands the deductive closure and reports
   whether it introduces owl:Nothing (a logical inconsistency signal).
3. SHACL (pyshacl) — validates against a shapes file if one is given.

Usage:
    python tools/validate_ontology.py path/to/schema.ttl [more.ttl ...] \
        [--shapes path/to/shapes.ttl]

Exit code is non-zero if SHACL validation fails, OWL-RL finds owl:Nothing, or
an owl:imports cannot be resolved.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS, OWL

import _bootstrap  # noqa: F401
from workbench.paths import REPO_ROOT, relative

#: owl:imports IRIs resolved from the repository instead of over the network.
#:
#: rdflib does not follow owl:imports. Without this map the declaration in
#: upper-core.ttl was decorative: BFO was committed to vendor/ but no code path
#: ever loaded it, so the anchoring rule in each shapes.ttl was checking that a
#: class reaches an IRI *string* beginning "…/upper/" and nothing verified that
#: those upper terms reach BFO at all. Resolving locally rather than over the
#: network keeps validation offline and keeps every run reasoning over the same
#: hierarchy instead of whatever the remote copy says today.
LOCAL_IMPORTS = {
    "https://example.org/upper/": REPO_ROOT / "upper" / "upper-core.ttl",
    "http://purl.obolibrary.org/obo/bfo.owl": REPO_ROOT / "vendor" / "bfo.owl",
}


def parse_into(g: rdflib.Graph, path: Path) -> None:
    g.parse(str(path), format=rdflib.util.guess_format(str(path)) or "turtle")


def load_graph(paths: list[Path]) -> rdflib.Graph:
    g = rdflib.Graph()
    for p in paths:
        parse_into(g, p)
    return g


def resolve_imports(g: rdflib.Graph, already: set[Path]) -> list[str]:
    """Parse every owl:imports transitively from LOCAL_IMPORTS, in place.

    Returns the IRIs that could not be resolved. An unresolved import is
    reported rather than passed over: the axioms it was meant to contribute are
    simply absent, and a check that silently loses its axioms still passes.
    """
    unresolved: list[str] = []
    seen: set[str] = set()
    while True:
        pending = [str(o) for o in set(g.objects(None, OWL.imports))
                   if str(o) not in seen]
        if not pending:
            return unresolved
        for iri in sorted(pending):
            seen.add(iri)
            path = LOCAL_IMPORTS.get(iri)
            if path is None:
                unresolved.append(f"{iri} — no entry in LOCAL_IMPORTS")
                continue
            if not path.exists():
                unresolved.append(f"{iri} — mapped to {relative(path)}, which is missing")
                continue
            if path.resolve() in already:
                continue
            already.add(path.resolve())
            parse_into(g, path)
            print(f" + {iri}\n     from {relative(path)}")


def qname(g: rdflib.Graph, term) -> str:
    try:
        return g.namespace_manager.qname(term)
    except Exception:
        return str(term)


#: Namespaces owned by external standards. We reference their terms but do not
#: define them, so auditing them for local metadata is noise, not findings.
EXTERNAL_NS = (
    "http://purl.obolibrary.org/obo/",
    "http://www.w3.org/ns/sosa/",
    "http://www.w3.org/ns/ssn/",
    "http://www.opengis.net/ont/geosparql#",
    "http://www.w3.org/ns/prov#",
    "http://qudt.org/",
    "http://purl.org/dc/terms/",
    "http://www.w3.org/2004/02/skos/core#",
)


def is_external(term) -> bool:
    return str(term).startswith(EXTERNAL_NS)


#: BFO-numbered IRIs are minted for both classes (in bfo.owl) and relations
#: (in ro.owl, which is referenced rather than vendored — see upper-core.ttl).
#: Only the class half can be checked against the vendored copy.
BFO_PREFIX = "http://purl.obolibrary.org/obo/BFO_"


def check_anchors(g: rdflib.Graph) -> list[str]:
    """Every BFO class used as a superclass must exist in the loaded BFO.

    This is the check that makes vendor/bfo.owl load-bearing. Reaching a BFO
    IRI proves nothing on its own: `obo:BFO_0000301` is not a BFO class, but
    subClassOf will happily point at it and every prefix-matching rule in the
    repository would go on passing. Resolving the import and then confirming
    the target is declared turns the anchoring from a naming convention into a
    statement checkable against the standard.
    """
    issues: list[str] = []
    targets = {o for o in g.objects(None, RDFS.subClassOf)
               if str(o).startswith(BFO_PREFIX)}
    if not targets:
        return issues
    declared = {s for s in g.subjects(RDF.type, OWL.Class)}
    for t in sorted(targets, key=str):
        if t in declared:
            continue
        users = sorted(qname(g, s) for s in g.subjects(RDFS.subClassOf, t))
        issues.append(
            f"[anchor] {t} is not a class in the loaded BFO — used by "
            f"{', '.join(users)}. Either the IRI is a typo or the owl:imports "
            f"did not resolve; the anchoring is unverified either way.")
    print(f"BFO anchor targets: {len(targets)}  ({len(targets) - len(issues)} confirmed against the vendored standard)")
    return issues


#: Terms under these namespaces are ours to declare. Anything else is
#: referenced from a standard and is not expected to be defined here.
LOCAL_NS = "https://example.org/"

#: Predicates from the standards the schema is written IN rather than terms it
#: defines. Using rdfs:label does not oblige us to declare rdfs:label.
VOCAB_NS = (
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/2004/02/skos/core#",
    "http://www.w3.org/ns/shacl#",
    "http://purl.org/dc/terms/",
)

PROPERTY_TYPES = (OWL.ObjectProperty, OWL.DatatypeProperty,
                  OWL.AnnotationProperty, RDF.Property)


def check_undeclared(g: rdflib.Graph) -> list[str]:
    """Terms used in our own namespace but never declared.

    The gap that let eios:anthropogenicOrigin live in two example files for
    several commits without existing: the lint above audits declared terms for
    missing metadata, so a term that was never declared at all had nothing to
    be audited against. A typo'd predicate fails exactly the same way, silently
    and forever, because RDF is happy to assert anything about anything.
    """
    issues: list[str] = []

    declared_props = {s for t in PROPERTY_TYPES for s in g.subjects(RDF.type, t)}
    used_props = {p for p in set(g.predicates())
                  if str(p).startswith(LOCAL_NS) and not str(p).startswith(VOCAB_NS)}
    for p in sorted(used_props - declared_props, key=str):
        subjects = sorted({qname(g, s) for s in g.subjects(p, None)})[:3]
        issues.append(
            f"[undeclared] property {qname(g, p)} is used but never declared "
            f"(on {', '.join(subjects)}{' ...' if len(subjects) == 3 else ''}). "
            f"Declare it with a domain, range and comment, or fix the spelling.")

    declared_classes = {s for s in (set(g.subjects(RDF.type, OWL.Class))
                                    | set(g.subjects(RDF.type, RDFS.Class)))}
    used_classes = {o for o in set(g.objects(None, RDF.type))
                    if str(o).startswith(LOCAL_NS)}
    # A class used only as a vocabulary individual's type is declared elsewhere
    # as a class; one used as a type and never declared is the error case.
    for c in sorted(used_classes - declared_classes, key=str):
        if (c, RDF.type, None) in g:
            continue  # it is an individual of something, not a class reference
        issues.append(
            f"[undeclared] class {qname(g, c)} is used as a type but never "
            f"declared. Declare it and say what kind of thing it is.")

    print(f"Local terms used: {len(used_props)} properties, {len(used_classes)} classes"
          f"  ({len(issues)} undeclared)")
    return issues


def lint(g: rdflib.Graph) -> list[str]:
    issues: list[str] = []
    # Blank nodes are anonymous class expressions (owl:unionOf, restrictions).
    # They have no independent identity and cannot carry a label, so linting
    # them for one produces noise rather than findings.
    classes = {c for c in (set(g.subjects(RDF.type, OWL.Class))
                           | set(g.subjects(RDF.type, RDFS.Class)))
               if not isinstance(c, rdflib.BNode) and not is_external(c)}
    props = {p for p in (set(g.subjects(RDF.type, OWL.ObjectProperty))
                         | set(g.subjects(RDF.type, OWL.DatatypeProperty))
                         | set(g.subjects(RDF.type, RDF.Property)))
             if not isinstance(p, rdflib.BNode) and not is_external(p)}

    for c in sorted(classes, key=str):
        if not any(g.objects(c, RDFS.label)):
            issues.append(f"[class] {qname(g, c)} — missing rdfs:label")
        if not any(g.objects(c, RDFS.comment)):
            issues.append(f"[class] {qname(g, c)} — missing rdfs:comment")
        if not any(g.objects(c, RDFS.subClassOf)):
            issues.append(f"[class] {qname(g, c)} — no rdfs:subClassOf (orphan; fine only if intentionally a root)")

    for p in sorted(props, key=str):
        if not any(g.objects(p, RDFS.label)):
            issues.append(f"[property] {qname(g, p)} — missing rdfs:label")
        if not any(g.objects(p, RDFS.domain)):
            issues.append(f"[property] {qname(g, p)} — missing rdfs:domain")
        if not any(g.objects(p, RDFS.range)):
            issues.append(f"[property] {qname(g, p)} — missing rdfs:range")

    print(f"Classes: {len(classes)}  Properties: {len(props)}")
    return issues + check_anchors(g) + check_undeclared(g)


def run_owlrl(g: rdflib.Graph) -> bool:
    import owlrl
    closure_graph = rdflib.Graph()
    closure_graph += g
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(closure_graph)
    inconsistent = (None, RDF.type, OWL.Nothing) in closure_graph
    added = len(closure_graph) - len(g)
    print(f"OWL-RL closure: +{added} inferred triples")
    if inconsistent:
        print("OWL-RL: INCONSISTENT — something is typed as owl:Nothing")
    return not inconsistent


def run_shacl(g: rdflib.Graph, shapes_path: Path) -> bool:
    from pyshacl import validate
    shapes_graph = rdflib.Graph().parse(str(shapes_path), format=rdflib.util.guess_format(str(shapes_path)) or "turtle")
    conforms, results_graph, results_text = validate(g, shacl_graph=shapes_graph, inference="rdfs")
    print(results_text)
    return conforms


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ttl_files", nargs="+", type=Path)
    parser.add_argument("--shapes", type=Path, default=None)
    parser.add_argument("--skip-reasoning", action="store_true", help="skip the OWL-RL closure (slow on large graphs)")
    parser.add_argument("--skip-imports", action="store_true",
                        help="do not follow owl:imports (the anchoring rule then checks IRI strings only)")
    args = parser.parse_args()

    for p in args.ttl_files:
        if not p.exists():
            print(f"error: {p} not found", file=sys.stderr)
            return 1

    g = load_graph(args.ttl_files)
    print(f"Loaded {len(g)} triples from {len(args.ttl_files)} file(s)")

    ok = True
    if args.skip_imports:
        print("\n== Imports ==\nskipped (--skip-imports)")
    else:
        print("\n== Imports ==")
        before = len(g)
        unresolved = resolve_imports(g, {p.resolve() for p in args.ttl_files})
        if len(g) == before:
            print("No imports to resolve.")
        else:
            print(f"Import closure: +{len(g) - before} triples ({len(g)} total)")
        for u in unresolved:
            print(f" ! UNRESOLVED IMPORT: {u}")
            print("     Its axioms are absent from the graph, so anything that "
                  "depended on them is unchecked. Vendor the ontology and add it "
                  "to LOCAL_IMPORTS, or drop the owl:imports.")
        ok = not unresolved

    print("\n== Lint ==")
    issues = lint(g)
    if issues:
        for i in issues:
            print(" -", i)
    else:
        print("No lint issues.")

    if not args.skip_reasoning:
        print("\n== OWL-RL reasoning ==")
        ok = run_owlrl(g) and ok

    if args.shapes:
        print("\n== SHACL validation ==")
        ok = run_shacl(g, args.shapes) and ok

    print(f"\n{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
