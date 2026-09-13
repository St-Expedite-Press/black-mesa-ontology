# Black Mesa documentation

The documentation is organized by purpose rather than release number.

## Document types

- **NORMATIVE:** explains rules directly represented or enforced by ontology, SHACL, or tests.
- **EXPLANATORY:** explains intent and use; executable artifacts remain authoritative.
- **GOVERNANCE:** defines project processes for identifiers, licenses, reference data, rules, and releases.
- **EXAMPLE:** teaches a modeling pattern using executable or deliberately invalid data.
- **GENERATED:** derived from schema/SHACL; do not edit manually.

## Read by role

### New project member
1. [Mission and scope](overview/mission-and-scope.md)
2. [System architecture](overview/system-architecture.md)
3. [Evidence chain](model/evidence-chain.md)
4. [Canonical workflow](examples/canonical-workflow.md)
5. [Glossary](overview/glossary.md)

### Ontology engineer
1. [Modeling principles](model/modeling-principles.md)
2. [Evidence chain](model/evidence-chain.md)
3. [Interoperability](model/interoperability.md)
4. [Generated reference](reference/README.md)
5. [Extension workflows](operations/extension-workflows.md)
6. [Architecture decisions](decisions/README.md)

### ML / sensing engineer
1. [Sensing and anomalies](model/sensing-and-anomalies.md)
2. [Hypotheses and next-best action](model/hypotheses-and-next-best-action.md)
3. [Assertions, dispositions, and confidence](model/assertions-dispositions-confidence.md)
4. [Graph boundaries](operations/graph-boundaries.md)

### Field / laboratory operations
1. [Specimens and custody](model/specimens-and-custody.md)
2. [Diagnostics](model/diagnostics.md)
3. [Custody and aliquots example](examples/custody-and-aliquots.md)

### Regulatory reviewer
1. [Regulatory boundary](model/regulatory-boundary.md)
2. [Regulatory-rule governance](governance/regulatory-rules.md)
3. [Rule lifecycle example](examples/regulatory-rule-lifecycle.md)

### Contributor
1. [CONTRIBUTING.md](../CONTRIBUTING.md)
2. [Extension workflows](operations/extension-workflows.md)
3. [Validation and CI](operations/validation-and-ci.md)
4. [Deployment gates](operations/deployment-gates.md)

Generated exact declarations live under [reference/](reference/).
