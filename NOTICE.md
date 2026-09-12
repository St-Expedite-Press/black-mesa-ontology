# NOTICE

## IUCN Global Ecosystem Typology

`schema/get-core.ttl` is generated from:

> Keith, D.A., Ferrer-Paris, J.R., Nicholson, E. and Kingsford, R.T. (eds.)
> (2020). *IUCN Global Ecosystem Typology 2.0: Descriptive profiles for biomes
> and ecosystem functional groups.* Gland, Switzerland: IUCN.

It carries the realm, biome and Ecosystem Functional Group names and, for 106
of the 108 groups, the ECOLOGICAL TRAITS, KEY ECOLOGICAL DRIVERS and
DISTRIBUTION text of the descriptive profiles, reproduced verbatim.

The monograph states: *"Reproduction of this publication for educational or
other non-commercial purposes is authorized without prior written permission
from the copyright holder provided the source is fully acknowledged."* This
repository is non-commercial research and the source is acknowledged here, in
the generated file's header, and in its `dct:source` triple.

Copyright in that text remains with IUCN. The `get:` namespace used here is a
project-local stand-in and is **not** an official IUCN identifier scheme.

## IUCN Red List of Ecosystems

`schema/rle-core.ttl` models categories and criteria from:

> Bland, L.M., Keith, D.A., Miller, R.M., Murray, N.J. and Rodriguez, J.P.
> (eds.) (2016/2017). *Guidelines for the application of IUCN Red List of
> Ecosystems Categories and Criteria, Version 1.1.* Gland, Switzerland: IUCN.

**No assessment in this repository is an IUCN assessment.** Every one is a
`rle:ProvisionalAssessment`, marked PROVISIONAL AND NON-IUCN, and the official
status of every unit proposed here is `rle:NE` (Not Evaluated).

## Basic Formal Ontology

`vendor/bfo.owl` is BFO 2.0 (ISO/IEC 21838-2), redistributed unmodified under
its own licence. It is vendored so that validation resolves `owl:imports`
offline and every run reasons over the same hierarchy.
