# RFC 0004: Delivery-model reset: the accepted Product Definition, semantic Product Changes, and direct citations

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-03
- **Refined:** 2026-08-05
- **Supersedes:** #1 (baseline lock file), #3 (implementation claims, applicability contracts and reconciliation states)
- **Related:** #2 (deployment topologies — remains open; scopes where cited models live and how cross-repository citations resolve)
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/4>

## Problem

The gap PDaC exists to close is re-statement: every time product knowledge is re-expressed in natural language (in a spec, a task, a prompt, a document), it can mutate without anyone noticing. The specification answered this with a push pipeline (Product Change → Delivery Slice → Product Handoff → Promotion) that itself re-states knowledge into new containers, and self-hosted use showed the pipeline does not hold:

1. **No conforming greenfield path.** The initial baseline was authored without a Product Change ([`product-changes.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/product-changes.md), bootstrap exception), but every Delivery Slice had to live inside a Product Change ([`delivery-slices.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/delivery-slices.md)) and every handoff had to start from an approved slice ([`handoff-contract.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/handoff-contract.md), generation rule 1). There was no conforming way to deliver the initial baseline.
2. **Vacuous promotion gates.** Promotion rules 2 and 3 ([`product-changes.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/product-changes.md)) were satisfied vacuously by a change with zero slices: no slices to complete, no requirements to evidence. An implemented change could be promoted with no delivery evidence at all.
3. **Scope loss.** A slice declared per-requirement `coverage` and `scope`, but the handoff `implements[]` carried bare IDs ([`frontmatter-reference.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/frontmatter-reference.md)). Partial scope was flattened before it reached any consumer, and promotion unioned requirement IDs.
4. **Unbounded context.** The closure rule had no budget. Real generated contexts exceeded 16,000 words for a single slice, which contradicts "exactly the product subgraph that increment needs".
5. **Delivery state modelled as product state.** `in-progress`, `implemented`, slice completion, coverage evidence and deployment attestation are facts about delivery, and PDaC made them gates on the evolution of product intent. Product intent could not be accepted until delivery said so.

The failure is not that product change was made explicit. It is that PDaC modelled the delivery of a change instead of the meaning of a change, and then made the two inseparable. This RFC keeps the semantic mechanism and removes the pipeline.

## Decision

### 1. The Product Definition

The **Product Definition** is the accepted, versioned and validated graph of product artifacts on the repository's canonical branch. It is the accepted product intent. Acceptance is a fact about the definition, not about implementation: an accepted artifact may be unimplemented, and implemented behaviour that was never accepted is not part of the definition.

### 2. Product Change

Product evolution is expressed through `Product Change`.

A Product Change is a semantic delta that proposes additions, modifications or removals to the accepted Product Definition. It records the meaning, rationale, scope and affected product artifacts of that change. It is elaborated iteratively: a change may be opened, discussed, widened, narrowed and revised over time, and several Product Changes may be live at once.

A Product Change is not a pull request, a delivery container or an implementation state.

- **Not a pull request.** A pull request provides the human review and acceptance boundary for a Product Change. The pull request and the Product Change are related, but they are not the same concept. A Product Change carries product meaning (rationale, intended outcome, open questions, affected areas) that a branch and a diff cannot carry.
- **Not a delivery container.** A Product Change does not decompose work, schedule it, or track its implementation.
- **Not an implementation state.** A Product Change is done when the definition it proposes has been applied and accepted, regardless of whether anything has been built.

An approved Product Change is **applied** by an explicit, human-triggered operation that executes its operations against the model, computes the resulting product diff, validates the resulting graph, and archives the change as history.

Apply materializes and validates a proposal; it does not accept it. `docs/product/model` on a working branch is a proposal; the same path on the canonical branch is the accepted Product Definition. Apply changes the former and never the latter: it never merges, never commits, and never runs implicitly. Treating a successful apply as acceptance is the one misreading of this RFC that would reinstate the failure it exists to remove, because it would let a tool decide that product intent is accepted.

When the pull request carrying the applied result is merged, its resulting product definition becomes the new accepted Product Definition. Acceptance of product intent is independent from implementation, deployment and production verification.

A change is mutable while it is a workspace and immutable once it is a record. `draft` and `proposed` changes may be edited, rewritten or discarded freely, and a change whose baseline moved is rebased rather than patched. An applied and accepted change is immutable: it is the record of what was reviewed and approved, and any later correction is expressed through a new Product Change.

The normative structure of a Product Change - the change record, its frontmatter, its operations, overlay validation, its lifecycle and the apply rules - is specified in [Product Changes](../spec/product-changes.md).

### 3. Initialisation

Greenfield and brownfield products use the same initialisation model. `CHG-INITIAL` establishes the first Product Definition from the product knowledge available at that time.

That knowledge may come from new product objectives and discussions, existing documentation, source code and tests, interviews and question-and-answer sessions, or conversations and existing team knowledge.

Brownfield discovery is an input activity to `CHG-INITIAL`, not a separate lifecycle. Provenance, confidence, contradictions, gaps and unresolved questions belong to the affected product artifacts or their supporting evidence. They do not define a different kind of Product Change. There is no `CHG-RECOVERY` and no normative `recover` operation.

This replaces the initial-baseline bootstrap exception: the first Product Definition enters through the same mechanism as every later change.

### 4. The Product Definition as reference

SDD specifications and other delivery artifacts cite canonical Product Definition artifacts directly, per the [Citation Contract](../spec/citation-contract.md).

PDaC does not create a mandatory handoff containing a copied or restated version of the product intent. The consuming SDD or delivery process remains responsible for deciding how work is decomposed, creating and maintaining its specifications, defining technical design, creating implementation tasks, implementing and verifying the change, and deciding when and how to deploy it.

PDaC provides the stable product reference consumed by those processes. A generated view, scope report or projection may be provided for convenience, but it is not an additional canonical product artifact and does not require an independent lifecycle.

### 5. Change impact

When the accepted Product Definition changes, PDaC calculates the product difference and identifies the downstream citations and consumer documents that may be affected.

The resulting relationship is:

```text
Product Change
      ↓
new Product Definition state
      ↓
product diff
      ↓
affected citations
      ↓
affected specifications and documents
```

The semantic relationship between the three is fixed here, because leaving it ambiguous is what lets a tool quietly substitute one for another:

- A `Product Change` records the **intent** and the proposed semantic operations. It is authoritative for what the change meant.
- The diff computed between the baseline and the accepted result is authoritative for the **effective change**. It is computed from the result, never read off the declared operations.
- **Impact** is computed from that diff and the citation index.
- A report MAY present intent and effective change together, and SHOULD when both are available. Neither may be presented as the other: declared operations are not the effective change, and a diff is not a statement of intent.

This allows dependent delivery work to detect that the product intent it cited has changed, and to decide whether to update the citing document, plan rework, or contest the change. Detecting the drift is PDaC's obligation; deciding what to do about it is not.

Citations resolve within one repository in v0.1; cross-repository resolution is out of scope for this RFC and is owned by RFC #2. The detailed representation and verification rules for citations, digests, diffs and impact analysis are defined by the relevant PDaC specifications. This RFC establishes their architectural role and the relationships above, not their serialization.

## Removed from the normative model

This RFC removes the following concepts from the normative PDaC model:

- Product Handoff as an intermediate delivery container;
- mandatory Delivery Slices;
- Promotion, the delivery-gated operation that required slice completion and coverage evidence before product intent could enter the baseline;
- Reconciliation;
- Implementation Claims;
- Deployment Evidence;
- a PDaC-owned implementation pipeline;
- a separate brownfield recovery lifecycle;
- the assumption that PDaC prepares and delivers an implementation unit to SDD.

A delivery process may use its own handoffs, slices, claims or deployment evidence. Those concepts are outside the PDaC model and are not required to maintain the Product Definition.

The `SLI-` and `HOF-` prefixes are retired and, per [`identifiers.md`](../spec/identifiers.md), never reused. The `CHG-` prefix is retained.

Apply is not Promotion renamed. Promotion gated the acceptance of product intent on delivery facts; apply gates nothing but the change's own validity, and carries no evidence contract.

Chapters removed from the normative spec: [`delivery-slices.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/delivery-slices.md) and [`handoff-contract.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/handoff-contract.md). Retiring the Delivery Slice artifact does not retire slicing: PDaC does not own delivery decomposition. Consumers may slice work however their process demands.

## Resulting ownership boundary

PDaC owns the accepted Product Definition, semantic Product Changes, the history of product evolution, validation of the product graph, product-aware diffs, direct citations to product artifacts, and citation verification and impact analysis.

PDaC does not own delivery decomposition, technical specifications, implementation, deployment, release orchestration, implementation verification, or the lifecycle of external SDD artifacts.

## Diagnostics

Retained with their original meanings: `PRODUCT020`-`PRODUCT027` (change operations, overlay integrity, concurrent-change overlap, baseline-revision compatibility at apply) and `PRODUCT108` (unresolved open questions on an approved change). `PRODUCT027` now governs apply rather than promotion.

Retired, not deprecated: `PRODUCT030`-`PRODUCT032` (delivery slices), `PRODUCT040`-`PRODUCT041` (handoffs), `PRODUCT043`-`PRODUCT044` (coverage and delivery evidence), `PRODUCT109`-`PRODUCT110` (slice and handoff closure). Retired codes are never reused, mirroring the ID immutability rule.

Added by the citation contract: `PRODUCT060`-`PRODUCT063`. `PRODUCT042` is generalized to citation digests.

Added by the second refinement: `PRODUCT028` (apply attempted on a change whose status is not `approved`). It sits inside the `PRODUCT020`-`PRODUCT028` Product Change band and is an apply-time finding, never a baseline finding.

## Impact

- **On existing conformant repositories:** `docs/product/model/**` is untouched. `docs/product/changes/**` remains the change surface, without `slices/`. Changes in flight under the previous lifecycle finish as `approved` and are applied, or are archived as `superseded`. Each terminal status has its own archive directory: `completed/`, `rejected/` and `superseded/`.
- **On existing implementations (ProductShape):** keep the parser, graph, validation, digests and change commands; retire `slice`, `promote` and handoff generation; replace promotion with `apply`; add citation emission and citation verification.
- **On the conformance corpus:** the initialisation and citation cases carry a `CHG-INITIAL` record; change-operation, overlay and apply cases are added; no slice or handoff fixtures existed to drop.

## Alternatives considered

- **Mark the workflow chapters `experimental`.** Honest, but closes nothing: the re-statement gap remains and adopters still learn a vocabulary nobody speaks.
- **Repair the handoff in place (scope fields, closure budget).** Keeps the push model; every handoff is still a re-statement surface and a second thing to keep in sync.
- **`implementation-status` on requirements.** Rejected: conflates intent validity, work state, satisfaction and deployment, which have four different owners.
- **Adopt RFC #3 as filed.** Turns PDaC into a delivery control plane; the manifesto forswears it. Only the obligation-realization-evidence relation is worth keeping, and it composes naturally with citations.
- **Change-as-PR, as accepted in the first revision of this RFC.** Dissolving `Product Change` into the repository's branch-review-merge mechanism removed the pipeline, but it also removed the product-level record of *why* the definition changed, the workspace in which a change is elaborated before it is worth proposing, and the unit a product diff and its impact analysis attach to. Git records that files changed; it does not record that the product changed, or what that meant. Corrected by this revision.

## Consequences

This decision separates two related but independent concerns: the Product Definition evolves through semantic Product Changes, and delivery processes decide how accepted intent is implemented.

Product Definition and implementation may therefore evolve at different speeds. A Product Change may be accepted before implementation begins, while an SDD specification is being prepared, or without immediate implementation. Conversely, a citation going stale is a signal to a delivery process, not a defect in the Product Definition.

The repository remains the source of history and review. PDaC adds product-aware meaning to that history without recreating Git or becoming a second delivery system.

The core principle is:

> Product Changes evolve accepted product intent. Pull requests review and accept those changes. SDD specifications cite the Product Definition directly. PDaC exposes the impact of definition changes without owning delivery.

## Revision history

- **2026-08-03, accepted (PR #5).** First accepted revision. Removed the pipeline, and additionally dissolved `Product Change` into the repository's branch-review-merge mechanism ("change as PR"), retiring the `CHG-` prefix and the change record.
- **2026-08-05, refined (PR #9).** Corrects the overcorrection. The pipeline stays removed; `Product Change` is restored as the semantic mechanism of product evolution, with `CHG-INITIAL` as the single initialisation change for greenfield and brownfield. A pull request reviews and accepts a Product Change; it is not the Product Change.
- **2026-08-05, refined (PR #14).** Determines the five points of [issue #12](https://github.com/product-definition-as-code/spec/issues/12) that did not fix implementation behaviour. Apply reports the product diff and never persists it into the archived change. Each terminal status has its own archive directory, including `superseded/`. Applying a change that is not `approved` is `PRODUCT028`, exit `1`, with the working tree untouched. Baseline drift covers `modify` and `remove`, judged by content digest. `PRODUCT108` counts Markdown list items in `## Open Questions`. No decision of this RFC is reversed; five deferrals are closed.
- **2026-08-06, refined (PR #19).** Determines the citation status precedence of [issue #17](https://github.com/product-definition-as-code/spec/issues/17). The four statuses are evaluated in a fixed order: resolution failures first, then `tampered`, then `stale`, then `current`. A citation reports the diagnostic of its status and no other, so an embedded projection edited by hand whose cited text has also moved is `PRODUCT062` and not `PRODUCT061`. Faithfulness of an embedded block is decided against the recorded digest rather than against current canonical content, which is what makes the order implementable. No code is added and no decision of this RFC is reversed.

## Open questions

1. Concrete citation forms per host format (inline structured reference, Markdown marker block, YAML sidecar ledger). The pilot exercises all three; a follow-up normalizes.
2. Section-slug anchors and non-ASCII headings: do we need canonicalization rules, or do we restrict anchors to verification-scenario ids and skip the problem? **v0.1 decision:** restrict to scenario ids; section-slug anchors deferred to a follow-up.
3. The serialization of the product diff and of impact reports. The semantic relationship between intent, effective change and impact is settled under Change impact above; only the representation is deferred to a follow-up specification. **v0.1 decision:** apply reports the diff in its output in a human-readable and a machine-readable form and does not write it into the archived change, which is immutable once archived; the diff record - impacted artifact, kind of impact, resulting digest for additions and modifications - is fixed in [Product Changes](../spec/product-changes.md), an on-disk serialization is not.
