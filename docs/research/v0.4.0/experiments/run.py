#!/usr/bin/env python3
"""Run a pinned tool under a whole-job systemd cgroup; no LLM and no retries."""
import argparse, hashlib, json, platform, subprocess, time, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(name, command, output, cwd=None):
    cwd = Path(cwd).resolve() if cwd is not None else HERE
    output.mkdir(parents=True, exist_ok=True)
    assert name and '/' not in name
    if any((output/f'{name}.{suffix}').exists() for suffix in ['json','stdout','stderr']):
        raise FileExistsError('Preserve prior attempt: '+name)
    unit = 'pdac-research-'+uuid.uuid4().hex+'.service'
    # A service cgroup contains verifier descendants; timeout kills the entire job.
    wrapped = ['systemd-run', '--user', '--quiet', '--wait', '--pipe', '--collect', '--unit='+unit,
               '-p', 'MemoryMax=2147483648', '-p', 'MemorySwapMax=0',
               '-p', 'RuntimeMaxSec=30', '-p', 'TasksMax=64',
               '-p', 'KillMode=control-group', '--working-directory='+str(cwd),
               '--', *command]
    inputs = {}
    for arg in command:
        path = Path(arg) if Path(arg).is_absolute() else cwd/arg
        if path.is_file() and path.suffix in ['.smt2', '.als', '.dfy']:
            inputs[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    start = time.monotonic()
    failure_class = None
    cleanup = None
    try:
        result = subprocess.run(wrapped, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
    except subprocess.TimeoutExpired as error:
        failure_class = 'outer_timeout'
        result = subprocess.CompletedProcess(wrapped, 124, error.stdout or b'', error.stderr or b'')
        try:
            killed = subprocess.run(['systemctl','--user','kill','--kill-whom=all',
                                     '--signal=KILL',unit], capture_output=True, timeout=5)
            cleanup = {'returncode':killed.returncode, 'stderr':killed.stderr.decode(errors='replace')}
        except (OSError, subprocess.TimeoutExpired) as cleanup_error:
            cleanup = {'error':str(cleanup_error)}
    except OSError as error:
        failure_class = 'launch_error'
        result = subprocess.CompletedProcess(wrapped, 127, b'', str(error).encode())
    for suffix, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        (output / f'{name}.{suffix}').write_bytes(data)
    record = {'command': command, 'containment_command': wrapped, 'input_sha256': inputs, 'cwd': str(cwd),
              'returncode': result.returncode, 'failure_class': failure_class, 'cleanup': cleanup, 'wall_seconds': round(time.monotonic()-start, 6),
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
    raise SystemExit(run(args.name, cmd, args.output).returncode)
