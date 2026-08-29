<p align="center"> <img src="https://raw.githubusercontent.com/product-definition-as-code/.github/main/profile/pdac-social-banner.png" alt="PDaC: Product Definition as Code" width="720" /> </p>

# The PDaC Specification

**The normative specification of Product Definition as Code (PDaC).**

<!-- canonical-pdac-definition:start: copy verbatim or link; see CONTRIBUTING.md, "Agreed wording" -->

Product Definition as Code keeps the agreed product definition in versioned Markdown that delivery work cites instead of restating.

The definition lives in small, related Markdown files: actors, journeys, use cases, business rules, domain terms and requirements. Together they form a validated product graph that humans and AI agents can read alike. It changes only through an explicit Product Change, reviewed and accepted by a human. Consumer documents such as SDD specs, tasks and agent prompts cite the exact product text they rely on by stable ID and content digest. When cited text changes, tools flag every recorded citation for review, so documentation drift is detected instead of remaining silent. Deterministic tools check structure and references, never truth. People decide what is true and what should change.

<!-- canonical-pdac-definition:end -->

Shown with ProductShape, the reference implementation of Product Definition as Code:

```console
$ prodshape citations verify
stale	BR-REFUND-001	openspec/checkout-flow.citations.yaml:1
warning PRODUCT061 openspec/checkout-flow.citations.yaml [BR-REFUND-001]: Citation of 'BR-REFUND-001' is stale: canonical content changed since the citation was recorded
1 citation(s): 0 current, 1 stale, 0 tampered, 0 unresolved
```

