# Four public feasibility checks — initial plan

Current execution and explicit corrections: [results](../experiments/README.md). The text below is the initial check selection, not an execution restriction.

Selection follows [synthesis](https://github.com/product-definition-as-code/spec/blob/3da4c1b4dad6e0905ad9aff285708a22856bd243/docs/research/v0.4.0/reports/07-baseline-synthesis.md), especially fragment portability, assurance boundaries and reusable mechanisms. These checks investigate availability, licensing, installation, pinned reproduction, supported fragments and useful outputs; they do not select a formalism, architecture or pilot winner. No held-out data or scored benchmark is used.

| Check | Public toy input and expected observation | Limits of interpretation |
| --- | --- | --- |
| Z3 | QF_LIA integer `0 <= x <= 2`: obtain a witness; add `x > 2` and request unsatisfiability output. Two top-level satisfiability queries in one invocation. | A witness/unsat response is fragment-specific. Record whether a proof artifact is available, its format and checker/trust boundary; do not equate a status with independently checked proof. |
| cvc5 | Same frozen SMT-LIB input and two queries, recording model and supported proof/unsat explanation output. | Compare portability and access, not solver superiority from one toy. Unsupported proof output is a limitation, not an invented proof. |
| Alloy | Public finite relation of three nodes; seek a counterexample to an intentionally false acyclicity assertion. One bounded check. | Counterexample search is within the declared scope; absence would not prove unbounded correctness. |
| Dafny | One file containing a valid arithmetic postcondition and a deliberately false postcondition, with distinct names; one verification invocation. Record successful obligation and concrete failure diagnostics separately. | Feasibility of contracts and diagnostics only; not the phase-3 PDaC-to-implementation bridge or a product-level result. |

Before execution freeze exact source bytes, commands, tool/backend versions and assets. The initial sample has four tool checks; help/version inspection and explicit corrections are recorded separately. Preserve failures; ordinary bounded, versioned corrections are authorized. No automatic retry loops. Record all tool and nested solver invocations, top-level queries and backend queries if observable; hidden VC/query counts must remain explicitly unknown. Do not invent an aggregate scored-pilot query ceiling from these planned counts.

Use isolated local directories and existing infrastructure, with no inference inside tool invocations. Apply the owner's wall-time/memory caps to the complete process tree. Stop the affected job on containment failure, timeout or memory breach; retain logs. Escalate paid provisioning, security issues or unavailable dependencies. Unknown metering does not block execution. Installation failure consumes that check. Record exit codes, durations, peak memory if measurable, exact input/output hashes, assumptions, platform, licences and exclusions. Reproduction must use the same assets and bytes; no feasibility claim until it actually runs.

## Pins and licensing preflight

See [metadata](tool-candidates.json) for immutable source commits, release assets, sizes and publisher-supplied SHA-256 digests. Retrieved from GitHub release/tag and licence endpoints on 2026-11-27; binaries were not downloaded and digests have not been checked against bytes.

- **Z3 5.3.3**: source licence at the pinned tag is MIT. Candidate Linux x64 glibc 2.39 archive; platform compatibility untested.
- **cvc5 1.4.2**: COPYING specifies modified BSD with optional GPL-linked configurations. Candidate non-`gpl` static Linux archive; inspect bundled notices before use, without assuming the asset name clears transitive licensing.
- **Alloy 6.2.0**: pinned root LICENSE begins with a warning that its Apache text is not valid yet and code is currently MIT. Record this ambiguity, inspect distribution notices before use, and seek clarification if unresolved; do not report licence clearance. Publisher asset digest unavailable in inspected metadata; a later locally computed hash would establish downloaded-byte identity, not publisher provenance.
- **Dafny 4.11.0**: root source licence MIT; candidate Ubuntu 22.04 x64 archive. Bundled solver/runtime notices and actual compatibility remain unverified.

These are candidate pins, not installed versions. Licensing links are retained in the metadata. TLA+/ProB would add state-machine environments beyond this four-check sample; Verus/F* add bridge-specific dependencies; PDD Kit access/reproduction remains unestablished. These exclusions are budget choices, not evidence against their methods. Reconsider only through the gate; do not silently replace failed checks.
