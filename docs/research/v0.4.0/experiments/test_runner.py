"""Exercise failure-recording branches without spawning solver processes."""
import json, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from run import run

class AttemptRecording(unittest.TestCase):
    def setUp(self):
        # Python may lazily call subprocess while discovering platform metadata.
        for target,value in [('run.platform.platform','test-linux'),('run.platform.machine','x86_64')]:
            patched=patch(target,return_value=value);patched.start();self.addCleanup(patched.stop)

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
    def test_explicit_working_directory_pins_relative_input(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp, patch('run.subprocess.run',return_value=subprocess.CompletedProcess([],0,b'sat\n',b'')) as call:
            fixture=Path(temp)/'product';fixture.mkdir();source=fixture/'model.smt2';source.write_text('(check-sat)\n')
            output=Path(temp)/'records';run('relative',['solver','model.smt2'],output,cwd=fixture)
            record=json.loads((output/'relative.json').read_text())
            self.assertEqual(record['cwd'],str(fixture))
            self.assertEqual(record['input_sha256'][str(source)],hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertIn('--working-directory='+str(fixture),call.call_args.args[0])
    def test_launch_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp, patch('run.subprocess.run',side_effect=FileNotFoundError('no systemd-run')):
            result=run('launch',['missing-solver'],Path(temp))
            record=json.loads((Path(temp)/'launch.json').read_text())
            self.assertEqual((result.returncode,record['failure_class']),(127,'launch_error'))
            self.assertIn('no systemd-run',(Path(temp)/'launch.stderr').read_text())

if __name__=='__main__':unittest.main()
