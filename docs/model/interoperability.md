# Interoperability

Black Mesa reuses external vocabularies where they improve semantic compatibility and avoids copying entire taxonomies into the project.

| Vocabulary / standard | Role |
|---|---|
| BFO | upper categories and category discipline |
| IAO / RO | information-artifact and relation semantics |
| SOSA/SSN | sensors, platforms, observations |
| PROV-O | provenance, derivation, agents, generation time |
| GeoSPARQL | spatial/geometry semantics |
| QUDT | quantitative values and units as measurement modules grow |
| OBI | selected assay/specimen concepts |
| NCBITaxon | canonical organism identifiers for current pilot data |
| NPDN concepts | diagnostic reporting interoperability |
| OASIS CAP | downstream alert-message semantics |

Referencing an external IRI does not mean the repository vendors or owns the entire external ontology.

## BFO alignment

Local classes must reach BFO through `upper/upper-core.ttl`. Offline validation loads the vendored BFO copy so anchoring is checked against actual declared BFO classes rather than merely an IRI prefix.

## Crosswalk fidelity

`ReportingCrosswalk` records a directional mapping and one of `Exact`, `Broader`, `Narrower`, `Partial`, or `NoMapping`.

`NoMapping` is a valid result and preferable to silently forcing an internal concept into an external field with different semantics.

## NPDN and CAP

Black Mesa diagnostic dispositions can map to project-local proxy resources representing NPDN concepts. A sensor-only indication intentionally has no direct diagnostic-confidence mapping because it is not a diagnostic record.

CAP certainty belongs to alert-message semantics, not diagnostic disposition. Any diagnostic-to-alert translation belongs in explicit reporting policy.
