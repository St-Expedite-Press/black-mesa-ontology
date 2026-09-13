# Graph boundaries

RDF is used for semantic relationships and auditability, not as a bulk sensor-data format.

| Put in the graph | Keep outside the graph |
|---|---|
| stable identity | raw imagery bytes |
| semantic relationships | video frames |
| provenance | dense spectral cubes |
| assertions | per-pixel/per-band arrays |
| timestamps | large point clouds |
| rule/model versions | model tensors |
| checksums | bulk analytical arrays |
| artifact URIs | large binary instrument outputs |
| spatial support descriptions | |
| custody events | |
| diagnostic interpretation | |

`ImageryReference` carries exactly one storage URI and checksum under current SHACL. The checksum matters because a location alone does not prove that the retrieved bytes are the same bytes analyzed originally.

The `NoTiledImageryShape` protects this boundary by rejecting project-local imagery predicates that attempt to expand tiles, pixels, or bands into the RDF record.

Use an object/analytical store for bulk bytes and the RDF graph for their identity, integrity reference, provenance, and interpretation.
