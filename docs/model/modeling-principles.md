# Modeling principles

## Preserve epistemic stages

Do not collapse observation, anomaly, indication, hypothesis, diagnostic result, scientific detection, regulatory determination, reporting decision, and alert. Each represents a different claim with different evidence requirements.

## Prefer external identifiers

Use authoritative identifiers for crops, pathogens, units, sensors, and standards-managed entities where practical. A local proxy is justified only for an explicit interoperability reason.

## Reference data before schema expansion

Deployment inventory is not automatically ontology structure. Pilot host/pathogen pairs belong in `reference/`; state rules belong in `rules/`; hardware normally belongs in SOSA/SSN-aligned instance data.

## Anchor local classes

Every local class must reach BFO through the shared upper module. Material, site, process, information, quality, and role must not be conflated.

## Distinguish world from record

A specimen is material. A collection or transfer is a process. A result or assertion is information. A custody record describes events; it is not the event itself.

## Make provenance and spatial warrant explicit

Consequential assertions should carry source evidence, generation time, and version. A result from one specimen does not automatically warrant a field-wide claim.

## Represent uncertainty honestly

Do not manufacture a probability from a score/rank. Do not transform “no anomaly recorded” into `NotDetected`. Do not force an external mapping where `NoMapping` is more defensible.

## Keep bulk data outside RDF

The graph represents relationships and verifiable artifact references; dense sensor data belong in analytical/object stores.

## Class-addition test

Before minting a class, answer: What operational distinction does it represent? Is an external ontology adequate? Is it schema or instance data? Which competency question becomes answerable? Which validation rule/query/workflow depends on it? What breaks if the class is absent?

“May be useful later” is not sufficient.
