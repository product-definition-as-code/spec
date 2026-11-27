> Historical G1 candidate: [owner approval](https://github.com/product-definition-as-code/spec/issues/130#issuecomment-7228575750) froze commit `d7a2553`. Attempt1 is preserved and invalid due to tool transport; [G2 recommends bounded revision](../gates/phase-2-decision.md). This historical text is not a new approval request or retry authorization.

# G1 — approve intent and the controlled pilot

**Decision requested:** approve this exact package for #131–134, ending at G2. Preparation/review is complete; no scored author has run. No tools, agents or infrastructure need choosing by the owner. The full [intent](product-intent.md), [protocol](frozen-protocol.md) and [custody commitments](custody.json) are linked for inspection.

## 1. Accept this synthetic product intent

- One atomic reservation operation over integer pool capacity/usage; REQUESTED consumes zero, CONFIRMED consumes its footprint. Owner never changes. Reject invalid inputs/unauthorized operations without repairing state; missing state fields echo null. Integers exclude booleans; complete input has exactly eleven keys. Capacity zero is valid except where occupancy forbids it. No concurrency, clock inference, history migration or external authenticator proof.
- Trust externally authenticated issuer 0. CONFIRM/CANCEL permit owner or trusted editor; EXPIRE/EDIT require trusted editor. Confirm REQUESTED within **0–48 inclusive whole days**, adding one capacity unit if available. Cancel REQUESTED at any valid day, or CONFIRMED at least **two days** before start; release units only for CONFIRMED. Due CONFIRMED reservations may expire, releasing their footprint. EDIT changes no represented state. Terminal operations reject; all unaffected state is preserved.
- Successive approved requests: lead window **48→21**; footprint **1→3** with examples; allow due REQUESTED expiry releasing **zero**; trust issuers **0 and 1**; unrelated audit retention **7→14 days**; editorial example edit only. Final authorization contrast permits owner-or-editor EDIT; otherwise unchanged. No silent extra decisions.

## 2. Approve the proposed screening protocol

Four matched cohorts, with/without PDaC and verification; primary contrast is proof-driven C4 versus C3. Eight episodes × two schedules × four cohorts = **64 fresh author sessions**. Independent custodian holds **1,164 finite cases**; no feedback to authors before output freeze. Separate fresh sessions review the results. Same provider/host and opaque serving-model revision remain limitations; agents are not human expert validators.

**Explicit endpoint amendment:** screen for at least **10 percentage points fewer finite executable-or-contract discrepancies** in C4 than C3 in each schedule, with **zero additional rejection of valid behaviours**. Use the conservative improvement bound, publish 5/10/15-point sensitivity, unknowns and negative results. This is not the original seeded-mutation detection endpoint or a demonstrated human-review-time saving; those remain unmeasured. No general correctness, H0 advantage or normative extension follows from a screening pass alone.

Existing-resource limits: two authors concurrently, **8 minutes/4 GiB each**, zero automatic retries. Host jobs **30 seconds/2 GiB**, serialized; author solvers capped at **2,048 processes/65,536 queries aggregate**, independent scoring **64 batches/7,776 queries**. Documentary review: eight trajectory sessions plus one synthesis, eight minutes each. No money/token prerequisite, service purchase or phase3 authorization.

**Mobile reply:** “Approve G1 package” or state the intent/protocol change requested. The coordinator records that actual owner decision with the merged commit and prepared-manifest hash, executes #131–134, and returns evidence at G2. Silence or merging this preparation does not approve scored work.
