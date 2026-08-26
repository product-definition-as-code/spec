# RFC 0084: Explicit behaviour semantics

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-26
- **Proposed target:** PDaC specification 0.2.0; additive `v1alpha1` schema evolution

## Problem

The v0.1 reference profile can state an obligation and attach acceptance criteria to it, but it
cannot model either of these product facts explicitly:

1. one concrete, implementation-independent example of accepted product behaviour; or
2. the business-observable states and legal transitions of a domain concept.

Functional and Quality Requirements currently carry a non-empty `verification` list whose entries
contain one `scenario` string and an optional local `id` ([Artifacts](../spec/artifacts.md)). This is
a useful minimum, but the string does not distinguish context, stimulus and expected outcome. It
cannot declare which Use Case, Business Rule, Constraint or domain transition the behaviour
illustrates. It has no artifact lifecycle or provenance of its own, and its only address is an
anchor inside its parent Requirement.

Anchoring does not make that scenario an independent citation target. A v0.1 citation always
records the whole target artifact's digest ([Citation Contract](../spec/citation-contract.md)), so a
change anywhere in a Requirement makes every citation anchored within that Requirement stale. That
is correct under v0.1, but too coarse when a delivery specification implements one of many stable
behaviours carried by the same Requirement.

The missing structure is visible at the delivery boundary. [OpenSpec's writing guide][openspec-writing]
defines a spec as behaviour rather than code, composed of Requirements and concrete Given/When/Then
Scenarios that could become automated tests. [Spec Kit's feature-spec template][speckit-template]
expresses acceptance scenarios as Given/When/Then, while [Kiro's Requirements-First
workflow][kiro-requirements] generates system behaviours in EARS form. PDaC can currently ground the
parent Requirement but cannot give those consumers one independently versioned product behaviour to
cite. The delivery framework therefore either cites too broadly or restates behaviour whose
canonical home is absent.

The domain model has a related temporal gap. Journeys order Use Cases and Use Cases describe flows,
but neither states which business states a Domain Term may occupy, which transitions are legal, or
which Actors, Use Cases and Business Rules participate in a transition. Teams using DDD, BDD,
state-transition analysis or event-oriented discovery must keep that knowledge in prose or in an
external diagram. The graph consequently cannot validate it, include it in impact analysis, or
connect a concrete behaviour to the transition it covers.

This RFC adds two complementary reference-profile artifact kinds:

- **Structured Behaviour**, one concrete observable example with explicit context, stimulus and
  expected outcomes; and
- **Domain Lifecycle**, the business-observable state space and legal transitions of one Domain
  Term.

The proposal models accepted product semantics only. It does not make Gherkin, EARS, UML, BPMN or a
test framework canonical; does not generate executable test code; and does not move implementation,
test execution or delivery evidence inside PDaC.

## Proposal

### Release and serialization

This RFC targets PDaC specification `0.2.0`. It evolves the existing `v1alpha1` serialization
additively rather than introducing `v1alpha2` or prematurely advancing to `v1beta1`.

Every document valid before this RFC remains valid afterwards with the same meaning: both new
artifact kinds are optional to author, the existing nine kinds keep their fields and semantics, and
the existing inline verification form remains accepted unchanged. The additions therefore satisfy
the repository's rule that a schema change within one serialization version be backward compatible
([Schemas](../schemas/README.md)).

A conforming v0.2 implementation MUST recognize the expanded `v1alpha1` schemas and semantics. An
implementation conforming only to the tagged v0.1 specification is not thereby conforming to v0.2;
the method/spec version, not a new serialization label, distinguishes those normative contracts.
Repositories require no configuration edit or migration merely to remain valid under v0.2.

This RFC does not advance the serialization to beta: the new semantics should be exercised by an
independent implementation and external adopters before the project makes a maturity claim. A later
maturity decision, not this feature's size, should introduce `v1beta1`.

### Structured Behaviour (`structured-behaviour`, `SB-`)

A Structured Behaviour is one concrete, implementation-independent example of accepted observable
product behaviour. It separates the context in which behaviour occurs, the single stimulus that
occurs, and the observable outcomes that follow.

Structured Behaviour uses prefix `SB-` and type `structured-behaviour`.

In addition to the common product-artifact fields, its frontmatter is:

| Field | Presence | Shape | Meaning |
| --- | --- | --- | --- |
| `illustrates` | required | non-empty list of Use Case, Business Rule, Constraint or Domain Lifecycle IDs | Product semantics made concrete by the example |
| `given` | optional | non-empty ordered list of non-empty strings | Observable context or preconditions |
| `when` | required | non-empty string | The single stimulus, action or event |
| `then` | required | non-empty ordered list of non-empty strings | Observable expected outcomes |
| `covers-transition` | optional | closed object containing `lifecycle` and `transition` | The Domain Lifecycle transition this example covers |
| `uses-terms` | optional | list of Domain Term IDs | Terms required to interpret the example |

`covers-transition.lifecycle` MUST be a Domain Lifecycle ID. `covers-transition.transition` MUST be
a local Transition ID declared by that lifecycle.

The required body sections, in order, are:

1. `## Intent`
2. `## Boundaries`

`## Intent` explains why the example is product-significant. `## Boundaries` states what the example
does not assert where a reader could otherwise mistake it for broader behaviour. `None.` is valid
when no material boundary is known.

The following example is conforming:

```yaml
---
id: SB-CANCEL-PAID-ORDER
type: structured-behaviour
title: Cancel a paid order while cancellation remains available
status: active
illustrates:
  - UC-CANCEL-ORDER
  - BR-CANCELLATION-WINDOW
  - LC-ORDER
given:
  - The order is in the PAID state
  - The cancellation window remains open
when: The customer requests cancellation
then:
  - The order enters the CANCELLED state
  - A refund is requested
covers-transition:
  lifecycle: LC-ORDER
  transition: CANCEL
uses-terms:
  - TERM-ORDER
---

## Intent

Establish the accepted result of cancelling an order whose payment has already been captured.

## Boundaries

This example does not specify how or when the refund is settled.
```

The semantic keywords are intentionally format-neutral despite their familiar spelling:

- each `given` entry states product context, not test-fixture setup;
- `when` states one product-level stimulus, not a sequence of implementation steps; and
- each `then` entry states an externally or business-observable outcome, not an assertion against
  implementation internals.

Multiple context or outcome clauses are represented by multiple ordered list entries. Authors MUST
NOT include literal `GIVEN`, `WHEN`, `THEN` or `AND` prefixes in the values. Renderers MAY supply
those words for a target format. All `given` entries are conjunctive, and all `then` entries are
conjunctive: every listed context condition holds and every listed outcome is expected. Alternative
contexts or outcomes MUST be expressed as separate Structured Behaviour artifacts rather than an
ambiguous `or` clause.

Structured Behaviour MUST NOT name test classes, step definitions, selectors, mocks, database rows,
internal messages or other implementation machinery. An externally visible API operation, event or
document MAY be named when it is itself part of the product contract.

### Requirement verification references

Under the expanded `v1alpha1` schema, each Functional or Quality Requirement `verification` item is
exactly one of:

1. the existing inline form, with `scenario` and optional local `id`; or
2. a reference form containing exactly one `scenario-ref` whose value is a Structured Behaviour ID.

```yaml
verification:
  - scenario: A malformed URL is rejected with a reason
    id: REJECT-MALFORMED
  - scenario-ref: SB-CANCEL-PAID-ORDER
```

The two forms MUST NOT be combined in one item and MUST NOT carry unknown properties. A
`scenario-ref` is the canonical authored relationship from a Functional or Quality Requirement to
a Structured Behaviour. “Verifies” and all other reverse views are derived and MUST NOT be authored.

Inline verification remains conforming. A repository MAY mix inline and referenced entries within
one Requirement, which permits incremental migration without duplicating the same scenario in both
forms. The same Structured Behaviour MAY verify more than one Requirement.

An author MUST NOT represent the same expected behaviour as both an inline `scenario` and a
`scenario-ref` in the same Requirement. Whether two differently worded entries are semantically the
same is a review question and not a deterministic validation rule.

### Structured Behaviour identity and citations

A Structured Behaviour is a Product Artifact. It has its own immutable ID, lifecycle, provenance,
content digest, Product Change history, graph node and citation target under the existing contracts.

A consumer that depends on the complete Structured Behaviour SHOULD cite `SB-…` directly. Its
citation uses the existing whole-artifact digest and no anchor:

```text
pdac:cite id="SB-CANCEL-PAID-ORDER" digest="sha256:<64 lowercase hex digits>"
```

This RFC does not change v0.1 anchor semantics. An anchor on a Functional or Quality Requirement
continues to address an inline `verification[].id`, and the citation digest continues to cover the
whole parent artifact. `scenario-ref` does not introduce an anchor in the parent Requirement: the
referenced Structured Behaviour is cited by its own ID.

An implementation MUST reject an anchor on a Structured Behaviour as unresolved unless a later
specification revision defines anchors within that artifact kind.

### Domain Lifecycle (`domain-lifecycle`, `LC-`)

A Domain Lifecycle defines the business-observable states and legal transitions of one Domain Term.
It does not imply a class, DDD aggregate, database representation, workflow engine, service boundary
or source-code module.

Domain Lifecycle uses prefix `LC-` and type `domain-lifecycle`.

In addition to the common product-artifact fields, its frontmatter is:

| Field | Presence | Shape | Meaning |
| --- | --- | --- | --- |
| `subject` | required | Domain Term ID | The concept whose lifecycle is defined |
| `states` | required | non-empty ordered list of closed State records | Business-observable states |
| `transitions` | required | non-empty ordered list of closed Transition records | Legal state changes |
| `uses-terms` | optional | list of Domain Term IDs | Additional terms required to interpret the lifecycle |

A State record is closed and contains:

| Field | Presence | Shape | Meaning |
| --- | --- | --- | --- |
| `id` | required | local ID matching `[A-Z0-9]+(-[A-Z0-9]+)*` | Stable identity within the lifecycle |
| `title` | required | non-empty string | Human-readable state name |
| `initial` | optional | boolean, default `false` | Whether the lifecycle begins in this state |
| `terminal` | optional | boolean, default `false` | Whether no legal transition leaves this state |

A Transition record is closed and contains:

| Field | Presence | Shape | Meaning |
| --- | --- | --- | --- |
| `id` | required | local ID matching `[A-Z0-9]+(-[A-Z0-9]+)*` | Stable identity within the lifecycle |
| `title` | required | non-empty string | Human-readable transition name |
| `from` | required | non-empty list of local State IDs | Legal source states |
| `to` | required | one local State ID | Resulting state |
| `trigger` | required | non-empty string | Product-level event or action that initiates the transition |
| `initiated-by` | optional | list of Actor IDs | Actors capable of initiating it |
| `governed-by` | optional | list of Business Rule IDs | Rules governing whether or how it occurs |
| `realized-by` | optional | list of Use Case IDs | Use Cases through which it occurs |

State IDs MUST be unique within one lifecycle. Transition IDs MUST be unique within one lifecycle.
State and Transition IDs occupy separate local namespaces, so a State and Transition MAY share the
same local ID.

Exactly one State MUST declare `initial: true`. A terminal State MUST NOT appear in any
Transition's `from` list. Every `from` and `to` value MUST resolve to a State in the same lifecycle.
Every non-initial State SHOULD be reachable from the initial State by following zero or more
Transitions in their declared direction.

A transition with more than one `from` State means that the same named product transition has the
same trigger and result from each listed source. If its rules, result or product meaning differ by
source state, authors SHOULD declare separate Transitions.

Within the scope stated by `## Boundaries`, the Transition list is exhaustive: a state change not
represented by a Transition is not accepted product behaviour. Transition list order carries no
priority, conflict-resolution or execution semantics. Where two Transitions could respond to the
same trigger from the same State, their governing Business Rules or their documented semantics MUST
make the accepted outcomes distinguishable; deterministic validation does not decide whether that
natural-language distinction is complete.

The required body sections, in order, are:

1. `## Purpose`
2. `## Invariants`
3. `## State Semantics`
4. `## Transition Semantics`
5. `## Boundaries`

The body explains product meaning that the structured records cannot carry without duplicating the
records as prose. It MUST NOT restate the full state or transition tables. Generated views MAY render
those tables from frontmatter.

The following abbreviated frontmatter is conforming:

```yaml
---
id: LC-ORDER
type: domain-lifecycle
title: Order lifecycle
status: active
subject: TERM-ORDER
states:
  - id: PENDING
    title: Pending payment
    initial: true
  - id: PAID
    title: Paid
  - id: FULFILLED
    title: Fulfilled
    terminal: true
  - id: CANCELLED
    title: Cancelled
    terminal: true
transitions:
  - id: PAY
    title: Accept payment
    from: [PENDING]
    to: PAID
    trigger: Payment is accepted
    governed-by: [BR-PAYMENT-ACCEPTANCE]
    realized-by: [UC-PAY-ORDER]
  - id: CANCEL
    title: Cancel order
    from: [PENDING, PAID]
    to: CANCELLED
    trigger: The customer requests cancellation
    initiated-by: [ACT-CUSTOMER]
    governed-by: [BR-CANCELLATION-WINDOW]
    realized-by: [UC-CANCEL-ORDER]
---
```

### Canonical relationships

The canonical relationship vocabulary gains these rows:

| Source | Field | Allowed targets |
| --- | --- | --- |
| Functional Requirement | `verification[].scenario-ref` | Structured Behaviour |
| Quality Requirement | `verification[].scenario-ref` | Structured Behaviour |
| Structured Behaviour | `illustrates` | Use Case, Business Rule, Constraint, Domain Lifecycle |
| Structured Behaviour | `covers-transition.lifecycle` | Domain Lifecycle |
| Structured Behaviour | `uses-terms` | Domain Term |
| Domain Lifecycle | `subject` | Domain Term |
| Domain Lifecycle | `uses-terms` | Domain Term |
| Domain Lifecycle | `transitions[].initiated-by` | Actor |
| Domain Lifecycle | `transitions[].governed-by` | Business Rule |
| Domain Lifecycle | `transitions[].realized-by` | Use Case |

`covers-transition.transition`, Transition `from` and Transition `to` are validated local
references, not product-graph edges to Product Artifacts. A graph serialization MAY expose local
State and Transition nodes as a derived view, but they are not authored Product Artifacts and do not
receive globally unique IDs or independent lifecycle states.

The existing Functional Requirement `derived-from` relationship additionally allows Domain
Lifecycle targets. The existing Quality Requirement and Constraint `applies-to` relationships
additionally allow Domain Lifecycle targets.

Every reverse view is derived. In particular, implementations MAY display:

- the Requirements verified by a Structured Behaviour;
- the behaviours covering a Lifecycle Transition;
- the lifecycle of a Domain Term;
- the Actors, Business Rules and Use Cases participating in a Transition; and
- the Requirements derived from or applying to a Domain Lifecycle.

Those reverse relationships MUST NOT be authored.

### Reachability and impact

Structured Behaviour and Domain Lifecycle edges participate in the Product Graph and in the
undirected reachability definition under the same rule as existing canonical product relationships.
Local State and Transition references participate only through their containing Domain Lifecycle.

Consequently:

- a Requirement verified by a Structured Behaviour is connected to the behaviour's source Use
  Cases, Rules, Constraints and Lifecycle;
- a Lifecycle is connected to Actors and Use Cases through its Transitions; and
- a change to a Structured Behaviour or Domain Lifecycle is included in structural impact analysis
  through those authored edges.

Structural reachability continues to make no semantic impact claim.

### Validation and diagnostics

Existing schema, identity, relationship, lifecycle and body-section diagnostics apply to the two new
artifact kinds. `PRODUCT006` reports unresolved Product Artifact references and `PRODUCT007` reports
wrong target types in the new relationships.

The following error diagnostics are added:

| Code | Condition |
| --- | --- |
| `PRODUCT010` | Duplicate local State ID or duplicate local Transition ID within one Domain Lifecycle |
| `PRODUCT011` | Domain Lifecycle Transition `from` or `to` references an unknown local State ID |
| `PRODUCT012` | Domain Lifecycle does not declare exactly one initial State |
| `PRODUCT013` | A State declared terminal appears in a Transition's `from` list |
| `PRODUCT014` | Structured Behaviour `covers-transition.transition` does not resolve in the referenced Domain Lifecycle |

The following warning diagnostics are added:

| Code | Condition |
| --- | --- |
| `PRODUCT112` | Active Structured Behaviour is not referenced by any Functional or Quality Requirement `verification[].scenario-ref` |
| `PRODUCT113` | A non-initial Domain Lifecycle State is unreachable from the initial State |
| `PRODUCT114` | An active Domain Lifecycle Transition has no incoming Structured Behaviour `covers-transition` relationship |

`PRODUCT112` does not mean the behaviour is false or unusable: it identifies an accepted example
that verifies no stated obligation. `PRODUCT114` does not require automatic scenario generation: it
identifies a legal transition for which the product definition contains no concrete accepted
example. Both remain warnings because partial models and models under construction are valid uses.

Diagnostics involving local IDs set `artifact` to the containing global Artifact ID. Their exact
granularity and attribution are:

| Code | Emission granularity | `field` | `target` |
| --- | --- | --- | --- |
| `PRODUCT010` | once per duplicated local ID per State or Transition namespace | `states` or `transitions` | duplicated local ID |
| `PRODUCT011` | once per Transition, reference field and unknown State ID | `transitions.<transition-id>.from` or `transitions.<transition-id>.to` | unknown State ID |
| `PRODUCT012` | once per invalid Lifecycle | `states.initial` | absent |
| `PRODUCT013` | once per Transition and terminal source State | `transitions.<transition-id>.from` | terminal State ID |
| `PRODUCT014` | once per Structured Behaviour | `covers-transition.transition` | unknown Transition ID |
| `PRODUCT112` | once per Structured Behaviour | absent | absent |
| `PRODUCT113` | once per unreachable State | `states.<state-id>` | unreachable State ID |
| `PRODUCT114` | once per uncovered Transition | `transitions.<transition-id>` | uncovered Transition ID |

The literal dots above define the field-path serialization for these diagnostics; list indexes MUST
NOT appear because reordering an otherwise identical list must not change diagnostics. Multiple
local-reference diagnostics follow the existing deterministic order by file, code and target, with
`field` as the final tie-breaker when file, code and target are equal. This local refinement does not
change the ordering contract for diagnostics outside this RFC.

### Citations and consumer projections

The Citation Contract's Product Artifact target set expands to include Structured Behaviour and
Domain Lifecycle IDs. Digest computation, carriers, statuses, precedence and delivery ownership are
otherwise unchanged.

An implementation MAY render a consumer-specific projection from accepted Structured Behaviour and
Domain Lifecycle artifacts. A projection is generated, non-canonical consumer material and MUST
carry citations to the Product Artifacts from which its product semantics came. Generating a
projection MUST NOT create, approve, apply or accept a Product Change and MUST NOT claim that any
test was implemented or executed.

The following mappings are non-normative examples:

| PDaC | OpenSpec-like consumer | Spec Kit-like consumer | EARS-like consumer | Gherkin-like consumer |
| --- | --- | --- | --- | --- |
| Structured Behaviour title | Scenario heading | Acceptance-scenario label | Requirement label | Scenario name |
| `given[]` | GIVEN clauses | Given clause | precondition clause | Given/And steps |
| `when` | WHEN clause | When clause | WHEN trigger | When step |
| `then[]` | THEN clauses | Then clause | THE SYSTEM SHALL responses | Then/And steps |
| Structured Behaviour citation | scenario-adjacent comment or ledger | scenario-adjacent comment or ledger | requirement-adjacent comment or ledger | tag, comment or sidecar supported by the consumer |
| Domain Lifecycle | referenced lifecycle context | state-oriented edge cases | state-driven conditions | scenario discovery and coverage input |

For example, an OpenSpec-like Markdown projection could bind one native Scenario to the exact
accepted behaviour it elaborates:

```markdown
#### Scenario: Cancel a paid order while cancellation remains available

- **GIVEN** the order is in the PAID state
- **AND** the cancellation window remains open
- **WHEN** the customer requests cancellation
- **THEN** the order enters the CANCELLED state
- **AND** a refund is requested

<!-- pdac:cite id="SB-CANCEL-PAID-ORDER" digest="sha256:<64 lowercase hex digits>" -->
```

Provider-specific syntax and validity remain the provider's responsibility. PDaC conformance tests
MUST NOT require OpenSpec, Spec Kit, Kiro, Cucumber or any other named consumer.

PDaC tooling MAY generate a Mermaid, UML-compatible or other state diagram from a Domain Lifecycle.
Such a diagram is a generated view and MUST NOT become canonical or be required to rebuild the
Lifecycle.

### Schema changes

`schemas/v1alpha1/common.schema.json` adds:

- `structuredBehaviourId` with the `SB-` prefix;
- `domainLifecycleId` with the `LC-` prefix;
- both prefixes to `productArtifactId`;
- both types to `productArtifactType`;
- local State and Transition ID definitions;
- the expanded verification-item union; and
- shared closed definitions for Lifecycle State and Transition records.

`schemas/v1alpha1/structured-behaviour.schema.json` and
`schemas/v1alpha1/domain-lifecycle.schema.json` define the two artifact contracts above.

The Functional and Quality Requirement schemas keep `verification` required and non-empty
but use the new inline-or-reference item union. Their relationship target validation recognizes
`scenario-ref`. The Functional Requirement, Quality Requirement and Constraint schemas widen the
target sets described under Canonical relationships.

The Product Change operation schema accepts `SB-` and `LC-` as Product Artifact IDs. The exhaustive
frontmatter reference MUST be regenerated from the changed schemas rather than edited independently.

### Conformance

The v0.2 conformance suite adds at least these zero-diagnostic cases:

- one Structured Behaviour referenced from a Functional Requirement;
- one Structured Behaviour referenced from a Quality Requirement;
- one Requirement mixing an existing inline scenario with a `scenario-ref`;
- one Domain Lifecycle whose transitions connect its Actor, Business Rules and Use Cases;
- one Structured Behaviour covering a Lifecycle Transition;
- a direct current citation of a Structured Behaviour; and
- an unchanged Structured Behaviour citation remaining current when a different Requirement or
  behaviour changes.

Negative cases add:

- a `scenario-ref` to an unknown ID (`PRODUCT006`);
- a `scenario-ref` to a known wrong artifact type (`PRODUCT007`);
- a Structured Behaviour with an unknown lifecycle (`PRODUCT006`);
- a Structured Behaviour covering an unknown transition (`PRODUCT014`);
- duplicate State and Transition local IDs (`PRODUCT010`);
- a Transition referencing an unknown source or destination State (`PRODUCT011`);
- zero and multiple initial States (`PRODUCT012`);
- a terminal State with an outgoing Transition (`PRODUCT013`);
- an unreachable State (`PRODUCT113`); and
- warning coverage for unused Structured Behaviour and uncovered Lifecycle Transitions
  (`PRODUCT112`, `PRODUCT114`).

The existing `artifact-kinds-valid` case gains the two new kinds. Existing zero-diagnostic fixtures
remain valid; their expected results change only when the new graph edges intentionally affect the
fixture's graph or warning population.

## Impact

- **On existing conformant repositories:** no migration and no changed meaning. Existing
  repositories remain valid and may continue using inline verification and whole-Requirement
  scenario anchors.
- **On repositories adopting the new kinds:** they may add Structured Behaviour and Domain Lifecycle
  artifacts incrementally and may replace inline verification items with `scenario-ref` entries
  through ordinary Product Changes.
- **On existing implementations:** v0.2 conformance requires version-dispatched schema loading, two
  new artifact parsers, graph relationships, local Lifecycle validation, new diagnostics, Product
  Change support, citation target support and graph/impact projections. Provider-specific rendering
  is optional and outside conformance.
- **On the conformance tests:** existing valid documents remain valid, while the artifact-kind,
  relationship, validation and citation cases expand as listed above.
- **On downstream integrations:** OpenSpec, Spec Kit, Kiro, BDD and other adapters may cite
  Structured Behaviour directly and project its clauses into native scenario syntax. They retain
  ownership of their documents and validation.

## Alternatives considered

### Introduce a new `v1alpha2` serialization

Rejected for this RFC. The schema changes are backward compatible under the repository's published
rule: every previously valid document remains valid and unchanged, while new documents may use the
expanded vocabulary. Creating a second alpha serialization would require a version-selection and
migration contract that the current specification does not otherwise need, while an implementation's
conformance claim already names the method/spec version that defines which `v1alpha1` vocabulary it
supports. The v0.1 Git tag preserves the old schemas; v0.2 expands them on its own tagged line.

This decision should be reversed if review concludes that adding enum members or new artifact kinds
is not backward compatible under `schemas/README.md`; in that case the serialization-version policy
must be clarified as part of this RFC rather than handled differently by each implementation.

### Expand inline `verification[]` entries only

Add `given`, `when` and `then` to the existing nested scenario record without a new Artifact kind.

Rejected as the complete solution. It improves formulation but keeps whole-Requirement citation
granularity, prevents independent lifecycle and provenance, and cannot make the behaviour an
ordinary graph and Product Change target. The retained inline form remains appropriate for simple
acceptance criteria that do not need those properties.

### Change anchored citations to digest only the anchored scenario

Rejected for v0.2. V0.1 explicitly defines the digest as the whole target artifact's bytes. Changing
that meaning would invalidate existing anchored citations, require a canonical serialization of a
nested YAML value, complicate marker-block embedding and overload one citation record with two digest
domains. A standalone Structured Behaviour obtains fine-grained identity using the existing digest
contract.

### Make Gherkin or EARS canonical

Rejected. Both are useful consumer formulations, but either would privilege a delivery notation and
import syntax whose evolution PDaC does not govern. The proposed semantic clauses project to those
formats without making either authoritative.

### Generate executable tests from Domain Lifecycles

Rejected as a PDaC responsibility. A Lifecycle can identify transitions and missing behavioural
coverage; Structured Behaviour can provide product-level examples; and an adapter can generate a
Gherkin or EARS starting point. Test harnesses, fixtures, step bindings, execution and evidence remain
delivery concerns.

### Add Domain Event and Command artifact kinds now

Deferred. A Transition's `trigger` and `initiated-by` fields carry enough information to test the
Lifecycle and Structured Behaviour model. Events or commands should become independent Artifacts
only after adoption demonstrates that they change independently, are reused across Lifecycles or
need their own citations and impact analysis.

### Make local States and Transitions global Product Artifacts

Rejected. Their identity is meaningful within one Lifecycle, and giving every State and Transition a
file, global ID, lifecycle and Product Change surface would impose large artifact overhead before a
cross-lifecycle reuse case exists. Stable local IDs provide deterministic references and leave open a
later promotion path.

### Store a UML state machine, BPMN model or diagram as canonical

Rejected. It would bind the reference profile to an external notation, toolchain or interchange
format and make generated visual layout authoritative. Domain Lifecycle records are the semantic
source; diagrams remain reproducible views.

### Put lifecycle states inside a Domain Term or Use Case

Rejected. A Lifecycle changes independently, is reused by multiple Use Cases and Rules, and needs
its own impact and citation target. Embedding it would recreate the coarse-grained citation problem
this RFC resolves for behaviour.

### Wait for a general custom-profile mechanism

Rejected as a prerequisite. Structured Behaviour promotes semantics already mandatory on every
Functional and Quality Requirement, and Domain Lifecycle supplies broadly applicable product
semantics without requiring any repository to author one. A future custom-profile mechanism remains
valuable for specialized event, regulatory or safety vocabularies, but these two kinds can be
specified and tested in the reference profile independently.

### Defer both kinds to specification 0.3.0

Rejected. No identified 0.2 dependency prevents a backward-compatible expansion of the draft alpha
serialization. Deferral without an evidence-producing prerequisite would only postpone the feedback
needed to improve the model. Version 0.3 should respond to implementation and adoption evidence from
0.2 rather than reserve these semantics speculatively.

### Split Structured Behaviour and Domain Lifecycle into unrelated RFCs

Rejected for this proposal. Each kind is independently useful, but the `covers-transition`
relationship, transition-coverage diagnostics and shared SDD projection are the central capability:
accepted behaviour can state which legal domain change it exemplifies. Specifying either half alone
would leave that relationship undefined and invite incompatible follow-up designs. Maintainers may
still require a mechanical PR split, but the semantic decision should be reviewed as one model.

## Consequences

PDaC 0.2 gains an explicit, citable unit of accepted observable behaviour and an explicit temporal
model of domain semantics. Requirements can keep lightweight inline criteria or refer to reusable
behaviours. Stateful domains can define legal transitions without importing implementation design.
The graph can answer which rules and use cases govern a transition, which behaviours cover it, which
requirements depend on it and which delivery documents cited the result.

The cost is real: the reference profile grows, validators must support more semantics, repositories
can create more artifacts, and Lifecycle validation introduces local identity in addition to global
Product Artifact identity. The proposal contains that cost by keeping inline
verification valid, making both new kinds optional to author, keeping States and Transitions local,
and leaving consumer rendering outside conformance.

This is a normative change under [CONTRIBUTING.md](../CONTRIBUTING.md). It remains public and requires
maintainer consensus and resolution of substantive feedback. The temporary stabilization note
suspends a fixed minimum elapsed time while the specification is pre-stable; it does not bypass
review.

[openspec-writing]: https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md
[speckit-template]: https://github.com/github/spec-kit/blob/main/templates/spec-template.md
[kiro-requirements]: https://kiro.dev/docs/specs/feature-specs/requirements-first/
