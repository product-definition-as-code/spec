# Decisions for the consistency and plain-language pass

Working document. It records the wording and vocabulary the cross-repo consistency
pass agreed once, so every repo copies from here instead of inventing its own phrasing.
Tracked by spec#34 (status) and spec#35 (plain language). Remove it once the pass has
landed in every repo, or keep it as a style record.

## 1. Conformance-tests status (use this wording verbatim)

The runner is published; the tests are only partly written. Say exactly this wherever
the status is stated (README, MATURITY, IMPLEMENTATIONS, the org profile):

> The conformance runner (pdac-lint) is published and usable. The conformance tests
> are scaffolded and versioned with the spec: the initialisation, citation-contract,
> topology and artifact-kind cases exist, and most change-semantics cases are still to
> come. They are not yet published as a complete, normative set.

Short forms, when a full paragraph does not fit:
- table cell: "Scaffolded; runner published, most change-semantics cases to come"
- one clause: "the conformance tests are scaffolded, not yet a complete normative set"

Do not write that the runner is "planned" or "not usable". It is on npm.

## 2. The word "corpus" is retired

Nobody outside this project says it, and it was used for two different things. Replace
by meaning, not with a blanket swap:

| Meaning in context | Replace with |
|---|---|
| The conformance tests, as prose | "the conformance tests" |
| A single one | "a conformance test" / "a test case" |
| The initial set (was "seed corpus") | "the seed test cases" / "the initial conformance tests" |
| ProductShape Snapshot sense (all artifacts) | "the whole product model" / "all the artifacts at once" |
| Code identifiers (`corpusDir`, `discoverCorpus`, `CorpusCase`) | `testCases` / `discoverTests` etc. (pdac-lint, lower priority) |
| The `Corpus` GitHub Actions workflow | rename to `Conformance` |

Accepted RFCs (0004, 0021, 0022) are historical records and keep their original text.
The RFC template (`rfcs/0000-template.md`) is fixed so future RFCs do not seed the word.

## 3. Artifact count

Never hardcode a count that will drift. ProductShape README derives it from a command.
Where a soft public figure is needed elsewhere, say "80+ artifacts" (real count was 83
on 2026-08-09). Reconcile the four stale numbers (64 / 60+ / 73 / 56) against this.

## 4. Standard tagline

Wherever ProductShape is introduced on any surface, first line:

> ProductShape, the reference implementation of Product Definition as Code.

## 5. Plain-language principles

Short sentences. Plain words over jargon. Say what a tool does before why it matters.
One idea per sentence. Cut any term the reader has to decode (self-referential,
archaeology, overlay). Applies to the surfaces a newcomer reads first (READMEs, the
landing page, MATURITY, MANIFESTO, the adoption guide), not the archival change records.
