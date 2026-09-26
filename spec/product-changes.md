# Product Changes

A requested product modification MUST NOT silently modify the current model, and it does not directly become a backlog item. It becomes a **Product Change**: an explicit, validated delta against the baseline that records the meaning, rationale, scope and affected artifacts of the change.

A Product Change is not a pull request, a delivery container or an implementation state. A pull request is the human review and acceptance boundary for a Product Change; it is not the change itself. Decomposing, scheduling and implementing the work are the concerns of whatever consumes the definition (see the [Citation Contract](citation-contract.md)).

![How the accepted definition changes, in three labelled bands. Intention of change: the current product definition. Proposed change: a proposed Product Change carrying add, modify and remove operations, marked semantic intent. Accepted state: after a review and acceptance step, a new accepted product state, annotated "this is the resulting accepted definition, not implementation". A separate panel shows the graph diff as a derived effect, where modifying BR-014 marks UC-003, JRN-002 and the SDD citations stale or affected. Three boxes separate the roles: Product Change is semantic intent, pull request is the review mechanism, graph diff is the derived effect. The closing line reads: PDaC detects impact, the consuming process decides what to do.](../assets/diagrams/pdac-4-product-change.png)

_Figure PDaC-4 - how does the accepted definition change? Non-normative; this chapter is authoritative._

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
base-revision: <git-commit-sha> # or '0000000' only for CHG-INITIAL with no baseline commit
operations:
  add: [BR-CITE-CANONICAL, FR-CITATIONS-001]
  modify: [UC-VALIDATE-001]
  remove: []
---
```

Required body sections: `## Problem`, `## Intended Product Outcome`, `## Rationale`, `## Affected Product Areas`, `## Open Questions`, `## Product Acceptance`, `## Out of Scope`.

Each terminal status has exactly one archive directory: applied changes are archived under `docs/product/changes/completed/<chg-id>/`, rejected changes under `docs/product/changes/rejected/<chg-id>/`, and superseded changes under `docs/product/changes/superseded/<chg-id>/`. An archived change's directory MUST agree with its status: a change that was approved and then superseded is not a change that was rejected, and the change history is the evidence of which happened. Archived changes are inert history: they are not compiled into the product graph, and their IDs and proposed artifacts take no part in duplicate detection, reference resolution or operation checks.

## Elaboration

A Product Change is elaborated iteratively while it is `draft` or `proposed`: opened with a partial intent, then widened, narrowed, corrected and revised until it is worth proposing for approval. Several Product Changes MAY be active at once.

