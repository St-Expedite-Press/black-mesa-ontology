# Invalid-record handbook

The adversarial fixture at `tests/fixtures/bmo-violations.ttl` documents failure modes the ontology actively rejects.

| Fixture | Risk | Correction |
|---|---|---|
| `UnanchoredThing` | local class has no upper/BFO category | anchor through upper module |
| `SensorClaimingPathogen` | sensor evidence becomes diagnosis | indication cannot assert pathogen |
| `UntraceableDetection` | assertion lacks physical-evidence trace | attach custody record |
| `DetectionNoDisposition` | diagnostic assertion has no interpretation | add one disposition |
| `IndicationWithBlindConfidence` | model applicability omitted | record model applicability |
| `DetectionWithBlindConfidence` | assay applicability omitted | record assay applicability |
| `BrokenTransfer` | handoff lacks receiving custodian | add receiving custodian |
| `TiledImagery` | bulk sensor data leaks into RDF | use URI + checksum |
| `SilentCrosswalk` | mapping hides semantic loss | state fidelity |
| `CrosswalkNoTarget` | mapped crosswalk lacks target | provide target unless NoMapping |
| `IncompletePilot` | pathosystem lacks pathogen | add exactly one canonical pathogen |
| `UnsafeDraftRule` | draft could bypass human gate | require human review |
| `DraftRuleNoReviewNote` | unresolved legal questions hidden | add review note |

The exact shape messages are documented in the generated [SHACL reference](../reference/shacl-reference.md).

A constraint that has never been demonstrated to reject its target failure mode can provide false confidence; that is why the fixture is deliberately adversarial.
