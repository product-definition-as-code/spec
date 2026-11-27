#!/usr/bin/env python3
"""Freeze approved inputs, isolate fresh sessions and preserve immutable attempts; no approval synthesis."""
import argparse, ast, concurrent.futures, hashlib, json, os, shutil, subprocess, sys, time, uuid
from pathlib import Path
from isolation import namespace, environment
from solver_gateway import Gateway, CLIENT, PRODUCTSHAPE_CLIENT, SOLVER_LOCK, run as bounded
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
COHORTS={1:'ordinary requirements; no PDaC or formal tools',2:'released PDaC/ProductShape; no formal tools',3:'ordinary requirements/traceability plus formal tools; no PDaC',4:'released PDaC/ProductShape plus identical formal tools'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def load(p):return json.loads(Path(p).read_text())
def inputs():return {p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.suffix in ['.py','.md','.json']}
def git(root,*args):
    env={**environment(),'GIT_AUTHOR_NAME':'Synthetic research fixture','GIT_AUTHOR_EMAIL':'research@example.invalid','GIT_COMMITTER_NAME':'Synthetic research fixture','GIT_COMMITTER_EMAIL':'research@example.invalid'}
    command=['git','-c','user.name=Synthetic research fixture','-c','user.email=research@example.invalid','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false',*args]
    if Path(root).resolve()!=REPO:
        command=['systemd-run','--user','--quiet','--wait','--pipe','--collect','-p','MemoryMax=2147483648','-p','RuntimeMaxSec=30','-p','TasksMax=64','-p','KillMode=control-group','--',*namespace(root,command,network=False)]
    return subprocess.check_output(command,cwd=root,env=env,stderr=subprocess.PIPE,timeout=45).decode().strip()

def prepare(out,tools,package):
    out.mkdir(parents=True,exist_ok=False)
    custody=load(HERE/'custody.json')
    assert all(sha(HERE/name)==pin for name,pin in custody['source_pins'].items()),'custody source pins require requalification'
    tasks=load(HERE/'tasks.json');order=[]
    for seed in tasks['seed_schedules']:
        for index,episode in enumerate(tasks['episode_order']):
            cohorts=[1,2,3,4] if seed==17 else [4,3,2,1]
            cohorts=cohorts[index%4:]+cohorts[:index%4]
            order.extend({'id':f's{seed}-c{c}-{episode}','seed':str(seed),'cohort':c,'episode':episode,'episode_index':index} for c in cohorts)
    binaries={'z3':str(tools/'Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3'),'cvc5':str(tools/'cvc5/cvc5-Linux-x86_64-static/bin/cvc5')}
    versions={k:{'path':p,'sha256':sha(p)} for k,p in binaries.items()}
    assert load(package/'node_modules/@prodshape/cli/package.json')['version']=='0.26.1'
    cli=shutil.which('codex');assert cli
    protocol={'status':'prepared, not approved or executed','source_revision':git(REPO,'rev-parse','HEAD'),'public_inputs':inputs(),'tools':versions,'productshape':str(package),'productshape_lock_sha256':sha(package/'package-lock.json'),'productshape_cli_sha256':sha(package/'node_modules/@prodshape/cli/dist/bin.js'),'codex_cli_version':subprocess.check_output([cli,'--version'],text=True).strip(),'codex_launcher_sha256':sha(cli),'model_requested':'gpt-6.1-sol','reasoning_effort':'medium','model_resolved_weights':'not exposed by provider; alias drift is a limitation','limits':{'author_sessions':64,'author_concurrency':2,'author_wall_seconds':480,'author_memory_bytes':4294967296,'author_solver_processes_per_session':64,'author_solver_queries_per_session':2048,'automatic_author_retries':0},'plan':order,'custody_commitment':load(HERE/'custody.json')}
    assert len(order)==64
    dump(out/'frozen-inputs.json',protocol)
    print('Prepared 64 fresh-session jobs; no author or scored evaluator launched.')

def approve(out,url):
    f=load(out/'frozen-inputs.json');assert f['public_inputs']==inputs(),'public inputs changed; prepare a new immutable run'
    # The coordinator must not generate this decision without an actual owner instruction.
    assert url.startswith('https://github.com/product-definition-as-code/spec/issues/130#issuecomment-')
    comment_id=url.rsplit('-',1)[1]
    repo=load_json_command(['gh','api','repos/product-definition-as-code/spec']);assert (repo['full_name'],repo['id'])==('product-definition-as-code/spec',1318490705)
    c=load_json_command(['gh','api',f'repos/product-definition-as-code/spec/issues/comments/{comment_id}'])
    assert c['user']['login']=='juangcarmona' and c['html_url']==url
    assert 'G1 decision: approve' in c['body'] and f['source_revision'] in c['body'] and sha(out/'frozen-inputs.json') in c['body'],'approval must pin exact source and prepared manifest'
    record={'url':url,'comment_body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),'source_revision':f['source_revision'],'frozen_manifest_sha256':sha(out/'frozen-inputs.json'),'identity_limitation':'delegated account access cannot technically prove human origin; coordinator requires actual owner instruction'}
    target=out/'approval.json';assert not target.exists();dump(target,record)

def load_json_command(command):return json.loads(subprocess.check_output(command))

def packet(work,f,job,previous):
    if previous:shutil.copytree(previous,work,ignore=shutil.ignore_patterns('home','bin'))
    else:work.mkdir(parents=True);git(work,'init','-q','-b','main')
    (work/'home').mkdir(exist_ok=True);(work/'bin').mkdir(exist_ok=True)
    snapshots=load(HERE/'intent.json')['episodes'];snapshot=snapshots[job['episode']]
    text=(HERE/'intent-template.md').read_text()
    for key,value in snapshot['parameters'].items():text=text.replace('{{'+key+'}}',json.dumps(value) if not isinstance(value,str) else value)
    assert '{{' not in text
    public=load(HERE/'public-examples.json');examples={k:v for k,v in public.items() if k!='episodes'};examples['episode_cases']=public['episodes'][job['episode']]
    task=next(x for x in load(HERE/'tasks.json')['episodes'] if x['id']==job['episode'])
    for name in ['INTERFACE.md','author-instructions.md']:shutil.copyfile(HERE/name,work/name)
    (work/'product-intent.md').write_text(text)
    dump(work/'current-parameters.json',snapshot['parameters']);dump(work/'public-examples.json',examples)
    history=work/'intent-history';history.mkdir(exist_ok=True);dump(history/(job['episode']+'.json'),{'request':task['request'],'parameters':snapshot['parameters']})
    (work/'episode-request.txt').write_text(task['request']+'\n')
    (work/'AGENTS.md').write_text('Research fixture only. Never access credentials, private cases, other cohorts, network services, or retired agent-toolkit instructions. No remote writes or paid provisioning. Read current product-intent.md, author-instructions.md, INTERFACE.md and episode-request.txt. Respect assigned cohort. Never change the immutable input files. No automatic retries.\n')
    if job['cohort'] in [2,4]:
        ps=work/'bin/productshape';ps.write_text(PRODUCTSHAPE_CLIENT);ps.chmod(0o755)
        target=work/'released-spec';target.mkdir(exist_ok=True)
        for p in (REPO/'spec').glob('*.md'):shutil.copyfile(p,target/p.name)
    if job['cohort'] in [3,4]:
        for name in ['z3','cvc5']:
            p=work/'bin'/name;p.write_text(CLIENT);p.chmod(0o755)
    git(work,'add','.');git(work,'commit','-qm','Provide '+job['episode']+' identical intent and cohort-specific method access')
    return {str(p.relative_to(work)):sha(p) for p in [work/'product-intent.md',work/'current-parameters.json',work/'public-examples.json',work/'episode-request.txt',work/'INTERFACE.md',work/'author-instructions.md',work/'AGENTS.md']}

def readiness(work,cohort,previous=None):
    reasons=[]
    if any(p.is_symlink() for p in work.rglob('*')):return ['symlink in untrusted author output']
    for name in ['decision.py','report.json']+(['contract.smt2'] if cohort in [3,4] else []):
        if not (work/name).is_file():reasons.append('missing '+name)
    if reasons:return reasons
    try:
        tree=ast.parse((work/'decision.py').read_text());assert any(isinstance(n,ast.FunctionDef) and n.name=='decide' for n in tree.body)
        report=load(work/'report.json');assert report['status']=='ready' and report['unresolved_decisions']==[]
        for key in ['assumptions','semantic_decisions','evidence','findings']:assert isinstance(report[key],list)
        assert isinstance(report['dependencies'],dict)
        if cohort in [2,4]:
            assert (work/'.product/config.yaml').is_file()
            completed=work/'docs/product/changes/completed'
            new={p.parent.name for p in completed.glob('*/change.md')}
            old={p.parent.name for p in (previous/'docs/product/changes/completed').glob('*/change.md')} if previous else set()
            assert new-old,'no new completed Product Change for current episode'
            if previous:
                for p in (previous/'docs/product/changes/completed').rglob('*'):
                    if p.is_file():assert (completed/p.relative_to(previous/'docs/product/changes/completed')).read_bytes()==p.read_bytes(),'old accepted change mutated'
    except (AssertionError,KeyError,ValueError,SyntaxError) as e:reasons.append('missing/blocked/invalid required handoff: '+str(e))
    return reasons

def author(out,f,job):
    target=out/'attempts'/job['id'];target.mkdir(parents=True,exist_ok=False)
    prior=None
    if job['episode_index']:
        ep=load(HERE/'tasks.json')['episode_order'][job['episode_index']-1];prior=out/'attempts'/f's{job["seed"]}-c{job["cohort"]}-{ep}'/'work'
        prior_record=load(prior.parent/'receipt.json')
        if prior_record['status']!='completed':dump(target/'receipt.json',{'job':job,'status':'blocked by failed predecessor','returncode':125});return
    work=target/'work';inputpins=packet(work,f,job,prior)
    auth=target/'auth';auth.mkdir(mode=0o700);shutil.copyfile(Path.home()/'.codex/auth.json',auth/'auth.json');(auth/'auth.json').chmod(0o600)
    mounts={};gateway=None;method_gateway=None
    if job['cohort'] in [2,4]:
        method_sock=target/'method.sock';method_gateway=Gateway(method_sock,{},target/'method-receipts',queries=0,work=work,package=f['productshape']);mounts['productshape.sock']=str(method_sock);method_gateway.__enter__()
    if job['cohort'] in [3,4]:
        sock=target/'solver.sock';gateway=Gateway(sock,{k:v['path'] for k,v in f['tools'].items()},target/'solver-receipts');mounts['solver.sock']=str(sock)
        gateway.__enter__()
    prompt=f'Assigned cohort {job["cohort"]}: {COHORTS[job["cohort"]]}. Execute only current episode {job["episode"]}. Read AGENTS.md and assigned inputs. Complete concrete files; no owner approval is needed for routine research commands within frozen G1. Tool limits:480s author wall; formal cohorts only z3 FILE/cvc5 FILE wrappers,64 calls/2048 queries,30s/2GiB per process. No external API/network calls or reference-source lookup. Preserve old evidence and report unknowns. Finish with concise handoff. Do not commit; coordinator records history.'
    command=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--model',f['model_requested'],'-c','model_reasoning_effort="medium"','--sandbox','workspace-write','--json',prompt]
    unit='pdac-author-'+uuid.uuid4().hex
    wrapped=['systemd-run','--user','--quiet','--wait','--pipe','--collect','--unit='+unit,'-p','RuntimeMaxSec=480','-p','MemoryMax=4294967296','-p','MemorySwapMax=0','-p','TasksMax=128','-p','KillMode=control-group','--',*namespace(work,command,auth=auth,tools=mounts)]
    start=time.monotonic()
    try:
        try:r=subprocess.run(wrapped,env=environment(),capture_output=True,timeout=495)
        except OSError as e:r=subprocess.CompletedProcess(wrapped,127,b'',str(e).encode())
        except subprocess.TimeoutExpired as e:
            subprocess.run(['systemctl','--user','kill','--kill-whom=all',unit],capture_output=True);r=subprocess.CompletedProcess(wrapped,124,e.stdout or b'',e.stderr or b'')
    finally:
        if gateway:gateway.__exit__()
        if method_gateway:method_gateway.__exit__()
        (auth/'auth.json').unlink(missing_ok=True)
    (target/'events.jsonl').write_bytes(r.stdout);(target/'stderr').write_bytes(r.stderr)
    unchanged=all((work/p).is_file() and not (work/p).is_symlink() and sha(work/p)==pin for p,pin in inputpins.items())
    receipt={'job':job,'returncode':r.returncode,'wall_seconds':round(time.monotonic()-start,3),'input_pins':inputpins,'inputs_unchanged':unchanged,'command':command,'events_sha256':sha(target/'events.jsonl'),'usage':None,'status':'completed' if r.returncode==0 and unchanged else 'failed; no automatic retry'}
    for line in r.stdout.decode(errors='replace').splitlines():
        try:
            event=json.loads(line)
            if event.get('type')=='turn.completed':receipt['usage']=event.get('usage')
        except ValueError:pass
    receipt['readiness_defects']=readiness(work,job['cohort'],prior)
    if job['cohort'] in [2,4]:
        method_receipts=[load(p) for p in (target/'method-receipts').glob('query-*.json')]
        apply_receipts=[x for x in method_receipts if x.get('returncode')==0 and any(x.get('gateway_request',{}).get('args',[])[i:i+2]==['change','apply'] for i in range(len(x.get('gateway_request',{}).get('args',[])))) and '--dry-run' not in x['gateway_request']['args']]
        if not apply_receipts:receipt['readiness_defects'].append('no independently captured successful actual change apply')
        receipt['actual_apply_receipts']=len(apply_receipts)
        if not any(p.is_symlink() for p in work.rglob('*')):
            with SOLVER_LOCK:
                command=namespace(work,['node','/tools/productshape/node_modules/@prodshape/cli/dist/bin.js','--serialization-version','v1alpha2','validate','--format','json'],tools={'productshape':f['productshape']},network=False)
                validation=bounded('method-final-validation',command,target/'method-receipts',cwd=work)
            if validation.returncode!=0:receipt['readiness_defects'].append('post-author ProductShape validation failed')
    if not any(p.is_symlink() for p in work.rglob('*')):
        git(work,'add','.');git(work,'commit','--allow-empty','-qm','Preserve '+job['episode']+' authored output and limitations');receipt['revision']=git(work,'rev-parse','HEAD')
    if receipt['readiness_defects']:receipt['status']='blocked handoff; no automatic retry'
    receipt['outputs']={name:sha(work/name) for name in ['decision.py','contract.smt2','report.json'] if (work/name).is_file() and not (work/name).is_symlink()}
    dump(target/'receipt.json',receipt)

def execute(out):
    f=load(out/'frozen-inputs.json');approval=load(out/'approval.json')
    assert approval['frozen_manifest_sha256']==sha(out/'frozen-inputs.json') and f['public_inputs']==inputs()
    assert git(REPO,'rev-parse','HEAD')==f['source_revision'],'execute pinned source revision'
    assert subprocess.check_output(['codex','--version'],text=True).strip()==f['codex_cli_version']
    assert sha(shutil.which('codex'))==f['codex_launcher_sha256']
    assert sha(Path(f['productshape'])/'package-lock.json')==f['productshape_lock_sha256']
    assert sha(Path(f['productshape'])/'node_modules/@prodshape/cli/dist/bin.js')==f['productshape_cli_sha256']
    for v in f['tools'].values():assert sha(v['path'])==v['sha256']
    assert not (out/'attempts').exists(),'one-shot execution; failed attempts never overwritten or automatically resumed'
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for seed in ['17','29']:
            for episode in load(HERE/'tasks.json')['episode_order']:
                jobs=[j for j in f['plan'] if j['seed']==seed and j['episode']==episode]
                list(pool.map(lambda j:author(out,f,j),jobs))
    rows=[]
    for j in f['plan']:
        target=out/'attempts'/j['id'];receipt=load(target/'receipt.json');work=target/'work'
        rows.append({'path':str(work),'cohort':j['cohort'],'seed':j['seed'],'episode':j['episode'],'sha256':receipt.get('outputs',{}),'author_status':receipt['status']})
    dump(out/'submissions.json',{'submissions':rows,'tools':f['tools'],'solver_call_budget':64,'solver_query_budget':7776,'frozen_manifest_sha256':sha(out/'frozen-inputs.json'),'heldout_commitment':f['custody_commitment'],'g1_approval':approval})
    print('Authorship complete. Freeze submissions before custodian evaluation; no G2 transition.')

if __name__=='__main__':
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='action',required=True)
    q=s.add_parser('prepare');q.add_argument('output',type=Path);q.add_argument('--tools',type=Path,required=True);q.add_argument('--productshape',type=Path,required=True)
    q=s.add_parser('approve');q.add_argument('output',type=Path);q.add_argument('--owner-comment',required=True)
    q=s.add_parser('run');q.add_argument('output',type=Path)
    a=p.parse_args();out=a.output.resolve()
    if a.action=='prepare':prepare(out,a.tools.resolve(),a.productshape.resolve())
    elif a.action=='approve':approve(out,a.owner_comment)
    else:execute(out)