Implementations SHOULD use the product graph to support elaboration: surfacing the artifacts a proposed operation would affect, the artifacts put in question by those artifacts under the impact polarity of [Relationships → Canonical vocabulary](relationships.md#canonical-vocabulary), and the open questions the change has not answered. This is assistance, not authority. A tool MUST NOT resolve an open question, invent a product decision or set `approved` on the author's behalf ([manifesto](../MANIFESTO.md) principles 6 and 7).

## Operations

Operation IDs MAY name any Product Artifact, including Structured Behaviour and Domain Lifecycle.

- Every ID in `operations.add` MUST NOT exist in the baseline, and MUST have a complete proposed future-state artifact under `proposed/`.
- Every ID in `operations.modify` MUST exist in the baseline, and MUST have a complete proposed future-state artifact under `proposed/` using the same ID.
- Every ID in `operations.remove` MUST exist in the baseline. Removed artifacts need no tombstone files.
- Every artifact under `proposed/` MUST be listed in `operations.add` or `operations.modify`.

## Overlay validation

To validate a Product Change, an implementation MUST compile an **overlay** - the baseline graph with additions added, modifications replaced and removals deleted, without modifying any baseline file - and then apply full structural validation to the overlay. Overlay-specific errors are enumerated in [Validation](validation.md).

When a dangling reference in the overlay is caused by an ID named in the change's `remove` set, an implementation MUST report `PRODUCT024` and MUST NOT additionally report `PRODUCT006` for the same reference. `PRODUCT006` remains the diagnostic for a reference that dangles for any other reason.

While a Product Change is active, the baseline artifacts it touches remain authoritative and unchanged. An implementation MUST check concurrent active Product Changes for overlapping `modify`/`remove` sets. For each change, the overlap set is the union of `operations.modify` and `operations.remove`; every target present in two or more active changes is an error against each change that names it, including modify/remove and remove/remove intersections. The overlap remains an error until all but one of those changes is rebased or withdrawn.

## Impact accounting

Every live Product Change MUST account for its one-hop graph neighborhood. A declared addition or modification is an **effective change** only when its normalized content differs from baseline (an addition has no baseline content); a removal is effective. Content comparison uses [the raw-byte digest normalization](validation.md#digests). A declared modification whose normalized bytes are unchanged is not an effective change.

Compile canonical product relationships separately for baseline and overlay. For impact accounting only, normalize each to a set keyed by `(source artifact ID, canonical relationship field, target artifact ID)`. Repeated authored occurrences, including the same reference in multiple LC transitions, count once. Different fields remain different edges. Local transition IDs and indexes are not part of the key. Relationship diagnostics still retain authored occurrence granularity.

Compare the two sets: an edge present in both is `existing`, only in overlay is `added`, only in baseline is `removed`. Each impact cause is the tuple `(candidate, effectively changed cause artifact, canonical relationship field, disposition)`. The candidate MUST exist in the baseline and MUST NOT itself be effectively changed. A no-op declared modification can therefore still be a candidate. Newly added artifacts are never candidates.

Use [relationship polarity](relationships.md#canonical-vocabulary): for dependency edges, a changed target questions the source; governance edges question the opposite end when either end changes; none produces no cause. Consider existing, added and removed edges. Deduplicate causes by the tuple above. This is one hop, not transitive closure. If review edits a candidate, it becomes an effective change and the next computation considers its direct neighbors. A reviewed unchanged candidate does not propagate impact.

An absent Constraint `applies-to` authors implicit product-wide governance. Treat that as one edge to product scope, producing one product-scope cause when the Constraint effectively changes, including addition, removal, widening to implicit scope or narrowing away from it. An empty list is not absent. Business Rules have no implicit product scope.

### Acknowledgments

The optional `unaffected` ledger records a human judgment that a candidate remains valid. Its two closed shapes are in the [Frontmatter reference](frontmatter-reference.md#impact-acknowledgments). Artifact entries name `id`, `cause`, `relationship`, baseline candidate `digest`, `cause-digest` and a nonblank `reason`. Product-scope entries use `scope: product`, the Constraint `cause`, `relationship: applies-to`, `cause-digest` and a nonblank `reason`, without candidate ID/digest.

The candidate pin MUST equal its current baseline digest. The cause pin MUST equal the proposed digest for addition/modification, or the current baseline digest for removal. Each schema-valid entry MUST match a computed cause by candidate (or product scope), cause and relationship. Disposition is derived, not authored. Repeated valid entries acknowledge the same cause once. Invalid entries acknowledge nothing and MUST still be diagnosed even if another entry is valid.

For each schema-valid entry, emit `PRODUCT033` for the first condition that holds:

1. The artifact candidate ID does not exist in baseline: `target` is that ID.
2. No computed cause matches candidate/scope, cause and relationship: `target` is the cause ID.
3. The candidate digest differs from current baseline: `target` is the candidate ID.
4. The cause digest differs from the selected cause content: `target` is the cause ID.

Product-scope entries skip steps 1 and 3. Every such diagnostic names `change.md`, the change ID and `field: unaffected[n]` using one-based entry position. Schema-invalid entries use `PRODUCT002` JSON Pointer attribution, not `PRODUCT033` for the same entry.

Validation reports one `PRODUCT029` warning per unacknowledged cause. It reports all independent computable findings without guessing causes from malformed or ambiguous graph inputs. Apply and dry run instead enforce unresolved causes as `PRODUCT034`, under the stage order below. Neither acknowledgment nor a clean structural result proves semantic completeness; human review remains necessary.

## Lifecycle

`productChangeStatus`: `draft` → `proposed` → `approved` → `applied`, with `rejected` (from `draft` or `proposed`) and `superseded` (from any non-terminal state) as terminal alternatives.

Entering a terminal status archives the change: its directory moves out of `active/` into the archive directory for that status (see [Structure](#structure)), and the archived `change.md` records the terminal status. Archiving is a move, not a copy.

`approved` is a human product decision: the change is judged correct and wanted. It is what authorizes apply. It says nothing about implementation, and there is no status for implementation: whether the accepted intent has been built is a fact about delivery, not about the change ([RFC 0004](../rfcs/0004-delivery-model-reset.md)).

Acceptance is not a status on the change. An applied change enters the accepted Product Definition when a human merges the pull request carrying it (see [Terminology → Accepted](terminology.md)).

A Product Change in status `approved` whose `## Open Questions` section still contains one or more unresolved questions SHOULD produce exactly one warning (`PRODUCT108`) against the Product Change. The warning is state-based, not one warning per list item. It is reported whenever the change is validated, not only at the moment the status changes, so that it is reproducible from repository content alone.

For `PRODUCT108`, an unresolved question is a Markdown list item within the change's `## Open Questions` section, at any nesting depth. A list item counts as unresolved regardless of its content: nothing in the syntax distinguishes an answered item from an open one, and task-list checkboxes are not interpreted. Resolving a question therefore means removing its list item - deleting it, or folding it into the prose that answers it. A section with no list items has no unresolved questions: prose is not a question, so `None.` and an empty section are resolved by construction. The rule is syntactic on purpose: two implementations reading the same bytes have to agree, and no deterministic tool can judge whether prose contains an open question.

## Apply

**Apply materializes and validates a proposal. It does not accept the change, and it does not by itself modify the accepted Product Definition.**

The distinction is a distinction of location, not of file content. `docs/product/model` on a working branch is a proposal; `docs/product/model` on the canonical branch is the accepted Product Definition. Apply changes the former. Only a human merging the pull request changes the latter. An implementation that treats a successful apply as acceptance is non-conforming.

After configuration validation, apply evaluates stages 1–5 in order. A failing stage leaves the working tree untouched and stops later stages, while reporting every computable failure in that stage. `validation.warnings-as-errors` can stop a stage without changing diagnostic severity. Apply and dry run use the same stages and MUST NOT emit validation-only `PRODUCT029`.

1. MUST require change status `approved`. Applying a change in any other status MUST fail with `PRODUCT028`, leaving the working tree untouched.
2. MUST validate change structure, schema, operations and the complete overlay. Invalid ledger shape is a schema failure at this stage.
3. MUST check baseline-revision compatibility before writing. For `CHG-INITIAL` carrying exactly `0000000`, apply MUST skip Git resolution and baseline drift comparison and MUST NOT emit `PRODUCT027` because the sentinel does not resolve. Every ordinary `base-revision`, including other all-zero strings and `0000000` on another change, MUST resolve to exactly one commit; failure emits one `PRODUCT027` against `base-revision` and leaves the working tree untouched. After resolution, each artifact named in `operations.modify` or `operations.remove` is compared by content digest with its content at that commit. Each differing target emits `PRODUCT027` and apply fails until the change is explicitly rebased - proposed artifacts regenerated and reviewed, `base-revision` updated, and the overlay revalidated. A commit that touched a file without changing normalized content is not drift. `operations.add` is not drift-checked: an addition has no baseline artifact to compare, and an ID added since is already `PRODUCT020` in the revalidated overlay ([RFC 0066](../rfcs/0066-initial-base-revision-sentinel.md)).
4. MUST validate every schema-valid impact acknowledgment semantically (`PRODUCT033`).
5. MUST reject each unacknowledged impact cause with `PRODUCT034`, exit 1.
6. MUST compute and report the prospective product diff and [affected citations](#affected-citations), and preflight every action, before writing anything.
7. Writes additions, modifications and removals into the working tree's `docs/product/model`, naming files by lowercase ID.
8. MUST compute the product diff between the baseline and the applied result, and MUST report it in the operation's output in both a human-readable and a machine-readable form. Each entry names the impacted artifact, the kind of impact (`added`, `modified` or `removed`) and, for an addition or a modification, the resulting content digest; a removal has no resulting content and carries no digest. The diff is computed from the result, never read off `operations`: `operations` states what the change meant to do, the diff records what it effectively did. Apply MUST NOT write the diff into the archived change directory, which is immutable once archived: the diff is derived, not canonical, and is recomputable from `base-revision` and the applied result. An implementation MAY persist it elsewhere as a generated, non-canonical file. This specification fixes what the diff records and where apply reports it, not an on-disk serialization ([RFC 0004](../rfcs/0004-delivery-model-reset.md) open question 3).
9. MUST run full structural validation of the resulting model, and MUST leave the working tree untouched if it fails.
10. Sets the change status to `applied` and moves the change directory to `docs/product/changes/completed/<chg-id>/`, preserving its history. `applied` means materialized and archived, not accepted. An implementation MAY omit `proposed/` from the archived change, since the applied artifacts are now in the model and Git retains their proposed form; `change.md` MUST be retained.
11. MUST support `--dry-run`, reporting every action without performing any. Before mutating anything, apply MUST preflight every planned action (readable sources, existing delete targets, absent archive destination); a preflight failure leaves the working tree untouched. Apply performs the change-directory move last, so the archived change appears only when every other action has succeeded.
12. MUST NOT be executed implicitly - not by an AI hook, not by SDD archival, not by any automatic trigger. Apply MUST NOT create Git commits, push, open, approve or merge anything; committing is the user's decision.

Apply carries no delivery contract either: it does not require, discover or attest that anything has been implemented, verified or deployed.

## Acceptance

The branch carrying the applied model and the archived change is reviewed as a pull request (or the host's equivalent). Merging is a human decision: tools MUST NOT merge, auto-approve or self-merge model changes, and MUST NOT merge a proposal whose structural validation fails (see [Conformance](conformance.md)).

## Initialisation

`CHG-INITIAL` is a reserved identifier for the single initialisation change that establishes the first Product Definition. Greenfield and brownfield products use the same mechanism: `CHG-INITIAL` is elaborated from the product knowledge available at the time, applied into an empty model, and accepted through review like every later change. It uses the `0000000` no-baseline sentinel when no Git commit names that empty model, or MAY name a real commit whose Product Definition is empty.

That knowledge may come from new product objectives and discussions, existing documentation, source code and tests, interviews and question-and-answer sessions, or conversations and existing team knowledge.

Brownfield discovery is an input activity to `CHG-INITIAL`, not a separate lifecycle. There is no recovery change type and no `recover` operation. Provenance, confidence and the evidence behind recovered claims belong to the proposed artifacts themselves (see [Frontmatter reference → Provenance](frontmatter-reference.md#provenance)); recovered drafts with low confidence surface through `PRODUCT111` as the queue of candidates needing human validation. Contradictions between recovered candidates are resolved in the change, before the definition is accepted, not in the baseline afterwards.

A product MUST NOT have more than one `CHG-INITIAL`. Every semantic evolution after it MUST be represented through a Product Change.

## Change history

`docs/product/changes/**` is the semantic history of product evolution: what changed, why, what it affected, and what was still open when it was accepted. Git history records who changed which files and when; the change history records what the product change meant.

Mutability follows acceptance:

- A `draft` or `proposed` change MAY be edited, rewritten or discarded freely. It is a workspace, not a record.
- If the baseline moves under an active change, the change is rebased rather than patched: its proposed artifacts are regenerated against the new baseline, `base-revision` is updated, and the overlay is revalidated (`PRODUCT027`).
- An applied and accepted change is immutable. It MUST NOT be edited, rebased or reworded afterwards, in whole or in part.
- Any later correction is expressed through a new Product Change. A decision that is superseded is superseded by a change, never by an edit.

The reason is evidentiary: an accepted change is the record of what was actually reviewed and approved. A change that can be edited after acceptance stops being that record, and the change history stops being evidence.

## Change impact

A Product Change and a product diff answer two different questions, and neither substitutes for the other:

- The change records the **intent**: why the product should differ, and the semantic operations proposed to make it so. It is authoritative for what the change meant.
- The product diff between the baseline and the accepted result records the **effective change**: what actually differs in the Product Definition. It is authoritative for what changed.

They can legitimately disagree in scope. A declared `modify` may leave the artifact's meaning untouched, and a change may alter text no operation called out. A conforming tool MUST NOT present declared operations as the effective change, nor a diff as the change's intent. A report MAY present both, and SHOULD when both are available.

Model-impact causes question direct graph neighbors under [Impact accounting](#impact-accounting). Downstream citation consequences use the effective product diff under the following contract. An unchanged acknowledged neighbor does not make citations to that neighbor stale.

## Affected citations

After all apply preconditions pass and before any mutation, apply and `--dry-run` MUST report the affected live citation set in both human-readable and machine-readable output. The set is the intersection of live citation targets with artifact IDs added, modified or removed in the effective prospective product diff. It MUST NOT be derived from declared operations, transitive reachability or the impact-cause set. No-op modifications contribute nothing; additions can make previously unresolved citations resolve.

Use exactly the same documented live consumer population and citation interpretation as current citation verification. Exclude archived history and the applying change's own container; other current active consumers remain included. Explicitly current evidence MAY participate under the [evidence adapter](verification-evidence.md#discovery-and-live-population) contract; immutable historical runs do not.

Each occurrence MUST report its repository-relative POSIX source path, point-of-use line or entry when available, target ID, optional anchor and prospective citation status against the resulting model under [citation precedence](citation-contract.md#precedence). Distinct occurrences MUST remain separate, even if they cite the same artifact. Count records, not unique targets. Sort by path in Unicode code-point order, location kind (absent, line, entry), numeric location, target ID, anchor (absent first), then status.

Output MUST explicitly state zero when the population was evaluated and the intersection is empty. A failed earlier precondition does not require a forecast and MUST NOT be reported as an evaluated zero. Given identical inputs, dry run and real apply MUST report the same prospective records, count and order. Serialization details are implementation-defined; semantic content and order are fixed.

Forecast statuses are report data, not consumer diagnostics emitted by apply. A stale, unresolved or tampered citation MUST NOT by itself block apply, enter warnings-as-errors handling, or become a new apply precondition. This distinction does not relax the model-impact gate. Consumers decide whether to update their documents, plan rework or contest the change.

Apply MUST NOT persist the affected-citation report anywhere in the repository, alter consumers or automatically refresh their pins. The separate permission to persist a generated product diff remains unchanged. Citations resolve within one repository in v0.3; cross-repository resolution remains out of scope.
