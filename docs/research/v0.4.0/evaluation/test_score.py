#!/usr/bin/env python3
"""Public dummy fixtures only. No custodian inputs are used or discovered."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('scorer', Path(__file__).with_name('score.py'))
score = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score)

X = dict(status=0, used=0, capacity=1, days=0, due=False, actor=1, owner=1,
         issuer=1, authenticated=True, editor=False, operation=0)
Y = dict(accepted=True, status=0, used=0, owner=1)
EVIDENCE = Path(tempfile.mkdtemp(prefix='pdac-score-public-selftest-'))
ARGS = '(s Int) (u Int) (c Int) (d Int) (due Bool) (a Int) (o Int) (i Int) (auth Bool) (e Bool) (op Int) (ok Bool) (ns Int) (nu Int) (no Int)'
IDENTITY = '(set-logic QF_LIA)\n(define-fun Step (' + ARGS + ') Bool (and ok (= ns s) (= nu u) (= no o)))\n'


def case(name='public-identity', expected=None):
    return {'id': name, 'episode': 'PUBLIC', 'input': dict(X),
            'expected': dict(Y) if expected is None else expected, 'class': 'public-dummy', 'eligible': True}


class ScorerTests(unittest.TestCase):
    def test_contract_query_includes_completeness(self):
        text = score.queries(IDENTITY, [case()]).decode()
        self.assertEqual(text.count('(check-sat)'), 2)
        self.assertIn('(not (and (= oracle_', text)
        for command in ('(assert false)', '(check-sat)', '(exit)', '(declare-const evil Int)', '(set-option :print-success true)'):
            with self.assertRaises(ValueError):
                score.queries(IDENTITY + command, [case()])

    def test_schema_and_typed_equality(self):
        self.assertEqual(score.classify(Y, dict(Y)), 'correct')
        self.assertEqual(score.classify(Y, dict(Y, accepted=False)), 'valid_rejection')
        self.assertEqual(score.classify(Y, dict(Y, used=1)), 'semantic_error')
        self.assertEqual(score.classify(Y, dict(Y, status=False)), 'semantic_error')
        self.assertEqual(score.classify(Y, {'accepted': True}), 'unknown')
        malformed = case(expected=dict(accepted=False, status=None, used=False, owner='bad'))
        malformed['input'] = {'status': None, 'used': False, 'owner': 'bad'}
        score.validate_cases({'cases': [malformed]})
        self.assertEqual(score.classify(malformed['expected'], malformed['expected']), 'correct')
        with self.assertRaises(ValueError):
            score.validate_cases({'cases': [case(), case()]})

    def test_write_ahead_budget_preserves_failed_launches(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / 'ledger.json'
            score.reserve(ledger, 1, 2, 1, 2, 'failed-call')
            with self.assertRaises(RuntimeError):
                score.reserve(ledger, 1, 2, 1, 2, 'forbidden-retry')
            with self.assertRaises(ValueError):
                score.reserve(ledger, 1, 2, 10, 20, 'inflated-budget')
            self.assertEqual(len(json.loads(ledger.read_text())['attempts']), 1)

    def test_unknown_never_success_and_safeguard_is_paired(self):
        rows = []
        for cohort, outcomes in ((3, ('valid_rejection', 'correct')), (4, ('correct', 'valid_rejection'))):
            for pos, outcome in enumerate(outcomes):
                rows.append(dict(cohort=cohort, seed=17, episode='PUBLIC', id=str(pos),
                                 outcome=outcome, **{'class': 'dummy'}))
        result = score.summarize(rows)['comparisons'][0]
        self.assertFalse(result['zero_additional_valid_rejections'])
        self.assertFalse(result['primary_screen_10pp'])
        self.assertEqual(result['rates']['3']['finite_discrepancy_all_eligible'], .5)
        self.assertEqual(score.combine_outcomes('correct', 'semantic_error'), 'semantic_error')
        self.assertEqual(score.combine_outcomes('unknown', 'semantic_error'), 'semantic_error')
        self.assertEqual(score.combine_outcomes('correct', 'unknown'), 'unknown')
        self.assertEqual(score.combine_outcomes('correct', 'valid_rejection'), 'valid_rejection')
        self.assertEqual(score.parse_solver({'returncode': 0, 'failure': None}, b'sat\nunknown\n', 2), ['sat', 'unknown'])
        self.assertEqual(score.parse_solver({'returncode': 1, 'failure': None}, b'sat\nunsat\n', 2), ['unknown', 'unknown'])
        self.assertEqual(score.parse_solver({'returncode': 0, 'failure': None}, b'sat\n(error fake)\n', 2), ['unknown', 'unknown'])

    def test_unknown_baseline_does_not_establish_improvement(self):
        rows = [dict(cohort=c, seed=17, episode='PUBLIC', id='dummy',
                     outcome='unknown' if c == 3 else 'correct', **{'class': 'dummy'}) for c in (3, 4)]
        for result in score.summarize(rows)['comparisons']:
            self.assertEqual(result['improvement_percentage_points'], 100)
            self.assertEqual(result['lower_bound_improvement_percentage_points'], 0)
            self.assertFalse(result['primary_screen_10pp'])
            self.assertFalse(any(result['sensitivity'].values()))

    def test_missing_blocked_and_tampered_rows_remain_unknown(self):
        root = EVIDENCE / 'missing-submissions'
        root.mkdir()
        tampered = root / 'tampered'
        tampered.mkdir()
        (tampered / 'decision.py').write_text('raise RuntimeError("must never load")')
        submissions = [dict(cohort=3, seed=17, episode='PUBLIC', author_status='blocked by failed predecessor'),
                       dict(cohort=4, seed=17, episode='PUBLIC', path=str(root / 'absent'), sha256={}),
                       dict(cohort=1, seed=17, episode='PUBLIC', path=str(tampered), sha256={'decision.py': '0' * 64})]
        score.write_json(root / 'manifest.json', {'submissions': submissions, 'solver_call_budget': 4, 'solver_query_budget': 8})
        score.write_json(root / 'cases.json', {'cases': [case()]})
        score.score(root / 'manifest.json', root / 'cases.json', root / 'score', root / 'ledger.json')
        rows = json.loads((root / 'score' / 'rows.json').read_text())
        self.assertEqual(len(rows), 3)
        self.assertEqual([x['outcome'] for x in rows], ['unknown'] * 3)
        self.assertTrue(rows[0]['formal_unknown'])
        self.assertTrue(rows[1]['formal_unknown'])
        self.assertFalse(rows[0]['invalid_experiment'])
        self.assertTrue(rows[1]['invalid_experiment'])
        self.assertTrue(rows[2]['invalid_experiment'])
        self.assertFalse((root / 'ledger.json').exists())
        for index in range(3):
            self.assertTrue((root / 'score' / str(index) / 'attempt-defect.json').exists())

    def test_cases_commitment_and_approval_binding(self):
        root = EVIDENCE / 'commitments'
        root.mkdir()
        cases = root / 'cases.json'
        score.write_json(cases, {'cases': [case()]})
        manifest = {'submissions': [], 'heldout_commitment': {'private_commitments': {'cases.json': '0' * 64}}}
        score.write_json(root / 'manifest.json', manifest)
        with self.assertRaisesRegex(ValueError, 'commitment mismatch'):
            score.score(root / 'manifest.json', cases, root / 'forbidden', root / 'ledger.json')
        manifest['heldout_commitment']['private_commitments']['cases.json'] = score.digest(cases.read_bytes())
        manifest['frozen_manifest_sha256'] = 'actual-frozen-pin'
        manifest['g1_approval'] = {'url': 'https://github.com/product-definition-as-code/spec/issues/130#issuecomment-123',
                                   'frozen_manifest_sha256': 'wrong-frozen-pin'}
        score.write_json(root / 'manifest.json', manifest)
        with self.assertRaisesRegex(ValueError, 'G1 approval'):
            score.score(root / 'manifest.json', cases, root / 'forbidden', root / 'ledger.json')
        self.assertFalse((root / 'forbidden').exists())

    def test_real_sandbox_public_dummy_and_exception(self):
        if True:
            root = EVIDENCE / 'sandbox'
            root.mkdir()
            submitted = root / 'decision.py'
            submitted.write_text("def decide(x):\n    try:\n        open('/etc/passwd').read()\n    except FileNotFoundError:\n        pass\n    else:\n        raise RuntimeError('host visible')\n    return dict(accepted=True,status=x['status'],used=x['used'],owner=x['owner'])\n")
            rec, stdout = score.execute(['/usr/bin/python3', '-I', '-B', '/worker.py'],
                [(submitted, '/submission/decision.py'), (score.HERE / 'deterministic-worker.py', '/worker.py')],
                json.dumps([{'id': 'dummy', 'input': X}]).encode(), root, 'identity')
            self.assertEqual(rec['returncode'], 0, (root / 'identity.stderr').read_text())
            self.assertEqual(json.loads(stdout)['results'][0]['output'], Y)
            submitted.write_text("def decide(x):\n    raise ValueError('dummy')\n")
            rec, stdout = score.execute(['/usr/bin/python3', '-I', '-B', '/worker.py'],
                [(submitted, '/submission/decision.py'), (score.HERE / 'deterministic-worker.py', '/worker.py')],
                json.dumps([{'id': 'dummy', 'input': X}]).encode(), root, 'exception')
            self.assertEqual(json.loads(stdout)['results'][0]['error'], 'ValueError')

    def test_full_frozen_manifest_union_and_schedule_filter(self):
        root = EVIDENCE / 'full-manifest'
        root.mkdir()
        tools = {'z3': Path('/tmp/pdac-v040-tools/Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3'),
                 'cvc5': Path('/tmp/pdac-v040-tools/cvc5/cvc5-Linux-x86_64-static/bin/cvc5')}
        manifest = {'submissions': [], 'solver_call_budget': 4, 'solver_query_budget': 8,
                    'tools': {key: {'path': str(value), 'sha256': score.digest(value.read_bytes())}
                              for key, value in tools.items()}}
        for cohort in (3, 4):
            folder = root / str(cohort)
            folder.mkdir()
            (folder / 'decision.py').write_text("def decide(x):\n    return dict(accepted=True,status=x['status'],used=x['used'],owner=x['owner'])\n")
            (folder / 'contract.smt2').write_text(IDENTITY if cohort == 3 else '(define-fun Step (' + ARGS + ') Bool ok)')
            manifest['submissions'].append(dict(path=str(folder), cohort=cohort, seed=17, episode='PUBLIC',
                sha256={name: score.digest((folder / name).read_bytes()) for name in ('decision.py', 'contract.smt2')}))
        public = case()
        public['schedule'] = 17
        other_schedule = case('other-schedule')
        other_schedule['schedule'] = 29
        score.write_json(root / 'manifest.json', manifest)
        score.write_json(root / 'cases.json', {'cases': [public, other_schedule]})
        summary = score.score(root / 'manifest.json', root / 'cases.json', root / 'score', root / 'ledger.json')
        rows = json.loads((root / 'score' / 'rows.json').read_text())
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['outcome'], 'correct')
        self.assertEqual(rows[1]['decision_outcome'], 'correct')
        self.assertEqual(rows[1]['formal_outcome'], 'semantic_error')
        self.assertEqual(rows[1]['outcome'], 'semantic_error')
        self.assertFalse(summary['comparisons'][0]['primary_screen_10pp'])
        self.assertEqual(json.loads((root / 'score' / 'planned-counts.json').read_text())['solver_queries'], 8)
        self.assertEqual(len(json.loads((root / 'ledger.json').read_text())['attempts']), 4)

    def test_real_pinned_solvers_public_identity_and_incomplete(self):
        tools = {'z3': Path('/tmp/pdac-v040-tools/Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3'),
                 'cvc5': Path('/tmp/pdac-v040-tools/cvc5/cvc5-Linux-x86_64-static/bin/cvc5')}
        if True:
            root = EVIDENCE / 'solvers'
            root.mkdir()
            ledger = root / 'ledger.json'
            pins = {'z3': 'fcd0ca765d1c0b4eac776f442ec0f10294b9a6416be91fad4e52fa19012c8d01',
                    'cvc5': '6aecddf466552b83bb5883756c7955e0c9d5ddcc6d7f45b48c2f6e06a741b102'}
            for engine, path in tools.items():
                score.checked(path, pins[engine], limit=512 * 1024 * 1024)
                args = ['/solver', '-in'] if engine == 'z3' else ['/solver', '--lang=smt2', '--incremental']
                query = score.queries(IDENTITY, [case()])
                score.reserve(ledger, 1, 2, 4, 8, engine + '-identity')
                rec, out = score.execute(args, [(path, '/solver')], query, root, engine + '-identity')
                self.assertEqual(score.parse_solver(rec, out, 2), ['sat', 'unsat'], (root / (engine + '-identity.stderr')).read_text())
                # This weak relation permits arbitrary state: the alternative query detects it.
                weak = '(define-fun Step (' + ARGS + ') Bool ok)'
                score.reserve(ledger, 1, 2, 4, 8, engine + '-weak')
                rec, out = score.execute(args, [(path, '/solver')], score.queries(weak, [case()]), root, engine + '-weak')
                self.assertEqual(score.parse_solver(rec, out, 2), ['sat', 'sat'])


if __name__ == '__main__':
    print('Public selftest evidence:', EVIDENCE, flush=True)
    unittest.main()
