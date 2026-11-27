import json,shutil,tempfile,unittest
from pathlib import Path
from audit_results import audit
SOURCE=Path(__file__).resolve().parent/'results/attempt-1'
class SavedResultIntegrity(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        for name in ['result.json','public-evidence.tar.gz']:shutil.copyfile(SOURCE/name,self.root/name)
    def test_changed_archive_is_rejected(self):
        with (self.root/'public-evidence.tar.gz').open('ab') as f:f.write(b'changed')
        with self.assertRaises(AssertionError):audit(self.root)
    def test_incorrect_published_counter_is_rejected(self):
        p=self.root/'result.json';s=json.loads(p.read_text());s['unknown_observations']=0;p.write_text(json.dumps(s))
        with self.assertRaises(AssertionError):audit(self.root)
if __name__=='__main__':unittest.main()
