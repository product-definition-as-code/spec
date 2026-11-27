# Microsoft/GitHub Next foundations

Snapshot boundary: the documentary findings and execution-status statements below describe the original phase-one report revision. Subsequent authorized [executable exploration](../experiments/README.md) and independent review are tracked separately; unavailable cost/token metering is not a current prerequisite. No historical result is silently upgraded.

Issue: [#122](https://github.com/product-definition-as-code/spec/issues/122). Evidence cutoff: 2026-11-27. Status: documentary findings, independent review pending. Authority: [approved research proposal](../../v0.4.0-formal-product-definition.md), not a v0.4.0 feature decision.

## Findings and provenance

| Primary source and inspected version | Published finding | Limit / reproduction prerequisite |
| --- | --- | --- |
| Lahiri, [Intent Formalization](https://arxiv.org/html/2603.17150v1), arXiv:2603.17150v1, 2026-03-17; sections 2.1, 3 and 4 | Distinguishes specification from verification and identifies human validation of intent and compositionality across changes as research problems. | An agenda/survey does not establish a PDaC effect or a generally reliable intent oracle. Replication would require the underlying study artifacts and matching tasks. |
| GitHub Next, [PDD Kit](https://githubnext.com/projects/pdd-kit/), November 2026 live project page; “What to Expect” | Describes a Rust/Verus prototype, combining intent review with proofs and tests. | One demonstrated application is not cross-domain or cross-session effectiveness evidence. A reproducible kit revision, licence and accessible execution bundle were not established from this page; this is an access uncertainty, not a claim that no bundle exists. |
| Lavaee/Philipose, [Microsoft Research walkthrough](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/), 2026-11-05; steps 4, 6–7 and proof boundary | Reports assumed database/cryptographic/clock contracts, clause-targeted implementation mutations and routing the real login handler through verified logic. | The surrounding services and toolchain remain trusted; tests do not prove those assumptions. The demonstration does not measure PDaC against an equivalent non-PDaC workflow. |
| Swamy/Lahiri, [SPOTs](https://risemsr.github.io/blog/2026-04-16-spotting-specs/), 2026-04-16; “Small Proof-Oriented Tests” and takeaways | Verified clients exercise abstract component specifications; the authors report gaps and subsequent refinements. | Small clients can miss gaps, need review and risk overfitting. Their result is not a completeness guarantee or an independent replication here. |
| Fakhoury et al., [DeepTest](https://risemsr.github.io/blog/2026-05-04-deeptest/), 2026-05-04; specification inference and test generation | Builds inferred specification knowledge from several sources and generates behavioural tests; the article links concrete bug reports. | Inferred intent may reflect existing implementation mistakes. Test coverage and bug examples do not establish mathematical correctness or governed product intent. |

All five pages were retrieved on the cutoff date; dated posts are publication versions, not immutable software releases. [The ART manuscript](https://fstar-lang.org/papers/PoP-ART.pdf) timed out; its full-text findings were not used. No kit, prover, test generator or study was installed or executed.

## Reusable mechanisms and evidence against extending PDaC

**Interpretation for H0/H1/H3/H4, not measured results:** separate approved intent, formal obligations, tests and trust decisions; expose unsupported clauses rather than silently weakening them. Existing PDD work already combines these mechanisms without PDaC. Their usefulness alone cannot justify adding a PDaC profile or native semantics.

The distinctive question is whether PDaC's identities, structured decisions and Product Changes improve fidelity, contract adequacy and maintenance across successive intent changes enough to repay governance cost. Compare equivalent formal tooling, intent facts and agent capability in cohorts 3/4. Do not give the non-PDaC control an intentionally poor plan, missing history or no traceability.

Proposed observations: semantic substitutions missed by owners, reconstruction work between independent sessions, obligations/evidence incorrectly carried forward, and human attention needed to resolve ambiguity. These are evaluation candidates under the proposal, not published PDD measurements.

## Reproduction and disposition

A reviewer can follow the cited sections to audit the claim boundaries. Actual replication needs accessible licensed artifacts, pinned tool/model revisions, commands, assumptions, limits and raw results; routine exploratory execution is now authorized; scored comparisons still require a frozen protocol and independent evaluation. If PDD Kit remains inaccessible, compare a clearly named external-tool workflow, never call it a PDD Kit replication.

Independent review is pending; no statistical, product-model or implementation-proof experiment ran. No empirical finding supports or refutes H0 yet. Source retrieval and document checks are the only executed work. Token/spend and human-review metering are unavailable; there were no delegated agents or solver jobs. Continue to the other phase-1 reviews; carry the access uncertainty and strong-control requirement into synthesis and G1.
