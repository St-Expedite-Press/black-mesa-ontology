# NOTICE

This repository contains the Black Mesa sensor-agnostic agricultural biosecurity detection ontology and supporting validation/documentation.

External standards and vocabularies remain the intellectual property of their respective maintainers. Black Mesa reuses identifiers, structural concepts, or project-local proxy terms only as needed for interoperability.

## Basic Formal Ontology (BFO)

`vendor/bfo.owl` is BFO 2.0 (ISO/IEC 21838-2), redistributed unmodified under its own licence.

It is vendored so validation resolves `owl:imports` offline and every validation run reasons over the same hierarchy.

## IAO / RO

The shared upper module references selected published Information Artifact Ontology and Relation Ontology IRIs. It does not redistribute the full ontologies.

## W3C SOSA/SSN

Black Mesa aligns sensor, platform, and observation semantics to SOSA/SSN so the domain ontology remains sensor-agnostic.

Source: https://www.w3.org/TR/vocab-ssn/

## W3C PROV-O

PROV-O is used for provenance and derivation semantics.

Source: https://www.w3.org/TR/prov-o/

## OGC GeoSPARQL

GeoSPARQL is the intended spatial vocabulary for geometry and spatial relationships.

Source: https://www.ogc.org/standard/geosparql/

## NPDN National Data Repository

`schema/reporting-crosswalks.ttl` contains project-local proxy resources for the National Plant Diagnostic Network National Data Repository diagnostic-confidence values:

- Confirmed
- Suspected
- Not Detected
- Undetermined

These proxy IRIs are **not official NPDN RDF identifiers**. They exist only so Black Mesa can represent explicit, directional mappings while citing the public NPDN definitions.

Sources:

- https://www.npdn.org/public/understanding_ndr_data
- https://www.npdn.org/public/confidence_levels_definitions

Black Mesa's sensor-indication stage is explicitly recorded as having no direct NPDN diagnostic-confidence mapping.

## OASIS Common Alerting Protocol 1.2

`schema/reporting-crosswalks.ttl` contains project-local proxy resources for selected CAP 1.2 alert certainty terms.

These are **not official OASIS RDF identifiers**.

Source: https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2.html

The ontology deliberately does not equate Black Mesa/NPDN diagnostic dispositions with CAP certainty. CAP is an alert-message standard; diagnostic-to-alert translation belongs in an explicit reporting policy.

## Taxonomic and diagnostic reference data

The ontology is designed to reference canonical external identifiers for crops, pathogens, hosts, and diagnostic methods rather than copying external taxonomies into the local schema.

Specific pilot identifiers and method profiles will be added when the initial crop/pathogen use cases and diagnostic procedures are selected.


## Black Mesa licensing

Project-authored ontology/semantic content, SHACL, crosswalks, RDF reference data, examples, diagrams, and documentation are licensed CC BY 4.0 unless otherwise stated.

Software/tooling under `src/`, `tools/`, `tests/`, and `.github/` is licensed Apache-2.0.

See `LICENSE`, `LICENSE-ONTOLOGY.md`, and `LICENSE-SOFTWARE.md`.

## Persistent identifiers

The canonical Black Mesa identifier base is `https://w3id.org/black-mesa/`. The repository contains the canonical declarations and a redirect-registration plan in `docs/persistence.md`. W3ID dereferenceability remains dependent on registration with the external W3ID registry.
