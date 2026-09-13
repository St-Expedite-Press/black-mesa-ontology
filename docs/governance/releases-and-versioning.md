# Releases and versioning

Black Mesa separates stable ontology identity from version identity.

- ontology IRI: `https://w3id.org/black-mesa/bmo`
- current version IRI: `https://w3id.org/black-mesa/bmo/releases/0.4.0`
- current `owl:versionInfo`: `0.4.0`

Release history belongs in [CHANGELOG.md](../../CHANGELOG.md). Durable architectural rationale belongs in [ADRs](../decisions/README.md). Current behavior belongs in topical documentation.

Do not keep multiple release-specific architecture handbooks active at the same time.

## Compatibility

Prefer deprecation over silently assigning contradictory meaning to an existing identifier.

Current compatibility concepts include:

- `Detection` — deprecated legacy class; use `DiagnosticDetectionAssertion` or `ConfirmedDetectionAssertion`;
- `ConfidenceTier` — deprecated because it conflated independent dimensions;
- `PreSymptomatic` — deprecated compatibility value; use sensor indication + evidence stage.

A future semantic release should document migrations, deprecations, identifier stability, and changed validation contracts.
