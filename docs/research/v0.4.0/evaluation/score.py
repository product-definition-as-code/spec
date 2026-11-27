#!/usr/bin/env python3
"""Deterministic finite oracle scoring. Never imports submitted Python.

CLI: --manifest frozen.json --cases cases.json --output NEW_DIR --ledger ledger.json
Manifest: {submissions:[{path,cohort,seed,episode,sha256:{"decision.py":hex,
"contract.smt2":hex}}], tools:{z3:{path,sha256},cvc5:{path,sha256}},
solver_call_budget:N, solver_query_budget:N}. Tools required for cohorts 3/4.
Cases: {cases:[{id,episode,input,expected,class,eligible:true}]}.
Mutation detection, evidence continuity and human time need independent adjudication;
this scorer does not infer them from decision outputs. Episodes are dependent.
"""
import argparse
import collections
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
INPUTS = ('status', 'used', 'capacity', 'days', 'due', 'actor', 'owner', 'issuer',
          'authenticated', 'editor', 'operation')
OUTPUTS = ('accepted', 'status', 'used', 'owner')
BOOLS = {'due', 'authenticated', 'editor', 'accepted'}
SIGNATURE = ['Int', 'Int', 'Int', 'Int', 'Bool', 'Int', 'Int', 'Int', 'Bool',
             'Bool', 'Int', 'Bool', 'Int', 'Int', 'Int']
MAX_BYTES = 8 * 1024 * 1024


def reject_constant(value):
    raise ValueError('non-JSON constant: ' + value)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def checked(path, expected, limit=MAX_BYTES):
    data = Path(path).read_bytes()
    if len(data) > limit or digest(data) != expected:
        raise ValueError('size/hash pin mismatch: ' + str(path))
    return data


def validate_fields(value, fields):
    return (isinstance(value, dict) and set(value) == set(fields)
            and all(type(value[key]) is (bool if key in BOOLS else int) for key in fields))


def valid_output(value):
    return isinstance(value, dict) and set(value) == set(OUTPUTS) and type(value['accepted']) is bool


def validate_cases(document):
    cases = document['cases'] if isinstance(document, dict) else document
    seen = set()
    for case in cases:
        identity = (str(case.get('schedule', '*')), str(case['episode']), case['id'])
        if identity in seen or not isinstance(case['id'], str):
            raise ValueError('duplicate/invalid case id')
        seen.add(identity)
        if (type(case['eligible']) is not bool or not isinstance(case['class'], str)
                or not isinstance(case['input'], dict)
                or not valid_output(case['expected'])):
            raise ValueError('invalid case schema')
    return cases


def reserve(ledger, calls, queries, call_limit, query_limit, identity):
    """One locked write-ahead reservation; failed/abandoned launches remain charged."""
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open('a+') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        raw = handle.read()
        state = json.loads(raw) if raw else {'attempts': [], 'call_limit': call_limit, 'query_limit': query_limit}
        if state['call_limit'] != call_limit or state['query_limit'] != query_limit:
            raise ValueError('cannot change frozen aggregate ledger limits')
        prior = state['attempts']
        if (sum(x['calls'] for x in prior) + calls > call_limit
                or sum(x['queries'] for x in prior) + queries > query_limit):
            raise RuntimeError('aggregate solver budget exhausted')
        prior.append({'id': identity, 'calls': calls, 'queries': queries,
                      'reserved_at_unix': time.time()})
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps(state) + '\n')
        handle.flush()
        os.fsync(handle.fileno())


def sandbox(command, mounts):
    args = ['/usr/bin/bwrap', '--unshare-all', '--die-with-parent', '--new-session',
            '--clearenv', '--setenv', 'PATH', '/usr/bin', '--setenv', 'HOME', '/tmp',
            '--setenv', 'PYTHONHASHSEED', '0', '--setenv', 'LC_ALL', 'C',
            '--ro-bind', '/usr', '/usr']
    for library in ('/lib', '/lib64'):
        if Path(library).exists():
            args += ['--ro-bind', library, library]
    args += ['--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--dir', '/submission']
    for source, target in mounts:
        args += ['--ro-bind', str(source), target]
    return args + ['--chdir', '/tmp', '--', *command]


