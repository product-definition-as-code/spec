import json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from preflight import preflight
from pilot import prepare

class TransportCanary(unittest.TestCase):
    def test_failure_is_retained_without_model_calls_or_fallback(self):
        with tempfile.TemporaryDirectory() as root,patch('preflight.run',return_value=subprocess.CompletedProcess([],1,b'',b'namespace unavailable')) as run:
            out=Path(root)/'canary';record=preflight(out)
            self.assertFalse(record['passed']);self.assertEqual(record['model_calls'],0);self.assertEqual(run.call_count,1)
            self.assertIn('sandbox',run.call_args.args[1]);self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',run.call_args.args[1])
            self.assertFalse(json.loads((out/'preflight.json').read_text())['fallback_or_security_relaxation'])
    def test_prepare_cannot_freeze_inputs_on_failed_full_transport(self):
        with tempfile.TemporaryDirectory() as root,patch('pilot.preflight',return_value={'passed':False}):
            out=Path(root)/'pilot'
            with self.assertRaises(AssertionError):prepare(out,Path('/not-read'),Path('/not-read'))
            self.assertFalse((out/'frozen-inputs.json').exists());self.assertFalse((out/'attempts').exists())

if __name__=='__main__':unittest.main()
