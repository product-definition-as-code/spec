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
| `digest` | required | the content digest of the cited canonical text (see [Validation → Digests](validation.md#digests))  |
| `anchor` | optional | a stable address within the target artifact (see Anchors below)                                     |

A citation MAY exist in any of three forms; v0.1 does not mandate one:

- an **inline structured reference** embedded in the consumer document;
- a **Markdown marker block** delimiting an embedded projection (see Embedding below);
- a **YAML sidecar ledger** accompanying the consumer document.

The spec defines the citation record shape, not a mandatory serialization.

## Anchors

An anchor addresses a location within the target artifact. In v0.1, an anchor is a verification scenario's stable `id` (see [Frontmatter reference → verification](frontmatter-reference.md)): a citation with `anchor: S1` on target `FR-X` addresses the scenario whose `id` is `S1` within `FR-X`. Scenario anchors make partial scope expressible as a set of cited scenario ids instead of prose.

Section-slug anchors (addressing a required body section by its heading slug) are deferred to a follow-up. Restricting v0.1 anchors to scenario ids keeps citation resolution deterministic ([manifesto](../MANIFESTO.md) principle 10) and avoids non-ASCII heading canonicalization.

![Deriving verification from the definition, and keeping it aligned. In the first band, a requirements artifact, FR-REFUND-001, carrying a verification obligation and derived from BR-REFUND-001, leads through Gherkin scenarios, executable tests and evidence to human assessment. In the second band, the definition moves from D1 to D2: a specification citing D1 has its citation go stale, the digest is updated so the specification now cites D2, affected scenarios are reviewed, new or revised Gherkin scenarios are written, and tests are implemented and executed. A note reads: explanatory projection, arrows clarify derivation and continuity, authored relationships remain defined by relationships.md. The closing line reads: PDaC derives traceable verification scenarios from accepted product intent; it proposes and keeps them aligned, while completeness and execution remain outside PDaC.](../assets/diagrams/pdac-8-verification-derivation-and-continuity.png)

_Figure PDaC-8 - how does a scenario-anchored citation stay aligned when the definition changes? Non-normative; [Artifacts](artifacts.md) and the [Frontmatter reference](frontmatter-reference.md) are authoritative for verification scenarios._

## Embedding

Embedding is a projection of a citation, not its definition. A consumer MAY additionally embed the cited canonical text in its document; when it does:

- the embedded block MUST be delimited by machine-readable markers carrying the citation record;
- the embedded text MUST be byte-identical to the canonical text at the recorded `digest`;
- the embedded block MUST be treated as read-only and regenerable.

A consumer that embeds canonical text without a citation record, or whose embedded text differs from canonical content at the recorded digest, is non-conforming (see `PRODUCT062` below).

A tool decides whether an embedded block is faithful by recomputing the digest of the embedded text and comparing it to the recorded `digest`, under the same normalization ([Validation → Digests](validation.md#digests)). The comparison is against the recorded digest, never against the target's current content, so a projection that was edited by hand stays detectable after the cited text has moved.

## Statuses

A conforming tool MUST compute, deterministically, exactly one status per citation:

| Status       | Meaning                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `current`    | The target resolves and its recomputed digest matches the recorded `digest`.                    |
| `stale`      | The target resolves, but canonical content changed since the citation was recorded.              |
| `tampered`   | Only for embedded projections: the block differs from canonical content at the recorded digest. |
| `unresolved` | The target `id` does not resolve, or the `anchor` does not resolve within the target.            |

Digest recomputation uses the normalization defined in [Validation → Digests](validation.md#digests). Staleness is judged exclusively by the digest of the cited target: unrelated commits, unrelated artifact edits and generated-file churn MUST NOT make a citation stale.

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

`PRODUCT061` is a warning; a repository MAY escalate it via its existing `warnings-as-errors` configuration. Tools MUST NOT apply per-artifact-type severity defaults: risk policy belongs to the repository, not the kernel.

## Semantic contradiction

Semantic contradiction between a citation and its surrounding consumer text is explicitly non-normative. Tools MAY flag suspected contradictions for human review; such findings are never a conformance criterion. Deterministic tools enforce structure, AI does semantic work, humans decide ([manifesto](../MANIFESTO.md) principle 7).

## Delivery boundary

Consumers of the model (SDD frameworks, AI agents, human teams) retain native ownership of their own artifacts and workflow. A consumer MUST NOT write to the canonical product model. A consumer MAY propose a [Product Change](product-changes.md) when implementation reveals a contradiction; a human decides whether to approve and accept it ([manifesto](../MANIFESTO.md) principle 9). Acceptance is a human decision: tools MUST NOT merge, auto-approve or self-merge model changes.

A cited model may live in a repository of its own: [Conformance → Topologies](conformance.md#topologies) defines the co-located and dedicated topologies and the pointer a consuming repository carries to a dedicated model repository. Cross-repository citation *resolution* is a different question and remains out of scope for v0.1: how a tool verifies a citation digest against a model repository the consumer does not contain, and what that tool reports when the repository is unreachable, are deferred ([RFC 0021](../rfcs/0021-deployment-topologies.md)). Citations resolve within one repository in v0.1.

## Generated context documents

A repository MAY generate a readable document composed entirely of citations, for the convenience of a consumer that prefers a single bundle over resolving citations individually. Such a generated document is non-canonical, reproducible from the citations it contains, and carries an explicit size budget it never silently exceeds. It is not a PDaC artifact and is not required for conformance; the citation contract is the normative surface, not any generated bundle.
