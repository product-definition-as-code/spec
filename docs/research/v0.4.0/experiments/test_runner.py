"""Exercise failure-recording branches without spawning solver processes."""
import json, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from run import run

class AttemptRecording(unittest.TestCase):
    def test_timeout_retains_partial_evidence_and_kills_only_its_unit(self):
        with tempfile.TemporaryDirectory() as temp, patch('run.subprocess.run') as call:
            call.side_effect=[subprocess.TimeoutExpired('systemd-run',45,output=b'partial verdict',stderr=b'partial error'),subprocess.CompletedProcess([],0,b'',b'')]
            result=run('timeout',['missing-solver'],Path(temp))
            record=json.loads((Path(temp)/'timeout.json').read_text())
            self.assertEqual(result.returncode,124)
            self.assertEqual(record['failure_class'],'outer_timeout')
            self.assertEqual((Path(temp)/'timeout.stdout').read_bytes(),b'partial verdict')
            self.assertEqual((Path(temp)/'timeout.stderr').read_bytes(),b'partial error')
            wrapped=call.call_args_list[0].args[0];unit=next(x.split('=',1)[1] for x in wrapped if x.startswith('--unit='))
            self.assertEqual(call.call_args_list[1].args[0][-1],unit)
            self.assertIn('--kill-whom=all',call.call_args_list[1].args[0])
            with self.assertRaises(FileExistsError):run('timeout',['missing-solver'],Path(temp))
    def test_launch_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp, patch('run.subprocess.run',side_effect=FileNotFoundError('no systemd-run')):
            result=run('launch',['missing-solver'],Path(temp))
            record=json.loads((Path(temp)/'launch.json').read_text())
            self.assertEqual((result.returncode,record['failure_class']),(127,'launch_error'))
            self.assertIn('no systemd-run',(Path(temp)/'launch.stderr').read_text())

if __name__=='__main__':unittest.main()
