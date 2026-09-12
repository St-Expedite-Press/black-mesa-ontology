# Black Mesa detection ontology

Phase 1 conceptual schema for pre-symptomatic agricultural pathogen detection:
from a drone-sensed spectral anomaly, through sample collection and field
assay, to a record a state agriculture department can act on.

## Read this first

This is a **documented conceptual schema**, not a fully axiomatised OWL
ontology. The formalisation beyond this point is deliberately deferred, and
what is deferred is recorded rather than left implicit.

- 20 classes, 22 properties, every class anchored to BFO 2.0.
- `schema/shapes.ttl` carries 10 SHACL shapes, tested against 7 planted violations.
- **Crosswalk entries are not authored.** `bmo:ReportingCrosswalk` is defined and constrained, but no NPDN or CAP term appears anywhere in the schema yet. The mapping the design argues is most fragile is, as of now, unwritten.
- Class-count and sizing figures in the paper derive from a Data Architecture Assessment that is not in this repository and are second-hand.

## Design commitments

**Reuse before invention.** SOSA/SSN for sensing, QUDT for units, GeoSPARQL for
geometry, Plant Ontology for plant part and growth stage, NCBITaxon for
pathogen and host identifiers by reference only. Cherry-picked terms from OBI
and PATO. The NPDN confidence enumeration and the CAP severity/certainty/
urgency triad are adopted rather than reinvented.

**Three things are invented**, because nothing models them: a pre-symptomatic
confidence tier, since every published enumeration presupposes visible
symptoms; the sensor-to-sample chain of custody, which no vocabulary spans; and
assay-specific result semantics.

**The architecture constraint.** Raw spectral imagery must never enter the graph
as per-pixel or per-tile triples - it inflates the store by roughly two orders
of magnitude and destroys query performance. Imagery is referenced by URI and
checksum from object storage, and a SHACL shape refuses the alternative.

**A detection is an assertion**, carrying evidence and provenance, rather than
a property stamped on a field. It must resolve back to the flight, the
collection and the assay that produced it, and it records the rule set version
in force when it was made.

## Layout

```
schema/     bmo-core.ttl and shapes.ttl
upper/      the shared BFO-anchored upper module
vendor/     BFO 2.0, redistributed unmodified
tools/      validate, visualise
tests/      pytest, including adversarial SHACL fixtures
docs/       the detection ontology paper
```

## Verify it

```bash
pip install -r requirements.txt
python tools/validate_ontology.py schema/*.ttl --shapes schema/shapes.ttl
python -m pytest tests/ -q
```

See `NOTICE.md` for source acknowledgements and `CLAUDE.md` for working rules.

---

Assembled from a source monorepo by `tools/publish_repo.py`. Edits made
directly here are overwritten on the next publish.
