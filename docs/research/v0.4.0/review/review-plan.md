# Independent documentary review — approval proposal

**Not launched.** Separate resource approval is required by the owner's G1 decision. Calibration caps do not cover these reviews. Coordinator prepares packets and consolidates findings; reviewers must not be authors of the reports they review. This administrative follow-up is stacked on PR #148 and does not modify the eight original PR heads.

## Proposed limits, not approved allowances

| Track | Candidate requested model | Monetary ceiling | Total tokens | Active time |
| --- | --- | --- | --- | --- |
| [Scientific/formal methods](scientific.md) | gpt-6-astra | EUR 1 | 28,000 | 12 minutes |
| [Experimental methodology](methodology.md) | gpt-6.1-sol | EUR 1 | 28,000 | 12 minutes |
| [PDaC architecture](architecture.md) | gpt-6.1-terra | EUR 1 | 28,000 | 12 minutes |

Aggregate proposed ceiling: EUR 3, 84,000 total tokens, 36 active minutes, one active reviewer, sequential execution, zero retries/repairs. Tokens include all packet/context, tool turns, output and reasoning where billed; aim for at most 24,000 input/context and 4,000 output/reasoning within each ceiling. Availability, pricing and enforceable accounting are not verified. If a packet cannot fit, stop and request a smaller explicit scope; do not silently omit evidence. Use existing subscriptions only. No purchases, solver jobs, delegation, code changes or GitHub writes by reviewers.

These ceilings are a bounded proposal, not a claim that each full review will fit or be complete. Before launch record actual billing source, enforceable caps and conservative accounting margins; fail closed if containment is unavailable. Requested/local model settings must be distinguished from resolved and provider-reported identities. Record unavailable identity fields as unknown. Different advertised model names do not establish independent expertise or eliminate correlated model/provider errors.

Separately proposed consolidation/remediation allowance: EUR 1, 16,000 tokens, 10 active minutes, coordinator only, one focused correction pass for evidenced documentary defects, zero automatic retries. It requires explicit approval too; unresolved material findings or scope beyond that allowance return to the owner. No allowance for new experiments or features. Total review plus remediation proposal: EUR 4 / 100,000 tokens / 46 active minutes. None is approved by publishing this proposal.

## Packet and independence

Use fresh sessions with no authoring conversation, memory, other reviewer findings or author explanations. Supply the relevant standalone brief, this plan, the exact [snapshot manifest](snapshot-manifest.json), all thirteen listed files, the approved research proposal at the stated revision, and relevant released v0.3.0 contracts/governance at that main revision. Allow read-only primary-source access; log every additional source and exact revision consulted. Distinguish source inaccessibility from a verified source finding. These follow-up calibration documents may be supplied as explicitly labelled administrative context, never as experiment evidence.

Before starting, record packet hashes, session identity, requested/resolved/provider-reported model, author involvement/conflicts, infrastructure and limits. Afterward record actual exposure, source retrievals, consumption, duration, truncation and other limitations. Author session's provider-reported model identity is unavailable; local requested configuration was gpt-6.1-sol. Model overlap and a common packet curator are conflicts/limitations to disclose, not concealed independence. Reviewer sessions must not participate in drafting fixes before recording their independent findings.

Agent review provides a separate documentary critique; **it is not independent human expert validation**. Human acceptance, held-out custody and evaluator assignments remain unresolved. Do not invent named experts or claim evaluation independence from session separation alone.

## Finding contract and consolidation

Return a concise report to `docs/research/v0.4.0/review/<track>-findings.md` through the coordinator's focused PR, without publishing it yourself. Each finding needs severity, exact PR/commit/file/line or claim, concrete evidence/primary source, impact, certainty and smallest corrective action. Separate verified defects, unsupported claims, source-access limitations and open questions. No speculative enhancements or scope expansion.

- **P0:** fabricated evidence, concealed semantic decisions or false proof claims.
- **P1:** material mathematical, methodological or compatibility defect that blocks acceptance.
- **P2:** concrete reproducibility, clarity or usability defect with limited impact.
- **P3:** minor correction with evidence.

Report all observed material findings; if budget prevents coverage, list unreviewed claims rather than declare them sound. Include a coverage statement and acceptance recommendation. Failed verification, prototype defects, inconclusive evidence and research rejection remain distinct.

Coordinator preserves each original review, consolidates duplicates without deleting dissent, links disposition and exact corrected revisions, and reconciles every dependent report/ledger/protocol. Correction does not erase original evidence. Material changes require proportionate re-review under separately approved limits. PR #141–148 remain unmerged and G1 open until the owner accepts exact revisions and all required gate fields. No scored experiments follow automatically.
