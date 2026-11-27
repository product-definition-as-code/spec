> Execution update: G1 was [approved](https://github.com/product-definition-as-code/spec/issues/130#issuecomment-7228575750); [attempt1 failed at full tool transport](../reports/12-independent-evaluation.md). All outcomes preserved; [G2 revision approval](../gates/phase-2-decision.md) is pending. The new deterministic `preflight.py` blocks preparation on this host. Original commands below describe the historical frozen package, not authority to retry it.

# Controlled comparison preparation

Prepared after merged #150; non-normative, owner G1 pending. [Single owner decision](G1-decision.md), [complete frozen candidate](frozen-protocol.md), [private commitments and limits](custody.md). Author-only packets are constructed from current approved intent, never the full future episode files. All mathematical checks use deterministic tools; agent interpretation/review is labelled separately.

Existing prerequisites: Linux bwrap + user systemd cgroups, Python requirements from repository, Node >=22, Git, Codex CLI0.172.0 with existing subscription, ProductShape0.26.1 lock from `../experiments/11-evolution/tools`, pinned Z3/cvc5 installed by the existing installer. No new services or paid infrastructure. Current machine transport and namespace probes passed; recorded below. No scored session has started.

```sh
python3 docs/research/v0.4.0/evaluation/test_pilot.py
python3 docs/research/v0.4.0/evaluation/test_score.py
python3 docs/research/v0.4.0/evaluation/pilot.py prepare /tmp/pdac-v040-controlled-1 \
  --tools /tmp/pdac-v040-tools --productshape /tmp/pdac-v040-productshape
```

`prepare` pins exact source/public files, packages/binaries, agent client/model request and counterbalanced64-job order. It makes no model calls. Run from the final merged revision; after owner approval record the genuine decision in #130 with `G1 decision: approve`, full source commit and frozen-inputs.json SHA256. Do not generate that comment without the owner's actual instruction. Then:

```sh
python3 docs/research/v0.4.0/evaluation/pilot.py approve /tmp/pdac-v040-controlled-1 \
  --owner-comment https://github.com/product-definition-as-code/spec/issues/130\#issuecomment-OWNER_DECISION
python3 docs/research/v0.4.0/evaluation/pilot.py run /tmp/pdac-v040-controlled-1
# Evaluator-only, after all author attempts freeze. Custody directory is never author-mounted.
python3 docs/research/v0.4.0/evaluation/score.py \
  --manifest /tmp/pdac-v040-controlled-1/submissions.json \
  --cases /home/juan/.local/share/pdac-v040-evaluation/g1-custody/cases.json \
  --output /home/juan/.local/share/pdac-v040-evaluation/scored-attempt-1 \
  --ledger /home/juan/.local/share/pdac-v040-evaluation/solver-ledger.json
python3 docs/research/v0.4.0/evaluation/review.py \
  --pilot /tmp/pdac-v040-controlled-1 \
  --score /home/juan/.local/share/pdac-v040-evaluation/scored-attempt-1 \
  --output /tmp/pdac-v040-controlled-1/independent-review
```

No automatic author retries/resume; one output directory per scored invocation. A failed/missing author trajectory remains unknown, not removed or repaired until a preferred result appears. Stop on unavailable dependency/security/containment failure, material unresolved product intent, cap or gate. Preserve negative/inconclusive/invalid attempts separately. No normative files, production features, packages or releases change.

Public selftests include mount isolation, approval refusal, current-only handoff, budget reservation, worker failure, finite both-engine relation checks and deliberately weak contracts. They are infrastructure tests, not additional feasibility studies/cohort data. Authentication-only fresh CLI probe returned TRANSPORT_OK without tool use; requested gpt-6.1-sol medium, CLI0.172.0, no global config/skills/plugins; provider serving revision unavailable. Reported usage14,847input/7outputtokens (12,288cached), subscription billing amount unavailable. It is not included as a research author. See [preparation receipt](preparation.json) for checks and [review findings](independent-review.md).
