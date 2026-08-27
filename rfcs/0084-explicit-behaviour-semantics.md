# RFC 0084: Structured Behaviour and scenario references

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-26
- **Issue:** <https://github.com/product-definition-as-code/spec/pull/84>
- **Proposed target:** PDaC specification 0.2.0; additive `v1alpha1` schema evolution

## Problem

The v0.1 reference profile can state an obligation and attach acceptance criteria to it, but it cannot model one concrete, implementation-independent example of accepted product behaviour as a Product Artifact in its own right.

Functional and Quality Requirements currently carry a non-empty `verification` list whose entries contain one `scenario` string and an optional local `id` ([Artifacts](../spec/artifacts.md)). This is a useful minimum, but the string does not distinguish context, stimulus and expected outcome. It cannot declare which Use Case, Business Rule or Constraint the behaviour illustrates. It has no artifact lifecycle or provenance of its own, and its only address is an anchor inside its parent Requirement.

Anchoring does not make that scenario an independent citation target. A v0.1 citation always records the whole target artifact's digest ([Citation Contract](../spec/citation-contract.md)), so a change anywhere in a Requirement makes every citation anchored within that Requirement stale. That is correct under v0.1, but too coarse when a delivery specification relies on one of several stable behaviours carried by the same Requirement.

[RFC 0022](0022-criteria-in-verification-list.md) rejected a separate artifact kind for ordinary acceptance criteria because their local IDs already provided sufficient identity and they could not have an independent lifecycle. This RFC does not reverse that decision. Structured Behaviour is for behaviour that needs independent reuse, lifecycle or whole-artifact citation, while ordinary criteria remain inline.

