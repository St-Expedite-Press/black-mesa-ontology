# Worked example: add a pathosystem

New pilots normally extend reference data rather than the ontology class hierarchy.

## Workflow

1. Locate the canonical host identifier.
2. Locate the canonical pathogen identifier.
3. Decide `OperationalPilot` or `RegulatoryStressTest`.
4. Mint a project reference-data IRI.
5. Record source/provenance links.
6. Add exactly one host taxon.
7. Add exactly one pathogen taxon.
8. Add exactly one scenario role.
9. Run SHACL/tests.

```turtle
@prefix pilot: <https://w3id.org/black-mesa/reference/pilot/> .
@prefix bmo:   <https://w3id.org/black-mesa/bmo/> .

pilot:ILLUSTRATIVE-EXAMPLE a bmo:PilotPathosystem ;
    bmo:hostTaxon <canonical-host-IRI> ;
    bmo:pathogenTaxon <canonical-pathogen-IRI> ;
    bmo:scenarioRole bmo:OperationalPilot .
```

Do **not** add `IllustrativeCrop` and `IllustrativePathogen` as core ontology classes merely to create the pilot.

If a canonical identifier is uncertain, resolve the reference-data issue before claiming the profile is operational.
