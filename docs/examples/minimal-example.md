---
title: Minimal example
subtitle: A synthetic structurally valid detection-oriented record
style: mesa
---

## Status and limitations

Source: authored synthetic example. Evidence type: illustrative RDF.
Verification status: not empirical. Authority: repository maintainers.
Limitation: it demonstrates only a relationship pattern and is not an assay
result.

```turtle
@prefix bmo: <https://example.org/bmo/> .
@prefix up: <https://example.org/upper/> .
@prefix ex: <https://example.org/example/> .

ex:zone a bmo:Zone .
ex:result a bmo:AssayResult .
ex:chain a bmo:CustodyChain .
ex:rules a up:RuleSetVersion .
ex:detection a bmo:Detection ;
  bmo:concernsZone ex:zone ;
  bmo:derivedFromResult ex:result ;
  bmo:hasCustodyChain ex:chain ;
  up:generatedUnder ex:rules .
```

The isolated snippet is syntactically valid Turtle. Full SHACL validation also
requires the schema import closure and a complete data graph.
