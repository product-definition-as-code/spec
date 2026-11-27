# Controlled pilot attempt 1 — invalid execution, no scientific comparison

**G2 recommendation: revise execution, not PDaC.** Owner-approved G1 was executed once against immutable commit `d7a255328b48d9830fd927f964de1834edaa3805`, manifest `96dbd553c7118d7f3274d0c99081e24e5f774d8b295c650ac2e7d6c6ec923a1e`. [Actual owner approval](https://github.com/product-definition-as-code/spec/issues/130#issuecomment-7228575750). A common transport defect prevented author tools from running. There are no authored decision/formal models, Product Changes or valid comparative outcomes. This is an **invalid experiment**, not refutation of H0 or a failed mathematical proof.

## Observed execution

| Cohort | Launched baseline sessions | Blocked successor slots | Eligible case observations | Unknown |
| --- | ---: | ---: | ---: | ---: |
| C1 ordinary requirements | 2 | 14 | 1,164 | 1,164 |
| C2 PDaC, no formal verification | 2 | 14 | 1,164 | 1,164 |
| C3 proof-driven, no PDaC | 2 | 14 | 1,164 | 1,164 |
| C4 proof-driven with PDaC | 2 | 14 | 1,164 | 1,164 |

All 64 planned slots have immutable records: eight actual fresh author invocations, 56 dependency-blocked slots. All eight CLI processes returned zero but lacked required outputs; readiness checks correctly rejected them. The four host ProductShape post-checks validated empty initialized kernels, **not implemented product decisions or applied changes**. Actual author solver processes, independent scoring solver processes, Python model workers and Product Changes: **zero**. Planned scoring maxima (64 batches / 7,776 queries) were not executed.

The deterministic scorer retained all **4,656 observations as unknown**, with no exclusions or automatic relaunches. Matched C3/C4 observations number 1,164, 582 per schedule. The machine's both-schedule screen is false because there is no demonstrated improvement; its conservative lower bound is not an observed 100-point disadvantage. No correct outcomes or known discrepancies were observed because nothing was evaluable. Do not interpret either zero as a correctness/error-rate estimate.

Nine separate fresh documentary/synthesis sessions were launched under the frozen protocol. All nine produced **no assessment artifact**; their process receipts alone do not constitute independent review. The coordinator's diagnosis below is not an independent expert evaluation. Original author/reviewer events, receipts and Git histories are preserved; no replacement sessions were launched.

## Deterministic diagnosis and bounded correction

The user systemd manager supplies `TMPDIR=/home/juan/.cache/lighthouse/tmp`. Filtering the caller's environment did not filter the manager's environment. The outer namespace hid that host path. A no-LLM reproduction of the exact nested tool path failed with exit 101: `failed to resolve synthetic mount registry temp directory ... No such file or directory`. Author messages also reported this failure before their first executable command.

The proposed correction clears inherited namespace environment and sets temporary variables to namespace-local `/tmp`. A deterministic probe confirms the missing-directory defect is corrected while host home remains hidden. **Full tool transport still fails**: the nested sandbox reports that it cannot create a namespace. Three user-namespace variants and a legacy backend probe also failed; raw outputs are retained, not reclassified as passes. The specific kernel/policy mechanism is not conclusively attributed. No host security policy was changed and no sandbox was disabled.

This exposes the preparation gap: the prior checks tested authentication, outer mounts and individual gateways, but not a real CLI tool command through the complete nested transport. New `preflight.py` tests a public read/write command in that exact transport **without a model call**. Failed preflight now prevents `prepare` from issuing another freeze/dispatch package. The new guard correctly fails on this host; it is not a claim that execution is repaired or ready. Corrections are in the reporting branch only, never substituted into the frozen attempt.

## Evidence, reproducibility and exposure

[Machine result](../evaluation/results/attempt-1/result.json), compressed public evidence with SHA256 and eight Git bundles, and [deterministic audit](../evaluation/audit_results.py). The audit rechecks all file pins, frozen approval/source, event hashes, source snapshots, dependency accounting and finite-discrepancy summaries with **zero LLM/solver calls**:

```sh
python3 docs/research/v0.4.0/evaluation/audit_results.py \
  docs/research/v0.4.0/evaluation/results/attempt-1
```

Private oracle/case files remain private. Public case identifiers are hashed; expected answers/input payloads are excluded. Exact original score files remain in the evaluator's local custody. Hash auditing checks consistency, not authenticity of a provider or faithfulness of a missing formalization. The requested model was gpt-6.1-sol, medium, Codex CLI 0.172.0; serving weights are opaque. Same-provider/host independence limitations persist, and none of the unsuccessful agent reviews is human expert validation.

Author wall time summed **143.968 s**; documentary wall time **382.790 s**, excluding preparation, coordinator analysis and diagnostics. Reported author usage: 381,022 input tokens (310,912 cached), 2,442 output; documentary usage: 997,101 input (860,288 cached), 13,419 output. Billing amount/coordinator usage unavailable; no zero-cost or cost-advantage claim. These are failed infrastructure costs, not method-governance or reconstruction benchmarks.

H0/H1/H2/H3/H5 remain unassessed by this attempt; original seeded-mutation detection and human-review-time endpoints remain unmeasured. H4/implementation correspondence was out of scope and remains untested. Earlier #149–150 engineering evidence remains valid within its stated boundaries and cannot substitute for this missing controlled comparison. No architectural/formalism selection or normative v0.4.0 conclusion follows.
