import concurrent.futures, json, socket, subprocess, tempfile, threading, time, unittest
from pathlib import Path
from unittest.mock import patch
from pilot import approve, packet, execute, prepare, load, inputs, readiness
from isolation import namespace, environment
from review import evaluate
from solver_gateway import Gateway

class Preparation(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
    def test_no_execution_without_exact_approval(self):
        (self.root/'frozen-inputs.json').write_text(json.dumps({'public_inputs':inputs()}))
        with self.assertRaises(FileNotFoundError):execute(self.root)
        self.assertFalse((self.root/'attempts').exists())
        with self.assertRaises(FileNotFoundError):evaluate(self.root,self.root/'score',self.root/'review')
        self.assertFalse((self.root/'review').exists())
        with self.assertRaises(AssertionError):approve(self.root,'https://wrong.example/approval')
    def test_current_only_packets_and_real_git_handoff(self):
        # No auth, model, network or held-out material required to prepare packets.
        job={'episode':'B0','cohort':1};first=self.root/'first'
        pins=packet(first,{},job,None)
        self.assertTrue(pins);self.assertNotIn('{{',(first/'product-intent.md').read_text())
        self.assertFalse((first/'intent.json').exists());self.assertFalse((first/'tasks.json').exists())
        self.assertNotIn('B4',(first/'product-intent.md').read_text())
        second=self.root/'second';packet(second,{},dict(job,episode='B1'),first)
        self.assertEqual(len(list((second/'intent-history').glob('*.json'))),2)
        self.assertFalse((first/'intent-history/B1.json').exists())
    def test_mount_boundary_omits_host_and_disables_worker_network(self):
        (self.root/'facts.txt').write_text('immutable')
        result=subprocess.run(namespace(self.root,['python3','-c','from pathlib import Path; assert not Path("/home/juan").exists(); assert not Path("/srv/repos").exists(); assert not Path("/run/user").exists(); p=Path("/work/facts.txt"); assert p.read_text()=="immutable"; assert not __import__("os").access(p,__import__("os").W_OK)'],network=False,readonly=['facts.txt']),capture_output=True,env=environment())
        self.assertEqual(result.returncode,0,result.stderr)
    def test_gateway_reserves_budget_before_compute_and_refuses_retry(self):
        tool=self.root/'fake-solver';tool.write_bytes(b'pinned fake binary')
        def fake_run(name,command,output,cwd):
            (output/(name+'.json')).write_text('{}')
            return subprocess.CompletedProcess(command,0,b'unsat\n',b'')
        with patch('solver_gateway.run',side_effect=fake_run) as called:
            sock=self.root/'s'
            with Gateway(sock,{'z3':str(tool)},self.root/'receipts',calls=1,queries=1):
                def request():
                    s=socket.socket(socket.AF_UNIX);s.connect(str(sock));s.sendall(json.dumps({'engine':'z3','model':'(assert false)\n(check-sat)'}).encode()+b'\n');reply=json.loads(s.makefile('rb').readline());s.close();return reply
                self.assertEqual(request()['stdout'],'unsat\n');self.assertEqual(request()['returncode'],125)
            self.assertEqual(called.call_count,1)
            self.assertEqual(load(self.root/'receipts/budget.json')['queries_reserved'],1)
            self.assertIn('gateway_model_sha256',load(self.root/'receipts/query-001.json'))

    def test_global_gateway_execution_serialization(self):
        tool=self.root/'solver';tool.write_bytes(b'fake');active=0;peak=0;lock=threading.Lock()
        def fake_run(name,command,output,cwd):
            nonlocal active,peak
            with lock:active+=1;peak=max(peak,active)
            time.sleep(.04)
            with lock:active-=1
            (output/(name+'.json')).write_text('{}')
            return subprocess.CompletedProcess(command,0,b'sat\n',b'')
        def request(path):
            sock=socket.socket(socket.AF_UNIX);sock.connect(str(path));sock.sendall(json.dumps({'engine':'z3','model':'(check-sat)'}).encode()+b'\n');reply=json.loads(sock.makefile('rb').readline());sock.close();return reply
        with patch('solver_gateway.run',side_effect=fake_run):
            with Gateway(self.root/'a',{'z3':str(tool)},self.root/'ra'),Gateway(self.root/'b',{'z3':str(tool)},self.root/'rb'):
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                    result=list(pool.map(request,[self.root/'a',self.root/'b']))
        self.assertEqual(peak,1);self.assertTrue(all(r['returncode']==0 for r in result))
    def test_existing_completed_change_cannot_satisfy_next_episode(self):
        prior=self.root/'prior';work=self.root/'work'
        for folder in [prior,work]:
            (folder/'docs/product/changes/completed/old').mkdir(parents=True);(folder/'docs/product/changes/completed/old/change.md').write_text('immutable')
            (folder/'.product').mkdir();(folder/'.product/config.yaml').write_text('fixture')
        (work/'decision.py').write_text('def decide(x): return {}')
        (work/'report.json').write_text(json.dumps({'status':'ready','unresolved_decisions':[],'assumptions':[],'semantic_decisions':[],'findings':[],'evidence':[],'dependencies':{}}))
        self.assertTrue(readiness(work,2,prior))
        (work/'docs/product/changes/completed/new').mkdir();(work/'docs/product/changes/completed/new/change.md').write_text('new')
        self.assertEqual(readiness(work,2,prior),[])

    def test_transient_manager_environment_cannot_escape_namespace(self):
        # The user service manager, unlike the caller, supplies TMPDIR and may supply credentials.
        command=namespace(self.root,['python3','-c','import os; from pathlib import Path; assert os.environ["TMPDIR"]=="/tmp"; assert Path(os.environ["TMPDIR"]).is_dir(); assert "PDAC_INHERITED_SENTINEL" not in os.environ'],network=False)
        env=environment();env.update(TMPDIR='/unmounted-host-temp',PDAC_INHERITED_SENTINEL='must-not-reach-child')
        result=subprocess.run(command,env=env,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=='__main__':unittest.main()
