# Historical preflight — superseded

The owner explicitly removed billing/token prerequisites and authorized execution. The stop below records an earlier decision, **not a current blocker**. See [executable results](../experiments/README.md) for current status.

# Calibration preflight — stopped before execution

Non-normative administrative record, 2026-11-27. Coordinator: this Codex session. Baseline: PR #148 at `e5542f2ea486100c35327b418e3e020e4a93b3aa`. [Owner decision recorded at G1](https://github.com/product-definition-as-code/spec/issues/130#issuecomment-7211316146).

## Authorization and observed controls

The owner authorized at most four public non-held-out checks, EUR 5 incremental cost, 32,000 tokens and 20 active execution minutes; one active agent; each solver process at most 30 seconds / 2 GiB; zero automatic retries or repairs. Existing infrastructure/subscriptions only. Scored experiments and review execution are not authorized by these limits.

Administrative inspection only: local Codex CLI 0.172.0 reports ChatGPT authentication metadata, no configured API key, and requested model `gpt-6.1-sol`. No configured OpenAI, Anthropic or Azure API key was detected in the inspected environment. Credentials and account identifiers are excluded from this record. This does not establish the billing source or provider-reported identity of the current coordinating session.

Actual billing source, available included allowance, credit/pay-as-you-go applicability and attributable monetary consumption could not be established. The inspected CLI help and session interface did not establish an enforceable per-execution monetary or total-token cutoff. This is a limitation of this preflight, not a claim that no Codex deployment can enforce budgets. Official [authentication](https://learn.chatgpt.com/docs/auth.md) and [pricing](https://learn.chatgpt.com/docs/pricing.md) documentation distinguish authentication, included usage and additional billing; authentication alone does not settle the applicable charge.

**STOP:** cost containment cannot be guaranteed. No binaries downloaded, tools installed, solver processes launched, retries or repairs attempted. **0/4 feasibility checks executed.** No purchase or paid provisioning. Actual coordinator token consumption and billing are unavailable, not zero. Calibration execution time/results are not measured because it did not start; administrative preparation is not a solver result or evidence of compliance with a metered execution budget.

## Local availability and remaining entry conditions

Observed on PATH: Python 3.14.4, Node 22.22.1, OpenJDK 21.0.13.1, `timeout`, `prlimit`, `unshare`, `dotnet`. Z3, cvc5, Dafny, Verus, ProB and F* commands were not found on PATH; this is not a host-wide installation inventory. Java availability does not prove Alloy installation. No container was pulled or started.

Before the first check, expose the actual billing source and a controlled execution mechanism that guarantees the authorized EUR/token limits, with a ledger covering coordinator use and tooling. Record remaining allowance, token accounting, conservative stop margins, active-time accounting and process-tree enforcement for solver wall time/memory. If this cannot be established, remain stopped; an additional approval alone does not supply a cost control. Solver wrappers must enforce limits for descendants, not only a parent process; no wrapper has been qualified here.

[Four selected public checks](public-check-plan.md) and [independent review proposal](../review/review-plan.md) are prepared, not executed. Exact asset metadata is in [tool candidates](tool-candidates.json). Accessibility means release metadata was readable, not installation or execution succeeded. No calibration-based pilot reduction, aggregate query limit or final threshold can honestly be justified yet.