The missing structure is visible at the delivery boundary. [OpenSpec's writing guide][openspec-writing] defines a spec as behaviour rather than code, composed of Requirements and concrete Given/When/Then Scenarios that could become automated tests. [Spec Kit's feature-spec template][speckit-template] expresses acceptance scenarios as Given/When/Then, while [Kiro's Requirements-First workflow][kiro-requirements] generates system behaviours in EARS form. PDaC can currently ground the parent Requirement but cannot give those consumers one independently versioned product behaviour to cite. The delivery framework therefore either cites too broadly or restates behaviour whose canonical home is absent.

This RFC adds **Structured Behaviour**, one concrete observable example with explicit context, stimulus and expected outcomes, and permits Functional and Quality Requirements to refer to it from `verification[]`.

The proposal models accepted product semantics only. It does not make Gherkin, EARS or a test framework canonical, generate executable test code, or move implementation, test execution or delivery evidence inside PDaC. Domain Lifecycle and state-transition modelling are deferred to a separate RFC targeting specification 0.3 so their distinct semantics, evidence and validation surface can be decided independently.

## Proposal

### Release and serialization

This RFC targets PDaC specification `0.2.0`. It evolves the existing `v1alpha1` serialization additively rather than introducing `v1alpha2` or prematurely advancing to `v1beta1`.

For a schema change within one serialization version to be backward compatible, every document valid under an earlier released schema set in that version MUST remain valid with the same interpretation under the later set. A backward-compatible change MAY accept new documents, fields or enum members. This definition will be added to `schemas/README.md`.

Every document valid before this RFC remains valid afterwards with the same meaning: Structured Behaviour is optional to author, the existing nine kinds keep their fields and semantics, and the existing inline verification form remains accepted unchanged. The additions therefore satisfy the repository's backward-compatibility rule ([Schemas](../schemas/README.md)).

A conformance claim MUST identify both the method/spec version and the serialization version. `v1alpha1` alone does not identify which backward-compatible expansion an implementation supports. A conforming v0.2 implementation MUST recognize the expanded `v1alpha1` schemas and semantics; an implementation conforming only to the tagged v0.1 specification is not thereby conforming to v0.2. The version-dimensions table in `MATURITY.md` will state that the pair selects the accepted document set and semantic contract.

Those two values are claimed version metadata. An implementation MAY additionally record the Git revision of the repository content it observed, but that revision identifies the observed input state and MUST NOT substitute for either claimed version. This RFC does not prescribe runner field names, command output or a machine-readable report serialization for the version metadata.

Repositories require no configuration edit or migration merely to remain valid under v0.2. This RFC does not advance the serialization to beta: independent implementation and adoption evidence, rather than this feature's size, should drive that maturity decision.

### Structured Behaviour (`structured-behaviour`, `SB-`)

A Structured Behaviour is one concrete, implementation-independent example of accepted observable product behaviour. It separates the context in which behaviour occurs, the single stimulus that occurs, and the observable outcomes that follow.

Structured Behaviour uses prefix `SB-` and type `structured-behaviour`.

In addition to the common product-artifact fields, its frontmatter is:

| Field | Presence | Shape | Meaning |
| --- | --- | --- | --- |
| `illustrates` | required | non-empty list of Use Case, Business Rule or Constraint IDs | Product semantics made concrete by the example |
| `given` | optional | non-empty ordered list of non-empty strings | Observable context or preconditions |
| `when` | required | non-empty string | The single stimulus, action or event |
| `then` | required | non-empty ordered list of non-empty strings | Observable expected outcomes |
| `uses-terms` | optional | list of Domain Term IDs | Terms required to interpret the example |

The required body sections, in order, are:

1. `## Intent`
2. `## Boundaries`

`## Intent` explains why the example is product-significant. `## Boundaries` states what the example does not assert where a reader could otherwise mistake it for broader behaviour. `None.` is valid when no material boundary is known.

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
given:
  - The order is in the PAID state
  - The cancellation window remains open
when: The customer requests cancellation
then:
  - The order enters the CANCELLED state
  - A refund is requested
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
- each `then` entry states an externally or business-observable outcome, not an assertion against implementation internals.

Multiple context or outcome clauses are represented by multiple ordered list entries. Authors MUST NOT include literal `GIVEN`, `WHEN`, `THEN` or `AND` prefixes in the values. Renderers MAY supply those words for a target format.

All `given` entries are conjunctive, and all `then` entries are conjunctive: every listed context condition holds and every listed outcome is expected. Alternative contexts or outcomes MUST be expressed as separate Structured Behaviour artifacts rather than an ambiguous `or` clause.

Structured Behaviour MUST NOT name test classes, step definitions, selectors, mocks, database rows, internal messages or other implementation machinery. An externally visible API operation, event or document MAY be named when it is itself part of the product contract.

The required `illustrates` relationship gives every Structured Behaviour an authored position in the Product Graph. Absence of a Requirement reference does not make the behaviour disconnected or invalid. This RFC therefore adds no orphan-Behaviour diagnostic. Implementations MAY report possible omissions as non-conformance advice for human review, but MUST NOT present that advice as a deterministic diagnostic.

### Business Rule examples

A Business Rule's required `## Examples` section remains explanatory body prose. It MAY contain local illustrations that do not require independent identity, reuse, lifecycle or citation.

When a concrete, testable example is authored as a Structured Behaviour, that artifact is the canonical carrier of its clauses and its `illustrates` relationship is the canonical association to the Business Rule. The Business Rule body MUST NOT present an authored restatement as a second canonical carrier. It MAY mention the Structured Behaviour ID or contain non-canonical explanatory prose. It MAY carry a restatement only as a non-canonical projection that cites the Structured Behaviour and follows the [Citation Contract's embedding rules](../spec/citation-contract.md#embedding). Whether differently worded prose restates the same behaviour is a review question, not a deterministic validation rule.

### Requirement verification references

Under the expanded `v1alpha1` schema, each Functional or Quality Requirement `verification` item is exactly one of:

1. the existing inline form, with `scenario` and optional local `id`; or
2. a reference form containing exactly one `scenario-ref` whose value is a Structured Behaviour ID.

```yaml
verification:
  - scenario: A malformed URL is rejected with a reason
    id: REJECT-MALFORMED
  - scenario-ref: SB-CANCEL-PAID-ORDER
```

The two forms MUST NOT be combined in one item and MUST NOT carry unknown properties. A `scenario-ref` is the canonical authored relationship from a Functional or Quality Requirement to a Structured Behaviour. “Verifies” and all other reverse views are derived and MUST NOT be authored.

Inline verification remains conforming. A repository MAY mix inline and referenced entries within one Requirement, which permits incremental migration without duplicating the same scenario in both forms. The same Structured Behaviour MAY verify more than one Requirement.

An author MUST NOT represent the same expected behaviour as both an inline `scenario` and a `scenario-ref` in the same Requirement. Whether two differently worded entries are semantically the same is a review question and not a deterministic validation rule.

### Structured Behaviour identity and citations

A Structured Behaviour is a Product Artifact. It has its own immutable ID, lifecycle, provenance, content digest, Product Change history, graph node and citation target under the existing contracts.

A consumer that relies on behaviour carried by a `scenario-ref` MUST cite each referenced Structured Behaviour on which it relies directly. Citing the parent Requirement alone records reliance on the obligation, not on the referenced behaviour. This semantic-dependency obligation is enforced by review: implementations MAY suggest a suspected omission for human review, but MUST NOT emit a deterministic conformance diagnostic for citation completeness ([Citation Contract](../spec/citation-contract.md#population-aware-consumer-verification)).

A direct Structured Behaviour citation uses the existing whole-artifact digest and no anchor:

```text
pdac:cite id="SB-CANCEL-PAID-ORDER" digest="sha256:<64 lowercase hex digits>"
```

This RFC does not change v0.1 anchor semantics. An anchor on a Functional or Quality Requirement continues to address an inline `verification[].id`, and the citation digest continues to cover the whole parent artifact. `scenario-ref` does not introduce an anchor in the parent Requirement: the referenced Structured Behaviour is cited by its own ID.

An anchor on a Structured Behaviour does not resolve and produces the existing `PRODUCT063` diagnostic unless a later specification revision defines anchors within that artifact kind.

### Canonical relationships

The canonical relationship vocabulary gains these rows:

| Source | Field | Allowed targets |
| --- | --- | --- |
| Functional Requirement | `verification[].scenario-ref` | Structured Behaviour |
| Quality Requirement | `verification[].scenario-ref` | Structured Behaviour |
| Structured Behaviour | `illustrates` | Use Case, Business Rule, Constraint |
| Structured Behaviour | `uses-terms` | Domain Term |

Array-member relationship fields use the existing `[]` attribution convention. `scenario-ref` relationship diagnostics (`PRODUCT006`, `PRODUCT007`, `PRODUCT008` and `PRODUCT024`) MUST report `field` as `verification[].scenario-ref`, just as a Journey step relationship reports `steps[].use-case`. Schema diagnostics such as `PRODUCT002` continue to report their own instance paths.

Every reverse view is derived. In particular, implementations MAY display the Requirements verified by a Structured Behaviour and the Structured Behaviours illustrating a Use Case, Business Rule or Constraint. Those reverse relationships MUST NOT be authored.

### Reachability and impact

Structured Behaviour edges participate in the Product Graph and in the undirected reachability definition under the same rule as existing canonical product relationships.

Consequently, a Requirement verified by a Structured Behaviour is connected to the behaviour's source Use Cases, Business Rules and Constraints, and a change to a Structured Behaviour is included in structural impact analysis through those authored edges. Structural reachability continues to make no semantic impact claim.

### Validation and diagnostics

This RFC allocates no new diagnostic codes.

Existing schema, identity, relationship, lifecycle and body-section diagnostics apply to Structured Behaviour and the new relationships. In particular:

- `PRODUCT005` and `PRODUCT023` cover duplicate global Structured Behaviour IDs in the baseline and Product Change overlay;
- `PRODUCT006` covers an unresolved `illustrates`, `uses-terms` or `scenario-ref` target;
- `PRODUCT007` covers the source relationship entry whose target has a known but disallowed artifact type; when prefix typing also makes the target artifact violate ID/type alignment, an implementation MUST emit both `PRODUCT004` against the target artifact and `PRODUCT007` against the source relationship entry;
- `PRODUCT008` covers an active artifact referencing a retired target;
- `PRODUCT009` covers a missing or out-of-order required Structured Behaviour body section;
- `PRODUCT024` covers removal that leaves one of the new relationships dangling; and
- `PRODUCT063` covers an anchor that does not resolve within a Structured Behaviour.

The relationship sets for the knowledge warnings are exact:

- For `PRODUCT105`, a non-retired Business Rule MUST be treated as consumed if and only if it has at least one valid outgoing `Business Rule.applies-to` relationship, incoming `Use Case.governed-by` relationship or incoming `Functional Requirement.derived-from` relationship, and the artifact authoring that relationship is non-retired. An incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer.
- For `PRODUCT106`, a non-retired Domain Term MUST be treated as used if and only if it has at least one valid incoming `uses-terms` relationship authored by a non-retired Use Case or Structured Behaviour. A valid `Structured Behaviour.uses-terms` relationship from a non-retired source therefore MUST suppress `PRODUCT106` for its target.

Retired Business Rules and Domain Terms MUST be excluded from the `PRODUCT105` and `PRODUCT106` warning populations. An active Structured Behaviour that references one still produces `PRODUCT008`, but the retired target does not receive either warning.

Whether clauses leak implementation detail, two entries express the same behaviour, explanatory prose restates canonical clauses, or a consumer omitted a semantic dependency remains review-enforced rather than a deterministic diagnostic.

### Citations and consumer projections

The Citation Contract's Product Artifact target set expands to include Structured Behaviour IDs. Digest computation, carriers, statuses, precedence and delivery ownership are otherwise unchanged.

An implementation MAY render a consumer-specific projection from an accepted Structured Behaviour. A projection is generated, non-canonical consumer material and MUST carry a citation to the Structured Behaviour from which its product semantics came. Generating a projection MUST NOT create, approve, apply or accept a Product Change and MUST NOT claim that any test was implemented or executed.

The following mappings are non-normative examples:

| PDaC | OpenSpec-like consumer | Spec Kit-like consumer | EARS-like consumer | Gherkin-like consumer |
| --- | --- | --- | --- | --- |
| Structured Behaviour title | Scenario heading | Acceptance-scenario label | Requirement label | Scenario name |
| `given[]` | GIVEN clauses | Given clause | precondition clause | Given/And steps |
| `when` | WHEN clause | When clause | WHEN trigger | When step |
| `then[]` | THEN clauses | Then clause | THE SYSTEM SHALL responses | Then/And steps |
| Structured Behaviour citation | scenario-adjacent comment or ledger | scenario-adjacent comment or ledger | requirement-adjacent comment or ledger | tag, comment or sidecar supported by the consumer |

For example, an OpenSpec-like Markdown projection could bind one native Scenario to the exact accepted behaviour it elaborates:

```markdown
#### Scenario: Cancel a paid order while cancellation remains available

- **GIVEN** the order is in the PAID state
- **AND** the cancellation window remains open
- **WHEN** the customer requests cancellation
- **THEN** the order enters the CANCELLED state
- **AND** a refund is requested

<!-- pdac:cite id="SB-CANCEL-PAID-ORDER" digest="sha256:<64 lowercase hex digits>" -->
```

Provider-specific syntax and validity remain the provider's responsibility. PDaC conformance tests MUST NOT require OpenSpec, Spec Kit, Kiro, Cucumber or any other named consumer.

### Schema and specification changes

`schemas/v1alpha1/common.schema.json` adds:

- `structuredBehaviourId` with the `SB-` prefix;
- `SB-` to `productArtifactId`;
- `structured-behaviour` to `productArtifactType`;
- an ID definition for the allowed `illustrates` targets; and
- the expanded verification-item union.

`schemas/v1alpha1/structured-behaviour.schema.json` defines the artifact contract above and MUST reject a `given[]`, `when` or `then[]` value that begins with the case-sensitive ASCII word `GIVEN`, `WHEN`, `THEN` or `AND`. Such a value is a schema violation under `PRODUCT002`.

The Functional and Quality Requirement schemas keep `verification` required and non-empty but use the new inline-or-reference item union. Their relationship target validation recognizes `scenario-ref`. Existing Requirement fields and target vocabularies are otherwise unchanged.

The Product Change operation schema accepts `SB-` as a Product Artifact ID. The exhaustive frontmatter reference MUST be updated by hand against the changed schemas, which remain authoritative.

The specification chapters for artifacts, identifiers, relationships, validation, citations, conformance, terminology and maturity will be updated when this RFC is accepted, together with the exhaustive Frontmatter reference and `conformance/README.md`. Relationships will define the exact `PRODUCT105` and `PRODUCT106` relationship sets and the array-member attribution convention; Validation will define the retired-target warning exclusion. Terminology will add Structured Behaviour to the Product Artifact definition and distinguish an inline verification scenario from a `scenario-ref` entry. The Citation Contract will carry the normative distinction between reliance on a Requirement obligation and reliance on a referenced Structured Behaviour. The conformance index will update the artifact-kind count and list the added cases. `schemas/README.md` and `MATURITY.md` will carry the compatibility clarifications under Release and serialization.

### Conformance

The v0.2 conformance suite adds at least these positive cases:

- one Structured Behaviour referenced from a Functional Requirement;
- one Structured Behaviour referenced from a Quality Requirement;
- one Requirement mixing an existing inline scenario with a `scenario-ref`;
- one Structured Behaviour illustrating each allowed target type across the fixture set;
- one Structured Behaviour using a Domain Term, demonstrating that the relationship counts as usage for `PRODUCT106`;
- a valid Product Change adding a Structured Behaviour;
- a valid Product Change modifying an existing Structured Behaviour;
- a direct current citation of a Structured Behaviour;
- a direct citation becoming stale when the cited Structured Behaviour changes; and
- an unchanged Structured Behaviour citation remaining current when a different Requirement or Structured Behaviour changes.

Existing inline-only verification remains covered and conforming. The mixed-form case is additional coverage, not a migration requirement.

Relationship-negative coverage exercises each new authored relationship field, `verification[].scenario-ref`, `illustrates` and `uses-terms`, against an unknown target (`PRODUCT006`), an active source referencing a retired target (`PRODUCT008`), and removal of the target leaving the relationship dangling in a Product Change overlay (`PRODUCT024`). Each diagnostic is asserted with the source artifact, exact field and target required by the existing attribution contract, including the exact `verification[].scenario-ref` field spelling.

The suite adds no `PRODUCT007` case for these new fields. Their schemas admit only target prefixes allowed by the relationship, so a resolving artifact with an admitted prefix but a disallowed type necessarily also violates that artifact's ID/type alignment. An implementation MUST emit both `PRODUCT004` against the target artifact and `PRODUCT007` against the source relationship entry. The two diagnostics have different subjects, but a fixture expecting both cannot isolate one normative clause as required by the conformance-case convention. This exclusion does not make `PRODUCT007` inapplicable.

Additional negative coverage includes a forbidden literal semantic-keyword prefix (`PRODUCT002`), both a missing and an out-of-order required Structured Behaviour body section (`PRODUCT009`), an anchored Structured Behaviour citation (`PRODUCT063`), and an active Business Rule with no outgoing `applies-to` relationship whose only incoming association is an `illustrates` edge from a Structured Behaviour, demonstrating that the rule still receives `PRODUCT105`. The `illustrates` and `uses-terms` retired-target cases use a retired Business Rule and retired Domain Term respectively and assert `PRODUCT008` alone, confirming that retired targets are outside the `PRODUCT105` and `PRODUCT106` warning populations. Separate warning cases assert that a retired Use Case's `governed-by` relationship does not suppress `PRODUCT105` for an active Business Rule and a retired Structured Behaviour's `uses-terms` relationship does not suppress `PRODUCT106` for an active Domain Term.

The existing `artifact-kinds-valid` case gains one kind, not two. Existing zero-diagnostic fixtures remain valid; their expected results change only when a new authored edge intentionally affects the fixture's graph or warning population.

The semantic-dependency citation obligation, implementation-independence rule, no-restatement rules and semantic duplication rule are implementation-conformance criteria verified by review. A fixture cannot determine what prose or consumer text means without making AI judgment normative.

## Impact

- **On existing conformant repositories:** no migration and no changed meaning. Existing repositories remain valid and may continue using inline verification and whole-Requirement scenario anchors.
- **On repositories adopting the new kind:** they may add Structured Behaviour artifacts incrementally and may replace inline verification items with `scenario-ref` entries through ordinary Product Changes.
- **On existing implementations:** v0.2 conformance requires version-dispatched schema loading, one new artifact parser, graph relationships, Product Change support, citation target support and graph/impact projections. Provider-specific rendering is optional and outside conformance.
- **On the conformance tests:** existing valid documents remain valid, while the artifact-kind, relationship, validation and citation cases expand as listed above. No new diagnostic code is introduced.
- **On downstream integrations:** OpenSpec, Spec Kit, Kiro, BDD and other adapters may cite Structured Behaviour directly and project its clauses into native scenario syntax. They retain ownership of their documents and validation.

## Alternatives considered

### Introduce a new `v1alpha2` serialization

Rejected for this RFC. The schema changes are backward compatible under the explicit definition proposed above: every previously valid document remains valid with the same interpretation, while new documents may use the expanded vocabulary. Creating a second alpha serialization would require migration despite no existing document becoming invalid.

The v0.1 Git tag preserves the earlier schemas and the v0.2 tag will carry the expanded schemas. Because `v1alpha1` alone no longer selects one accepted document set, this RFC also requires conformance claims to identify the method/spec version and amends the versioning documentation rather than leaving implementations to infer the distinction.

### Expand inline `verification[]` entries only

Add `given`, `when` and `then` to the existing nested scenario record without a new Artifact kind.

Rejected as the complete solution. It improves formulation but keeps whole-Requirement citation granularity, prevents independent lifecycle and provenance, and cannot make the behaviour an ordinary graph and Product Change target. The retained inline form remains appropriate for simple acceptance criteria that do not need those properties.

### Change anchored citations to digest only the anchored scenario

Rejected for v0.2. V0.1 explicitly defines the digest as the whole target artifact's bytes. Changing that meaning would invalidate existing anchored citations, require a canonical serialization of a nested YAML value, complicate marker-block embedding and overload one citation record with two digest domains. A standalone Structured Behaviour obtains fine-grained identity using the existing digest contract.

### Make Gherkin or EARS canonical

Rejected. Both are useful consumer formulations, but either would privilege a delivery notation and import syntax whose evolution PDaC does not govern. The proposed semantic clauses project to those formats without making either authoritative.

### Generate executable tests

Rejected as a PDaC responsibility. Structured Behaviour provides product-level examples from which an adapter MAY generate a Gherkin, EARS or framework-native starting point. Test harnesses, fixtures, step bindings, execution and evidence remain delivery concerns.

### Make `illustrates` optional

Rejected. Independent identity should not create context-free examples. The required relationship states which accepted Use Case, Business Rule or Constraint the example makes concrete and gives every Structured Behaviour a sanctioned graph position without forcing it to verify a Requirement.

### Add Domain Lifecycle in this RFC

Deferred to a separate RFC targeting specification 0.3 after the challenge review showed that state-transition modelling introduces a distinct evidence requirement, local identity model, validation surface and set of design choices. The follow-up will be exercised against at least one real lifecycle in a real Product Definition before acceptance. It may add `covers-transition` to Structured Behaviour without changing the semantics accepted here. This RFC neither defines Lifecycle semantics nor reserves diagnostic codes for that future decision.

### Wait for a general custom-profile mechanism

Rejected as a prerequisite. Structured Behaviour promotes semantics already mandatory on every Functional and Quality Requirement and remains optional to author. A future custom-profile mechanism remains valuable for specialized vocabularies, but this kind can be specified and tested in the reference profile independently.

### Defer Structured Behaviour to specification 0.3.0

Rejected. The independent citation-granularity problem exists now, and no identified 0.2 dependency prevents this backward-compatible expansion of the draft alpha serialization. Version 0.3 should respond to implementation and adoption evidence from 0.2 rather than postpone collecting it.

## Consequences

PDaC 0.2 gains an explicit, citable unit of accepted observable behaviour. Requirements can keep lightweight inline criteria or refer to reusable behaviours, and delivery consumers can cite the exact behaviour on which they rely rather than pinning a whole Requirement.

The reference profile grows by one artifact kind, validators must recognize a broader schema and graph, and repositories may create more artifacts. Requiring separate artifacts for alternative contexts and outcomes can produce multiplicative growth where a behaviour has many meaningful combinations. The proposal accepts that cost in exchange for unambiguous conjunctive semantics; authors retain inline verification for simple criteria that do not need independent identity.

The proposal contains its cost by allocating no new diagnostics, preserving inline verification, making Structured Behaviour optional to author and leaving consumer rendering and executable verification outside conformance.

This is a normative change under [CONTRIBUTING.md](../CONTRIBUTING.md). It remains public and requires maintainer consensus and resolution of substantive feedback. The temporary stabilization note suspends a fixed minimum elapsed time while the specification is pre-stable; it does not bypass review.

[openspec-writing]: https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md
[speckit-template]: https://github.com/github/spec-kit/blob/main/templates/spec-template.md
[kiro-requirements]: https://kiro.dev/docs/specs/feature-specs/requirements-first/
