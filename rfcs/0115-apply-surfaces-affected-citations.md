# RFC 0115: Apply surfaces the affected citation set before a change is accepted

- **Status:** accepted
- **Author(s):** Juan G. Carmona
- **Created:** 2026-08-19, revised 2026-09-06
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/48>; PR <https://github.com/product-definition-as-code/spec/pull/115>
- **Supersedes:** the draft in [PR #50](https://github.com/product-definition-as-code/spec/pull/50), closed on 2026-08-26 and deferred to 0.3.0
- **Class:** change (adds an implementation obligation); public comment window of at least seven days before v1.0, binding once gate 2 or the first listed adopter exists ([CONTRIBUTING → The RFC process](../CONTRIBUTING.md#the-rfc-process))
- **Proposed target:** PDaC specification 0.3.0 with the `v1alpha2` serialization established by RFC 0116; this RFC adds no further schema change
- **Release refinement:** 2026-09-25; follows [RFC 0116](0116-domain-behaviour-and-verification-evidence.md) and [RFC 0082](0082-a-change-accounts-for-its-graph-neighborhood.md), in that order.
- **Reference implementation:** ProductShape 0.19.0 and later

## Review in brief

Before apply writes anything, show which live downstream citations the effective change affects and what their status will become. The same forecast is required for dry run, including an explicit count of zero when nothing is affected.

- Run the forecast after RFC 0082's model-impact preconditions pass; it does not replace them.
- Use actual changed artifact content, not merely declared operations or graph neighbors. An unchanged acknowledged neighbor does not make its citations stale.
- Report location, target, optional anchor and prospective citation status in deterministic order, using the same live population as citation verification. Exclude archived history and the applying change's own container.
- Surface downstream consequences without turning them into another apply gate. Stale citations still require consumer review; apply does not refresh them automatically.

This is an implementation reporting obligation, with no new artifact, schema or diagnostic code. The RFC remains a proposal; the required apply-capable conformance cases are follow-up implementation work.

## Problem

[Product Changes → Change impact](../spec/product-changes.md#change-impact) defines impact from the product diff and the citation index: citations to changed artifacts become `stale`, and "the stale set is the machine-derivable answer to 'what does this change oblige us to revisit'". It then says: "PDaC surfaces that set."

No normative clause says when, where or in what form. "Surfaces" is an obligation no implementation can fail, no fixture can test and no reviewer can rely on. Without it a Product Change is reviewed and accepted blind to the consumer documents it invalidates, and the breakage appears later, on the consumer's initiative, only if someone runs citation verification. The review happens at the one moment the blast radius is invisible.

When the first draft of this RFC was written, the reference implementation reported the digest diff at apply and never consulted the citation index. It has since closed the gap: ProductShape 0.19.0 reports the affected citation set from `change apply`, from its dry run and from both hosted apply lanes (OpenSpec and Spec Kit), and 0.19.1 refined the population after two consumer spikes. The behaviour exists and has been exercised by outside runs. What is missing is the normative text that makes it an obligation for every implementation, so that a second implementation cannot claim conformance while leaving reviewers blind.

## Proposal

Replace the vague surfacing statement in [Product Changes → Change impact](../spec/product-changes.md#change-impact) with the following contract, after the impact-accounting contract from RFC 0082. Revise the surrounding explanation so it does not imply every affected citation becomes stale: removing its target can make a citation unresolved. The citation contract remains the single source of status and precedence semantics.

> Applying a Product Change, and equally previewing the apply with a dry run, MUST compute and report the **affected citation set** after all RFC 0082 apply preconditions pass and before any model or archive write: every citation in the live citation index whose target artifact the prospective effective product diff reports as added, modified or removed. For each affected citation the report MUST carry the consumer document's repository-relative POSIX path; the point of use when the carrier provides one (the line for a payload citation, the entry for a sidecar ledger, see [RFC 0047](0047-citation-carriers.md)); the target `id` and, when present, the `anchor`; and the prospective status the citation will hold against the applied result, computed under the [Citation Contract](../spec/citation-contract.md) precedence.
>
> The prospective result MUST be the same result the apply would materialize. Declared operations with no effective normalized-byte change contribute nothing. Impact causes and `unaffected` acknowledgments do not themselves add IDs to this set: only a cited artifact's own effective change does. A failed earlier precondition does not require this report, and MUST NOT be represented as an evaluated empty set. Dry run and real apply over identical inputs MUST report the same set and prospective statuses.
>
> An empty affected set MUST be reported explicitly, as a count of zero. Absence of impact is a claim the reviewer relies on; silence is not a claim.
>
> The report joins the apply output in both human-readable and machine-readable forms. Records MUST sort by consumer path in Unicode code-point order, location kind (absent, line, entry), numeric location with absence before a value, target ID, anchor with absence before a value, and prospective status. String comparisons use Unicode code-point order. Distinct source occurrences MUST remain distinct records even when they cite the same ID and digest. The count is the number of records. No output serialization is prescribed; determinism fixes record content and ordering, not identical bytes between different implementations. It is a report, not a persisted artifact: it MUST NOT be written to the archived change or another repository file.
>
> The report covers the consumer documents the implementation holds as live. Documents the implementation holds as immutable history, an archived change or the applying change's own container, are not part of the set, because they are never re-grounded. An implementation MUST document which population its report covers, and the population MUST be the one its citation verification treats as current, so that apply and verification name the same documents.
>
> Apply MUST NOT fail because citations become stale. Forecast statuses are report data, not emitted consumer-validation diagnostics, and MUST NOT be fed into `validation.warnings-as-errors` or RFC 0082's impact gate. Invalidating consumers is frequently the purpose of a change; the obligation is that the invalidation is seen at review time, not that it is prevented. Existing citation verification continues to emit its own diagnostics and apply its warning policy when separately invoked. Forecast `unresolved`, `tampered` and `current` statuses likewise describe the prospective consumer state and do not themselves add apply preconditions.

An optional RFC 0116 evidence adapter may contribute explicitly current evidence documents to the documented live population, using its evidence-file path and flattened citation entry ordinal. Historical run evidence remains excluded. The evidence run outcome is not a citation status and does not affect apply. This RFC does not mandate an evidence adapter or expand discovery to arbitrary external files.

No diagnostic code is allocated. The prospective statuses reuse the four citation statuses, and the report is a forecast of consumer-side states, not a defect.

## Impact

- **On existing conformant repositories:** none. The obligation binds implementations, not repositories.
- **On existing implementations:** an implementation that applies Product Changes must build the citation index at apply time and intersect it with the product diff, in the dry run as well as in the real apply. The reference implementation already does; its report lists each affected citation as location, id and prospective status under an explicit count, and its JSON form carries the same records.
- **On the Citation Contract and Validation:** preserve citation statuses and precedence; add cross-references to this apply obligation and clarify that forecast data is not a diagnostic. Preserve the product diff's unfixed serialization while fixing this report's semantic content and order.
- **On the conformance tests:** the [implementation checklist](#implementation-checklist) covers add/modify/remove, zero/no-op, payload/sidecar locations, repeated citations, anchors, precedence, population exclusions, evidence integration, dry-run equivalence, deterministic ordering, no persistence and warning escalation. A combined case first fails with PRODUCT034, then succeeds after a valid model-impact acknowledgment while still reporting stale downstream citations. The runner today executes validation-style commands only, so these cases require the same apply-capable format as RFC 0082. Until executable, the obligations remain explicitly not covered; v0.3 qualification requires that runner extension rather than treating validation-only passes as evidence for apply.
- **On versioning:** a new obligation, so 0.3.0.

## Implementation checklist

| Files | Required follow-up |
| --- | --- |
| `spec/product-changes.md` | Integrate the forecast after RFC 0082's preconditions and before writes; use the prospective effective diff; replace the implication that every affected citation becomes stale, since removals can be unresolved. Retain preflight, rollback and human-merge acceptance. |
| `spec/citation-contract.md`, `spec/conformance.md` | Link to mandatory apply/dry-run reporting while keeping citation status/precedence defined only in the Citation Contract. Current consumer verification keeps its own diagnostics and warning policy. |
| `spec/validation.md` | Distinguish report records from diagnostics and semantic report ordering from a fixed serialization. Forecast staleness must not enter warnings-as-errors. Allocate no code. |
| `conformance/cases/`, `conformance/README.md`, `.github/workflows/conformance.yml` | Add the matrix below, document coverage honestly and pin a runner with the apply/history/tree/report capabilities shared with RFC 0082. |

Each fixture must assert the report's semantic records and count, not ProductShape-specific JSON. The runner adapter may normalize an implementation's serialization but must preserve emitted record order so an ordering defect cannot be sorted away. No new report file or schema becomes canonical product data.

- `apply-citations-{modified,removed,added,zero,no-op,unrelated-target}`: changed-target intersection only; modified content may become stale, removal unresolved, an added target may resolve a previously unresolved citation; an ineffective declared modify produces zero.
- `apply-citations-{payload,sidecar,multiple-locations,anchor-missing,tampered-and-stale}`: exact attribution, distinct occurrences and unchanged citation precedence.
- `apply-citations-{history-excluded,own-container-excluded,other-active-consumer}`: documented live population; exclusion of the applying container must not hide unrelated current consumers.
- `apply-citations-{current-evidence,historical-evidence}` when the optional RFC 0116 adapter is claimed: stable flattened entry locations, explicitly current evidence included, historical runs excluded; run outcome is irrelevant to apply.
- `apply-citations-{dry-run-equivalence,deterministic-order,not-persisted,stale-warning-escalation}`: identical-input forecasts, untouched dry-run tree, no report persistence or consumer re-citation, and stale forecasts remain non-blocking even when warnings-as-errors is enabled.
- `apply-combined-impact-and-citations`: missing model-impact accounting yields PRODUCT034, no writes and no false evaluated-zero report; after a valid acknowledgment, apply succeeds while showing stale citations. A citation to an unchanged acknowledged neighbor stays current.

The runner extension must isolate fixture working copies, set up required Git history, invoke the selected apply/dry-run operation, and assert diagnostics, exit status, report content/order and before/after trees. It must not treat an unsupported or skipped case as conformance evidence. The existing validation-only suite does not establish this reporting obligation.

## Evidence from the reference implementation

The observations below motivate the original visibility/population contract. They are not evidence that those historical releases implement the later RFC 0082 staging, RFC 0116 evidence integration or every ordering/fixture requirement of this coordinated revision.

- ProductShape 0.19.0 (PR #245) reports the affected citation set from native `change apply`, from `--dry-run` and from the hosted OpenSpec and Spec Kit apply lanes, all through one core computation over the citation index and the product diff.
- Two consumer spikes on the published 0.19.0 (2026-09-05, one per host) confirmed the set is deterministic and matches a subsequent `citations verify` run, and exposed two population defects: the applying change's own proposal was named as stale, and archived containers were counted by apply but not by verification. ProductShape 0.19.1 (PR #256) excludes both, which is the population clause above.
- The same spikes recorded that a task citing only a derived requirement is not named when the underlying rule changes, because staleness follows the cited artifact's own digest. That is correct under this RFC and is a citation-authoring rule for consumers, not a gap in the set.

## Alternatives considered

### Keep discovery pull-based, through citation verification alone

Rejected. Verification answers "what is stale now", after the fact, on the consumer's initiative. The decision that creates the staleness is the change's acceptance, and a review that cannot see consequences reverses the order of authority the methodology exists to protect.

### Block apply when citations would go stale

Rejected. A change that corrects product intent should invalidate the consumers that cited the old intent; that is the contract working. A veto would be overridden routinely or push changes into unreviewable fragments.

### Allocate a diagnostic code for "change invalidates citations"

Rejected. Staleness is a state of the consumer document with existing codes and precedence. At apply time nothing is wrong yet; giving a forecast an error code would conflate preview with defect.

### Surface the set only in a standalone impact query

Rejected as the sole home. An implementation MAY extend impact analysis to citing consumers, but a report the reviewer must remember to request recreates the gap. Every change passes through apply and its dry run; that is where the obligation belongs.

### Include archived history in the set

Rejected. An archived change and the applying change's own container record the intent of their moment and are never re-grounded; naming them tells the reviewer to fix documents that must not change, and makes apply disagree with verification, which excludes them.

## Out of scope

- Cross-repository citation resolution; the set covers the repository the model lives in, per the boundary restated in [Change impact](../spec/product-changes.md#change-impact).
- Automatic revision, digest refresh or rewriting of consumer documents; [RFC 0042](0042-consumer-binding-for-sdd-alignment.md) forbids it and nothing here relaxes that.
- Consumer-population accounting, which is [RFC 0042](0042-consumer-binding-for-sdd-alignment.md)'s subject; this RFC only requires apply and verification to agree on the population.

## Maintainer decision

Accepted by Juan G. Carmona on 2026-09-25 and merged through PR #115. Before apply writes anything, report the live downstream citations affected by the effective product diff, including an explicit zero. Use the same population and status rules as citation verification, with deterministic records and no persistence. Surface stale or unresolved consequences without making them an apply veto. This record reconciles the RFC file with the acceptance already recorded on the merged PR.
