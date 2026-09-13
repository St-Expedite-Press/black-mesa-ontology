# Persistent identifiers

Black Mesa declares persistent identifiers under `https://w3id.org/black-mesa/` so ontology identity is not tied to a GitHub repository path.

## Canonical identifiers

```text
Ontology IRI:
https://w3id.org/black-mesa/bmo

Term namespace:
https://w3id.org/black-mesa/bmo/

Current version IRI:
https://w3id.org/black-mesa/bmo/releases/0.4.0

Upper ontology IRI:
https://w3id.org/black-mesa/upper

Upper term namespace:
https://w3id.org/black-mesa/upper/
```

Project instances also use paths such as `/reference/`, `/rules/`, `/authority/`, and `/example/`.

## Identity types

- **Ontology IRI:** stable identity of the ontology.
- **Term IRI:** stable identity of a class/property/individual.
- **Version IRI:** identity of a published ontology version.
- **External identifier:** identity governed by another authority.
- **Instance identifier:** project identity for a concrete rule/profile/example.

## Public resolution status

**UNVERIFIED / DEPLOYMENT GATE.**

Declaring these IRIs in RDF does not create a public redirect. A public check during this rebuild did not yield verifiable evidence that the Black Mesa W3ID path is currently resolving. Treat public dereferenceability as unverified until registered and tested.

Offline validation is separate: `tools/validate_ontology.py` maps the upper ontology import to local repository files, so CI validates without network access.

Do not mint substitute Black Mesa identifiers for well-governed crops, pathogens, units, or similar external entities without an explicit interoperability reason.