That is the citation contract and the delivery boundary of PDaC. It is an open methodology for the upstream layer of the AI-SDLC. Those citations brief a Spec-Driven Development framework, an AI coding agent or a human team. [See it in 30 seconds on pdac.dev](https://pdac.dev/).

This repository holds the Product Definition as Code specification, the manifesto and the conformance tests. It is implementation-independent by design: contracts, not commands.

<p align="center"> <img src="assets/diagrams/pdac-0-one-minute-map.png" alt="Two zones. On the left, product thinking: what the product means, holding the accepted product definition, versioned, related and reviewable. On the right, software delivery: how the product is built, holding SDD specs, AI agents, developers, backlog and code. An arrow labelled 'cited by' runs from the definition to delivery, and a dashed amber arrow returns, labelled 'delivery evidence reveals new product questions or changes'." width="720" /> </p>

<p align="center"><em>PDaC-0 - what is PDaC, in one minute? <a href="https://pdac.dev/diagrams/">All nine diagrams</a>.</em></p>

## Try it in five minutes

Every conformance case in this repository carries a miniature repository state. Copy this positive case and make a citation go stale. The only prerequisite is Node.js; `npx` downloads the pinned CLI package for the run.

```bash
git clone https://github.com/product-definition-as-code/spec.git
cp -r spec/conformance/cases/citation-current/repo pdac-demo
cd pdac-demo

# The citation is current: the cited requirement has not changed since it was recorded.
npx @prodshape/cli@0.13.0 citations verify specs

# Change the cited requirement.
echo "The product MUST also report the file and line of each unresolved reference." \
  >> docs/product/model/requirements/functional/fr-validate-001.md

# Same citation, same consumer document, now stale.
npx @prodshape/cli@0.13.0 citations verify specs
```

The first run prints:

```console
current	FR-VALIDATE-001#S1	specs/feature-x.citations.yml:1
1 citation(s): 1 current, 0 stale, 0 tampered, 0 unresolved
```

The second run prints:

```console
stale	FR-VALIDATE-001#S1	specs/feature-x.citations.yml:1
warning PRODUCT061 specs/feature-x.citations.yml [FR-VALIDATE-001]: Citation of 'FR-VALIDATE-001' is stale: canonical content changed since the citation was recorded
1 citation(s): 0 current, 1 stale, 0 tampered, 0 unresolved
```

`specs/feature-x.md`, the document that relies on the requirement, was never touched. Its citation ledger recorded the requirement's content digest, so amending the requirement flagged the document for review instead of leaving it quietly wrong. That is the citation contract, and it is the whole mechanism.

The transcript above was verified with the pinned `@prodshape/cli` 0.13.0 package on Node 22. It is a reproducible demonstration, not a claim about the latest ProductShape release. To run the conformance tests themselves against an implementation, use [`pdac-conformance`](https://www.npmjs.com/package/pdac-conformance) (see [conformance/README.md](conformance/README.md)).

## Examples

The fixtures under [`conformance/cases/`](conformance/cases/) are executable examples, not all examples of conforming repositories: negative cases deliberately contain a specific defect. Each `case.md` states the condition it verifies and its `repo/` supplies the repository state. These zero-diagnostic positive cases are reasonable places to start:

- [`greenfield-first-increment/repo/`](conformance/cases/greenfield-first-increment/repo/) - a model brought into existence by `CHG-INITIAL`, the applied change kept as archived history, and a delivery spec citing both a requirement scenario and a business rule.
- [`artifact-kinds-valid/repo/`](conformance/cases/artifact-kinds-valid/repo/) - one artifact of each of the ten kinds, plus a second Domain Term, wired into a complete graph.
- [`dedicated-topology/repo/`](conformance/cases/dedicated-topology/repo/) - a model repository holding the product definition and no software.

## How implementation disagreement has already corrected this spec

[Validation](spec/validation.md) defined a content digest as SHA-256 over an artifact's "UTF-8 bytes". Two codebases read that differently: the conformance runner, then named `pdac-lint`, hashed the file's bytes, while the reference implementation hashed the re-encoding of the file's decoded text. For well-formed UTF-8 the two readings agree, so every fixture passed under both and nothing surfaced the gap. On bytes that are not well-formed UTF-8 they diverge, and the same citation is `current` under one tool and `stale` under the other.

[RFC 0038](rfcs/0038-digest-bytes.md) settled it: the digest hashes bytes, never decoded text. The conformance tests then gained [`digest-bytes-not-text`](conformance/cases/digest-bytes-not-text/), a fixture whose cited artifact is deliberately not well-formed UTF-8, so an implementation that decodes before hashing now fails a case instead of agreeing by coincidence.

This is not independent validation of the specification: the two codebases share a maintainer, `pdac-conformance` is a separately versioned conformance runner rather than an implementation, and there is still no second full implementation of the reference profile ([MATURITY.md](MATURITY.md)). It is one concrete instance of a second codebase finding an ambiguity a single implementation could not see, which is the argument for wanting more of them.

## Status

**v0.2.0 (request for comments), released 2026-08-28.** First published 2026-08-07: this is an early draft, not a near-final standard. The honest picture of every surface, the version dimensions and the gates to v1 are in [MATURITY.md](MATURITY.md); what the methodology cannot claim yet is in [known limits](https://pdac.dev/known-limits/).

The specification text was extracted from the [reference implementation](https://github.com/juangcarmona/productshape), where it was developed and validated against a self-hosted product model. The chapters no longer name the reference implementation or depend on its repository layout. v1.0 freezes after the public comment period.

The comment period is open. Disagreements are the point: open an issue, or an RFC if you can name the normative text you would change. RFC comment windows are deliberately not running yet, because an elapsed-time window with no external reviewer behind it delays the work without buying review; they begin on their own once an independent implementation or a second adopter exists ([CONTRIBUTING.md](CONTRIBUTING.md)).

| Milestone | State |
| --- | --- |
| Chapters extracted | Done at v0.2.0 |
| Conformance tests (complete, normative set) | In progress; the 44 published cases run today via [pdac-conformance](https://www.npmjs.com/package/pdac-conformance) |
| Public comment period (v0.2) | Open from 2026-08-28, until the v1.0 freeze |
| v1.0 freeze | Planned; gated on [MATURITY.md](MATURITY.md) |

## Contents

The specification lives in [`spec/`](spec/index.md): ten normative chapters, terminology to conformance.

The founding position is [the manifesto](MANIFESTO.md), which you can [sign](SIGNATORIES.md).

## Implementations

| Implementation | Language | Status |
| --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | Reference implementation, v0.x, self-hosted |

The specification wants more than one implementation. If you are building one, open an issue; the [conformance chapter](spec/conformance.md) and the published conformance tests define what "conformant" means (they are not yet a complete normative set). See [IMPLEMENTATIONS.md](IMPLEMENTATIONS.md) for listing criteria.

## Contributing

Changes to the specification go through the [RFC process](CONTRIBUTING.md), which also records the [agreed cross-repo wording](CONTRIBUTING.md#agreed-wording). Governance, maintainers and decision rules are in [GOVERNANCE.md](GOVERNANCE.md). Adopters can add themselves to [ADOPTERS.md](ADOPTERS.md).

## License

The specification text and the manifesto are licensed under [CC BY 4.0](LICENSE.md). Code samples and conformance fixtures are licensed under Apache 2.0.
