# ADR-0002: Separate evidence stages

Status: Accepted  
Date: 2026-09-13

## Context

A single “detected/confidence” field erases how knowledge was produced and encourages sensor anomalies to be mistaken for diagnoses.

## Decision

Observation, anomaly, sensor indication, diagnostic hypothesis, diagnostic result, scientific detection, regulatory determination, reporting decision, and alert remain distinct objects.

Evidence stage, diagnostic disposition, and confidence assessment remain independent dimensions.

## Consequences

The graph preserves investigation history and can state what evidence warrants at each stage. More objects are required, but their meanings remain auditable.

## Alternatives rejected

A ranked confidence tier in which pre-symptomatic, suspected, confirmed, and not-detected states occupy one scale.

## Revisit if

A proposed simplification can preserve all current competency questions and safety boundaries without semantic loss.
