# RFC 0116: Domain Behaviour and Verification Evidence

- **Status:** draft
- **Author(s):** Juan G. Carmona
- **Created:** 2026-09-24
- **PR:** [#116](https://github.com/product-definition-as-code/spec/pull/116)
- **Class:** change (adds an artifact kind and implementation obligations, and removes an allowed relationship target)
- **Proposed target:** PDaC specification 0.3.0; additive `v1alpha1` evolution except where noted

## Problem

The current [artifact contract](../spec/artifacts.md) defines Domain Terms, Business Rules, Use Cases, Requirements and Structured Behaviours, but no artifact for a concept's business-observable states and legal transitions. A Structured Behaviour can illustrate a rule or use case ([Structured Behaviour](../spec/artifacts.md#structured-behaviour-structured-behaviour-sb-)), but cannot identify the particular lifecycle transition it exercises. Domain knowledge about state, invariants and negative cases therefore stays in prose or external diagrams, outside deterministic graph validation and transition-level traceability.

The [canonical relationship vocabulary](../spec/relationships.md#canonical-vocabulary) permits a Business Rule to target a Use Case through `applies-to`, while `Use Case.governed-by` can record the same rule/use-case pair in the reverse authoring direction. The specification does not clearly distinguish a rule's broad product scope from the specific Use Cases it governs.

Finally, the [Citation Contract](../spec/citation-contract.md#citation-record) can bind test or QA documents to product intent, but PDaC has no standard record for test level, run result, test identity and source revision. A citation establishes which accepted intent a document refers to; it does not record that a test ran or passed.

This RFC adds lifecycle semantics and transition coverage, clarifies rule relationships, and defines a verification-evidence record that links external evidence to accepted Structured Behaviours. It also decides that typed Domain Term associations are not needed for the worked model and are not added here.

## Prior art and terminology

Eric Evans' DDD Reference discusses an Entity's continuity and identity through a lifecycle, and describes an Entity as tracking state and the rules that regulate its lifecycle. It also observes that the causes of state changes may be implicit and separately describes Domain Events as a way to make significant occurrences explicit. Those are related modeling concerns; Evans does not prescribe a Product Artifact named `Domain Lifecycle` or this RFC's schema, nor does this RFC require every transition to be a Domain Event. See [Evans, Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/).

Martin Fowler describes state machines as a general modeling technique for systems whose behavior depends on state and transitions. That is useful background for the explicit state/transition representation proposed here, but it is not a DDD-specific `Domain Lifecycle` artifact. See [Fowler, State Machine](https://martinfowler.com/dslCatalog/stateMachine.html).

Accordingly, `Domain Lifecycle` is PDaC terminology for a proposed product-model artifact, not a claim that Evans or Fowler named or standardized this artifact. The Product Change pilot is a lifecycle of a business concept/process in PDaC; it is not offered as an example of an Entity lifecycle in the narrower tactical DDD sense. The proposal adopts established modeling concerns and chooses a PDaC-specific way to make them linkable, reviewable and verifiable.

## Proposal

### Domain Lifecycle

Add a Product Artifact kind, `domain-lifecycle` with the `LC-` identifier prefix. A Domain Lifecycle defines business-observable states and legal transitions for one Domain Term. It MUST NOT imply an Entity class, Aggregate, database representation, workflow engine, service boundary or source-code module.

In addition to the common artifact fields, a Domain Lifecycle has:

| Field | Presence | Shape | Meaning |
|---|---|---|---|
| `subject` | required | Domain Term ID | Concept whose lifecycle is defined |
| `states` | required | non-empty ordered list of closed State records | Business-observable states |
| `transitions` | required | ordered list of closed Transition records; MAY be empty | Legal state changes |
| `uses-terms` | optional | Domain Term IDs | Additional terms needed to interpret the lifecycle |

A State record has `id` (local identifier matching `[A-Z0-9]+(-[A-Z0-9]+)*`), `title`, optional `initial` (default `false`) and optional `terminal` (default `false`). A Transition record has `id` (local identifier in a separate namespace), `title`, non-empty `from` (local State IDs), `to` (one local State ID), `trigger` (non-empty product-level stimulus), and optional `initiated-by` (Actor IDs), `governed-by` (Business Rule IDs) and `realized-by` (Use Case IDs).

Exactly one State MUST declare `initial: true`. A Lifecycle MAY have zero transitions to support a documented single-state concept or an incomplete model. A terminal State MUST NOT occur in any Transition's `from` list. A Transition MAY list multiple source states only when its trigger, outcome and product meaning are equivalent for every listed source state; otherwise the author MUST define separate Transitions. This equivalence is reviewed by people and MUST NOT be claimed as a deterministic validation result. State and Transition IDs are local to their Lifecycle, are not Product Artifact IDs and MUST NOT be independently cited.

A single State MAY be both initial and terminal to represent a single-state lifecycle. Multiple business entry paths MUST be represented by transitions from the initial State rather than by multiple initial States.

The body MUST contain, in order, `## Purpose`, `## Invariants`, `## State Semantics`, `## Transition Semantics` and `## Boundaries`. The body MUST NOT restate the complete state or transition tables; implementations MAY render derived tables or diagrams.

### Worked lifecycle: Product Change

The Product Change lifecycle in [Product Changes](../spec/product-changes.md#lifecycle) is the reference exercise for this RFC. It provides a real lifecycle in the specification and the self-hosted product model. The following is a domain-level projection of that lifecycle; filesystem moves, Git operations and merge acceptance remain governed by the Product Change and repository contracts.

The subject is a proposed Domain Term, `TERM-PRODUCT-CHANGE`, defined in the Product Definition Bounded Context. The lifecycle has these states:

| State | Initial | Terminal | Meaning |
|---|---:|---:|---|
| `DRAFT` | yes | no | Change intent being elaborated |
| `PROPOSED` | no | no | Change ready for human product review |
| `APPROVED` | no | no | Human has decided the proposal is correct and wanted |
| `APPLIED` | no | yes | Approved change materialized and archived; resulting baseline is not yet accepted by this state alone |
| `REJECTED` | no | yes | Human declined a draft or proposed change |
| `SUPERSEDED` | no | yes | Change withdrawn in favour of another direction |

The lifecycle defines `SUBMIT` (`DRAFT` to `PROPOSED`), `APPROVE` (`PROPOSED` to `APPROVED`), `APPLY` (`APPROVED` to `APPLIED`), `REJECT` (`DRAFT` or `PROPOSED` to `REJECTED`) and `SUPERSEDE` (any non-terminal state to `SUPERSEDED`). Editing a change while its status is `draft` or `proposed` is elaboration within that state, not a status transition. The explicit status chain does not allow reverse transitions.

The exercise identifies these invariants:

1. Only a human product decision can move a change to `APPROVED`.
2. Only an `APPROVED` change can be applied.
3. Apply does not accept the resulting Product Definition; human merge is a separate acceptance event.
4. `APPLIED`, `REJECTED` and `SUPERSEDED` are terminal lifecycle states.
5. A refused apply caused by an unapproved status or baseline drift leaves the change and working tree unchanged.

The first four are lifecycle or Business Rule semantics. The fifth is a rejected operation with no state transition and is represented by a Structured Behaviour that illustrates `UC-CHANGE-001` and `BR-CHANGE-001` without claiming to cover a transition.

The following complete artifact pair makes the proposal reviewable end to end. Both are proposed examples only; this RFC does not add them to ProductShape's accepted self-model.

```markdown
---
id: TERM-PRODUCT-CHANGE
type: domain-term
title: Product Change
status: draft
defined-in: BC-PRODUCT-DEFINITION
synonyms: []
---

## Definition

A reviewed proposal for a semantic change to the accepted Product Definition, carried through elaboration, human approval and explicit application before a human merge accepts the resulting baseline.

## Distinguish From

- **A pull request.** A pull request is a review mechanism; a Product Change records the semantic intent and proposed artifact operations.
- **An implementation change.** A Product Change describes accepted product meaning, whether or not any implementation work has begun.

## Usage

A Product Change is validated as an overlay against an accepted baseline. Human approval authorizes apply; apply does not itself accept the resulting Product Definition.
```

```markdown
---
id: LC-PRODUCT-CHANGE
type: domain-lifecycle
title: Product Change lifecycle
status: draft
subject: TERM-PRODUCT-CHANGE
states:
  - id: DRAFT
    title: Draft
    initial: true
  - id: PROPOSED
    title: Proposed
  - id: APPROVED
    title: Approved
  - id: APPLIED
    title: Applied
    terminal: true
  - id: REJECTED
    title: Rejected
    terminal: true
  - id: SUPERSEDED
    title: Superseded
    terminal: true
transitions:
  - id: SUBMIT
    title: Submit for review
    from: [DRAFT]
    to: PROPOSED
    trigger: The author declares the change ready for human review
    initiated-by: [ACT-PRODUCT-ENGINEER]
    governed-by: [BR-CHANGE-001]
    realized-by: [UC-CHANGE-001]
  - id: APPROVE
    title: Approve the proposal
    from: [PROPOSED]
    to: APPROVED
    trigger: A human approves the proposed product decision
    initiated-by: [ACT-PRODUCT-ENGINEER]
    governed-by: [BR-CHANGE-001]
    realized-by: [UC-CHANGE-001]
  - id: APPLY
    title: Apply the approved proposal
    from: [APPROVED]
    to: APPLIED
    trigger: The actor explicitly applies the change against a compatible baseline
    initiated-by: [ACT-PRODUCT-ENGINEER]
    governed-by: [BR-CHANGE-001]
    realized-by: [UC-CHANGE-001]
  - id: REJECT
    title: Reject the proposal
    from: [DRAFT, PROPOSED]
    to: REJECTED
    trigger: A human decides not to pursue the change
    initiated-by: [ACT-PRODUCT-ENGINEER]
    governed-by: [BR-CHANGE-001]
    realized-by: [UC-CHANGE-001]
  - id: SUPERSEDE
    title: Supersede the proposal
    from: [DRAFT, PROPOSED, APPROVED]
    to: SUPERSEDED
    trigger: The actor withdraws the change in favour of another direction
    initiated-by: [ACT-PRODUCT-ENGINEER]
    governed-by: [BR-CHANGE-001]
    realized-by: [UC-CHANGE-001]
---

## Purpose

Make the product-visible progress of one proposed semantic change explicit, from elaboration through apply or withdrawal.

## Invariants

Only a human product decision can approve a change. Only an approved change can be applied. Apply does not mean the resulting baseline has been accepted. Applied, rejected and superseded changes cannot transition again.

## State Semantics

`draft` and `proposed` changes may be edited during elaboration without changing lifecycle state. Approval is a human decision. `applied` means the proposal has been materialized and archived; acceptance occurs only when a human merges the resulting baseline.

## Transition Semantics

`apply` requires an approved change and a compatible baseline. If either condition fails, the operation is refused and the lifecycle state and working tree remain unchanged. Rejection is available from draft or proposed. Superseding is available from any non-terminal state.

## Boundaries

This lifecycle does not model Git branches, pull-request review, filesystem layout, test execution, implementation, release or deployment. Human merge acceptance is a separate repository event.
```

An accepted transition example MAY use this form once `covers-transition` below is implemented:

```yaml
id: SB-CHANGE-APPLY-APPROVED
type: structured-behaviour
title: Apply an approved Product Change
status: active
illustrates:
  - UC-CHANGE-001
  - BR-CHANGE-001
given:
  - The Product Change has status APPROVED
  - Its base revision is compatible with the current baseline
when: The actor applies the Product Change
then:
  - The proposed operations are materialized on the working branch
  - The Product Change is archived with status APPLIED
  - The resulting Product Definition is not accepted until a human merges it
covers-transition:
  lifecycle: LC-PRODUCT-CHANGE
  transition: APPLY
```

A refused-operation example remains an ordinary Structured Behaviour with no `covers-transition`:

```yaml
id: SB-CHANGE-APPLY-UNAPPROVED
type: structured-behaviour
title: Refuse to apply a Product Change that is not approved
status: active
illustrates:
  - UC-CHANGE-001
  - BR-CHANGE-001
given:
  - The Product Change has status PROPOSED
when: The actor attempts to apply the Product Change
then:
  - The apply operation is refused
  - The Product Change remains PROPOSED
  - The working tree remains unchanged
```

### Transition coverage relationship

Structured Behaviour gains an optional `covers-transition` closed object containing `lifecycle` (Domain Lifecycle ID) and `transition` (local Transition ID declared by that Lifecycle). The `lifecycle` member is a canonical Product Graph relationship. The `transition` member is resolved within that Lifecycle and is not a separate graph node or edge.

`covers-transition` MUST NOT replace the Structured Behaviour's required `illustrates` relationship. A transition example still identifies the Use Case, Business Rule or Constraint it makes concrete. A refused operation that leaves the state unchanged MUST NOT claim transition coverage.

### Canonical relationships

Add these canonical relationships, with the existing relationship-polarity rules:

| Source | Field | Allowed target | Polarity |
|---|---|---|---|
| Domain Lifecycle | `subject` | Domain Term | dependency |
| Domain Lifecycle | `uses-terms` | Domain Term | dependency |
| Domain Lifecycle | `transitions[].initiated-by` | Actor | dependency |
| Domain Lifecycle | `transitions[].governed-by` | Business Rule | dependency |
| Domain Lifecycle | `transitions[].realized-by` | Use Case | dependency |
| Structured Behaviour | `covers-transition.lifecycle` | Domain Lifecycle | dependency |
| Functional Requirement | `derived-from` | Domain Lifecycle, in addition to current targets | dependency |
| Quality Requirement | `applies-to` | Domain Lifecycle, in addition to current targets | governance |
| Constraint | `applies-to` | Domain Lifecycle, in addition to current targets | governance |

Extend the existing knowledge-warning relationship sets alongside these new edges. For `PRODUCT105`, a non-retired Business Rule is consumed if and only if it has at least one valid outgoing `applies-to` relationship, an incoming `Use Case.governed-by`, `Functional Requirement.derived-from` or `Domain Lifecycle.transitions[].governed-by` relationship authored by a non-retired artifact. An incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer.

For `PRODUCT106`, a non-retired Domain Term is used if and only if it has at least one valid incoming `Domain Lifecycle.subject` or `uses-terms` relationship authored by a non-retired artifact. The `uses-terms` author set MUST include Domain Lifecycle in addition to the existing artifact kinds. Prose occurrences, generated reverse relationships and other relationship paths do not count.

Reverse views MUST be derived and MUST NOT be authored. A Lifecycle Transition's local `from` and `to` references are validated within the containing Lifecycle. Its relationship fields are attributed as `transitions[].initiated-by`, `transitions[].governed-by` and `transitions[].realized-by`. `covers-transition.lifecycle` diagnostics use that exact field path; an invalid local transition is attributed to `covers-transition.transition`.

### Business Rule scope and Use Case governance

Give these relationships separate meanings:

- `Business Rule.applies-to` states the broad product scope in which the rule applies: Journey or Bounded Context. It does not stand for a Use Case-specific relationship.
- `Use Case.governed-by` states that the specific Use Case is governed by the Business Rule.

Remove Use Case from the allowed target set of `Business Rule.applies-to`. Authors MUST use `Use Case.governed-by` to associate a rule with a Use Case. The edge remains authored once, from Use Case to Business Rule; reverse “governed use cases” views are derived.

An absent `Business Rule.applies-to` means that no broad scope is declared in that field; it MUST NOT be interpreted as “applies to the entire product.” A rule can still govern one or more Use Cases through their `governed-by` fields.

Changing a Business Rule puts its citing Use Cases in question under dependency polarity and its declared Journey/Bounded Context scope in question under governance polarity. A Use Case change does not automatically put the Business Rule in question under dependency polarity. Structural impact remains a review signal, not a semantic judgment.

The `PRODUCT105` definition is extended as stated under [Canonical relationships](#canonical-relationships): a Lifecycle Transition governed by a rule is a consumer. An incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer.

This change removes an existing allowed edge and requires migration: every current `Business Rule.applies-to` entry targeting a Use Case MUST be moved to that Use Case's `governed-by` list. If the Business Rule also has a broader scope, its Journey or Bounded Context target remains in `applies-to`.

For example, a rule that applies throughout the Product Definition context and governs the change use case is authored as:

```yaml
# br-change-001.md
applies-to:
  - BC-PRODUCT-DEFINITION

# uc-change-001.md
bounded-context: BC-PRODUCT-DEFINITION
governed-by:
  - BR-CHANGE-001
```

The first relationship declares scope; the second declares specific use. `Business Rule.applies-to: UC-CHANGE-001` is invalid under this proposal. A Lifecycle Transition that is constrained by `BR-CHANGE-001` separately names that rule in its local `governed-by` field; this does not create another Use Case relationship.

### Domain Term associations and DDD pattern kinds

This RFC adds no generic typed association field to Domain Term. The Product Change lifecycle can be expressed using the existing `defined-in` and `uses-terms` relationships plus the Lifecycle's explicit links to rules, use cases and actors. The exercise reveals no product association, cardinality or ownership fact that would change a decision and cannot already be expressed. A future RFC may add a narrowly typed association after such a real case is demonstrated.

This RFC also adds no `Entity`, `Value Object`, `Aggregate`, `Command` or `Repository` artifact kind and no required DDD classification on Domain Terms. Domain Terms MAY define identity or value semantics in their prose; Business Rules and Domain Lifecycles state the resulting invariants and behavior. These DDD concepts can be valuable design vocabulary, but the pilot does not demonstrate a product-definition need for each to have independent artifact identity, relationships and citations. Commands remain product-level triggers or stimuli in Use Cases and Lifecycle Transitions unless a future case demonstrates such a need.

This RFC adds no `Domain Event` kind. A future Domain Event RFC is warranted when a real, immutable business fact has an independent consumer or citation need across Bounded Contexts and the event's stable identity improves traceability beyond a Structured Behaviour outcome. Such an artifact MUST describe the fact's product meaning; serialization, delivery, ordering, retries, storage and event sourcing remain outside its contract.

### Verification evidence

Verification evidence remains outside the Product Definition and Product Graph. A test or QA consumer MUST cite the accepted Structured Behaviour it verifies, using the existing citation record (`id`, whole-artifact `digest`, optional supported `anchor`). If the Structured Behaviour has `covers-transition`, that relationship identifies the transition exercised. Evidence MAY instead cite a Requirement with an existing supported anchor when it verifies an obligation rather than an independently identified behavior.

Add a canonical JSON verification-evidence document for integrations that claim PDaC verification traceability. A document MUST validate against `schemas/v1alpha1/verification-evidence.schema.json`, reject unknown properties, and contain:

| Field | Meaning |
|---|---|
| `format` | Required constant `pdac-verification-evidence/v1alpha1` |
| `provider` | Required non-empty provider identity string |
| `run-id` | Required non-empty provider-native stable run identifier or URL |
| `revision` | Required full Git commit SHA (40 or 64 lowercase hexadecimal characters) against which evidence was produced |
| `results` | Required non-empty list of result records |

Each result record is a closed object with required `test-id` (non-empty provider-native stable test/evidence identifier), `level` (one of `domain`, `component`, `integration`, `end-to-end`, `manual`, `exploratory`), `outcome` (one of `passed`, `failed`, `inconclusive`) and `citations` (non-empty list of standard PDaC citation records). A citation MUST target a Structured Behaviour, Functional Requirement or Quality Requirement. A citation to a Structured Behaviour MUST NOT carry an anchor. A citation to a Functional or Quality Requirement MAY use an anchor supported by the existing Citation Contract. Duplicate test IDs within one document MUST be rejected.

Example:

```json
{
  "format": "pdac-verification-evidence/v1alpha1",
  "provider": "example-test-runner",
  "run-id": "run-1042",
  "revision": "0123456789abcdef0123456789abcdef01234567",
  "results": [
    {
      "test-id": "change-apply-approved",
      "level": "domain",
      "outcome": "passed",
      "citations": [
        {
          "id": "SB-CHANGE-APPLY-APPROVED",
          "digest": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        }
      ]
    }
  ]
}
```

An implementation MAY emit this document in CI output or a provider-owned sidecar. This RFC fixes the document shape but does not prescribe test provider APIs, result retention, execution commands or a repository path. An adapter claiming support MUST report the exact run revision and citation status; it MUST NOT silently refresh a digest after the cited Product Artifact changes. Implementations MUST apply the existing citation digest, resolution and staleness rules to each evidence citation.

An implementation MAY derive a coverage view joining Business Rules, Lifecycle Transitions, Structured Behaviours and evidence records. It MUST display test level separately from outcome. Missing evidence at a particular level is not a validation error by default; a repository MAY set risk-based policy for selected behaviors. The existence of a passing evidence record MUST NOT be represented as proof that the product is correct or that the cited behavior is completely covered.

### Validation

The common relationship contract MUST resolve and type-check `subject`, `uses-terms`, Transition relationship fields and `covers-transition.lifecycle`. Lifecycle validation MUST report errors for duplicate local State IDs or duplicate local Transition IDs within their respective namespaces; unknown local State references in `from` or `to`; anything other than exactly one initial State; a terminal State used in `from`; and an unresolved `covers-transition.transition`. The Lifecycle body MUST contain the required sections in the stated order; conformance tests MUST cover missing and out-of-order sections.

Lifecycle validation SHOULD report a warning for a non-initial State unreachable from the initial State and an active Transition with no Structured Behaviour covering it. Both remain warnings so partial models can be authored. Transition coverage is per Transition; when a Transition has multiple source states, authors are responsible for the required equivalence stated above.

No new diagnostic codes are reserved here; the RFC implementation PR MUST allocate available codes and add portable conformance cases. Implementations MUST use stable local-ID field paths rather than array indexes for local State/Transition diagnostics.

### Worked-model DDD decisions

The Product Change pilot does not require Entity/Value Object classification or typed associations. It does require lifecycle states, transitions, rule constraints, examples of valid and refused operations, and transition-specific citations. This RFC therefore decides not to add Entity, Value Object or Aggregate artifacts as a bundle. It leaves Domain Event as a conditional future artifact, subject to the cross-context evidence threshold above.

## Impact

- **On existing conformant repositories:** adding Domain Lifecycle and `covers-transition` is optional and additive. Removing Use Case from `Business Rule.applies-to` is a normative breaking change to the current relationship target set; repositories using that edge MUST migrate it to `Use Case.governed-by` before claiming conformance to the RFC's target version. Existing repositories that do not use that edge require no relationship migration.
- **On existing implementations:** implementations must add a Lifecycle parser/schema, graph links, validation, impact handling and Structured Behaviour transition coverage. Implementations claiming verification-evidence traceability must implement the evidence record contract. Existing implementations that do not claim the optional evidence integration need not execute or store tests.
- **On the conformance tests:** add valid Lifecycle and transition-coverage cases; common relationship resolution and target-type cases for Lifecycle fields; unknown/duplicate local State and Transition cases; missing/multiple initial State cases; terminal-source cases; required body-section/order cases; unreachable-state and uncovered-transition warnings; migration coverage for `Business Rule.applies-to` Use Case removal; `PRODUCT105` cases proving a rule referenced only by a Lifecycle Transition is consumed; `PRODUCT106` cases proving a term referenced as a Lifecycle subject or through `uses-terms` is used; and verification-evidence cases for schema closure, citation target kinds, test levels, outcomes, full revision format, duplicate test IDs and stale targets.
- **On ProductShape's self-model:** a candidate `TERM-PRODUCT-CHANGE`, `LC-PRODUCT-CHANGE` and the two Structured Behaviours above exercise the contract. Adding them to ProductShape's accepted model requires its own Product Change and is outside this specification RFC.

## Alternatives considered

### Keep lifecycle states and transitions in prose or diagrams

Rejected for the pilot. Prose can explain a lifecycle but cannot give each transition a stable relationship target for validation, impact analysis and test traceability. Diagrams remain useful derived views, not the canonical lifecycle.

### Add generic Domain Term associations now

Rejected because the worked model does not expose a missing domain relationship that changes a product decision. A generic association object would require unsettled rules for role naming, cardinality, inverse links and ownership.

### Keep both `Business Rule.applies-to: UC-*` and `Use Case.governed-by`

Rejected because both can record the same rule/use-case pair and their distinction is not stable enough to justify duplicate authorship. Broad scope belongs on the rule; use-case-specific governance belongs on the Use Case.

### Store test outcomes on Structured Behaviour

Rejected because Structured Behaviour is accepted product intent whose digest should not change when a test run changes. Run outcomes are revision-specific evidence owned by delivery providers.

### Add all DDD patterns as artifact kinds

Rejected because the patterns answer different questions. Entity/Value Object distinctions may inform Domain Term identity semantics; Aggregates and Repositories primarily guide design; Commands may be represented as triggers; Domain Events may warrant independent artifacts when business facts cross contexts. They do not share one schema or one justification.

### Prescribe an end-to-end test ratio or a rhomboid portfolio

Rejected. PDaC records evidence level and outcome, while product risk and test portfolio shape remain repository policy. A fixed geometry would confuse a heuristic with a product contract.
