# Intent and consistency — exploratory result (#131)

Question: can actual v0.3.0 product artifacts and ProductShape changes be checked against an external formal interpretation without changing normative contracts?

[Executable integration and guarantees](../experiments/11-evolution/README.md), [raw results](../experiments/11-evolution/results/summary.json). Booking capacity/lead rules, domain footprint, issuer assumptions and lifecycle topology produce eleven declared SMT queries. Two engines agree before/after six actual Product Changes. A contradictory proposed rule passes structural overlay validation but is unsatisfiable formally; rejected, not applied. No LLM participates in computation.

Formalization is a handwritten interpretation. States/edges come from lifecycle frontmatter; integer guards/effects, credential trust and prose meaning require semantic judgment. A two-to-three-slot source edit with unchanged encoding still passes; explicitly correcting the encoding falsifies the capacity-2 Structured Behaviour. Hashes reveal change, not translation adequacy. Independent review found another real prose/encoding mismatch, corrected with all affected artifacts updated.

This supports feasibility of an external integration with unchanged v0.3.0, not intent fidelity, H1 or distinctive H0 value. No owner-approved held-out intent oracle or four-cohort experiment exists. #131 remains open for those acceptance criteria; public data cannot become held-out evaluation material.

## Controlled attempt after G1

The approved controlled attempt was executed once and is [invalid due to common tool-transport failure](12-independent-evaluation.md). Eight authors produced no models; successor slots remain blocked and all case outcomes unknown. Earlier exploratory observations above remain engineering evidence only. This issue's controlled scientific acceptance is not completed; [G2 recommends bounded revision](../gates/phase-2-decision.md).
