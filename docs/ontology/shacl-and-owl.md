---
title: SHACL and OWL
subtitle: Open-world semantics and closed-world data checks
style: mesa
---

## OWL

OWL declarations state intended semantics under an open-world assumption.
Absence of a triple is not, by itself, falsehood. The repository runs an OWL-RL
closure as a smoke check; it is not proof that the model is complete or
scientifically correct.

## SHACL

SHACL applies local requirements to supplied graphs: a detection needs a zone
and custody information, and imagery references need a URI and checksum.
Conformance means the supplied graph met these shapes; it does not prove the
referenced image exists, a detection is true, or provenance is trustworthy.
