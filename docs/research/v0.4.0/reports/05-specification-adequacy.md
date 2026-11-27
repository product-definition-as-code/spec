# Specification adequacy and intent validation

Issue: [#126](https://github.com/product-definition-as-code/spec/issues/126). Retrieved 2026-11-27. Status: documentary findings and proposed fault catalogue; independent review pending. [Proposal](../../v0.4.0-formal-product-definition.md) H0/H1/H2/H3 remain untested.

## Primary findings

| Source / inspected version | What it supports | What it does not establish |
| --- | --- | --- |
| Lahiri, [Intent Formalization v1](https://arxiv.org/html/2603.17150v1), section 3.2, 2026-03-17 | Discusses preserving correct behaviours and rejecting incorrect ones, using test/output-mutation proxies. | Finite examples or an unrealistic mutation set do not establish complete fidelity to human intent. |
| Swamy/Lahiri, [SPOTs](https://risemsr.github.io/blog/2026-04-16-spotting-specs/), 2026-04-16, takeaways | Small verified clients can reveal gaps in abstract specifications. | Authors explicitly retain missed-gap and overfitting risks; client proofs need human review. |
| [QuickCheck package documentation](https://hackage.haskell.org/package/QuickCheck), inspected 2.18.0.0 description; [2003 chapter metadata](https://research.chalmers.se/en/publication/177264) | Properties and generators support randomized checking; data distributions are inspectable. | Sampling is not universal verification. The chapter's full text was not available from its metadata page; the older Chalmers manual endpoint returned 403. |
| [QuickChick README](https://github.com/QuickChick/QuickChick), live `master`; [Software Foundations volume 4](https://softwarefoundations.cis.upenn.edu/qc-current/index.html), version 2.1, 2026-08-24 | Property-based testing, generator derivation and `MutateCheck` interfaces are documented in the project. | Availability of a framework or a verified generator does not make sampled product evidence a proof of intent adequacy. No installation was tested. |
| [Dafny reference](https://dafny.org/latest/DafnyRef/DafnyRef), live latest snapshot, section 13.7.5 | Documents contradictory/redundant-assumption warnings and proof-dependency reporting. | A passed proof may be vacuous under inconsistent assumptions. Diagnostic availability is not demonstrated detection of this benchmark's faults. |

No published detection rates are imported as expected PDaC results. The ART manuscript access failure is recorded in the Microsoft-foundations report; no unread findings are attributed to it.

## Proposed reusable fault catalogue

These are experiment-design candidates, not approved booking/authorization decisions or executed mutations. Owners first approve intended positive/negative scenarios; evaluators then hold back variants.

| Fault class | Candidate seed | Required observation |
| --- | --- | --- |
| Contradiction / vacuity | Incompatible capacity assumptions, or an always-disabled reservation guard | Non-empty intended witnesses and reachable scenarios, not only discharged implications |
| Under-specification | Remove capacity preservation, account identity, or an unrelated-state frame condition | A distinguishable undesired outcome accepted by the weakened contract |
| Over-specification | Forbid an owner-approved cancellation or valid authorization case | Rejection of accepted behaviour, even if the remaining model verifies |
| Domain ambiguity | Change time units or meaning of available capacity without matching dependent constraints | An independently judged semantic mismatch, not merely different wording |
| Interacting transitions / boundaries | Cancellation and expiry interact; an identity provider's issuer/role assumption changes | A counterexample or invalid applicability claim grounded in explicit assumptions |
| Agent drift | A fresh agent weakens a contract or silently chooses one interpretation | Missed intent decision, reconstruction/rework and owner-review effort |

Equivalent mutants, invalid seeds and unsupported/unknown analyses are separate categories, with reasons and preserved artifacts. A survivor is not automatically a real defect; a proof failure is not automatically a counterexample. Phase 2 mutates/checks product models and abstract contracts; implementation mutations wait for the authorized bridge.

## Evaluation and falsification design

Assess accepted-behaviour preservation, actionable fault detection by class, survivor/vacuity rates, unintended semantic choices and human-review agreement. Report eligible-case denominators, invalid exclusions and unknowns separately; do not improve a score by silently dropping timeouts. Record context reconstruction, repeated work, tokens/retries, verification latency and human attention alongside governance overhead.

Use the same owner intent and evaluation facts in all four cohorts; apply formal-specific diagnostics only where applicable. Reserve independent cases and fault variants before authoring, control seeds/order and mask cohort labels where feasible; representation may prevent full blinding and must be disclosed. An independent evaluator, not the report author, adjudicates intent fidelity and mutant validity.

H0/H1/H3 would lose support if the matched PDaC workflow misses more intent, rejects legitimate behaviour, gains only on exposed cases, or costs more than its useful improvements. Choose numerical margins and sensitivity analysis before evaluation at G1; none is accepted here. Calibration and scored evaluation must use distinct material, retaining amendments and failures.

## Verification and disposition

A fresh reviewer audits the cited definitions and whether each candidate fault has an independently reviewable observation. Future runs need frozen inputs, generator/tool versions, seeds, mutation IDs, expected classifications, commands, limits, raw verdicts and reviewer decisions. No fault was seeded or checked by a tool here. Independent review, empirical effectiveness and budgets remain pending; token/spend and human-attention metering are unavailable. Continue synthesis/protocol preparation without claiming adequacy or new implementation evidence.
