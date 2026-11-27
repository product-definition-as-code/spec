# Claim/evidence ledger — phase-1 preparation

Issue: #128; date 2026-11-27. Status: provisional, independent review pending. Source findings are documentary, not replicated; the original reports had no formal executions; subsequent public exploratory results are recorded below, without comparative claims. [Synthesis and exact six-report inputs](reports/07-baseline-synthesis.md). [Approved proposal](../v0.4.0-formal-product-definition.md).

| ID | Claim / question | Evidence class and source | Boundary / required next evidence |
| --- | --- | --- | --- |
| C01 | Product artifacts have stable identities, authored relationships and structured change contracts. | Existing contract: tagged [artifacts](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/artifacts.md), [relationships](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/relationships.md), [changes](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/product-changes.md). | Structural contracts do not establish mathematical intent semantics. |
| C02 | Citation freshness and external outcomes are separate. | Existing contract: tagged [citations](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/citation-contract.md) and [Verification Evidence](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/verification-evidence.md). | Direct freshness is not full semantic dependency validity; no new evidence fields. |
| C03 | PDD describes reviewed intent, proofs, mutation checks and explicit trust without PDaC. | Published demonstration: [Microsoft walkthrough](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/), steps 4–7. | Not independently replicated; no measured PDaC comparison. |
| C04 | Existing methods offer state, contracts, refinement and assumptions. | Published definitions: [Z](https://www.rose-hulman.edu/class/cs/cs415/zrm.pdf), [Event-B](https://wiki.event-b.org/images/SM%26D-KAR.pdf), [GORE](https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf), [AGREE](https://github.com/loonwerks/AGREE). | Capability does not establish owner usability or source-to-runtime correspondence. |
| C05 | Adequacy needs more than accepting a proof. | Published discussion: [SPOTs](https://risemsr.github.io/blog/2026-04-16-spotting-specs/); [Dafny diagnostics](https://dafny.org/latest/DafnyRef/DafnyRef), section 13.7.5. | Held-out faults, witnesses and independent intent evaluation remain unexecuted. |
| C06 | Representing assurance is distinct from validating it. | Standard: [SACM 2.3](https://www.omg.org/spec/SACM/2.3/PDF), sections 7.3–7.5. | No automatic trustworthy proof/evidence envelope follows. |
| H0 | Does PDaC add net effectiveness, reliability and maintenance value across changing intent? | Unverified overarching hypothesis in the approved proposal. | Matched four-cohort evidence, especially 3/4; governance cost and uncertainty included. |
| H1 | Do agents formalize intent more faithfully with human ownership? | Unverified hypothesis. | Independently judged semantic choices and owner-approved scenarios. |
| H2 | Do product predicates/lifecycles expose useful inconsistencies/obligations? | Unverified hypothesis. | Non-empty witnesses, contradictions/counterexamples and behaviour preservation. |
| H3 | Do adequacy methods expose missing/weak/vacuous contracts? | Unverified hypothesis. | Frozen fault classes, held-out evaluation, valid mutants, unknowns and false positives. |
| H4 | Can independent agents maintain traceable implementation contracts/proofs? | Unverified hypothesis. | Product-session aspects in phase 2; actual bridge/runtime correspondence only in phase 3. |
| H5 | Do Product Changes preserve honest verification continuity? | Unverified hypothesis. | Five-way structural/freshness/dependency/validity/applicability assessment across successive changes. |
| O01 | Which authority, formalism or architecture is adequate? | Open decision: A–D and all three authority models retained. | Independent evidence, net costs and explicit owner decision; no specification change remains possible. |

## Reproduction and updates

Audit primary definitions and exact report revisions before accepting a claim. Record dated reviewer judgments/conflicts and linked PRs; this author's self-check is not independent review. Future experiments add run IDs, raw evidence and assumptions without overwriting negative/inconclusive attempts. Classify invalid results, correctable defects, failed verification and unsupported analyses separately from evidence against hypotheses/architectures/extensions.

Access limitations and available substitutes are in the six input reports. Scored thresholds, tool/model freeze and held-out arrangements remain pending G1; literature pages are not pinned executable artifacts. Missing usage metering does not block exploration. No experimental results may be inserted from historical v0.3.0 qualification. Resource metering is unavailable, not zero. This ledger is non-normative and adds no canonical Product Artifact or proof level.

## Subsequent exploratory evidence

| ID | Observation | Evidence / limitation |
| --- | --- | --- |
| E01 | Two SMT engines agree on 17 declared product-model verdicts, including invariant checks, contradiction, weak-contract and vacuity probes. | [Models/raw logs](experiments/README.md); same encoding means agreement does not validate intent fidelity or H0. |
| E02 | Alloy yields a three-node cycle; Python checks a returned cycle. | Finite counterexample, not an unbounded theorem. |
| E03 | Dafny verifies reserve/release arithmetic and rejects a mutant. | Handwritten contract toy, not executed application correspondence or H4. |
| E04 | Five draft change snapshots separate hashes/one-hop impact from declared formal dependencies and isolated semantic deltas. | Manual unaudited dependency map; no ProductShape apply, full conformance or automated semantic equivalence claim. |
| E05 | Corrected SB probes add an omitted final-state conjunct; original results retained. Resource-limited query yields unknown. | Encoding defects and inconclusive outcomes are not successful verification. |

Independent agent review at `91053aa`: [scientific](review/scientific-findings.md), [methodology](review/methodology-findings.md), [architecture](review/architecture-findings.md). Three P2 findings corrected with retained inputs/results; no P0/P1 established within inspected coverage. No independent human expert validation or scored evidence follows. Corrected dispositions are coordinator-verified, not automatically re-accepted.

## Actual ProductShape integration

E06: [Six real Product Changes and deterministic post-apply rechecks](experiments/11-evolution/README.md), [raw receipts/two-run summary](experiments/11-evolution/results/summary.json). ProductShape 0.26.1 against unchanged v0.3.0; 334 executed queries per suite, not independent observations. Direct freshness and old proof outcomes can outlive intent applicability; editorial freshness can change without changing formulas. Handwritten semantic bindings remain a review boundary. Independent review caught a real prose mismatch and incomplete auditor, corrected with retained development evidence ([dispositions](review/integration-findings.md)). No H0/H1/H5 advantage, independent agent maintenance or normative requirement established.

E07: [Approved controlled attempt1](reports/12-independent-evaluation.md) failed at execution transport:64slots recorded,8authors launched,56blocked;4,656unknown observations,zero model/solver results. Nine independent documentary sessions produced no assessment. Deterministic reproductions establish infrastructure defects, not evidence for/against H0/H1/H2/H3/H5; H4 remains out of scope. All attempts preserved with hashed public case IDs/private answers excluded. [G2 recommends bounded revise](gates/phase-2-decision.md); no architecture or normative conclusion.
