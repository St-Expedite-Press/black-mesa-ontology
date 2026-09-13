# Contributing to Black Mesa

Black Mesa is an evidence ontology. Contributions are reviewed for semantic correctness, operational usefulness, provenance, and failure behavior—not merely valid RDF syntax.

## Development setup

```bash
python -m pip install -r requirements.txt
python -m pytest tests/ -q
```

Run the full validation contract before opening a pull request:

```bash
python tools/validate_ontology.py schema/bmo-core.ttl schema/reporting-crosswalks.ttl --shapes schema/shapes.ttl
python -m pytest tests/ -q
python tools/schema_docs.py --schema schema --out docs/reference
python tools/validate_docs.py
```

## Schema changes

A proposal for a new class or property must answer:

1. What operational distinction is represented?
2. Which competency question becomes answerable?
3. Is an external standard already adequate?
4. Is this genuinely schema, or should it be reference/instance data?
5. What BFO/upper category does it belong under?
6. Which validation rule, query, or workflow depends on it?
7. What breaks if the term does not exist?

Every local class needs a label, definition, and upper-ontology path. Every property needs a label, domain, range, and enough comment text to prevent misuse.

Do not mint a crop/pathogen/sensor taxonomy in the core merely because a deployment needs a new instance.

## SHACL changes

High-consequence constraints require the constraint, a human-readable violation message, a deliberate violating fixture, an automated test proving the violation is caught, and documentation of the protected failure mode.

## Reference data and rules

For a new pathosystem, prefer canonical external host/pathogen identifiers. Record provenance and a scenario role. See [pathosystem governance](docs/governance/pathosystems.md).

Rule records are versioned interpretations of external authority, not legislation themselves. New/unverified records remain draft, human-reviewed, and non-operative. See [regulatory-rule governance](docs/governance/regulatory-rules.md).

## Documentation

Write one canonical explanation per topic and link to it. Generated files under `docs/reference/` must not be edited manually. Use an ADR for a durable architecture decision and `CHANGELOG.md` for release history.

## Pull-request checklist

- [ ] competency question stated for semantic additions
- [ ] RDF parses and BFO anchoring is correct
- [ ] SHACL behavior is tested
- [ ] failing fixture added where appropriate
- [ ] examples use current persistent namespaces
- [ ] generated references regenerated
- [ ] documentation links validate
- [ ] regulatory claims do not exceed reviewed evidence
- [ ] license/external-source implications considered
- [ ] source/publishing workspace synchronization considered
