# ADR-0003: BFO-aligned upper ontology

Status: Accepted  
Date: 2026-09-13

## Context

Domain terms can silently mix physical material, processes, sites, information artifacts, qualities, and roles. The surrounding OBO ecosystem is BFO-aligned.

## Decision

Every local ontology class must reach BFO through the shared upper module. Offline validation loads the vendored BFO hierarchy and verifies that direct BFO anchor targets are real declared classes.

## Consequences

New classes require an explicit category decision. The vendored BFO copy is part of the validation contract rather than unused reference material.

## Alternatives rejected

Prefix-only anchoring and an unconstrained local top-level hierarchy.

## Revisit if

The project adopts a different upper-ontology strategy with equivalent category discipline and migration guidance.
