# Black Mesa ontology — agent instructions

This repository is the semantic/evidentiary core of Black Mesa.

Before making changes:

1. read `README.md`;
2. read `docs/README.md`;
3. treat `schema/`, `upper/`, SHACL, and tests as the executable source of truth;
4. inspect the relevant RDF before relying on prose.

## Non-negotiable rules

- Observation, anomaly, sensor indication, hypothesis, diagnostic result, scientific detection, regulatory determination, reporting decision, and alert are distinct stages.
- A `SensorIndicationAssertion` must never assert pathogen presence.
- `NotDetected` is a diagnostic disposition, not a synonym for “no anomaly observed.”
- Evidence stage, diagnostic disposition, and confidence are independent dimensions.
- Do not convert an uncalibrated score or rank into a probability.
- Specimens and aliquots have persistent identities; custody is represented by explicit events.
- Scientific detection is separate from regulatory action.
- Draft `ReportingRule` records are non-operative and cannot authorize autonomous external notification.
- Phase 1 external regulatory notification remains human-reviewed.
- Crops, pathogens, sensors, methods, and other governed entities should use external canonical identifiers or reference data rather than unnecessary core subclasses.
- Raw imagery and dense arrays stay outside RDF and are referenced by URI + checksum.

## Change discipline

Before adding a class, state the competency question and justify why the distinction belongs in schema rather than reference data. Every high-consequence new SHACL constraint needs a deliberate failing fixture proving that it fires.

After schema changes run:

```bash
python tools/validate_ontology.py schema/bmo-core.ttl schema/reporting-crosswalks.ttl --shapes schema/shapes.ttl
python -m pytest tests/ -q
python tools/schema_docs.py --schema schema --out docs/reference
python tools/validate_docs.py
```

Update an ADR when changing a durable architectural decision. Update `CHANGELOG.md` for release-significant behavior.

## Publishing warning

This public repository has historically been assembled from another source/publishing workspace. Before merge, determine whether accepted changes must also be ported to that source so a subsequent publish does not overwrite them.
