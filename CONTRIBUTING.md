# Contributing

Thanks for caring about the left side of the SDLC.

## What kind of change is it?

**Editorial** (clarity, typos, formatting, examples, non-normative notes): open a pull request directly.

**Normative** (changes what MUST, MUST NOT, SHOULD or MAY mean for a conforming repository or implementation; adds or removes artifact kinds, relationship types, diagnostics or lifecycle rules): open an RFC first. A pull request that changes normative text without an accepted RFC will be converted into one.

**Not sure?** Open an issue and ask. Worst case, it becomes an RFC.

## The RFC process

1. Copy `rfcs/0000-template.md` to `rfcs/0000-my-title.md` and fill it in. Keep it short; a good RFC states the problem, the proposed normative text, the alternatives considered and the impact on existing conformant repositories and implementations.
2. Open a pull request. The PR number becomes the RFC number; rename the file accordingly.
3. Public comment window, by what the RFC does:
   - **Determination**, filling a gap the specification left open, where no conforming repository or implementation changes behaviour: at least 72 hours.
   - **Change**, altering existing normative text or adding or removing an obligation: at least 7 days before v1.0, at least 14 days from v1.0.
   The longer window returns automatically at v1.0, or earlier once a second independent implementation exists, because that is the point at which a week of review costs someone else something.
4. Maintainers decide per [GOVERNANCE.md](GOVERNANCE.md). Accepted RFCs merge into `rfcs/` and the spec change lands in a follow-up PR referencing the RFC.

## Ground rules

- The specification is implementation-independent. Text that requires a specific tool, command or repository layout beyond what the spec itself defines will be rejected, including anything that privileges the reference implementation.
- Every normative statement must be testable. If the conformance tests cannot check it, either propose the fixture alongside it or explain why it is normative anyway.
- Discussions happen in issues and RFC pull requests, in English, under the [Code of Conduct](CODE_OF_CONDUCT.md).

## Agreed wording

Cross-repo wording the consistency pass agreed once (spec#34, spec#35, spec#68). Public surfaces copy these instead of inventing their own phrasing; this section supersedes the former `DECISIONS.md`.

- **The canonical PDaC definitions.** The one-line and one-paragraph definitions live between the `canonical-pdac-definition` markers in [README.md](README.md). Other first-contact surfaces copy them verbatim or link to them; paraphrase is drift.
- **Conformance-tests status.** "The conformance runner (`pdac-conformance`) is published and usable. The conformance tests are versioned with the spec: initialisation, the citation contract, configuration, topology, artifact-kind, full Structured Behaviour matrix and most Product Change cases are runnable; other gaps remain planned. They are not yet published as a complete, normative set." Check [conformance/README.md](conformance/README.md) for the live case count before restating it; never call the runner "planned", and never call the tests "a complete normative set".
- **ProductShape's first line**, wherever it is introduced: "ProductShape, the reference implementation of Product Definition as Code."
- **Artifact counts.** Never hardcode a count that will drift; derive it from a command, or say "80+ artifacts".
- **A retired word.** "corpus" is retired everywhere in the project; do not reintroduce it. The bar is `git grep -i corpus` finding only this rule and the changelog entry recording the retirement.

## Signing the manifesto

Not a code contribution, still a contribution: [SIGNATORIES.md](SIGNATORIES.md).
