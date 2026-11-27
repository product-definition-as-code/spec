"""Regression checks that incomplete or inconsistent saved evidence is rejected."""
import  json, shutil, sys, tempfile, unittest
from pathlib import Path
from verify import verify
SOURCE=Path(sys.argv.pop(1)).resolve()

class EvidenceRejection(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='pdac-audit-negative-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        for name in ['logs','formal']:shutil.copytree(SOURCE/name,self.root/name)
        for name in ['run-manifest.json','history.bundle']:shutil.copyfile(SOURCE/name,self.root/name)
    def test_missing_receipt(self):
        (self.root/'logs/baseline-z3.json').unlink()
        with self.assertRaises(AssertionError):verify(self.root)
    def test_all_receipts_absent(self):
        shutil.rmtree(self.root/'logs');(self.root/'logs').mkdir()
        with self.assertRaises(AssertionError):verify(self.root)
    def test_claimed_post_apply_status_disagrees_with_raw_output(self):
        p=self.root/'run-manifest.json';m=json.loads(p.read_text());m['stages'][1]['post_apply_full_recheck']['z3']['statuses'][0]='unknown';p.write_text(json.dumps(m))
        with self.assertRaises(AssertionError):verify(self.root)
    def test_semantic_source_pin_does_not_match_git(self):
        p=self.root/'formal/domain-accepted/semantic-inputs.json';m=json.loads(p.read_text());m['source_pins']['TERM-A']='sha256:'+'0'*64;p.write_text(json.dumps(m))
        with self.assertRaises(AssertionError):verify(self.root)

if __name__=='__main__':unittest.main()
