# Extension workflows

## Add a class

1. State the competency question.
2. Prove the distinction belongs in schema rather than reference data.
3. Check external ontologies for an adequate term.
4. Choose the correct upper/BFO category.
5. Add label, definition, and superclass.
6. Add necessary relationships.
7. Decide whether SHACL is required.
8. Add a valid example when useful.
9. Add a failing fixture for each high-consequence constraint.
10. Run validation/tests.
11. Regenerate `docs/reference/`.
12. Update an ADR if architecture changes.

## Add a property

Define label, domain, range, and enough commentary to prevent misuse. Confirm whether RO, PROV-O, SOSA/SSN, GeoSPARQL, or another adopted standard already provides the relation.

## Add a SHACL constraint

Add the shape, a precise violation message, a violating fixture, and an automated assertion that the fixture is rejected for the expected reason.

## Add a pilot pathosystem

Use external canonical host/pathogen IRIs, one scenario role, and provenance. See [worked example](../examples/add-a-pathosystem.md).

## Add a diagnostic-method profile

Instantiate `DiagnosticProcedureProfile` with verified applicability/performance facts only. Do not infer sensitivity, specificity, detection limit, host range, or matrix validity.

## Add a jurisdictional rule

Create/version a `ReportingRule` under the jurisdiction directory. New/unverified interpretations start as `DraftRequiresLegalRegulatoryReview`, require human review, and identify unresolved verification work.

## Deprecate a term

Preserve the IRI, mark it deprecated, document the replacement, maintain migration guidance, and avoid silently changing the old identifier's meaning.

## Add an external mapping

Record source/target and mapping fidelity explicitly. Use `NoMapping` when no defensible translation exists.