def execute(command, mounts, stdin, output, name):
    unit = 'pdac-score-' + uuid.uuid4().hex + '.service'
    isolated = sandbox(command, mounts)
    wrapped = ['systemd-run', '--user', '--quiet', '--wait', '--pipe', '--collect',
               '--unit=' + unit, '-p', 'MemoryMax=2147483648', '-p', 'MemorySwapMax=0',
               '-p', 'TasksMax=64', '-p', 'RuntimeMaxSec=30', '-p', 'KillMode=control-group',
               '-p', 'LimitFSIZE=' + str(MAX_BYTES), '--', *isolated]
    (output / (name + '.stdin')).write_bytes(stdin)
    start = time.monotonic()
    fault = None
    cleanup = None
    with (output / (name + '.stdout')).open('wb') as stdout, (output / (name + '.stderr')).open('wb') as stderr:
        try:
            result = subprocess.run(wrapped, input=stdin, stdout=stdout, stderr=stderr, timeout=40,
                                    preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_BYTES, MAX_BYTES)))
            returncode = result.returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            fault = type(error).__name__
            returncode = 124 if isinstance(error, subprocess.TimeoutExpired) else 127
            try:
                killed = subprocess.run(['systemctl', '--user', 'kill', '--kill-whom=all',
                                         '--signal=KILL', unit], capture_output=True, timeout=5)
                cleanup = {'returncode': killed.returncode, 'stderr': killed.stderr.decode(errors='replace')}
            except (OSError, subprocess.TimeoutExpired) as cleanup_error:
                cleanup = {'error': str(cleanup_error)}
    out = (output / (name + '.stdout')).read_bytes()
    err = (output / (name + '.stderr')).read_bytes()
    record = {'command': command, 'containment_command': wrapped, 'returncode': returncode,
              'failure': fault, 'cleanup': cleanup, 'elapsed_seconds': time.monotonic() - start,
              'stdin_sha256': digest(stdin), 'stdout_sha256': digest(out), 'stderr_sha256': digest(err),
              'mount_sha256': {target: digest(Path(source).read_bytes()) for source, target in mounts},
              'automatic_retries': 0}
    write_json(output / (name + '.json'), record)
    return record, out


def sexprs(source):
    """Strict contract subset: ordinary unquoted QF_LIA definitions, no commands."""
    source = re.sub(r';[^\n]*', '', source)
    if any(char in source for char in ('"', '|', '\\')):
        raise ValueError('strings/quoted symbols are outside the pilot contract subset')
    tokens = re.findall(r'\(|\)|[^\s()]+', source)
    stack = [[]]
    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            if len(stack) == 1:
                raise ValueError('unbalanced contract')
            item = stack.pop()
            stack[-1].append(item)
        else:
            stack[-1].append(token)
    if len(stack) != 1 or any(not isinstance(x, list) for x in stack[0]):
        raise ValueError('unbalanced contract')
    return stack[0]


def validate_contract(source):
    expressions = sexprs(source)
    if sum(x == ['set-logic', 'QF_LIA'] for x in expressions) > 1:
        raise ValueError('duplicate set-logic')
    names = []
    step = None
    for expression in expressions:
        if expression == ['set-logic', 'QF_LIA']:
            continue
        if (len(expression) != 5 or expression[0] != 'define-fun'
                or not isinstance(expression[1], str) or not isinstance(expression[2], list)):
            raise ValueError('contract permits only set-logic QF_LIA and define-fun')
        if expression[1] in names:
            raise ValueError('duplicate function')
        names.append(expression[1])
        if expression[1] == 'Step':
            step = expression
    if (step is None or step[3] != 'Bool' or len(step[2]) != len(SIGNATURE)
            or any(not isinstance(arg, list) or len(arg) != 2 for arg in step[2])
            or [arg[1] for arg in step[2]] != SIGNATURE):
        raise ValueError('Step signature mismatch')


