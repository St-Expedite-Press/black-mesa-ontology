---
title: Validation and limitations
subtitle: What automated checks establish and what they leave open
style: mesa
---

## What is checked

The tooling parses Turtle, resolves local imports, lints term metadata, runs an
OWL-RL smoke closure, and validates SHACL shapes. Tests include deliberate
violations for unanchored classes, incomplete detections, tiled imagery,
incomplete confidence, silent tiers, and incomplete crosswalks.

## What is not checked

These checks do not validate biology, sensing accuracy, assay accuracy,
calibration, source authenticity, custody integrity, interoperability,
regulatory compliance, security controls, privacy, deployment readiness, or
whether an alert is appropriate. The external crosswalk entries have not been
authored, so integration fidelity is unresolved.
