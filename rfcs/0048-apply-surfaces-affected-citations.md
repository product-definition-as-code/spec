# RFC 0048: Apply surfaces the affected citation set before a change is accepted

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-19
- **Class:** change
- **Target:** PDaC v0.2.0
- **PR:** <https://github.com/product-definition-as-code/spec/pull/50>
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/48>
- **Public comment:** seven days; earliest acceptance 2026-08-26
- **Reference implementation:** ProductShape (implementation issue linked from the RFC issue)

## Problem

[Product Changes → Change impact](../spec/product-changes.md#change-impact) already defines impact: it is computed from the product diff and the citation index, citations to changed artifacts become `stale`, and "the stale set is the machine-derivable answer to 'what does this change oblige us to revisit'". It then says: "PDaC surfaces that set."

No normative clause says **when**. "Surfaces" carries no obligation an implementation can fail, no fixture can test, and no reviewer can rely on. The reference implementation demonstrates the gap precisely: its impact analysis traverses only the model graph, and its apply reports the digest diff without ever consulting the citation index.

The consequence is the exact failure the methodology exists to prevent. A Product Change is reviewed and accepted **blind to the consumer documents it will break**; the breakage becomes visible only later, pull-based, if and when someone runs citation verification. The review happens at the one moment when the blast radius is invisible, and the blast radius appears at every moment except the review.

## Proposal

### The apply-time obligation

Applying a Product Change, and equally previewing it with a dry run, MUST compute and report the **affected citation set**: every citation in the citation index whose target artifact appears in the product diff. For each affected citation the report MUST carry:

- the consumer document's repository-relative path;
- the point of use, when the carrier provides one (file and line for a payload-carried citation, ledger file and entry for a sidecar citation - see [RFC 0047](0047-citation-carriers.md));
- the target artifact `id` and, when present, the `anchor`;
- the prospective status the citation will hold against the applied result, computed under the existing [Citation Contract](../spec/citation-contract.md) precedence.

An empty affected set MUST be reported explicitly, as a stated count of zero. Absence of impact is a claim the reviewer relies on; silence is not a claim.

### Where the report lands

The affected citation set joins the existing apply output, in both its human-readable and its machine-readable (`--format json`) forms, ordered under the deterministic ordering rules of [Validation](../spec/validation.md). It is a report, not a persisted artifact: like the product diff, it is recomputable and is not written into the archived change, which stays immutable.

### Visibility, not veto

Apply MUST NOT fail because citations go stale. Breaking consumers is frequently the purpose of a change; the obligation this RFC adds is that the breakage is **seen at review time**, not that it is prevented. What is done with the stale set - revising the citing document, planning rework, contesting the change - remains a decision of the consuming process, exactly as [Change impact](../spec/product-changes.md#change-impact) already states, and stale citations continue to hold their existing diagnostics on the consumer side after apply.

### What this closes

With this obligation the citation loop closes: a citation records a dependency, the citation index aggregates the dependencies, apply intersects the index with the product diff, and the change review sees the consequence before acceptance. [RFC 0042](0042-consumer-binding-for-sdd-alignment.md) guards the other direction - that consumer documents are accountably bound to the definition. Together the two directions make drift visible at both moments where a human decides.

## Impact

- **On Product Changes:** the Change impact section gains the apply-time MUST above; its definition of impact does not change, it becomes testable.
- **On the Citation Contract and Validation:** no change. No new diagnostic code is allocated: the prospective statuses reuse the four existing statuses, and the report is a preview, not a diagnostic.
- **On existing conformant repositories:** none. The obligation binds implementations, not repositories.
- **On implementations:** an implementation claiming apply support must build the citation index at apply time and intersect it with the product diff. For the reference implementation this is the highest-priority open gap, tracked in its own repository.
- **On conformance tests:** one case is added: a model, a consumer citing an artifact, and an approved change modifying that artifact; the dry-run report must list the consumer with its location and prospective status, and a control fixture with no affected citations must report a count of zero. Today's case format runs a single validation-style command per fixture, so this case needs the runner to invoke an apply-style command - the case-format extension [RFC 0021](0021-deployment-topologies.md) anticipated; that extension ships with the case, not before it.
- **On versioning:** this adds a normative obligation, so it targets v0.2.0.

## Alternatives considered

### Keep discovery pull-based, through citation verification alone

Rejected. Verification answers "what is stale now", after the fact, on the consumer's initiative. The decision that creates the staleness is the change's acceptance, and a review that cannot see consequences reverses the order of authority the methodology exists to protect: the definition would change first and the consumers would discover it later, which is drift with extra steps.

### Block apply when citations would go stale

Rejected. A change that corrects product intent SHOULD break the consumers that cited the old intent; that is the contract working. A veto would either be overridden routinely, teaching users to ignore it, or would push changes to be split into unreviewable fragments. The obligation is visibility at the moment of decision.

### Allocate a diagnostic code for "change breaks citations"

Rejected. Staleness is a state of the consumer document with existing codes and existing precedence. At apply time nothing is wrong yet; the report is a forecast of consumer-side states, and giving a forecast an error code would conflate preview with defect.

### Surface the set in a standalone impact query instead of in apply

Rejected as the sole home. A separate query is worth offering, and an implementation MAY extend its impact analysis to include citing consumers, but a report the reviewer must remember to request recreates the gap this RFC closes. The one command every change passes through is apply and its dry run; that is where the obligation belongs.

## Out of scope

- Cross-repository citation resolution; the affected set covers the repository the model lives in, per the v0.1 boundary restated in [Change impact](../spec/product-changes.md#change-impact).
- Automatic revision, digest refresh or rewriting of consumer documents ([RFC 0042](0042-consumer-binding-for-sdd-alignment.md) forbids it; nothing here relaxes that).
- Consumer-population accounting, which is [RFC 0042](0042-consumer-binding-for-sdd-alignment.md)'s subject.

## RFC classification and review window

This RFC is a **change** under [CONTRIBUTING.md](../CONTRIBUTING.md): it adds an implementation obligation and a conformance case. Before v1.0 it requires a public comment window of at least seven days.
