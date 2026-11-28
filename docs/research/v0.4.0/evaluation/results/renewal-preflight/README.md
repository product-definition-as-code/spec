# G2 REVISE — public environment diagnostics, 2026-11-28

[Interpretation and remaining dependency](../../../reports/12a-renewal-environment.md), [machine record and file hashes](result.json). These are four public deterministic transport checks, not a renewed trial. No held-out input/answer/oracle or authentication file is included. The native-only candidate was rejected as a replacement for the required CLI isolation.

Reproduce the original transport on a candidate worker from repository root, using a new output directory:

```sh
python3 docs/research/v0.4.0/evaluation/preflight.py /tmp/pdac-new-worker-preflight
```

On this host it exits 1. The three additional check scripts preserve the exact executed commands and public fixtures. Their local `/tmp/pdac-v040-renewal` paths and already-installed image/runtime are explicit environment dependencies; adapt those paths to a fresh public fixture directory on another worker. `check-*/` contains commands, containment, stdout/stderr, exit status and timing. The native allowlist check probes only public sentinels and denied paths; it does not qualify actual dispatch, gateway socket exceptions or independent evaluation. Do not treat its exit 0 as permission to dispatch.

Verify saved evidence without an LLM, solver or execution retry:

```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
p = Path('docs/research/v0.4.0/evaluation/results/renewal-preflight')
r = json.loads((p/'result.json').read_text())
assert all(hashlib.sha256((p/name).read_bytes()).hexdigest() == pin
           for name, pin in r['evidence_sha256'].items())
assert not r['renewed_trial_dispatched']
print('Public diagnostic evidence hashes match; renewed trial not dispatched.')
PY
```

No controls were relaxed and no model was called by these four checks. A separate documentary environment review is included, with its identity/exposure limitations. This evidence does not replace the required public end-to-end agent/verification/evaluation canary.
