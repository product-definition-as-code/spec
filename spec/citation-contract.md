# Citation Contract

A **citation** is a machine-verifiable reference from any consumer document - a Spec-Driven Development (SDD) spec, a task, an agent prompt file, a design doc - to canonical product text. This chapter uses "the consumer" for all of them.

The citation contract is the delivery boundary of Product Definition as Code. Consumers do not re-state product knowledge; they cite it. A citation records what was cited and at what content digest, so that drift between a consumer document and the canonical model is machine-detectable rather than silent.

![The citation chain and what happens when it drifts. A product artifact, UC-CHECKOUT-001, carrying accepted intent, is cited by an SDD specification, spec checkout-flow, which is implemented by code or another delivery artifact, which produces verification or delivery evidence. A panel lists four citation statuses: current, where the citation matches the accepted artifact; stale, where the cited artifact changed and the specification needs review; unresolved, where the citation cannot be resolved; and tampered, where an embedded block differs from canonical text at the recorded digest. A drift scenario shows UC-CHECKOUT-001 changing, the citation becoming stale, and a consumer reviewing the specification, marked human-controlled, with two rules stated: no automatic rewrite, and PDaC does not prescribe implementation.](../assets/diagrams/pdac-5-citation-and-drift.png)

_Figure PDaC-5 - how does PDaC connect to a consumer without replacing it? Non-normative; this chapter is authoritative._

## Citation record

A citation is a record, not a block of text. It MUST carry:

| Field    | Presence | Meaning                                                                                             |
| -------- | -------- | --------------------------------------------------------------------------------------------------- |
| `id`     | required | the target artifact's stable ID (see [Identifiers](identifiers.md))                                 |
| `digest` | required | the whole target artifact's content digest (see [Validation → Digests](validation.md#digests))     |
| `anchor` | optional | a stable address within the target artifact (see Anchors below)                                     |

## Citation carriers and canonical writing

A consumer document MUST use exactly one carrier: one or more comment payloads in the document, or one adjacent YAML sidecar. It MUST NOT combine them.

A comment payload occupies one physical line and uses this exact attribute order, separated by one or more ASCII spaces or tabs:

```text
pdac:cite id="<artifact-id>" digest="<digest>" [anchor="<anchor>"]
```

Values are double-quoted and have no escape syntax. Unknown, repeated or out-of-order attributes are invalid. Discovery scans text lines for the exact `pdac:cite` token followed by payload-like `id=` text; a malformed candidate produces `PRODUCT067` rather than disappearing as prose. The payload rides inside the host format's native comment, whose opener and closer carry no citation semantics.

For a consumer named `<stem>.<extension>`, the adjacent sidecar is `<stem>.citations.yml`, replacing only the final extension; a consumer with no extension appends `.citations.yml`. The sidecar MUST satisfy the normative [`citation-sidecar` schema](../schemas/v1alpha1/citation-sidecar.schema.json): one YAML 1.2 document, exactly one top-level `citations` key, and a non-empty sequence of closed citation records. Duplicate YAML keys, aliases, anchors, tags and merge keys are forbidden. The corresponding consumer file MUST exist. A ledger entry's location is its one-based sequence position.

```yaml
citations:
  - id: FR-CHECKOUT-001
    digest: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    anchor: S1
```

A conforming writer emits only these forms. Payload attributes are written in `id`, `digest`, `anchor` order with one ASCII space between elements. Sidecars are written in mapping form with `citations`, preserving requested entry order and field order `id`, `digest`, `anchor`. A writer MUST migrate a legacy bare-sequence sidecar when updating it and MUST NOT emit the legacy brace form, a bare-sequence sidecar, mixed carriers or a scenario-only digest. Readers MAY accept legacy forms as explicitly non-conforming extensions.

Payload verification and impact output report the consumer file and one-based `line`; sidecars report the ledger file and one-based `entry`.

## Anchors

An anchor addresses a location within the target artifact. In v0.1, an anchor is a verification scenario's stable `id` (see [Frontmatter reference → verification](frontmatter-reference.md)): a citation with `anchor: S1` on target `FR-X` addresses the scenario whose `id` is `S1` within `FR-X`. Scenario anchors make partial dependency scope expressible as a set of cited scenario ids instead of prose.

An anchor does not narrow digest scope. Every citation digest covers the whole target artifact. A verifier resolves the target and anchor, then compares the recorded digest with the whole artifact's recomputed digest. Any normalized-byte edit to that artifact makes the citation stale, including an edit to another scenario or to artifact prose; an edit to another artifact does not. The anchor tells a reviewer what was relied on, while whole-artifact staleness conservatively requires review of any change to its containing requirement ([RFC 0077](../rfcs/0077-whole-artifact-digests-for-anchored-citations.md)).

Section-slug anchors (addressing a required body section by its heading slug) are deferred to a follow-up. Restricting v0.1 anchors to scenario ids keeps citation resolution deterministic ([manifesto](../MANIFESTO.md) principle 10) and avoids non-ASCII heading canonicalization.

