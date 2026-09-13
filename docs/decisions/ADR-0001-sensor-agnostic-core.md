# ADR-0001: Sensor-agnostic core

Status: Accepted  
Date: 2026-09-13

## Context

Expected early deployments include drones and spectral imagery, but coupling the ontology to flight or one modality would make evidence semantics depend on hardware.

## Decision

`SurveyActivity` is the general surveillance process. `Flight` is only a subtype. `ObservedAnomaly` is general; `SpectralAnomaly` is only a subtype. Sensors/platforms use SOSA/SSN-aligned identities.

## Consequences

Fixed stations, robots, aircraft, thermal systems, satellite products, or other observation systems can enter without redesigning the evidence chain.

## Alternatives rejected

A drone-first ontology with `Flight` as the root surveillance concept and a local sensor taxonomy.

## Revisit if

A future operational distinction cannot be represented through survey/observation semantics plus external sensor/platform vocabularies.
