# Jurisdictional rule registry

This directory is the versioned regulatory-policy boundary between Black Mesa scientific detections and external action.

The ontology deliberately does **not** encode state law as subclasses of a pathogen or detection. Each rule is a versioned information record with source citations, jurisdiction, authority, review status, effective dates when verified, triggers, required confirmation methods, actions, recipients, deadlines, and movement restrictions when those facts have been reviewed.

## Phase 1 safety policy

Until a jurisdictional record has status `bmo:ApprovedRule`:

- sensor indications remain internal investigation records;
- a sensor indication never triggers external notification by itself;
- suspected diagnostic determinations require qualified human/pathologist review;
- confirmed detections are evaluated against applicable jurisdictional rules;
- regulated or quarantine-pathogen scenarios require regulatory evaluation;
- any external notification requires human approval;
- draft records are decision-support scaffolds only.

The five state files presently included are **DRAFT — requires legal/regulatory review**. They intentionally omit unverified legal triggers, deadlines, and enforcement consequences rather than guessing them.

## Initial jurisdictions

- Arkansas
- Louisiana
- Missouri
- Oklahoma
- Texas

Each state file cites an authoritative state agriculture source used as the starting point for legal/regulatory review.

## Promotion workflow

A draft rule may become operational only after a reviewer has:

1. verified the controlling source and current effective version;
2. identified regulated taxa, commodities, hosts, and geographic scope;
3. verified evidence/diagnostic thresholds;
4. verified notification recipient and deadline;
5. verified movement/quarantine consequences;
6. recorded effective dates;
7. changed `bmo:ruleReviewStatus` to `bmo:ApprovedRule`.

Historical versions are retained and linked using `bmo:supersedesRule`.
