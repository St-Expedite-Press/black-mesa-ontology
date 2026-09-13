# Changelog

This file records architecture-significant changes. It replaces the former practice of keeping multiple version-specific design documents active at once.

## 0.4.0

- adopted the persistent `https://w3id.org/black-mesa/` identifier space;
- declared the core ontology version IRI `https://w3id.org/black-mesa/bmo/releases/0.4.0`;
- split project-authored semantic content (CC BY 4.0) from executable tooling (Apache-2.0);
- instantiated four initial pilot pathosystems as reference data;
- added draft jurisdictional rule records for Arkansas, Louisiana, Missouri, Oklahoma, and Texas;
- added rule review-status and human-review safeguards;
- retained jurisdictional rules as data rather than ontology subclasses.

## 0.3 lineage

- generalized the core from a drone-specific model to sensor-agnostic surveillance;
- separated observation, anomaly, indication, hypothesis, diagnostics, scientific detection, and regulatory action;
- introduced explicit specimen/aliquot identity and custody events;
- separated diagnostic procedure from diagnostic result;
- separated evidence stage, diagnostic disposition, and confidence assessment;
- introduced multi-axis confidence rather than a single ranked tier;
- strengthened BFO anchoring and adversarial SHACL validation;
- separated scientific detection from reporting and alert semantics.

## 0.2 lineage

- used an earlier detection model in which confidence-stage concepts were more tightly coupled;
- introduced compatibility terms later deprecated, including `ConfidenceTier` and `PreSymptomatic`.

Exact historical commits remain available in Git history. This changelog summarizes durable architecture changes rather than reproducing obsolete specifications.