def literal(value):
    if type(value) is bool:
        return 'true' if value else 'false'
    return str(value) if value >= 0 else '(- ' + str(-value) + ')'


def queries(source, cases):
    validate_contract(source)
    # Fresh names cannot collide with authored definitions or their bound parameters.
    prefix = 'oracle_' + digest(source.encode())[:20]
    while prefix in source:
        prefix += '_'
    outputs = [prefix + str(i) for i in range(4)]
    text = ('' if any(x == ['set-logic', 'QF_LIA'] for x in sexprs(source)) else '(set-logic QF_LIA)\n') + source + '\n'
    for name, sort in zip(outputs, ('Bool', 'Int', 'Int', 'Int')):
        text += '(declare-const ' + name + ' ' + sort + ')\n'
    for case in cases:
        values = [literal(case['input'][key]) for key in INPUTS]
        expected = [literal(case['expected'][key]) for key in OUTPUTS]
        expected_step = '(Step ' + ' '.join(values + expected) + ')'
        any_step = '(Step ' + ' '.join(values + outputs) + ')'
        equal = '(and ' + ' '.join('(= ' + name + ' ' + val + ')' for name, val in zip(outputs, expected)) + ')'
        for assertion in (expected_step, '(and ' + any_step + ' (not ' + equal + '))'):
            text += '(push 1)\n(assert ' + assertion + ')\n(check-sat)\n(pop 1)\n'
    return (text + '(exit)\n').encode()


def parse_solver(record, stdout, count):
    lines = stdout.decode(errors='replace').split()
    if record['returncode'] or record['failure'] or len(lines) != count or any(x not in ('sat', 'unsat', 'unknown') for x in lines):
        return ['unknown'] * count
    return lines


def classify(expected, actual):
    if not valid_output(actual):
        return 'unknown'
    if json.dumps(actual, sort_keys=True, allow_nan=False) == json.dumps(expected, sort_keys=True, allow_nan=False):
        return 'correct'
    if expected['accepted'] and not actual['accepted']:
        return 'valid_rejection'
    return 'semantic_error'


def combine_outcomes(decision, formal):
    outcomes = {decision, formal}
    for outcome in ('valid_rejection', 'semantic_error', 'unknown'):
        if outcome in outcomes:
            return outcome
    return 'correct'


