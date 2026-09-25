# RFC 0116: Domain Behaviour and Verification Evidence

- **Status:** accepted
- **Accepted:** 2026-09-25 by Juan G. Carmona
- **Author(s):** Juan G. Carmona
- **Created:** 2026-09-24
- **PR:** [#116](https://github.com/product-definition-as-code/spec/pull/116)
- **Class:** change (adds an artifact kind and implementation obligations, and removes an allowed relationship target)
- **Revised:** 2026-09-25, coordinated v0.3.0 release
- **Proposed target:** PDaC specification 0.3.0, serialization `v1alpha2`
- **Sequence:** this RFC precedes [RFC 0082](https://github.com/product-definition-as-code/spec/pull/82), which precedes [RFC 0115](https://github.com/product-definition-as-code/spec/pull/115). All three target v0.3.0; neither later RFC is a prerequisite for accepting this vocabulary.

## Review in brief

This proposal asks for four decisions:

1. Add an optional Domain Lifecycle artifact. States and transitions live inside it; they do not become independently versioned graph nodes or citation targets.
2. Author rule/use-case governance once, on `Use Case.governed-by`. Keep Business Rule `applies-to` for Journey/Bounded Context scope. This breaks an existing allowed relationship and therefore requires `v1alpha2` and an explicit migration.
3. Keep Verification Evidence optional and external: record what an external provider claims it verified, against which revision and citations. PDaC does not run tests, manage them, mandate coverage or gate apply on their results.
4. Give #82 a stable artifact-level graph vocabulary. The later RFC owns cause deduplication and the one-hop apply gate; #115 owns the downstream citation forecast.

The worked Product Change lifecycle below exercises a successful transition and a refused operation. The [implementation checklist](#implementation-checklist) makes the follow-up scope explicit. This RFC records the accepted design; the schemas, diagnostics and fixtures remain follow-up implementation work.

## Decision record

Accepted for v0.3.0 by the founding maintainer, Juan G. Carmona, on 2026-09-25: explicit domain lifecycles and a single rule/use-case relationship give impact accounting a stable graph. Verification Evidence remains optional external traceability. The breaking relationship change uses v1alpha2 with migration, preserving v1alpha1.

The maintainer explicitly authorized recording this rationale and merging RFC #116. No substantive review feedback was outstanding at the decision. The repository's published MATURITY and ADOPTERS records show neither an independent implementation/clean-room validator nor an adopter other than the reference implementation, so CONTRIBUTING's conditional minimum elapsed comment window is not yet a merge condition. Publication, an explicit decision and rationale, and resolution of substantive feedback remain required and are recorded here.

Acceptance authorizes the specification implementation in a follow-up PR; it does not implement or release v0.3.0. RFC #82 and RFC #115 remain separate decisions.

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

A State record has `id` (local identifier matching `^[A-Z0-9]+(-[A-Z0-9]+)*$`), non-empty `title`, optional boolean `initial` (default `false`) and optional boolean `terminal` (default `false`). A Transition record has `id` (the same local identifier pattern in a separate namespace), non-empty `title`, non-empty `from` (local State IDs), `to` (one local State ID), `trigger` (non-empty product-level stimulus), and optional `initiated-by` (Actor IDs), `governed-by` (Business Rule IDs) and `realized-by` (Use Case IDs).

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
5. A refused apply leaves the change and working tree unchanged, including refusal for an unapproved status or baseline drift. RFC 0082 will add unresolved model impact as another precondition without changing this lifecycle.

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

`apply` requires approval and all preconditions in the Product Change apply contract. If a precondition fails, the operation is refused and the lifecycle state and working tree remain unchanged. Rejection is available from draft or proposed. Superseding is available from any non-terminal state.

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
  - Its overlay satisfies the Product Change apply preconditions
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

A Domain Lifecycle is an ordinary whole-artifact citation target. Its local State and Transition IDs MUST NOT resolve as citation anchors. Evidence of a particular transition cites its covering Structured Behaviour. Editing any part of the Lifecycle changes its whole-artifact digest under the existing normalization; this RFC defines no local-record digest.

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

The containing Domain Lifecycle is the source artifact of every Transition relationship. Local records have no separate artifact status; the Lifecycle's status determines the ordinary relationship status checks. All these canonical edges participate in the existing undirected actor-reachability rule. Derived reverse views and local `from`/`to` selectors add no Product Graph edges.

Preserve every authored relationship occurrence for the existing per-entry diagnostics. For impact accounting, [RFC 0082](https://github.com/product-definition-as-code/spec/pull/82) will define the set projection and cause identity. Repeated references from several transitions do not introduce independently acknowledged transition nodes. Distinct canonical fields remain distinct relationships: `subject` and `uses-terms` may both target the same term without being synonyms.

Extend the existing knowledge-warning relationship sets alongside these new edges. For `PRODUCT105`, a non-retired Business Rule is consumed if and only if it has at least one valid outgoing `applies-to` relationship, an incoming `Use Case.governed-by`, `Functional Requirement.derived-from` or `Domain Lifecycle.transitions[].governed-by` relationship authored by a non-retired artifact. An incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer.

For `PRODUCT106`, a non-retired Domain Term is used if and only if it has at least one valid incoming `Domain Lifecycle.subject` or `uses-terms` relationship authored by a non-retired artifact. The `uses-terms` author set MUST include Domain Lifecycle in addition to the existing artifact kinds. Prose occurrences, generated reverse relationships and other relationship paths do not count.

Reverse views MUST be derived and MUST NOT be authored. A Lifecycle Transition's local `from` and `to` references are validated within the containing Lifecycle. Its relationship fields are attributed as `transitions[].initiated-by`, `transitions[].governed-by` and `transitions[].realized-by`. `covers-transition.lifecycle` diagnostics use that exact field path; an invalid local transition is attributed to `covers-transition.transition`.

### Business Rule scope and Use Case governance

Give these relationships separate meanings:

- `Business Rule.applies-to` states the broad product scope in which the rule applies: Journey or Bounded Context. It does not stand for a Use Case-specific relationship.
- `Use Case.governed-by` states that the specific Use Case is governed by the Business Rule.

Remove Use Case from the allowed target set of `Business Rule.applies-to`. Authors MUST use `Use Case.governed-by` to associate a rule with a Use Case. The edge remains authored once, from Use Case to Business Rule; reverse “governed use cases” views are derived.

An absent or empty `Business Rule.applies-to` means that no broad scope is declared in that field; it MUST NOT be interpreted as “applies to the entire product.” A rule can still govern one or more Use Cases through their `governed-by` fields. The implicit product scope of a Constraint with absent `applies-to` remains specific to Constraints; it is not a general default for this field name.

Changing a Business Rule puts its citing Use Cases in question under dependency polarity and its declared Journey/Bounded Context scope in question under governance polarity. A Use Case change does not automatically put the Business Rule in question under dependency polarity. Structural impact remains a review signal, not a semantic judgment.

This change removes an existing allowed edge and requires migration: every current `Business Rule.applies-to` entry targeting a Use Case MUST be moved to that Use Case's `governed-by` list. If the Business Rule also has a broader scope, its Journey or Bounded Context target remains in `applies-to`.

Migration MUST preserve an existing matching `governed-by` entry rather than duplicate it, and MUST NOT infer a broad scope from the Use Case's context. Remove `applies-to` when no broad targets remain. Missing or invalid targets require repair, not silent deletion or invented artifacts. Review the accepted model and each active proposal; explicitly rebase active changes after baseline migration. Archived changes and historical evidence remain untouched. Changed artifact digests can stale consumer citations; migration MUST NOT automatically refresh them. This is a behavioral change: a Use Case edit no longer questions its rule through the removed governance edge.

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

Verification evidence remains outside the Product Definition and Product Graph. An integration claiming this optional evidence contract MUST cite the accepted Structured Behaviour it verifies, using the existing citation record (`id`, whole-artifact `digest`, optional supported `anchor`). If the Structured Behaviour has `covers-transition`, that relationship identifies the transition exercised. Evidence MAY instead cite a Functional or Quality Requirement with an existing supported anchor when it verifies an obligation rather than an independently identified behavior. No evidence integration, test execution or evidence storage is required for core PDaC conformance.

Add a standard JSON verification-evidence document for integrations that claim PDaC verification traceability. It is external evidence, never canonical product intent. A document MUST validate against `schemas/v1alpha2/verification-evidence.schema.json`, reject unknown properties, and contain:

| Field | Meaning |
|---|---|
| `format` | Required constant `pdac-verification-evidence/v1alpha1` |
| `provider` | Required non-blank provider identity string |
| `run-id` | Required non-blank provider-native stable run identifier or URL |
| `revision` | Required full Git commit SHA (40 or 64 lowercase hexadecimal characters) against which evidence was produced |
| `results` | Required non-empty list of result records |

Each result record is a closed object with required `test-id` (non-blank provider-native stable test/evidence identifier), `level` (one of `domain`, `component`, `integration`, `end-to-end`, `manual`, `exploratory`), `outcome` (one of `passed`, `failed`, `inconclusive`) and `citations` (non-empty list of standard PDaC citation records). A citation MUST target a Structured Behaviour, Functional Requirement or Quality Requirement. A citation to a Structured Behaviour MUST NOT carry an anchor. A citation to a Functional or Quality Requirement MAY use an anchor supported by the existing Citation Contract. Duplicate test IDs within one document MUST be rejected; the same provider test ID in another run document is permitted.

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

The run revision identifies the source revision of the external verification; it does not redefine the digest domain or prove that a run occurred. Citation status is evaluated against the explicitly selected model revision, which the adapter MUST report separately from the run revision. Historical comparison MAY select that revision; current verification selects the current model. A passing result with a stale citation remains `passed` evidence with a `stale` citation, not evidence of successful verification of the changed intent. PDaC neither authenticates a provider's claim nor executes it.

An evidence adapter MUST document how evidence documents are selected. This contract does not add a general citation carrier or require a duplicate `.citations.yml` ledger. The adapter reads each embedded citation once, attributes it to the evidence file and a one-based `entry` ordinal flattened in result/citation order, and records its result identity. Immutable historical runs are not current consumers. If an adapter includes explicitly current evidence in the live population, it MUST use the same population for current citation verification and any apply forecast; [RFC 0115](https://github.com/product-definition-as-code/spec/pull/115) will make that forecast mandatory. Arbitrary JSON documents MUST NOT be treated as evidence merely because they contain an `id` or `digest`.

This requires a narrow extension to [Validation's diagnostic model](../spec/validation.md#diagnostics): `entry` is permitted for an explicitly selected evidence document as well as a citation sidecar, and `field` may identify an evidence-document field. Evidence `entry` counts all citation records in document order, including those in a result later rejected for a duplicate test ID; suppression does not renumber later entries. Existing payload and sidecar attribution is unchanged. No new diagnostic attribute is introduced.

This contract introduces no test scheduling, suites, retries, test-management state, execution command, mandatory evidence coverage or apply gate. The evidence format identifier versions this first external envelope independently of the model serialization directory.

An implementation MAY derive a coverage view joining Business Rules, Lifecycle Transitions, Structured Behaviours and evidence records. It MUST display test level separately from outcome. Missing evidence at a particular level is not a validation error by default; a repository MAY set risk-based policy for selected behaviors. The existence of a passing evidence record MUST NOT be represented as proof that the product is correct or that the cited behavior is completely covered.

### Validation

The common relationship contract MUST resolve and type-check `subject`, `uses-terms`, Transition relationship fields and `covers-transition.lifecycle`. Lifecycle validation MUST report errors for duplicate local State IDs or duplicate local Transition IDs within their respective namespaces; unknown local State references in `from` or `to`; anything other than exactly one initial State; a terminal State used in `from`; and an unresolved `covers-transition.transition`. The Lifecycle body MUST contain the required sections in the stated order; conformance tests MUST cover missing and out-of-order sections.

Lifecycle validation MUST report a warning for each non-initial State of an active Lifecycle unreachable from its initial State and each Transition of an active Lifecycle with no active Structured Behaviour whose coverage pair resolves to it. There is no separate Transition status. Reachability follows directed local `from` to `to` links. Both remain warnings so partial models can be authored. Transition coverage is per Transition; when a Transition has multiple source states, authors are responsible for the required equivalence stated above. Retired or draft Lifecycles are outside these warning populations.

Allocate PRODUCT010 (duplicate local ID), PRODUCT011 (unknown local state), PRODUCT012 (initial-state cardinality), PRODUCT013 (terminal source), PRODUCT014 (unknown local coverage transition), PRODUCT112 (unreachable state) and PRODUCT113 (uncovered transition). Exact units and fields are in the diagnostic table below. A missing or wrong-type Lifecycle target receives the ordinary relationship diagnostic, not an additional PRODUCT014. Checks requiring unique IDs, valid local references or one initial state MUST NOT run when their prerequisites are invalid. Independent structural diagnostics remain reportable.

| Code | Unit | Required attribution beyond file |
| --- | --- | --- |
| PRODUCT010 | repeated local ID, once per repeated key in each namespace | artifact=LC, field=`states[ID].id` or `transitions[ID].id`, target=ID |
| PRODUCT011 | distinct unknown local state per Transition field | artifact=LC, field=`transitions[ID].from` or `transitions[ID].to`, target=state ID |
| PRODUCT012 | Lifecycle whose initial-state count is not one | artifact=LC, field=`states` |
| PRODUCT013 | distinct terminal source per Transition | artifact=LC, field=`transitions[ID].from`, target=state ID |
| PRODUCT014 | unresolved local coverage selector after Lifecycle resolution | artifact=SB, field=`covers-transition.transition`, target=transition ID |
| PRODUCT112 | unreachable non-initial state of an active Lifecycle | artifact=LC, field=`states[ID]`, target=state ID |
| PRODUCT113 | uncovered transition of an active Lifecycle | artifact=LC, field=`transitions[ID]`, target=transition ID |

These stable local-ID paths are semantic attribution only. PRODUCT002 continues to use JSON Pointers, including numeric array indexes, under RFC 0085. Relationship diagnostics continue to use canonical `transitions[].<field>` names and per-authored-entry granularity. PRODUCT009 handles body sections. Existing status and removal diagnostics apply to every new canonical relationship.

For evidence, allocate PRODUCT080 (error, one per malformed evidence document; when parseable, field is the first invalid JSON Pointer in Unicode code-point order) and PRODUCT081 (error, one per duplicate test-id occurrence after the first or resolved disallowed citation target kind). Duplicate JSON object keys make the evidence document malformed and MUST NOT be silently overwritten; because no unambiguous parsed object exists, that PRODUCT080 omits field. PRODUCT081 carries file and `field: results[n].test-id` or `results[n].citations[m].id` with one-based positions. The disallowed-target form additionally carries target equal to the cited artifact ID and the flattened entry ordinal; the duplicate-test form omits target and entry. Neither carries artifact or change. A malformed document stops its semantic checks; a duplicate result ID stops citation evaluation for that duplicate result. Resolve absent citation targets as PRODUCT060 before testing target kind. A disallowed resolved target produces PRODUCT081 alone for that citation. Other evidence citation failures reuse the Citation Contract and its precedence, with flattened entry attribution. Unsupported anchors are PRODUCT063. Evidence has no embedded projection and cannot itself produce PRODUCT062. Schema-validity checks precede semantic checks; malformed citation shapes within the closed evidence document are PRODUCT080.

### Serialization and release boundary

The removal of Use Case from Business Rule scope invalidates documents accepted by released `v1alpha1`, so [Schemas → Versioning](../schemas/README.md) requires a new `schemas/v1alpha2/` directory. Preserve released `v1alpha1` schemas unchanged. Copy the complete schema set with new URNs/references, select configuration `version: v1alpha2`, and add the Lifecycle and evidence schemas. Conformance claims identify specification 0.3.0 and serialization v1alpha2. Explicit v0.2/v1alpha1 operation remains governed by the old contract; no-config discovery uses the explicitly selected version pair rather than silently migrating data.

This RFC supplies graph vocabulary to #82; it does not duplicate that RFC's impact ledger or #115's citation-report rules. Its own follow-up scope is listed below so acceptance does not depend on an unpublished release plan.

### Implementation checklist

| Surface | Required follow-up |
| --- | --- |
| `spec/artifacts.md`, `spec/identifiers.md`, `spec/terminology.md`, `spec/frontmatter-reference.md` | Add LC, local State/Transition records and SB coverage; update all affected target unions and the BR migration; identify semantic authoring checks as human review. |
| `spec/relationships.md` | Add the nine relationship-table changes above, narrow BR scope, update PRODUCT105/106 sets, and retain LC as every transition reference's source. |
| `spec/validation.md` | Add the proposed code units and prerequisite rules, evidence field/entry attribution and standard LC relationship/body/status/removal diagnostics. Recheck code availability before allocation. |
| `schemas/v1alpha2/` | Copy the complete schema set with new URNs/references/config version; add LC and evidence schemas; extend common artifact ID/type unions with LC. Use separate BR scope (JRN/BC) and QR/Constraint scope (JRN/UC/BC/LC) definitions so narrowing BR does not narrow other kinds. FR derived-from gains LC; SB gains the closed coverage pair. Preserve `schemas/v1alpha1/` unchanged. |
| `spec/verification-evidence.md` (new), `spec/citation-contract.md` | Publish the conditional evidence contract and link to the existing citation rules without duplicating their precedence; support whole-LC citations without local anchors. Evidence JSON schema reuses standard citationRecord; duplicate test IDs and resolved target kinds are semantic checks. |
| `spec/configuration.md`, `spec/conformance.md`, `spec/index.md`, `schemas/README.md`, `MATURITY.md` | Document the version pair and configuration selection; require LC support but keep authoring optional; make evidence conformance conditional; distinguish executable checks from review criteria. |
| `templates/domain-lifecycle.md` (new), `templates/business-rule.md`, `templates/use-case.md`, `templates/structured-behaviour.md`, `templates/README.md`, `scripts/check-templates.mjs` | Add LC example, migrate BR/UC association, document coverage; select new schemas and support boolean scalars/validation and CRLF input. Evidence is external JSON, not an artifact template. |
| `docs/migrations/v0.2-to-v0.3.md` (new) | Document the migration above, idempotence, unresolved-target repair, explicit active-change rebase and preservation of archives/citation pins. |
| `conformance/cases/`, `conformance/README.md`, `.github/workflows/conformance.yml` | Implement the case matrix below, update known BR/UC fixtures, intentionally recompute affected pins and retain a pinned v0.2 regression lane. Pin a runner with evidence support before claiming evidence coverage. |

The existing runner accepts flat model fixtures with diagnostics and exit codes; it cannot execute an evidence-adapter case. That extension is an explicit implementation dependency, not a reason to represent unexecuted cases as passes. LC validation and migration cases can use the existing flat format. The worked model's multi-source equivalence, semantic adequacy and absence of implementation design remain human-review criteria.

Minimum fixture families for this RFC (each case names its clause and exact diagnostic attribution):

- `domain-lifecycle-valid`, `domain-lifecycle-single-state`, `domain-lifecycle-empty-transitions`, `domain-lifecycle-multiple-sources`: all relationship fields, common status/provenance, FR derivation, QR/Constraint scope and SB coverage; allow a state and transition to share a local spelling.
- `domain-lifecycle-schema-*`, `domain-lifecycle-duplicate-*`, `domain-lifecycle-unknown-*`, `domain-lifecycle-no-initial`, `domain-lifecycle-multiple-initial`, `domain-lifecycle-terminal-source`, `domain-lifecycle-section-*`: closed shapes, booleans, local uniqueness/references, cardinality and body order, including suppression when prerequisites fail.
- `domain-lifecycle-<relationship>-{unknown,wrong-type,retired,removed}` and `covers-transition-{unknown-lifecycle,wrong-lifecycle-type,removed-lifecycle,unknown-transition,removed-transition,missing-illustrates}`: existing per-entry codes, PRODUCT014 only after valid LC resolution, and no replacement of required illustrates.
- `domain-lifecycle-{unreachable-state,uncovered-transition,draft-no-warning,deprecated-no-warning,retired-no-warning,coverage-retired-sb}` plus `lifecycle-{rule-consumed,term-subject-used,term-uses-used,retired-source-no-consumption}`: warning populations, exact counts and absence assertions.
- `business-rule-{uc-scope-rejected,uc-governance-migrated,broad-scope-preserved,absent-scope-not-global}`, migration idempotence/unresolved-target checks, and `lifecycle-citation-{current,stale,anchor-rejected}`. Extend all-kinds and LC add/modify/remove fixtures; archives remain inert.
- `evidence-{valid,duplicate-test-id,duplicate-json-key,disallowed-target-kind,unknown-property,blank-identity,invalid-revision,invalid-level,invalid-outcome,empty-results,empty-citations}`: both full SHA lengths, all levels/outcomes, closed shapes and exact error precedence.
- `evidence-{unknown-target,missing-anchor,sb-anchor,stale-target,passed-stale,current-enumerated,historical-excluded,entry-after-duplicate-result}`: existing citation semantics, outcome/status separation, explicit selection and stable ordinals. Missing evidence alone produces no diagnostic. The same test ID in separate runs remains valid.

### Worked-model DDD decisions

The Product Change pilot does not require Entity/Value Object classification or typed associations. It does require lifecycle states, transitions, rule constraints, examples of valid and refused operations, and transition-specific citations. This RFC therefore decides not to add Entity, Value Object or Aggregate artifacts as a bundle. It leaves Domain Event as a conditional future artifact, subject to the cross-context evidence threshold above.

## Impact

- **On existing conformant repositories:** authoring Domain Lifecycle and `covers-transition` is optional. Removing Use Case from `Business Rule.applies-to` is a normative breaking change; repositories using that edge MUST migrate it to `Use Case.governed-by` before claiming conformance to 0.3.0/v1alpha2. Repositories without that edge need no relationship migration, but still select the new version pair and update configuration where present.
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
