# Frozen attempt 1 — invalid controlled execution

[Result](result.json), [interpretation and limitations](../../../reports/12-independent-evaluation.md), [G2 recommendation](../../../gates/phase-2-decision.md). The archive retains all64 slot records, eight author event logs/source histories, nine failed review logs, deterministic unknown summaries and diagnosis. Private inputs/oracle/answers/authentication files are excluded; public case IDs are hashed. Original scored custody files remain local and unchanged.

```sh
python3 docs/research/v0.4.0/evaluation/audit_results.py \
  docs/research/v0.4.0/evaluation/results/attempt-1
python3 docs/research/v0.4.0/evaluation/test_audit_results.py
```

Audit does not invoke an LLM or solver. It verifies provenance consistency and accounting; this attempt supplied no mathematical result or scientific comparison. No retry is authorized by these reproduction commands. The new transport guard fails on the current host; successful unit tests are not evidence of complete transport compatibility.