def summarize(rows):
    groups = collections.defaultdict(collections.Counter)
    for row in rows:
        key = (str(row['cohort']), str(row['seed']), str(row['episode']), row['class'])
        groups[key]['eligible'] += 1
        groups[key][row['outcome']] += 1
        groups[key]['decision_' + row.get('decision_outcome', row['outcome'])] += 1
        if row.get('formal_applicable'):
            groups[key]['formal_' + row['formal_outcome']] += 1
        for flag in ('execution_fault', 'formal_mismatch', 'formal_unknown', 'formal_applicable', 'invalid_experiment'):
            groups[key][flag] += bool(row.get(flag))
    counts = [dict(zip(('cohort', 'seed', 'episode', 'class'), key), **dict(value)) for key, value in sorted(groups.items())]
    paired = []
    by_identity = collections.defaultdict(dict)
    for row in rows:
        if row['cohort'] in (3, 4):
            by_identity[(str(row['seed']), str(row['episode']), row['id'])][row['cohort']] = row
    aggregate = collections.defaultdict(collections.Counter)
    for (seed, episode, case_id), pair in sorted(by_identity.items()):
        if set(pair) != {3, 4}:
            continue
        paired.append({'seed': seed, 'episode': episode, 'id': case_id,
                       'cohort3': pair[3]['outcome'], 'cohort4': pair[4]['outcome']})
        for scope in ((seed, episode), (seed, '*'), ('*', '*')):
            a = aggregate[scope]
            a['matched_eligible'] += 1
            a['additional_valid_rejections'] += (pair[4]['outcome'] == 'valid_rejection' and pair[3]['outcome'] != 'valid_rejection')
            for panel in ('decision', 'formal'):
                before = pair[3].get(panel + '_outcome', pair[3]['outcome'])
                after = pair[4].get(panel + '_outcome', pair[4]['outcome'])
                a['additional_' + panel + '_valid_rejections'] += (after == 'valid_rejection' and before != 'valid_rejection')
            for cohort in (3, 4):
                a[str(cohort) + '_' + pair[cohort]['outcome']] += 1
    comparisons = []
    for (seed, episode), counts_ in sorted(aggregate.items()):
        n = counts_['matched_eligible']
        # Unknown is never success; lower bound treats it as an undetected error.
        rates = {}
        for cohort in (3, 4):
            prefix = str(cohort) + '_'
            errors = counts_[prefix + 'semantic_error'] + counts_[prefix + 'valid_rejection']
            unknown = counts_[prefix + 'unknown']
            complete = n - unknown
            rates[str(cohort)] = {'finite_discrepancy_all_eligible': errors / n,
                                  'finite_discrepancy_complete_case': errors / complete if complete else None,
                                  'finite_discrepancy_unknown_as_error': (errors + unknown) / n,
                                  'unknown': unknown,
                                  'valid_rejections': counts_[prefix + 'valid_rejection']}
        improvement = rates['3']['finite_discrepancy_unknown_as_error'] - rates['4']['finite_discrepancy_unknown_as_error']
        lower_bound = rates['3']['finite_discrepancy_all_eligible'] - rates['4']['finite_discrepancy_unknown_as_error']
        safeguard = all(counts_[key] == 0 for key in ('additional_valid_rejections',
                        'additional_decision_valid_rejections', 'additional_formal_valid_rejections'))
        comparisons.append({'seed': seed, 'episode': episode,
                            'reporting_unit': 'pooled dependent cases' if seed == '*' else 'dependent trajectory' if episode == '*' else 'episode',
                            'counts': dict(counts_), 'rates': rates,
                            'improvement_percentage_points': 100 * improvement,
                            'lower_bound_improvement_percentage_points': 100 * lower_bound,
                            'zero_additional_valid_rejections': safeguard,
                            'sensitivity': {str(margin): lower_bound + 1e-12 >= margin / 100 and safeguard for margin in (5, 10, 15)},
                            'measure': 'PROPOSED G1 amendment: finite executable-or-formal case discrepancy; not seeded mutation detection',
                            'primary_screen_10pp': lower_bound + 1e-12 >= .10 and safeguard})
    schedule_screens = {row['seed']: row['primary_screen_10pp'] for row in comparisons if row['episode'] == '*'}
    return {'counts': counts, 'paired_4_vs_3': paired, 'comparisons': comparisons,
            'primary_screen_both_schedules': all(schedule_screens.get(seed, False) for seed in ('17', '29')),
            'limitations': ['Finite tested model consistency is not unbounded program/formal correspondence.',
                            'Dependent episodes have no independence-based statistics or p-values.',
                            'Mutation detection, continuity, human review and effort require independent evaluation.']}


