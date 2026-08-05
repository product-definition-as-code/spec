# Product Changes

A requested product modification does not directly become a backlog item and MUST NOT silently modify the current model. It becomes a **Product Change**: an explicit, validated delta against the baseline that records the meaning, rationale, scope and affected artifacts of the change.

A Product Change is not a pull request, a delivery container or an implementation state. A pull request is the human review and acceptance boundary for a Product Change; it is not the change itself. Decomposing, scheduling and implementing the work are the concerns of whatever consumes the definition (see the [Citation Contract](citation-contract.md)).

## Structure

A Product Change lives in its own directory, named by its lowercase ID:

```text
docs/product/changes/active/<chg-id>/
├── change.md          # canonical change definition
└── proposed/          # complete proposed future-state artifacts
    └── <same layout as docs/product/model>
```

`change.md` frontmatter contract (schema `product-change`):

```yaml
---
id: CHG-CITATIONS-001
type: product-change
title: Cite canonical product text instead of restating it
status: proposed
base-revision: <git-commit-sha> # the baseline this change was created against
operations:
  add: [BR-CITE-CANONICAL, FR-CITATIONS-001]
  modify: [UC-VALIDATE-001]
  remove: []
---
```

Required body sections: `## Problem`, `## Intended Product Outcome`, `## Rationale`, `## Affected Product Areas`, `## Open Questions`, `## Product Acceptance`, `## Out of Scope`.

Applied and rejected changes are archived under `docs/product/changes/completed/<chg-id>/` and `docs/product/changes/rejected/<chg-id>/`. Archived changes are inert history: they are not compiled into the product graph, and their IDs and proposed artifacts take no part in duplicate detection, reference resolution or operation checks.

## Elaboration

A Product Change is elaborated iteratively while it is `draft` or `proposed`: opened with a partial intent, then widened, narrowed, corrected and revised until it is worth proposing for approval. Several Product Changes MAY be active at once.

Implementations SHOULD use the product graph to support elaboration: surfacing the artifacts a proposed operation would affect, the artifacts that reference them, and the open questions the change has not answered. This is assistance, not authority. A tool MUST NOT resolve an open question, invent a product decision or set `approved` on the author's behalf ([manifesto](../MANIFESTO.md) principles 6 and 7).

## Operations

- Every ID in `operations.add` MUST NOT exist in the baseline, and MUST have a complete proposed future-state artifact under `proposed/`.
- Every ID in `operations.modify` MUST exist in the baseline, and MUST have a complete proposed future-state artifact under `proposed/` using the same ID.
- Every ID in `operations.remove` MUST exist in the baseline. Removed artifacts need no tombstone files.
- Every artifact under `proposed/` MUST be listed in `operations.add` or `operations.modify`.

## Overlay validation

Validating a Product Change MUST compile an **overlay**: the baseline graph with additions added, modifications replaced and removals deleted - without modifying any baseline file - and then apply full structural validation to the overlay. Overlay-specific errors are enumerated in [Validation](validation.md).

While a Product Change is active, the baseline artifacts it touches remain authoritative and unchanged. Concurrent active Product Changes MUST be checked for overlapping `modify`/`remove` sets; an overlap is an error until one change is rebased or withdrawn.

## Lifecycle

`productChangeStatus`: `draft` → `proposed` → `approved` → `applied`, with `rejected` (from `draft` or `proposed`) and `superseded` (from any non-terminal state) as terminal alternatives.

`approved` is a human product decision: the change is judged correct and wanted. It is what authorizes apply. It says nothing about implementation, and there is no status for implementation: whether the accepted intent has been built is a fact about delivery, not about the change ([RFC 0004](../rfcs/0004-delivery-model-reset.md)).

Acceptance is not a status on the change. An applied change enters the accepted Product Definition when a human merges the pull request carrying it (see [Terminology → Accepted](terminology.md)).

