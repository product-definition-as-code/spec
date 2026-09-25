import importlib.util
from pathlib import Path
import unittest
import yaml

spec = importlib.util.spec_from_file_location('migration', Path(__file__).with_name('migrate-rule-governance.py'))
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)

def doc(id, type, **fields):
    return '---\n' + yaml.safe_dump({'id': id, 'type': type, **fields}, sort_keys=False) + '---\n\nBody retained.\n'

class MigrationTests(unittest.TestCase):
    def test_sorted_append_preserves_broad_scope_and_is_idempotent(self):
        files = {'z.md': doc('BR-Z', 'business-rule', **{'applies-to': ['UC-A', 'BC-A']}), 'a.md': doc('BR-A', 'business-rule', **{'applies-to': ['UC-A']}), 'uc.md': doc('UC-A', 'use-case', **{'governed-by': ['BR-EXISTING', 'BR-EXISTING']})}
        changed = migration.migrate_documents(files)
        parsed = {p: yaml.safe_load(s.split('---\n')[1]) for p, s in changed.items()}
        self.assertEqual(parsed['uc.md']['governed-by'], ['BR-EXISTING', 'BR-A', 'BR-Z'])
        self.assertEqual(parsed['z.md']['applies-to'], ['BC-A'])
        self.assertNotIn('applies-to', parsed['a.md'])
        self.assertTrue(all(s.endswith('\n\nBody retained.\n') for s in changed.values()))
        self.assertEqual(migration.migrate_documents({**files, **changed}), {})

    def test_missing_or_wrong_type_target_stops_before_changes(self):
        for target in [None, doc('UC-A', 'actor')]:
            files = {'br.md': doc('BR-A', 'business-rule', **{'applies-to': ['UC-A']})}
            if target: files['uc.md'] = target
            original = dict(files)
            with self.assertRaisesRegex(ValueError, 'unresolved or wrong-type'): migration.migrate_documents(files)
            self.assertEqual(files, original)

    def test_bounded_context_membership_does_not_infer_specific_governance(self):
        files = {'br.md': doc('BR-A', 'business-rule', **{'applies-to': ['BC-A']}), 'uc.md': doc('UC-A', 'use-case', **{'bounded-context': 'BC-A'})}
        self.assertEqual(migration.migrate_documents(files), {})

if __name__ == '__main__': unittest.main()
