---
title: The Black Mesa Detection Ontology v0.4
subtitle: Persistent identity, licensed publication, initial pathosystems, and regulated-action governance
kicker: BLACK MESA / ONTOLOGY
doc_id: BM-ONT-0.4
status: Implemented schema revision
date: 12 September 2026
---

# Summary

v0.4 turns the v0.3 evidence model into a publishable, deployment-oriented ontology release.

The scientific/evidentiary architecture from v0.3 remains intact. v0.4 adds four missing institutional layers:

1. persistent ontology identifiers;
2. explicit repository licensing;
3. concrete initial crop/pathogen pilot profiles;
4. a versioned jurisdictional rule registry with a mandatory human-review gate for drafts.

# 1. Persistent identifier policy

Canonical identifiers now use the `https://w3id.org/black-mesa/` base.

~~~text
Ontology IRI:
https://w3id.org/black-mesa/bmo

Term namespace:
https://w3id.org/black-mesa/bmo/

Version IRI:
https://w3id.org/black-mesa/bmo/releases/0.4.0

Upper ontology IRI:
https://w3id.org/black-mesa/upper
~~~

The source repository no longer mints Black Mesa ontology terms under `example.org`.

W3ID redirect registration is an external deployment step. Offline ontology validation continues to resolve the upper ontology locally so CI does not depend on the network.

# 2. Licensing

Project-authored semantic content is licensed CC BY 4.0.

This includes:

- RDF/OWL ontology files;
- SHACL constraints;
- crosswalks;
- reference RDF data;
- worked RDF examples;
- ontology diagrams and documentation;
- project-authored regulatory-rule records.

Executable software/tooling is licensed Apache-2.0.

This includes:

- `src/`;
- `tools/`;
- `tests/`;
- `.github/`.

Third-party standards and vendored artifacts retain their own licenses.

# 3. Initial pathosystem profiles

v0.4 does not add crop or pathogen subclasses to the core ontology.

Instead, `reference/pilot-pathosystems.ttl` instantiates four `PilotPathosystem` records using external NCBITaxon IRIs.

| Scenario | Host | Pathogen | Role |
|---|---|---|---|
| RICE-BLAST | Oryza sativa — NCBITaxon:4530 | Pyricularia oryzae — NCBITaxon:318829 | Operational pilot |
| SOY-FROGEYE | Glycine max — NCBITaxon:3847 | Cercospora sojina — NCBITaxon:438356 | Operational pilot |
| WHEAT-STRIPE-RUST | Triticum aestivum — NCBITaxon:4565 | Puccinia striiformis f. sp. tritici — NCBITaxon:168172 | Operational pilot |
| WHEAT-KARNAL-BUNT-REGULATORY | Triticum aestivum — NCBITaxon:4565 | Tilletia indica — NCBITaxon:43049 | Regulatory stress test |

The Karnal bunt profile exists to exercise the evidence-to-regulation branch. It does not state that Karnal bunt is the first sensing model to build.

# 4. Pilot-profile schema

v0.4 adds:

~~~text
PilotPathosystem
PilotScenarioRole
OperationalPilot
RegulatoryStressTest
hostTaxon
pathogenTaxon
scenarioRole
~~~

SHACL requires every pilot profile to identify exactly one host taxon, one pathogen taxon, and one scenario role.

# 5. Jurisdictional rule registry

The initial registry contains one draft intake record for each operating jurisdiction:

~~~text
rules/US-AR/
rules/US-LA/
rules/US-MO/
rules/US-OK/
rules/US-TX/
~~~

Every record identifies:

- stable rule identifier;
- jurisdiction;
- responsible state agriculture authority;
- authoritative source URL;
- review status;
- whether human review is required;
- unresolved legal-review questions.

The initial records deliberately omit unverified legal triggers, notification deadlines, and enforcement consequences.

# 6. Rule governance vocabulary

v0.4 adds:

~~~text
RuleReviewStatus
  DraftRequiresLegalRegulatoryReview
  ApprovedRule
  SupersededRule

RegulatoryActionType
  InternalInvestigationOnly
  PathologistReview
  RegulatoryEvaluation
  ExternalNotification
  MovementRestrictionEvaluation
  QuarantineEvaluation
~~~

A `ReportingRule` can additionally represent:

~~~text
ruleIdentifier
regulatoryAuthority
effectiveFrom
effectiveUntil
regulatedTaxon
regulatedHost
regulatedCommodity
regulatedArea
triggerEvidenceStage
triggerDiagnosticDisposition
requiredConfirmationMethod
requiresHumanReview
requiredAction
notificationRecipient
notificationDeadline
movementRestrictionRequired
supersedesRule
ruleReviewStatus
legalReviewNote
~~~

# 7. Phase 1 external-action policy

Until a state rule has completed review:

~~~text
Sensor indication
    -> internal investigation

Diagnostic hypothesis
    -> internal investigation

Suspected diagnostic determination
    -> qualified human/pathologist review
    -> evaluate applicable jurisdictional rules

Confirmed diagnostic determination
    -> evaluate applicable jurisdictional rules

Potential regulated/quarantine pathogen
    -> regulatory evaluation required

External notification
    -> human approval required
~~~

No draft rule is machine-executable authority.

# 8. SHACL governance constraints

v0.4 adds validation rules requiring every jurisdictional rule to state:

- rule identifier;
- jurisdiction;
- regulatory authority;
- authoritative source;
- review status;
- human-review setting.

A draft rule must:

- require human review;
- include a legal-review note.

An approved rule must:

- include an effective-from date.

The adversarial fixture contains deliberate violations proving these constraints fire.

# 9. Reference-data boundary

The core ontology should not expand every time a new crop, pathogen, or state source is added.

The intended split is:

~~~text
schema/
    reusable evidence and governance concepts

reference/
    specific host/pathogen pilot profiles

rules/
    jurisdiction-specific, versioned regulatory records
~~~

This keeps ontology growth driven by semantic distinctions rather than deployment inventory.

# 10. Migration from v0.3

The principal semantic classes from v0.3 are unchanged.

Migration requirements:

1. replace local Black Mesa IRIs rooted at `https://example.org/bmo/` with `https://w3id.org/black-mesa/bmo/`;
2. replace the upper namespace with `https://w3id.org/black-mesa/upper/`;
3. update import resolution to the canonical upper ontology IRI;
4. preserve existing assertion, specimen, custody, diagnostic, and reporting records;
5. add licensing metadata to ontology publication;
6. move crop/pathogen deployment choices into `PilotPathosystem` reference data;
7. treat jurisdictional rules as versioned records with explicit review status.

# 11. Remaining deployment gates

v0.4 intentionally leaves the following open:

- external registration of the W3ID redirect;
- legal/regulatory review and approval of each state rule record;
- real diagnostic-method profiles for selected assays;
- actual sensor/model descriptions once hardware and models are selected;
- state/pest-specific approved triggers and deadlines;
- environmental and spread modules.

These are now explicit deployment tasks rather than hidden ontology assumptions.
