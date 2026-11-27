# Independent agent review — scientific/formal methods

Reviewed commit `91053aadbd2f40f9ae2a3c2a0c12bcd814328169`, 2026-11-27, fresh session `/root/scientific_review`, no author conversation or other reviewer findings supplied. Coordinator transcribed the returned report; reviewer did not edit or run experiments. Requested named model, resolved model and provider identity unavailable; system identifies Codex based on GPT-6. Same infrastructure/provider and coordinator-curated packet limit independence. Automatically supplied generic workspace/memory guidance was present; no research authoring discussion was used or memory files retrieved. This is **not independent human expert validation**.

## Findings

**SCI-01 — P2, high certainty.** Mutation probes `guard-mutant-overbooks`, `missing-frame-changes-owner` and `double-release-mutant` leave `nextState` free (`experiments/models/booking.smt2:105–138`, `experiments/check.py:25–27`, README:14/45 at reviewed commit). Both saved corrected solver outputs give state 0, inconsistent with the labelled confirmation/release transitions. Arithmetic counterexamples remain valid, but the full valuations do not yet describe those lifecycle transitions. Minimum correction: explicitly label partial probes or complete and check their final states; preserve earlier runs. The three invariant-preservation obligations already constrain final states and are unaffected.

No evidenced P0/P1 finding in this bounded review. Recommendation: continue public exploration; correct SCI-01 before using those valuations as lifecycle-transition evidence. This is not evidence against the research direction.

## Coverage and limitations

Verified all thirteen original manifest hashes against pinned Git objects. Inspected current reports, ledger, protocol/benchmark/evaluation, proposal, README, models, checker/evolution/reproduction scripts and relevant SMT/Dafny/Alloy outputs. Distinguished original documentary snapshots from new administrative/exploratory evidence. Excluded untracked reproduction-summary that appeared during review.

Primary-source spot checks: Intent Formalization, SPOTs, Microsoft PDD walkthrough, GitHub Next PDD page, DeepTest, Alloy 6 docs, F* overview/tutorial and Dafny 4.11 manual. Inspected attributions preserve human intent validation, trust boundaries, finite scopes and model/implementation distinction. Conditional integer preservation is not bounded enumeration; proof emission is correctly distinguished from independent checking. No scored PDaC benefit or H0–H5 confirmation established.

Not independently established: exhaustive Z/B/Event-B/OCL/TLA+/ProB/SACM/GORE/AGREE/QuickCheck/QuickChick attribution, licensing, dependency completeness, historical run authenticity or clean reproduction. Previously inaccessible ART/traceability full texts were not retried. The reviewer made no installations, solver runs, edits or recursive delegation.

## Coordinator disposition

SCI-01 corrected in model v3: result state 1 for confirmation mutants and 3 for double-release; witness checks now enforce those states. `booking-v2.smt2` and earlier raw results preserve reviewed inputs. Both engines retain the same 17 verdicts; new `*-booking-v3` outputs and the [reproduction receipt](../experiments/results/reproduction-summary.json) record explicit corrected execution. This disposition is coordinator verification, not reviewer re-acceptance of the correction.
