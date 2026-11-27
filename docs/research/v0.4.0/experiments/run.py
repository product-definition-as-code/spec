#!/usr/bin/env python3
"""Run a pinned tool under a whole-job systemd cgroup; no LLM and no retries."""
import argparse, hashlib, json, platform, subprocess, time
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(name, command, output):
    output.mkdir(parents=True, exist_ok=True)
    assert name and '/' not in name
    # A service cgroup contains verifier descendants; timeout kills the entire job.
    wrapped = ['systemd-run', '--user', '--quiet', '--wait', '--pipe',
               '-p', 'MemoryMax=2147483648', '-p', 'MemorySwapMax=0',
               '-p', 'RuntimeMaxSec=30', '-p', 'TasksMax=64',
               '-p', 'KillMode=control-group', '--working-directory='+str(HERE),
               '--', *command]
    inputs = {}
    for arg in command:
        path = Path(arg) if Path(arg).is_absolute() else HERE/arg
        if path.is_file() and path.suffix in ['.smt2', '.als', '.dfy']:
            inputs[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    start = time.monotonic()
    result = subprocess.run(wrapped, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
    for suffix, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        (output / f'{name}.{suffix}').write_bytes(data)
    record = {'command': command, 'containment_command': wrapped, 'input_sha256': inputs,
              'returncode': result.returncode, 'wall_seconds': round(time.monotonic()-start, 6),
              'platform': platform.platform(), 'machine': platform.machine(),
              'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
              'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
              'llm_calls_by_runner': 0, 'automatic_retries': 0}
    (output / f'{name}.json').write_text(json.dumps(record, indent=2)+'\n')
    print(name, result.returncode, record['wall_seconds'], flush=True)
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('name'); p.add_argument('--output', type=Path, default=HERE/'results')
    p.add_argument('command', nargs=argparse.REMAINDER)
    args = p.parse_args(); cmd = args.command
    if cmd and cmd[0] == '--': cmd = cmd[1:]
    if not cmd: p.error('a command is required')
    run(args.name, cmd, args.output)