A change moved to `approved` while its `## Open Questions` section still contains unresolved questions SHOULD produce a warning (`PRODUCT108`).

## Apply

Apply is the only operation that writes a Product Change into the baseline. Apply:

1. MUST require change status `approved`.
2. MUST revalidate the overlay.
3. MUST check baseline-revision compatibility: if any artifact named in the change's operations changed in the baseline since `base-revision`, apply MUST fail (`PRODUCT027`) until the change is explicitly rebased - its proposed artifacts reviewed against the new baseline and `base-revision` updated.
4. Applies additions, modifications and removals to `docs/product/model`, naming files by lowercase ID.
5. MUST record the applied operations and the resulting content digest of every impacted artifact. This record is the product diff consumed by citation verification and impact analysis.
6. MUST run full structural validation of the resulting model, and MUST leave the working tree untouched if it fails.
7. Sets the change status to `applied` and moves the change directory to `docs/product/changes/completed/<chg-id>/`, preserving its history. An implementation MAY omit `proposed/` from the archived change, since the applied artifacts are now canonical and Git retains their proposed form; `change.md` MUST be retained.
8. MUST support `--dry-run`, reporting every action without performing any. Before mutating anything, apply MUST preflight every planned action (readable sources, existing delete targets, absent archive destination); a preflight failure leaves the working tree untouched, and execution orders the change-directory move last so the archived change appears only when every other action succeeded.
9. MUST NOT be executed implicitly - not by an AI hook, not by SDD archival, not by any automatic trigger. Apply MUST NOT create Git commits or merge anything; committing is the user's decision.

Apply is a working-tree operation and carries no delivery contract: it does not require, discover or attest that anything has been implemented, verified or deployed.

## Acceptance

The branch carrying the applied model and the archived change is reviewed as a pull request (or the host's equivalent). Merging is a human decision: tools MUST NOT merge, auto-approve or self-merge model changes, and MUST NOT merge a proposal whose structural validation fails (see [Conformance](conformance.md)).

## Initialisation

`CHG-INITIAL` is a reserved identifier for the single initialisation change that establishes the first Product Definition. Greenfield and brownfield products use the same mechanism: `CHG-INITIAL` is elaborated from the product knowledge available at the time, applied into an empty model, and accepted through review like every later change.

That knowledge may come from new product objectives and discussions, existing documentation, source code and tests, interviews and question-and-answer sessions, or conversations and existing team knowledge.

Brownfield discovery is an input activity to `CHG-INITIAL`, not a separate lifecycle. There is no recovery change type and no `recover` operation. Provenance, confidence and the evidence behind recovered claims belong to the proposed artifacts themselves (see [Frontmatter reference → Provenance](frontmatter-reference.md#provenance)); recovered drafts with low confidence surface through `PRODUCT111` as the queue of candidates needing human validation. Contradictions between recovered candidates are resolved in the change, before the definition is accepted, not in the baseline afterwards.

A product MUST NOT have more than one `CHG-INITIAL`. Every semantic evolution after it MUST be represented through a Product Change.

## Change history

`docs/product/changes/**` is the semantic history of product evolution: what changed, why, what it affected, and what was still open when it was accepted. Git history records who changed which files and when; the change history records what the product change meant.

An archived change MUST NOT be edited to reflect later decisions. A decision that is superseded is superseded by a new Product Change.

## Change impact

Applying a change produces a product diff (apply rule 5). A conforming tool uses that diff to recompute citation statuses for consumer documents that cite the impacted artifacts, per the [Citation Contract](citation-contract.md): citations to unchanged artifacts stay `current`, and citations to artifacts the change touched become `stale`.

The stale set is the machine-derivable answer to "what does this change oblige us to revisit": which specifications, tasks and prompts cited intent that no longer says what it said. PDaC surfaces that set. Whether it is answered by updating the citing document, planning rework, or contesting the change is a decision for the consuming process, not a conformance criterion.
