# Renewed trial — blocked before dispatch

**G2 REVISE is approved; an execution dependency remains unresolved.** [Owner decision receipt](https://github.com/product-definition-as-code/spec/issues/135#issuecomment-7234784621), starting from merged #152 (`f530d053d685155724a73d2225ad98dc677fb982`). Four deterministic public checks and one separate agent review identified the boundary failure. **No renewed author session, scored evaluation, solver query or held-out inspection occurred.** The single renewed trial remains unused; no additional routine approval is requested.

## Results and diagnosis

| Public check | Observed | Meaning |
| --- | --- | --- |
| Frozen nested transport with corrected local temporary directory | Exit 1 | Full preflight still fails before artifact generation. |
| Existing local Docker image; default AppArmor/seccomp, no capabilities, no-new-privileges, network off, read-only root | Exit 1 | This confined alternative also cannot create the native sandbox. No image pull or paid provisioning. |
| Native Codex sandbox without outer namespace | Exit 0; public artifact written | Native tool sandbox works on the host; nesting is the relevant distinction. |
| Native tool sandbox with explicit minimal/work allowlist | Exit 0; public artifact written, five outside-path reads and two TCP connections unsuccessful | Candidate tool policy works for these checks, **not equivalent confinement of the CLI process**. Existing public sentinel/symlink checks are stronger than unavailable-path checks; not every denied probe proves the target existed. |

The kernel now explicitly attributes the original nested failure to AppArmor: `unpriv_bwrap` denies `CAP_SYS_ADMIN` to the second `bwrap`. The installed profile intentionally strips child capabilities. This refines #152's previously unattributed diagnosis; the Docker error alone does not establish an identical cause. [Raw commands, exits, hashes, kernel entries and profile snapshot](../evaluation/results/renewal-preflight/result.json) are preserved. The original temporary-directory correction remains applicable.

The native-only candidate was **not adopted**. It confines tool subprocesses but expands the trusted CLI's view to the host, including potential startup/context sources. The original outer namespace also confined that CLI and its process view. Trusting it with authentication is not equivalent to exposing all host sources. No host policy, sandbox flag or security control was disabled to manufacture success.

A fresh `/root/renewal_isolation_review` session inspected public source/receipts without authoring history or private evaluation access. Its [assessment](../evaluation/results/renewal-preflight/isolation-review.md) identified the trust-boundary change and unqualified actual-agent, socket, read-only-evidence, same-UID process/descriptor and descendant-cleanup paths. Identity: Codex based on GPT-6, exact serving revision unavailable. This is an agent assessment, not human expert validation or a security certification. It is not one of the frozen trial's nine documentary evaluations.

## Remaining operational dependency and standing authorization

An administrator must supply a compatible **confined executor** that retains the CLI's filesystem/process isolation and permits Codex's native tool sandbox. A dedicated service/container policy must be qualified with the real transport; globally disabling AppArmor, granting a privileged Docker container, removing the outer boundary or bypassing the native sandbox is not an accepted remedy. The current account has no noninteractive sudo authorization. No already-qualified alternative worker is available to this session; this does not assert that none exists elsewhere.

Once that dependency is available, the existing G2 REVISE instruction already authorizes deterministic preflight, a public non-scored end-to-end canary with actual agent artifact generation, formal verification and separate evaluation, then **one** renewed trial if every stage passes. The full canary was **not launched** through a known-failing boundary. Successful unit tests or native-only public commands do not substitute for it. Retain original controls, intent, cohorts, held-outs, thresholds, caps and evaluator independence; freeze corrected execution revisions before dispatch and document comparability implications. No new approval gate is introduced.

Issues #131–134 remain scientifically incomplete; G2 stays open on this external dependency. Original failures, unknown observations, source/manifest and custody commitments are unchanged. The saved-result audit still passes without an LLM/solver. No renewed comparative result, mathematical finding, H0 conclusion, normative change or phase-3 authorization follows.