![Deriving verification from the definition, and keeping it aligned. In the first band, a requirements artifact, FR-REFUND-001, carrying a verification obligation and derived from BR-REFUND-001, leads through Gherkin scenarios, executable tests and evidence to human assessment. In the second band, the definition moves from D1 to D2: a specification citing D1 has its citation go stale, the digest is updated so the specification now cites D2, affected scenarios are reviewed, new or revised Gherkin scenarios are written, and tests are implemented and executed. A note reads: explanatory projection, arrows clarify derivation and continuity, authored relationships remain defined by relationships.md. The closing line reads: PDaC derives traceable verification scenarios from accepted product intent; it proposes and keeps them aligned, while completeness and execution remain outside PDaC.](../assets/diagrams/pdac-8-verification-derivation-and-continuity.png)

_Figure PDaC-8 - how does a scenario-anchored citation stay aligned when the definition changes? Non-normative; [Artifacts](artifacts.md) and the [Frontmatter reference](frontmatter-reference.md) are authoritative for verification scenarios._

## Embedding

Embedding is a projection of a citation, not its definition. A consumer MAY additionally embed the cited canonical text in its document; when it does:

- the opening marker MUST carry a valid citation payload and the closing marker MUST carry the exact `/pdac:cite` token in the same host comment style;
- the embedded text MUST be byte-identical to the canonical text at the recorded `digest`;
- the embedded block MUST be treated as read-only and regenerable.

A consumer that embeds canonical text without a citation record, or whose embedded text differs from canonical content at the recorded digest, is non-conforming (see `PRODUCT062` below). Because the digest covers the whole artifact, an anchored embedded projection MUST embed the whole artifact. A scenario-only projection cannot be verified by that digest and is `PRODUCT062`.

