---
title: Assertions and confidence
subtitle: Detection claims and non-numeric uncertainty
style: mesa
---

## Detection is an assertion

A detection is an information artifact derived from an assay result and tied
to a zone, custody chain, and rule-set version. This makes a conclusion
reviewable without retroactively rewriting it when rules change.

## Confidence

The local tiers are Confirmed, Suspected, Pre-symptomatic indication, Not
detected, and Undetermined. Their ranks are ordinal labels, not probabilities.
The pre-symptomatic tier is a hypothesis that licenses sampling, not a presence
claim. A confidence assessment can record calibrated probability, evidence
strength and completeness, assay applicability, and provenance quality; SHACL
requires a tier and assay applicability, but does not establish calibration.
