# Decisions for the consistency and plain-language pass

Working document. It records the wording and vocabulary the cross-repo consistency
pass agreed once, so every repo copies from here instead of inventing its own phrasing.
Tracked by spec#34 (status) and spec#35 (plain language). Remove it once the pass has
landed in every repo, or keep it as a style record.

## 1. Conformance-tests status

The runner is published; the tests are only partly written. Use this wording wherever
the status is stated in prose (README, MATURITY, IMPLEMENTATIONS, the org profile). In
tables and column cells where the full clause does not fit, use a short form, and at a
minimum never contradict it:

> The conformance runner (pdac-lint) is published and usable. The conformance tests
> are scaffolded and versioned with the spec: the initialisation, citation-contract,
> topology and artifact-kind cases exist, and most change-semantics cases are still to
> come. They are not yet published as a complete, normative set.

Short forms, when a full paragraph does not fit:
- table cell: "Scaffolded; runner published, most change-semantics cases to come"
- one clause: "the conformance tests are scaffolded, not yet a complete normative set"

Never call the runner "planned" or "not usable" (it is on npm), and never call the
conformance tests "planned" (they are scaffolded and already running in CI).

## 2. The word "corpus" is retired

Nobody outside this project says it, and it was used for two different things. It is
banned EVERYWHERE, with no deferral and no "historical" exception: prose, headings,
directory names, filenames, code identifiers, CLI output strings, config, changelog and
RFCs. The bar is `git grep -i corpus` returning nothing (this file is the only allowed
exception, because its job is to define the ban). Replace by meaning, not with a blanket
swap:

| Meaning in context | Replace with |
|---|---|
| The conformance tests, as prose | "the conformance tests" |
| A single one | "a conformance test" / "a test case" |
| The initial set (was "seed corpus") | "the seed test cases" / "the initial conformance tests" |
| ProductShape Snapshot sense (all artifacts) | "the whole product model" / "all the artifacts at once" |
| Directories/filenames (`fixtures/corpus/`, `src/corpus.ts`) | `fixtures/cases/`, `src/cases.ts` (rename with `git mv`) |
| Code identifiers (`corpusDir`, `discoverCorpus`, `CorpusCase`) | `casesDir` / `discoverCases` / `TestCase` etc. |
| CLI output/config (`Corpus:` label, a `corpus:` CI job) | `Conformance:` / a `conformance` job |
| The `Corpus` GitHub Actions workflow | rename to `Conformance` |

The RFC template (`rfcs/0000-template.md`) is fixed so future RFCs do not seed the word.
The one place a rename must go through process, not a direct edit, is ProductShape's
canonical model under `docs/product/**`: that changes only through a promoted Product
Change.

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