A tool decides whether an embedded block is faithful by recomputing the digest of the embedded text and comparing it to the recorded `digest`, under the same normalization ([Validation → Digests](validation.md#digests)). The comparison is against the recorded digest, never against the target's current content, so a projection that was edited by hand stays detectable after the cited text has moved.

The embedded byte range begins immediately after the line ending that terminates the opening-marker line and ends immediately before the first byte of the closing-marker line. The marker lines and the opening marker's terminating line ending are not part of the projection. A line ending immediately before the closing marker is part of the projection, so the projection preserves the artifact's final line ending when the artifact has one.

## Statuses

A conforming tool MUST compute, deterministically, exactly one status per citation:

| Status       | Meaning                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `current`    | The target resolves and its recomputed digest matches the recorded `digest`.                    |
| `stale`      | The target resolves, but canonical content changed since the citation was recorded.              |
| `tampered`   | Only for embedded projections: the block differs from canonical content at the recorded digest. |
| `unresolved` | The target `id` does not resolve, or the `anchor` does not resolve within the target.            |

Digest recomputation uses the normalization defined in [Validation → Digests](validation.md#digests). Staleness is judged exclusively by the whole-artifact digest of the cited target: unrelated commits, edits to other artifacts and generated-file churn MUST NOT make a citation stale. Any normalized-byte edit to the target artifact does.

Applying a Product Change computes the product diff between the baseline and the applied result ([Product Changes → Apply](product-changes.md#apply)). The affected citation set is derived from that diff and the citation index, not from the change's declared `operations`: a citation goes stale because the text it cited effectively changed, never because a change said it would.

### Precedence

More than one condition can hold for the same citation: an embedded block edited by hand whose cited text has since moved satisfies the `tampered` and the `stale` condition at once. Because exactly one status is computed, the conditions are evaluated in this order and the first that holds decides:

| Order | Condition                                                                                    | Status       | Diagnostic   |
| ----- | -------------------------------------------------------------------------------------------- | ------------ | ------------ |
| 1     | The recorded `digest` is not a well-formed digest.                                           | `unresolved` | `PRODUCT042` |
| 2     | The target `id` does not resolve.                                                            | `unresolved` | `PRODUCT060` |
| 3     | The `anchor` does not resolve within the target.                                             | `unresolved` | `PRODUCT063` |
| 4     | An embedded projection is not byte-identical to the canonical text at the recorded `digest`. | `tampered`   | `PRODUCT062` |
| 5     | The target's recomputed digest differs from the recorded `digest`.                           | `stale`      | `PRODUCT061` |
| 6     | None of the above.                                                                           | `current`    | none         |

A citation reports the diagnostic of its status and no other: a tampered projection whose target has also moved is `PRODUCT062`, and `PRODUCT061` MUST NOT be emitted alongside it.

Tampering outranks staleness because it is a property of the consumer document that no edit to the canonical text can resolve, while staleness is resolved by the same act that repairs the projection: re-embedding the canonical text and recording its digest. The order also stops an unrelated canonical edit from turning an error into a warning, which would let a consumer document lower the severity of its own defect. Resolution failures are evaluated first because a statement about content presupposes the content: with no well-formed digest, no target, or no anchor within the target, there is nothing to compare.

## Diagnostics

| Code         | Severity | Condition                                                                                                |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------- |
| `PRODUCT042` | error    | Invalid or unverifiable citation digest.                                                                 |
| `PRODUCT060` | error    | Unresolved citation: target `id` does not resolve.                                                      |
| `PRODUCT061` | warning  | Stale citation: target resolves but canonical content changed since the citation was recorded.           |
| `PRODUCT062` | error    | Tampered embedded projection: the embedded block differs from canonical content at the recorded digest. |
| `PRODUCT063` | error    | Anchor not found: the target resolves but the named anchor does not exist within it.                    |
| `PRODUCT064` | error    | Current consumer document has no scope declaration during population-aware verification.               |
| `PRODUCT065` | error    | Consumer document declares `bound` but contains no citations.                                           |
| `PRODUCT066` | error    | Invalid exemption: empty reason or an exempt document containing a citation.                            |
| `PRODUCT067` | error    | Malformed citation carrier, missing sidecar consumer, or payload/sidecar conflict.                       |

`PRODUCT061` is a warning; a repository MAY make warnings fail the command through [`validation.warnings-as-errors`](configuration.md). Tools MUST NOT apply per-artifact-type severity defaults: risk policy belongs to the repository, not the kernel.

## Population-aware consumer verification

A conforming implementation MAY provide no consumer-framework integration. When it claims **population-aware PDaC verification** for an integration, the integration MUST satisfy this section ([RFC 0042](../rfcs/0042-consumer-binding-for-sdd-alignment.md)).

A consumer integration is an adapter that deterministically enumerates an external framework's current native consumer documents without taking ownership of them. It MUST document its enumeration rule, return the same population for identical repository content and integration configuration, exclude archived or historical documents by default, and report provider identity and integration version. Framework paths and lifecycle concepts remain adapter concerns and MUST NOT enter the Product Definition.

Every current document in the enumerated population has exactly one explicit scope declaration:

| Value | Contract |
| --- | --- |
| `bound` | The document contains product-semantic dependencies and carries at least one citation. |
| `exempt` | The document has no dependency requiring binding and carries a non-empty human-authored reason and no citations. |

The serialization and location of that declaration are adapter-defined but MUST be inspectable as repository data without executing code. Absence is **unclassified** and produces `PRODUCT064`; a tool MUST NOT infer exemption from no citations, file name, generated content or AI assessment. A bound document with no citations produces `PRODUCT065`. An empty exemption reason or an exempt document containing a citation produces `PRODUCT066`. A tool MUST NOT create or renew an exemption without an explicit human request.

Population-aware verification accounts for every enumerated current document before success. It reports provider and integration version; totals for current, bound, exempt and unclassified documents; citation totals by status; and the source location and diagnostic for every non-passing document. A valid exempt document remains visible. Zero discovered citations cannot succeed when any current document is bound or unclassified. Citation statuses and precedence remain exactly those above.

Success establishes only that the declared population was accounted for, every document was classified, every bound document carried at least one citation and every recorded citation was verified. It does not establish citation completeness, semantic agreement, implementation correctness or delivery status. Tools may suggest omissions for human review but MUST NOT report such suggestions as deterministic conformance results.

A stale citation requires review. A tool MUST NOT renew its digest, rewrite consumer text or change the canonical Product Definition automatically. The consumer owner either revises and deliberately re-cites accepted intent or proposes a Product Change; acceptance remains human-controlled.

## Semantic contradiction

Semantic contradiction between a citation and its surrounding consumer text is explicitly non-normative. Tools MAY flag suspected contradictions for human review; such findings are never a conformance criterion. Deterministic tools enforce structure, AI does semantic work, humans decide ([manifesto](../MANIFESTO.md) principle 7).

## Delivery boundary

Consumers of the model (SDD frameworks, AI agents, human teams) retain native ownership of their own artifacts and workflow. A consumer MUST NOT write to the canonical product model. A consumer MAY propose a [Product Change](product-changes.md) when implementation reveals a contradiction; a human decides whether to approve and accept it ([manifesto](../MANIFESTO.md) principle 9). Acceptance is a human decision: tools MUST NOT merge, auto-approve or self-merge model changes.

A cited model may live in a repository of its own: [Conformance → Topologies](conformance.md#topologies) defines the co-located and dedicated topologies and the pointer a consuming repository carries to a dedicated model repository. Cross-repository citation *resolution* is a different question and remains out of scope for v0.1: how a tool verifies a citation digest against a model repository the consumer does not contain, and what that tool reports when the repository is unreachable, are deferred ([RFC 0021](../rfcs/0021-deployment-topologies.md)). Citations resolve within one repository in v0.1.

## Generated context documents

A repository MAY generate a readable document composed entirely of citations, for the convenience of a consumer that prefers a single bundle over resolving citations individually. Such a generated document is non-canonical, reproducible from the citations it contains, and carries an explicit size budget it never silently exceeds. It is not a PDaC artifact and is not required for conformance; the citation contract is the normative surface, not any generated bundle.
