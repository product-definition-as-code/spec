# RFC 0115: Apply surfaces the affected citation set before a change is accepted

- **Status:** draft
- **Author(s):** Juan G. Carmona
- **Created:** 2026-08-19, revised 2026-09-06
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/48>; PR <https://github.com/product-definition-as-code/spec/pull/115>
- **Supersedes:** the draft in [PR #50](https://github.com/product-definition-as-code/spec/pull/50), closed on 2026-08-26 and deferred to 0.3.0
- **Class:** change (adds an implementation obligation); public comment window of at least seven days before v1.0, binding once gate 2 or the first listed adopter exists ([CONTRIBUTING → The RFC process](../CONTRIBUTING.md#the-rfc-process))
- **Proposed target:** PDaC specification 0.3.0; no schema or serialization-version change
- **Reference implementation:** ProductShape 0.19.0 and later

## Problem

[Product Changes → Change impact](../spec/product-changes.md#change-impact) defines impact from the product diff and the citation index: citations to changed artifacts become `stale`, and "the stale set is the machine-derivable answer to 'what does this change oblige us to revisit'". It then says: "PDaC surfaces that set."

No normative clause says when, where or in what form. "Surfaces" is an obligation no implementation can fail, no fixture can test and no reviewer can rely on. Without it a Product Change is reviewed and accepted blind to the consumer documents it invalidates, and the breakage appears later, on the consumer's initiative, only if someone runs citation verification. The review happens at the one moment the blast radius is invisible.

When the first draft of this RFC was written, the reference implementation reported the digest diff at apply and never consulted the citation index. It has since closed the gap: ProductShape 0.19.0 reports the affected citation set from `change apply`, from its dry run and from both hosted apply lanes (OpenSpec and Spec Kit), and 0.19.1 refined the population after two consumer spikes. The behaviour exists and has been exercised by outside runs. What is missing is the normative text that makes it an obligation for every implementation, so that a second implementation cannot claim conformance while leaving reviewers blind.

## Proposal

Add the following normative text to [Product Changes → Change impact](../spec/product-changes.md#change-impact), directly after the sentence "PDaC surfaces that set."

> Applying a Product Change, and equally previewing the apply with a dry run, MUST compute and report the **affected citation set**: every citation in the citation index whose target artifact the product diff reports as added, modified or removed. For each affected citation the report MUST carry the consumer document's repository-relative path; the point of use when the carrier provides one (the line for a payload citation, the entry for a sidecar ledger, see [RFC 0047](0047-citation-carriers.md)); the target `id` and, when present, the `anchor`; and the prospective status the citation will hold against the applied result, computed under the [Citation Contract](../spec/citation-contract.md) precedence.
>
> An empty affected set MUST be reported explicitly, as a count of zero. Absence of impact is a claim the reviewer relies on; silence is not a claim.
>
> The report joins the apply output in every form the implementation offers, human-readable and machine-readable, ordered under the [Validation](../spec/validation.md#determinism-requirements) determinism rules. It is a report, not a persisted artifact: like the product diff it is recomputable, and it is never written into the archived change.
>
> The report covers the consumer documents the implementation holds as live. Documents the implementation holds as immutable history, an archived change or the applying change's own container, are not part of the set, because they are never re-grounded. An implementation MUST document which population its report covers, and the population MUST be the one its citation verification treats as current, so that apply and verification name the same documents.
>
> Apply MUST NOT fail because citations become stale. Invalidating consumers is frequently the purpose of a change; the obligation is that the invalidation is seen at review time, not that it is prevented. Stale citations keep their existing diagnostics on the consumer side after apply.

No diagnostic code is allocated. The prospective statuses reuse the four citation statuses, and the report is a forecast of consumer-side states, not a defect.

## Impact

- **On existing conformant repositories:** none. The obligation binds implementations, not repositories.
- **On existing implementations:** an implementation that applies Product Changes must build the citation index at apply time and intersect it with the product diff, in the dry run as well as in the real apply. The reference implementation already does; its report lists each affected citation as location, id and prospective status under an explicit count, and its JSON form carries the same records.
- **On the Citation Contract and Validation:** no change.
- **On the conformance tests:** one case is due: a model, a consumer citing an artifact, an approved change modifying that artifact; the dry run must list the consumer with its location and prospective status, and a control fixture with no affected citations must report a count of zero. The runner today executes validation-style commands only, so the case needs the apply-capable case format [RFC 0021](0021-deployment-topologies.md) anticipated. Until that extension ships the obligation is listed as not yet covered in [Conformance tests → Diagnostic coverage](../conformance/README.md#diagnostic-coverage), and the badge says nothing about it.
- **On versioning:** a new obligation, so 0.3.0.

## Evidence from the reference implementation

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