def score(manifest_path, cases_path, output, ledger):
    manifest_bytes, case_bytes = manifest_path.read_bytes(), cases_path.read_bytes()
    manifest = json.loads(manifest_bytes, parse_constant=reject_constant)
    commitment = manifest.get('heldout_commitment', {}).get('private_commitments', {}).get('cases.json')
    if 'frozen_manifest_sha256' in manifest and not commitment:
        raise ValueError('production manifest requires frozen cases.json commitment')
    if commitment is not None and commitment != digest(case_bytes):
        raise ValueError('held-out cases commitment mismatch')
    approval = manifest.get('g1_approval')
    if approval is not None and (not isinstance(approval, dict) or
            approval.get('frozen_manifest_sha256') != manifest.get('frozen_manifest_sha256') or
            not approval.get('url', '').startswith('https://github.com/product-definition-as-code/spec/issues/130#issuecomment-')):
        raise ValueError('G1 approval receipt does not bind the frozen manifest')
    cases = validate_cases(json.loads(case_bytes, parse_constant=reject_constant))
    submissions = manifest['submissions']
    identities = [(x['cohort'], str(x['seed']), str(x['episode'])) for x in submissions]
    if len(set(identities)) != len(identities) or any(x[0] not in (1, 2, 3, 4) for x in identities):
        raise ValueError('duplicate/invalid submission identity')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'manifest.json').write_bytes(manifest_bytes)
    (output / 'cases.json').write_bytes(case_bytes)
    write_json(output / 'inputs.json', {'manifest_sha256': digest(manifest_bytes), 'cases_sha256': digest(case_bytes),
                                      'scorer_sha256': digest(Path(__file__).read_bytes()),
                                      'worker_sha256': digest((HERE / 'deterministic-worker.py').read_bytes())})
    planned = {'solver_calls': 0, 'solver_queries': 0, 'submissions': []}
    for submission in submissions:
        selected = [x for x in cases if x['eligible'] and str(x['episode']) == str(submission['episode'])
                    and ('schedule' not in x or str(x['schedule']) == str(submission['seed']))]
        ntyped = sum(validate_fields(x['input'], INPUTS) and validate_fields(x['expected'], OUTPUTS) for x in selected)
        nformal = ntyped if submission['cohort'] in (3, 4) else 0
        planned['solver_calls'] += 2 if nformal else 0
        planned['solver_queries'] += 4 * nformal
        planned['submissions'].append(dict(cohort=submission['cohort'], seed=submission['seed'], episode=submission['episode'], eligible=len(selected), formal_applicable=ntyped))
    write_json(output / 'planned-counts.json', planned)
    if (planned['solver_calls'] > manifest.get('solver_call_budget', 0)
            or planned['solver_queries'] > manifest.get('solver_query_budget', 0)):
        raise ValueError('planned solver work exceeds frozen aggregate budget')
    rows = []
    for index, submission in enumerate(submissions):
        current = [case for case in cases if str(case['episode']) == str(submission['episode']) and case['eligible']
                   and ('schedule' not in case or str(case['schedule']) == str(submission['seed']))]
        if not current:
            raise ValueError('submission has no eligible oracle cases')
        attempt = output / str(index)
        attempt.mkdir()
        defect = None
        required = ('decision.py', 'contract.smt2') if submission['cohort'] in (3, 4) else ('decision.py',)
        if submission.get('author_status', 'completed') != 'completed':
            defect = {'category': 'blocked_attempt', 'author_status': submission['author_status'], 'invalid_experiment': False}
        else:
            try:
                for filename in required:
                    data = checked(Path(submission['path']) / filename, submission['sha256'][filename])
                    (attempt / filename).write_bytes(data)
            except (OSError, KeyError, TypeError, ValueError) as error:
                defect = {'category': 'missing_or_tampered_required_output', 'error': str(error),
                          'invalid_experiment': True}
        if defect is not None:
            write_json(attempt / 'attempt-defect.json', defect)
            for case in current:
                row = {key: submission[key] for key in ('cohort', 'seed', 'episode')}
                row.update({'id': case['id'], 'class': case['class'], 'outcome': 'unknown',
                            'decision_outcome': 'unknown', 'execution_fault': True,
                            'attempt_defect': defect['category'], 'invalid_experiment': defect['invalid_experiment']})
                if submission['cohort'] in (3, 4):
                    applicable = validate_fields(case['input'], INPUTS) and validate_fields(case['expected'], OUTPUTS)
                    row.update(formal_applicable=applicable, formal_unknown=applicable,
                               formal_mismatch=False, formal_checks={},
                               formal_outcome='unknown' if applicable else 'not_applicable')
                rows.append(row)
            write_json(output / 'rows.json', rows)
            continue
        payload = json.dumps([{'id': x['id'], 'input': x['input']} for x in current]).encode()
        record, stdout = execute(['/usr/bin/python3', '-I', '-B', '/worker.py'],
                                 [(attempt / 'decision.py', '/submission/decision.py'),
                                  (HERE / 'deterministic-worker.py', '/worker.py')], payload, attempt, 'decision')
        try:
            decoded = json.loads(stdout, parse_constant=reject_constant)
            results = decoded['results']
            if not isinstance(results, list) or not all(isinstance(item, dict) for item in results):
                raise ValueError('worker fault')
            if (record['returncode'] or record['failure'] or len(results) != len(current)
                    or [item['id'] for item in results] != [x['id'] for x in current]):
                raise ValueError('worker fault')
        except (ValueError, KeyError, TypeError):
            results = [{'error': 'worker fault'} for _ in current]
        formal = {}
        typed = [case for case in current if validate_fields(case['input'], INPUTS) and validate_fields(case['expected'], OUTPUTS)]
        typed_positions = {case['id']: pos for pos, case in enumerate(typed)}
        if submission['cohort'] in (3, 4):
            contract = (attempt / 'contract.smt2').read_bytes()
            try:
                query = queries(contract.decode(), typed)
                (attempt / 'queries.smt2').write_bytes(query)
                for engine in (('z3', 'cvc5') if typed else ()):
                    tool = manifest['tools'][engine]
                    source = Path(tool['path']).resolve()
                    if not source.is_relative_to(Path('/tmp/pdac-v040-tools')):
                        raise ValueError('solver outside pinned tool directory')
                    binary = checked(source, tool['sha256'], limit=512 * 1024 * 1024)
                    frozen_tool = attempt / engine
                    frozen_tool.write_bytes(binary)
                    frozen_tool.chmod(0o500)
                    name = str(index) + '-' + engine
                    reserve(ledger, 1, 2 * len(typed), manifest['solver_call_budget'],
                            manifest['solver_query_budget'], name)
                    args = ['/solver', '-in'] if engine == 'z3' else ['/solver', '--lang=smt2', '--incremental']
                    with ledger.with_suffix('.runlock').open('a+') as runlock:
                        fcntl.flock(runlock, fcntl.LOCK_EX)
                        rec, out = execute(args, [(frozen_tool, '/solver')], query, attempt, engine + '-run')
                    formal[engine] = parse_solver(rec, out, 2 * len(typed))
            except (ValueError, UnicodeError) as error:
                write_json(attempt / 'contract-error.json', {'error': str(error)})
        for pos, (case, actual) in enumerate(zip(current, results)):
            outcome = classify(case['expected'], actual.get('output'))
            row = {key: submission[key] for key in ('cohort', 'seed', 'episode')}
            row.update({'id': case['id'], 'class': case['class'], 'outcome': outcome,
                        'execution_fault': outcome == 'unknown', 'decision_outcome': outcome})
            if submission['cohort'] in (3, 4):
                row['formal_applicable'] = case['id'] in typed_positions
                formal_pos = typed_positions.get(case['id'], 0)
                checks = {engine: values[2 * formal_pos:2 * formal_pos + 2] for engine, values in formal.items()} if row['formal_applicable'] else {}
                row['formal_checks'] = checks
                row['formal_unknown'] = row['formal_applicable'] and (len(checks) != 2 or any('unknown' in x for x in checks.values()))
                row['formal_mismatch'] = any(a == 'unsat' or b == 'sat' for a, b in checks.values())
                rejected = case['expected']['accepted'] and any(a == 'unsat' for a, b in checks.values())
                row['formal_outcome'] = ('not_applicable' if not row['formal_applicable'] else
                                         'valid_rejection' if rejected else
                                         'semantic_error' if row['formal_mismatch'] else
                                         'unknown' if row['formal_unknown'] else 'correct')
                row['outcome'] = combine_outcomes(row['decision_outcome'], row['formal_outcome'])
            rows.append(row)
        write_json(output / 'rows.json', rows)
    summary = summarize(rows)
    summary['case_exclusions'] = [{'id': x['id'], 'episode': x['episode'], 'reason': x.get('exclusion_reason', 'custodian marked ineligible')} for x in cases if not x['eligible']]
    write_json(output / 'summary.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ('manifest', 'cases', 'output', 'ledger'):
        parser.add_argument('--' + argument, type=Path, required=True)
    args = parser.parse_args()
    score(args.manifest, args.cases, args.output, args.ledger)
