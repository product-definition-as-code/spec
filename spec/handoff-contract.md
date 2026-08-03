# Citation Contract

A **citation** is a machine-verifiable reference from any consumer document — a Spec-Driven
Development (SDD) spec, a task, an agent prompt file, a design doc — to canonical product text. This
chapter uses "the consumer" for all of them.

The citation contract is the delivery boundary of Product Definition as Code. Consumers do not
re-state product knowledge; they cite it. A citation records what was cited and at what content
digest, so that drift between a consumer document and the canonical model is machine-detectable
rather than silent.

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

The pilot will exercise all three forms; a follow-up normalizes. The spec defines the citation
record shape, not a mandatory serialization.

## Anchors

An anchor addresses a location within the target artifact. In v0.1, an anchor is a verification
scenario's stable `id` (see [Frontmatter reference → verification](frontmatter-reference.md)): a
citation with `anchor: S1` on target `FR-X` addresses the scenario whose `id` is `S1` within
`FR-X`. This makes partial scope expressible as a set of cited scenario ids instead of prose.

Section-slug anchors (addressing a required body section by its heading slug) are deferred to a
follow-up. Restricting v0.1 anchors to scenario ids keeps citation resolution deterministic
([manifesto](../MANIFESTO.md) principle 10) and avoids non-ASCII heading canonicalization.

## Embedding

Embedding is a projection of a citation, not its definition. A consumer MAY additionally embed the
cited canonical text in its document; when it does:

- the embedded block MUST be delimited by machine-readable markers carrying the citation record;
- the embedded text MUST be byte-identical to the canonical text at the recorded `digest`;
- the embedded block MUST be treated as read-only and regenerable.

A consumer that embeds canonical text without a citation record, or whose embedded text differs
from canonical content at the recorded digest, is non-conforming (see `PRODUCT062` below).

## Statuses

A conforming tool MUST compute, deterministically, exactly one status per citation:

| Status       | Meaning                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `current`    | The target resolves and its recomputed digest matches the recorded `digest`.                    |
| `stale`      | The target resolves, but canonical content changed since the citation was recorded.              |
| `tampered`   | Only for embedded projections: the block differs from canonical content at the recorded digest. |
| `unresolved` | The target `id` or `anchor` does not resolve.                                                    |

Digest recomputation uses the normalization defined in
[Validation → Digests](validation.md#digests). Staleness is judged exclusively by the digest of the
cited target: unrelated commits, unrelated artifact edits and generated-file churn MUST NOT make a
citation stale.

## Diagnostics

| Code         | Severity | Condition                                                                                                |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------- |
| `PRODUCT042` | error    | Invalid or unverifiable citation digest.                                                                 |
| `PRODUCT060` | error    | Unresolved citation: target `id` or `anchor` does not resolve.                                          |
| `PRODUCT061` | warning  | Stale citation: target resolves but canonical content changed since the citation was recorded.           |
| `PRODUCT062` | error    | Tampered embedded projection: the embedded block differs from canonical content at the recorded digest. |
| `PRODUCT063` | error    | Anchor not found: the target resolves but the named anchor does not exist within it.                    |

`PRODUCT061` is a warning; a repository MAY escalate it via its existing `warnings-as-errors`
configuration. Tools MUST NOT apply per-artifact-type severity defaults: risk policy belongs to the
repository, not the kernel.

## Semantic contradiction

Semantic contradiction between a citation and its surrounding consumer text is explicitly
non-normative. Tools MAY flag suspected contradictions for human review; such findings are never a
conformance criterion. Deterministic tools enforce structure, AI does semantic work, humans decide
([manifesto](../MANIFESTO.md) principle 7).

## Delivery boundary

Consumers of the model (SDD frameworks, AI agents, human teams) retain native ownership of their
own artifacts and workflow. A consumer MUST NOT write to the canonical product model. A consumer MAY
propose a revision — a pull request — when implementation reveals a contradiction; a human decides
whether to merge it ([manifesto](../MANIFESTO.md) principle 9). Merging is a human decision: tools
MUST NOT merge, auto-approve or self-merge model changes.

Cross-repository citation resolution — where a cited model lives in a different repository than the
consumer document — is out of scope for this chapter and tracked under
[RFC #2 (deployment topologies)](https://github.com/product-definition-as-code/spec/issues/2).

## Handoff (non-normative)

A "handoff" remains available as a non-normative convenience: a generated document composed entirely
of citations, with a stated size budget. It is not a PDaC artifact, carries no `HOF-` ID, and is not
required for conformance. Consumers that find a generated citation bundle useful MAY produce one;
the citation contract is the normative surface, not the bundle.
