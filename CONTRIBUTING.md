# Contributing

Thanks for caring about the left side of the SDLC.

## What kind of change is it?

**Editorial** (clarity, typos, formatting, examples, non-normative notes): open a pull request directly.

**Normative** (changes what MUST, MUST NOT, SHOULD or MAY mean for a conforming repository or implementation; adds or removes artifact kinds, relationship types, diagnostics or lifecycle rules): open an RFC first. A pull request that changes normative text without an accepted RFC will be converted into one.

**Not sure?** Open an issue and ask. Worst case, it becomes an RFC.

## The RFC process

1. Copy `rfcs/0000-template.md` to `rfcs/0000-my-title.md` and fill it in. Keep it short; a good RFC states the problem, the proposed normative text, the alternatives considered and the impact on existing conformant repositories and implementations.
2. Open a pull request. The PR number becomes the RFC number; rename the file accordingly.
3. Public comment window: at least 14 days.
4. Maintainers decide per [GOVERNANCE.md](GOVERNANCE.md). Accepted RFCs merge into `rfcs/` and the spec change lands in a follow-up PR referencing the RFC.

## Ground rules

- The specification is implementation-independent. Text that requires a specific tool, command or repository layout beyond what the spec itself defines will be rejected, including anything that privileges the reference implementation.
- Every normative statement must be testable. If the conformance corpus cannot check it, either propose the fixture alongside it or explain why it is normative anyway.
- Discussions happen in issues and RFC pull requests, in English, under the [Code of Conduct](CODE_OF_CONDUCT.md).

## Signing the manifesto

Not a code contribution, still a contribution: [SIGNATORIES.md](SIGNATORIES.md).
