"""Per-author socket gateway: pinned solvers, host-owned budget/receipts, no paths from clients."""
import hashlib, json, re, socketserver, sys, threading, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'experiments'))
from run import run
from isolation import namespace

SOLVER_LOCK=threading.Lock()

class Gateway:
    def __init__(self,path,tools,logs,calls=64,queries=2048,work=None,package=None):
        self.logs=Path(logs);self.logs.mkdir(parents=True);self.tools=tools;self.calls=0;self.queries=0;self.maxcalls=calls;self.maxqueries=queries;self.lock=threading.Lock();self.closing=threading.Event()
        outer=self;self.work=work;self.package=package
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                try:
                    self.request.settimeout(10)
                    data=self.rfile.readline(262145)
                    if len(data)>262144:raise ValueError('model exceeds 256 KiB')
                    req=json.loads(data)
                    if outer.package:
                        assert set(req)=={'args'} and isinstance(req['args'],list) and all(isinstance(x,str) for x in req['args'])
                        assert '--serialization-version' not in req['args']
                        n=0
                    else:
                        assert set(req)=={'engine','model'} and req['engine'] in outer.tools and isinstance(req['model'],str)
                        text=re.sub(r'"(?:[^\"]|\"\")*"|;[^\n]*','',req['model'])
                        n=len(re.findall(r'\(\s*check-sat(?:-assuming)?\b',text))
                    with outer.lock:
                        if outer.closing.is_set() or outer.calls>=outer.maxcalls or outer.queries+n>outer.maxqueries:raise ValueError('predeclared author solver budget exhausted')
                        outer.calls+=1;outer.queries+=n;label=f'query-{outer.calls:03d}';model=outer.logs/(label+'.smt2')
                        if not outer.package:model.write_text(req['model'])
                        (outer.logs/'budget.json').write_text(json.dumps({'processes_reserved':outer.calls,'queries_reserved':outer.queries,'max_processes':calls,'max_queries':queries}))
                    with SOLVER_LOCK:
                        if outer.closing.is_set():raise ValueError('author session ended; queued job cancelled')
                        if outer.package:
                            cmd=['node','/tools/productshape/node_modules/@prodshape/cli/dist/bin.js','--serialization-version','v1alpha2',*req['args']]
                            wrapped=namespace(outer.work,cmd,tools={'productshape':outer.package},network=False)
                            result=run(label,wrapped,outer.logs,cwd=outer.logs)
                        else:
                            cmd=['/tools/solver','/tools/input.smt2']
                            if req['engine']=='cvc5':cmd[1:1]=['--lang=smt2','--incremental']
                            with tempfile.TemporaryDirectory(prefix='pdac-solver-scratch-') as scratch:
                                wrapped=namespace(scratch,cmd,tools={'solver':outer.tools[req['engine']],'input.smt2':model},network=False)
                                result=run(label,wrapped,outer.logs,cwd=outer.logs)
                    receipt=json.loads((outer.logs/(label+'.json')).read_text());receipt['gateway_request']=req if outer.package else {'engine':req['engine'],'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest()}
                    if not outer.package:
                        receipt['gateway_model_sha256']=hashlib.sha256(model.read_bytes()).hexdigest();receipt['gateway_solver_sha256']=hashlib.sha256(Path(outer.tools[req['engine']]).read_bytes()).hexdigest()
                    (outer.logs/(label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
                    answer={'returncode':result.returncode,'stdout':result.stdout.decode(errors='replace'),'stderr':result.stderr.decode(errors='replace')}
                except Exception as error:answer={'returncode':125,'stdout':'','stderr':str(error)}
                self.wfile.write(json.dumps(answer).encode()+b'\n')
        class Server(socketserver.ThreadingUnixStreamServer):
            daemon_threads=False
            block_on_close=True
        self.server=Server(str(path),Handler);self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*args):self.closing.set();self.server.shutdown();self.server.server_close();self.thread.join()

CLIENT='''#!/usr/bin/env python3
import json,socket,sys
from pathlib import Path
engine=Path(sys.argv[0]).name
if len(sys.argv)!=2:raise SystemExit("Use z3/cvc5 FILE.smt2; no retry loop")
model=Path(sys.argv[1]).read_text()
s=socket.socket(socket.AF_UNIX);s.connect('/tools/solver.sock')
s.sendall(json.dumps({'engine':engine,'model':model}).encode()+b'\\n')
r=json.loads(s.makefile('rb').readline());sys.stdout.write(r['stdout']);sys.stderr.write(r['stderr']);raise SystemExit(r['returncode'])
'''

PRODUCTSHAPE_CLIENT='''#!/usr/bin/env python3
import json,socket,sys
s=socket.socket(socket.AF_UNIX);s.connect('/tools/productshape.sock')
s.sendall(json.dumps({'args':sys.argv[1:]}).encode()+b'\\n')
r=json.loads(s.makefile('rb').readline());sys.stdout.write(r['stdout']);sys.stderr.write(r['stderr']);raise SystemExit(r['returncode'])
'''
