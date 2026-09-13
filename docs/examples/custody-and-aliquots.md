# Worked example: custody and aliquots

Suppose one field specimen is divided for two methods.

```text
Specimen S-100
├── Aliquot A-100 -> qPCR
├── Aliquot B-100 -> sequencing
└── retained material
```

Each aliquot must have its own identity and remain genealogically linked to the source specimen. The two diagnostic results should refer to the material actually used, not an ambiguous string such as “the sample.”

```text
Collection-100
  ↓
Transfer-100
  ↓
Receipt-100
  ↓
AliquotEvent-100
  ├── A-100
  └── B-100
```

## Deliberate failure

```turtle
ex:BrokenTransfer a bmo:TransferEvent ;
    bmo:custodySubject ex:Specimen-100 ;
    bmo:fromCustodian ex:Collector ;
    bmo:eventAgent ex:Collector ;
    bmo:eventTime "2026-09-12T16:20:00Z"^^xsd:dateTime .
```

The transfer lacks `toCustodian`; SHACL rejects it.

This proves a minimum record contract, not that every physical handoff actually occurred as recorded.
