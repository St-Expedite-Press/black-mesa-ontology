# System architecture

Black Mesa separates semantic state from raw analytical storage and from policy execution.

## System context

```mermaid
flowchart TB
    SENSOR[Sensor / observation systems]
    OBJECT[Object & analytical storage]
    GRAPH[Black Mesa RDF knowledge graph]
    FIELD[Field operations]
    LAB[Diagnostic laboratory]
    DECISION[Decision services]
    POLICY[Regulatory rule registry]
    HUMAN[Human reviewers]
    EXTERNAL[External reporting systems]
    SENSOR --> GRAPH
    SENSOR --> OBJECT
    OBJECT --> GRAPH
    FIELD --> GRAPH
    LAB --> GRAPH
    GRAPH --> DECISION
    POLICY --> DECISION
    DECISION --> HUMAN
    HUMAN --> EXTERNAL
```

The boxes are architectural responsibilities, not a requirement that each become a separate software service.

## Semantic layers

```mermaid
flowchart TB
    L1[Sensing & observation]
    L2[Anomaly & hypotheses]
    L3[Physical evidence & custody]
    L4[Diagnostics]
    L5[Scientific assertions]
    L6[Regulatory / reporting evaluation]
    L1 --> L2 --> L3 --> L4 --> L5 --> L6
```

## Storage boundary

```mermaid
flowchart LR
    RAW[Raw imagery / arrays / bulk artifacts]
    STORE[Object or analytical store]
    REF[URI + checksum]
    RDF[RDF evidence graph]
    ASSERT[Assertions / provenance / relationships]
    RAW --> STORE
    STORE --> REF
    REF --> RDF
    RDF --> ASSERT
```

RDF stores identity, relationships, provenance, assertions, rules, spatial support, and verifiable pointers. It is not intended to carry millions of pixel/band/tile triples.

The runtime semantic contract is distributed across `schema/bmo-core.ttl`, `schema/reporting-crosswalks.ttl`, `schema/shapes.ttl`, `upper/upper-core.ttl`, and `tests/`.
